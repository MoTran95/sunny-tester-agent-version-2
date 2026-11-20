#!/usr/bin/env python3
"""Self-test for scripts/test_automation: runs the whole flow against a fake local app (fake accounts, temp project).

    python -X utf8 scripts/selftest/run_selftest.py

Checks: config loading, login + saved sessions, runner verdicts (pass / pass with minor fail / fail / no verdict),
red-box error screenshot with caption, session invalidation, run recording, report page and bug page.
Run it after any change to scripts/test_automation. Exit code 0 = all checks passed.
"""
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
import _venv  # noqa: E402

_venv.ensure_playwright()  # chưa có Playwright thì tự chạy lại bằng venv của repo
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import fake_server  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

from test_automation import bug_page, config, docs_pages, theme, context as context_module, failure_counter, report, results, runner, session  # noqa: E402

FAILED = []


def check(name, condition, detail=""):
    print(f"  [{'OK' if condition else 'FAIL'}] {name}" + (f" — {detail}" if detail and not condition else ""))
    if not condition:
        FAILED.append(name)


CASES = {
    "tc-001": ('{"code": "TC-001", "title": "login ok but shows DEFAULT", "accounts": ["P1"]}', """
    ctx.goto("/"); ctx.wait_text("Danh sách việc")
    ctx.check_main("Có Danh sách việc", "Danh sách việc" in ctx.page_text())
    ctx.check_minor("Không có chữ DEFAULT", "DEFAULT" not in ctx.page_text(), mark_text="DEFAULT",
                    error_note="Lỗi ở bước 2: thanh điều hướng hiện chữ DEFAULT, đáng ra không có.")
"""),
    "tc-002": ('{"code": "TC-002", "title": "script error", "accounts": ["P1"]}', """
    ctx.goto("/"); ctx.wait_text("Danh sách việc")
    ctx.page.locator("#does-not-exist").click(timeout=1000)
"""),
    "tc-003": ('{"code": "TC-003", "title": "missing test data", "accounts": ["P1"]}', """
    ctx.test_data("missing_key")
"""),
    "tc-004": ('{"code": "TC-004", "title": "wait timeout", "accounts": []}', """
    ctx.goto("/"); ctx.wait_text("never appears", timeout_ms=1500)
"""),
    "tc-005": ('{"code": "TC-005", "title": "public login form", "accounts": []}', """
    ctx.goto("/"); ctx.wait_text("Đăng nhập")
    ctx.check_main("Có ô mật khẩu", ctx.page.locator("input[type=password]").count() == 1)
    ctx.check_main("Có chữ Đăng nhập (khung xanh)", True, mark_text="Đăng nhập")
"""),
    "tc-006": ('{"code": "TC-006", "title": "main check fails", "accounts": ["P1"]}', """
    ctx.goto("/"); ctx.wait_text("Danh sách việc")
    ctx.check_main("Điều không đúng", False)
"""),
    "tc-007": ('{"code": "TC-007", "title": "logout invalidates session", "accounts": ["P2"], "invalidates_sessions": ["P2"]}', """
    ctx.goto("/"); ctx.wait_text("Danh sách việc")
    ctx.page.get_by_role("button", name="Đăng xuất").click()
    ctx.check_main("Về form đăng nhập", ctx.poll_until(lambda: ctx.page.locator("input[type=password]").count() > 0, seconds=8))
"""),
    "tc-008": ('{"code": "TC-008", "title": "sign in from the form with ctx.sign_in", "accounts": []}', """
    ctx.goto("/"); ctx.sign_in("P1")
    ctx.wait_text("Danh sách việc")
    ctx.check_main("Vào Danh sách việc sau khi sign_in", "Danh sách việc" in ctx.page_text())
"""),
    "tc-009": ('{"code": "TC-009", "title": "wrong then correct submit", "accounts": [], "ready_account": "P1", "wrong_attempts": 1}', """
    ctx.goto("/"); ctx.wait_text("Đăng nhập")
    status = ctx.submit_login("P1", "wrong-pass", expect_success=False)
    ctx.check_main("Sai mật khẩu trả 401", status == 401, str(status))
    ctx.page.wait_for_timeout(500)
    status = ctx.submit_login("P1", password_of="P1", expect_success=True)
    ctx.check_main("Đúng mật khẩu trả 200", status == 200, str(status))
    ctx.check_main("Đăng nhập đúng không đưa bộ đếm về 0", __import__("test_automation.failure_counter", fromlist=["x"]).read(ctx.cfg)["consecutive_failures"] == 1)
"""),
    "tc-010": ('{"code": "TC-010", "title": "cap refuses the 10th wrong attempt", "accounts": [], "ready_account": "P1", "wrong_attempts": 12}', """
    ctx.goto("/"); ctx.wait_text("Đăng nhập")
    for i in range(12):
        ctx.submit_login("P1", f"wrong-{i}", expect_success=False)
        ctx.page.wait_for_timeout(200)
"""),
}


def build_project(root, base_url):
    project = root / "testing" / "demo"
    (project / "feature" / "auto").mkdir(parents=True)
    (root / ".env").write_text(
        f"FAKE_URL={base_url}\nFAKE_P1_USER=P1\nFAKE_P1_PASSWORD=fake-pass-1\nFAKE_P2_USER=P2\nFAKE_P2_PASSWORD=fake-pass-2\n", encoding="utf-8")
    (project / "auto-config.json").write_text(json.dumps({
        "env_prefix": "FAKE", "default_url": "http://127.0.0.1:1",
        "login": {"id_labels": ["Tên đăng nhập"], "button_labels": ["Đăng nhập"], "login_api": "/api/auth/sign-in",
                  "session_check_api": "/api/me", "session_minutes": 10,
                  "max_consecutive_failures": 9, "block_minutes": 5}}, ensure_ascii=False), encoding="utf-8")
    (project / "auto-data.json").write_text(json.dumps({"version": "9.9.9"}), encoding="utf-8")
    rows, test_case_rows = [], []
    for i, (name, (info, body)) in enumerate(sorted(CASES.items()), start=1):
        (project / "feature" / "auto" / f"{name}.py").write_text(f"CASE_INFO = {info}\n\n\ndef run(ctx):{body}", encoding="utf-8")
        rows.append(f"| {i} | Smoke {name} | [Demo · {name.upper()}](feature/test-case.md#{name}) | Fixed | why | 1 min | yes |")
        test_case_rows.append(f'| <a id="{name}"></a>{name.upper()} | Situation | High | pre | 1. Open page<br>2. Look | data | Expected for {name} | src | | Not run | me | None |')
    (project / "smoke-test.md").write_text("| # | Smoke case | Source | Part | Why | Time | Auto |\n|---|---|---|---|---|---|---|\n" + "\n".join(rows) + "\n", encoding="utf-8")
    (project / "feature" / "test-case.md").write_text(
        "| Mã | Tình huống | Ưu tiên | Điều kiện trước | Các bước | Dữ liệu test | Kết quả mong đợi | Nguồn | Kết quả thực tế | Trạng thái | Người viết | Tự động hóa |\n"
        "|---|---|---|---|---|---|---|---|---|---|---|---|\n" + "\n".join(test_case_rows) + "\n", encoding="utf-8")
    bug_dir = project / "feature" / "bug"
    bug_dir.mkdir()
    (bug_dir / "BUG-001.md").write_text(
        "# [Demo] Chữ DEFAULT vẫn hiện\n\n## Môi trường\n- Trình duyệt: Chrome\n\n## Mức độ nghiêm trọng\n**Rất nhỏ.** Chữ thừa. [Giả định: không gây nhầm]\n\n"
        "## Mức độ ưu tiên đề xuất\n**Thấp** — không chặn.\n\n## Thông tin đã gắn nhãn Giả định (cần kiểm lại)\n1. Không gây nhầm.\n", encoding="utf-8")
    return project


def main():
    server, base_url = fake_server.start()
    root = Path(tempfile.mkdtemp(prefix="selftest-"))
    config.ROOT = root
    try:
        project = build_project(root, base_url)
        print("1. Config")
        cfg = config.load("demo")
        check("load config", cfg.url == base_url and cfg.env_prefix == "FAKE")
        check("list accounts from .env", cfg.available_accounts() == ["P1", "P2"], str(cfg.available_accounts()))

        print("2. Login and saved sessions")
        with sync_playwright() as p:
            for account in ("P1", "P2"):
                exit_code, _, _ = session.login(p, cfg, account, headless=True)
                check(f"login {account}", exit_code == 0 and session.session_file(cfg, account).exists())

        print("3. Runner")
        argv = ["--project", "demo"]
        for name in sorted(CASES):
            argv += ["--case-id", f"feature/{name}"]
        exit_code = runner.main(argv)
        check("runner exit code is 'no verdict' (4) because some cases cannot conclude... but a fail exists", exit_code in (results.EXIT_FAIL, results.EXIT_NO_VERDICT))
        result_files = sorted(cfg.screenshots_dir.glob("result-*.json"))
        check("result json written", len(result_files) == 1)
        data = json.loads(result_files[-1].read_text(encoding="utf-8"))
        by_case = {r["case_id"].split("/")[-1]: r for r in data["results"]}
        expected = {"tc-001": results.PASS_MINOR_FAIL, "tc-002": results.NO_VERDICT, "tc-003": results.NO_VERDICT, "tc-004": results.NO_VERDICT,
                    "tc-005": results.PASS, "tc-006": results.FAIL, "tc-007": results.PASS, "tc-008": results.PASS,
                    "tc-009": results.PASS, "tc-010": results.NO_VERDICT}
        for name, verdict in expected.items():
            check(f"verdict {name} = {verdict}", by_case[name]["verdict"] == verdict, by_case[name]["verdict"])
        check("tc-003 says test data is missing", "missing_key" in by_case["tc-003"]["reason"])
        check("tc-004 says wait timed out", "quá" in by_case["tc-004"]["reason"])
        t1 = by_case["tc-001"]
        check("tc-001 has a red-box screenshot with caption", len(t1["error_images"]) == 1 and "bước 2" in next(iter(t1["error_image_captions"].values()), ""))
        check("red-box image file exists", (root / t1["error_images"][0]).exists())
        check("tc-007 removed the invalidated session file", not session.session_file(cfg, "P2").exists())
        check("tc-005 has a green/red check image (-kiem)", any("-kiem" in a for a in by_case["tc-005"]["images"]), str(by_case["tc-005"]["images"]))
        ffmpeg_ok = not context_module.Context._warned_no_ffmpeg   # thư viện tự ghi nhận khi thiếu ffmpeg của Playwright
        if ffmpeg_ok:
            check("tc-001 (minor fail) keeps its video", len(by_case["tc-001"]["videos"]) == 1 and (root / by_case["tc-001"]["videos"][0]).exists(), str(by_case["tc-001"]["videos"]))
        else:
            print("  [SKIP] video check: ffmpeg of Playwright is not installed")
        check("tc-005 (pass) has no kept video", by_case["tc-005"]["videos"] == [])
        check("tc-010 stopped at the cap of 9 consecutive failures", "trần 9" in by_case["tc-010"]["reason"], by_case["tc-010"]["reason"])
        check("counter file says 9", failure_counter.read(cfg)["consecutive_failures"] == 9, str(failure_counter.read(cfg)))
        check("tc-001 still has its session file", session.session_file(cfg, "P1").exists())

        print("4. Session check before running")
        exit_code = runner.main(["--project", "demo", "--case-id", "feature/tc-007"])
        check("expired/missing session stops the run (exit 3)", exit_code == results.EXIT_SESSION, str(exit_code))

        print("5. Run record, report page, bug page")
        # Lượt smoke cũng phải có kết luận: dựng kết luận mẫu, liệt kê đúng các case chưa có kết quả mà bộ kiểm báo.
        smoke_conclusion = {"headline": "Chưa nhận bản 9.9.9 vì case số 1 còn lỗi đã biết và 4 case chưa có kết luận.",
                            "passed": ["Các case có kết luận Đạt trong lượt này."], "not_tested": [], "risks": [],
                            "suggestion": "Chạy lại các case chưa có kết luận sau khi có phiên đăng nhập mới."}
        for _ in range(3):
            try:
                run_record = report.add_run(cfg, "smoke", "9.9.9", data["results"], sources=[str(result_files[-1].relative_to(root))],
                                            status_override={"1": "Đạt kèm lỗi đã biết"}, bug={"1": ["BUG-001"]}, conclusion=smoke_conclusion)
                break
            except report.ConclusionError as error:
                missing = re.findall(r"([A-Z]+-\d+) đang `([^`]+)` nhưng không được nêu", str(error))
                if not missing:
                    raise
                for code, status in missing:
                    smoke_conclusion["not_tested"].append({"cases": code, "status": status,
                                                           "reason": "Ca mẫu của bài tự kiểm chưa có kết luận trong lượt chạy giả."})
        check("run with a failed case is recorded as reject build", run_record["verdict"] == report.REJECT_BUILD, run_record["verdict"])
        check("run number and history", run_record["number"] == 1 and len(report.read_results_data(cfg, "smoke")["runs"]) == 1)
        md = (project / "smoke-ket-qua.md").read_text(encoding="utf-8")
        page = (project / "smoke-ket-qua.html").read_text(encoding="utf-8")
        check("report md has the 3 expected columns", "| Các bước |" in md and "Kết quả mong đợi" in md and "Kết quả thực tế" not in md)
        check("report html shows the red-box caption", "Lỗi ở bước 2: thanh điều hướng hiện chữ DEFAULT" in page)
        check("report html has drag/scroll helper", "scrollLeft" in page)
        check("report links the bug page", "BUG-001.html" in page)
        try:
            report.add_run(cfg, "feature", "9.9.9", data["results"], status_override={"6": "Bị chặn"}, bug={"1": ["BUG-001"]}, blocked_by={"6": ["BUG-001"]})
            refused = False
        except report.ConclusionError:
            refused = True
        check("a feature run without a conclusion is not recorded", refused and not (project / "run-results" / "feature.json").exists())
        feature_table = report.read_table(cfg, "feature")
        feature_status = {}
        for kq in data["results"]:
            feature_status[kq["case_id"].partition("/")[2].upper()] = "Chưa chạy" if kq["verdict"] == results.NO_SCRIPT else kq["verdict"]
        feature_status[[b["id"] for b in feature_table if b["number"] == "6"][0]] = "Bị chặn"
        pending = [(b["id"], feature_status.get(b["id"], "Chưa chạy")) for b in feature_table if feature_status.get(b["id"], "Chưa chạy") not in report.HAS_VERDICT]
        feature_conclusion = {
            "headline": "Chưa thể nhận bản 9.9.9: có ca Không đạt và có ca chưa có kết quả, nêu từng ca bên dưới.",
            "passed": ["Các ca Đạt chạy trọn, đã kiểm trên giao diện giả của bài tự kiểm."],
            "not_tested": [{"cases": code, "status": status, "reason": "Ca này chưa có kết luận trong bài tự kiểm vì script lỗi, quá hạn hoặc bị chặn."} for code, status in pending],
            "risks": [{"title": "Kết quả chỉ trên giao diện giả", "detail": "Đây là bài tự kiểm thư viện, không phản ánh hệ thống thật; không dùng để quyết nhận hay trả bản."}],
            "suggestion": "Đề xuất chỉ dùng bài này để kiểm thư viện; quyết nhận hay trả bản là việc của người kiểm thử.",
        }
        feature_run = report.add_run(cfg, "feature", "9.9.9", data["results"], status_override={"6": "Bị chặn"}, bug={"1": ["BUG-001"]}, blocked_by={"6": ["BUG-001"]}, conclusion=feature_conclusion)
        feature_page = (project / "feature" / "ket-qua-test-case.html").read_text(encoding="utf-8")
        check("feature page lists every test case of the feature", feature_page.count("<tr><td class=\"nw\">TC-") >= 10, str(feature_page.count("<tr><td class=\"nw\">TC-")))
        check("feature page shows blocked-by link and bug table", "Bị chặn bởi" in feature_page and "Bug đã mở" in feature_page)
        check("feature run verdict is 'not all run' (blocked and no-verdict cases remain)", feature_run["verdict"] == report.NOT_ALL_RUN, feature_run["verdict"])
        bug_html = project / "feature" / "bug" / "BUG-001.html"
        check("bug page built", bug_html.exists() and "Sao chép" in bug_html.read_text(encoding="utf-8"))
        print("5b. Summary report (test summary, reviewer form, stale decision)")
        from test_automation import summary_report

        model = summary_report.build_model(cfg)
        pages = summary_report.render_pages(cfg)
        md_path, html_path = summary_report.page_paths(cfg)
        check("summary picks the build of the newest run", model["build"] == "9.9.9" and set(model["based_on"]) == {"smoke", "feature"}, str(model.get("based_on")))
        check("summary writes an md and an html page", set(pages) == {md_path, html_path})
        summary_html, summary_md = pages[html_path], pages[md_path]
        check("summary html has the reviewer form, download button and print button",
              'data-k="approver.decision"' in summary_html and "Tải file duyệt" in summary_html and "In / Lưu PDF" in summary_html and "window.print" in summary_html)
        check("summary html embeds the run numbers the decision is based on", '"based_on"' in summary_html and '"smoke": 1' in summary_html)
        check("summary md shows empty reviewer fields before any decision", "(chưa điền)" in summary_md and "Duyệt build" in summary_md)
        approval = {"approvals": [{"build": "9.9.9", "based_on": model["based_on"], "approver": {"name": "Người duyệt thử", "decision": "Nhận có điều kiện", "conditions": "Sửa BUG-001", "date": "2026-01-01"}}]}
        summary_approval = project / summary_report.APPROVAL_FILE
        summary_approval.write_text(json.dumps(approval), encoding="utf-8")
        recorded_md = summary_report.render_pages(cfg)[md_path]
        check("a decision for the same runs is shown and still valid", "Người duyệt thử" in recorded_md and "Còn hiệu lực" in recorded_md)
        approval["approvals"][0]["based_on"] = dict(model["based_on"], smoke=0)
        summary_approval.write_text(json.dumps(approval), encoding="utf-8")
        check("a decision made before a newer run is marked stale", "Đã lỗi thời" in summary_report.render_pages(cfg)[md_path])
        approval["approvals"][0]["build"] = "8.8.8"
        summary_approval.write_text(json.dumps(approval), encoding="utf-8")
        other_md = summary_report.render_pages(cfg)[md_path]
        check("a decision for another build is only listed as history", "Các lần duyệt khác" in other_md and "Còn hiệu lực" not in other_md)
        lk = summary_report.Linker(cfg, model)
        check("summary: a TC code in a feature suite links to its row", "feature/test-case.md#tc-001" in lk.link("Xem TC-001.", "md", "feature"), lk.link("Xem TC-001.", "md", "feature"))
        check("summary: a smoke code links to the original test case", "feature/test-case.md#tc-" in lk.link("SM-01", "md", "smoke"))
        check("summary: a bug code links to its file", "feature/bug/BUG-001.md" in lk.link("BUG-001", "md", "smoke"))
        check("summary: an unknown code stays plain text", lk.link("TC-999", "md", "feature") == "TC-999")
        check("summary: a TC code in smoke text links only after a feature name",
              "feature/test-case.md#tc-002" in lk.link("Ở feature TC-002", "md", "smoke") and lk.link("Xem TC-002", "md", "smoke") == "Xem TC-002")
        check("summary: html links are escaped and point to html pages", lk.link("a<b TC-001", "html", "feature") == 'a&lt;b <a href="feature/test-case.html#tc-001">TC-001</a>', lk.link("a<b TC-001", "html", "feature"))
        check("summary: the bug table links every case that found the bug", "feature/test-case.md#tc-" in summary_md and "[BUG-001](feature/bug/BUG-001.md)" in summary_md)
        summary_approval.unlink()
        check("md of the summary is not converted as a plain document", md_path not in docs_pages.collect_sources("demo"))
        print("6. Docs pages (markdown to HTML)")
        sample = Path(root / "docs-sample")
        sample.mkdir()
        other = sample / "other.md"
        other.write_text("# Other", encoding="utf-8")
        md = chr(10).join([
            "# Title", "", "<!-- hidden", "comment -->", "",
            "Text with **bold**, `code <b>`, [link](other.md#x) and [web](https://example.com/a).", "",
            '<a id="tc-001"></a>', "",
            "| A | B | C | D | E | F |", "|---|---|---|---|---|---|",
            '| <a id="r1"></a>1 | Đạt | x' + chr(92) + '|y | Không đạt | | z<br>w |', "",
            "- one", "  - nested", "- two", "", "1. first", "2. second", "", "> note"])
        body, title, heads = docs_pages.render_markdown(md, sample / "a.md", {other.resolve()})
        check("docs: title found", title == "Title", title)
        check("docs: md link to a converted file becomes .html", 'href="other.html#x"' in body, body[:300])
        check("docs: web link kept, inline code escaped", 'href="https://example.com/a"' in body and "<code>code &lt;b&gt;</code>" in body)
        check("docs: comment hidden, anchor kept", "hidden" not in body and '<a id="tc-001"></a>' in body)
        check("docs: wide table (6 cols) with status badges and escaped pipe", 'class="wrap lon"' in body and 'class="badge ok">Đạt' in body and 'class="badge bad">Không đạt' in body and "x|y" in body)
        check("docs: nested list and ordered list", body.count("<ul>") == 2 and "nested" in body and "<ol>" in body and body.count("<li id=") >= 4, body[-300:])
        print("7. Line anchors, code links, sync freshness, offline fonts")
        srs_dir = root / "srs" / "demo"
        srs_dir.mkdir(parents=True)
        (srs_dir / "feature.md").write_text(chr(10).join(["# SRS", "", "| Mã | Nội dung |", "|---|---|", "| `DEMO-S01-AC01` | Mở form |", "| `DEMO-R01` | Quy tắc |"]) + chr(10), encoding="utf-8")
        (project / "feature" / "checklist.md").write_text("# Checklist" + chr(10) + chr(10) + "- Theo S01-AC01 và R01, xem [SRS](../../../srs/demo/feature.md#L5)" + chr(10), encoding="utf-8")
        changed, _ = docs_pages.sync("demo")
        check("sync writes pages on first run", len(changed) > 0, str(changed))
        srs_html = (srs_dir / "feature.html").read_text(encoding="utf-8")
        check("SRS table rows have line anchors", 'id="L5"' in srs_html and 'id="L6"' in srs_html)
        checklist_html = (project / "feature" / "checklist.html").read_text(encoding="utf-8")
        check("requirement codes link to the SRS row", 'class="ma" href="../../../srs/demo/feature.html#L5">S01-AC01</a>' in checklist_html, checklist_html[-400:])
        check("md link with #L anchor points to the html page", 'feature.html#L5">SRS</a>' in checklist_html)
        check("the defining cell does not link to itself", 'class="ma"' not in srs_html)
        changed_again, _ = docs_pages.sync("demo", write=False)
        check("second sync finds nothing stale (pages are idempotent)", changed_again == [], str(changed_again))
        (srs_dir / "feature.md").write_text((srs_dir / "feature.md").read_text(encoding="utf-8") + "- thêm" + chr(10), encoding="utf-8")
        check("editing the md makes the check report a stale page", len(docs_pages.sync("demo", write=False)[0]) > 0)
        fonts = root / "docs" / "thuong-hieu" / "fonts"
        fonts.mkdir(parents=True)
        (fonts / "Fraunces-roman-latin.woff2").write_bytes(b"x")
        (fonts / "fonts.json").write_text('[{"family": "Fraunces", "weight": "400 700", "style": "normal", "file": "Fraunces-roman-latin.woff2", "unicode_range": "U+0000-00FF", "subset": "latin"}]', encoding="utf-8")
        check("local font files replace Google Fonts", "@font-face" in theme.font_head(srs_dir) and "googleapis" not in theme.font_head(srs_dir))
        print("8. Brand config (logo)")
        check("no logo file yet: no brand block", theme.brand_html() == "")
        (root / "docs" / "thuong-hieu" / "logo-khac.svg").write_text("<svg xmlns='http://www.w3.org/2000/svg'/>", encoding="utf-8")
        (root / "docs" / "thuong-hieu" / "brand.json").write_text('{"name": "Công ty Khác", "logo": "docs/thuong-hieu/logo-khac.svg"}', encoding="utf-8")
        block = theme.brand_html()
        check("repo-wide brand.json sets name and logo (svg)", 'alt="Công ty Khác"' in block and "data:image/svg+xml;base64," in block, block[:120])
        check("the summary report never shows the logo, even when a logo is configured", 'class="brand"' not in summary_report.render_pages(cfg)[summary_report.page_paths(cfg)[1]]
              and 'class="brand"' in report.render_pages(cfg, "smoke")[report.page_files(cfg, "smoke")[1]])
        (project / "brand.json").write_text('{"logo_enabled": false}', encoding="utf-8")
        check("project brand.json can switch the logo off", theme.brand_html("demo") == "" and theme.brand_html() != "")
        (project / "brand.json").write_text("not json", encoding="utf-8")
        check("a broken brand file falls back safely", theme.brand_html("demo") != "")
        (project / "brand.json").unlink()
        print("9. New project and other machines")
        (project / "ten-tinh-nang.json").write_text('{"feature": "Tính năng mẫu"}', encoding="utf-8")
        check("feature display names come from the project's own file",
              report.feature_names("demo") == {"feature": "Tính năng mẫu"} and report.suite_title("feature", "demo") == "Test case Tính năng mẫu")
        check("a feature that is not listed shows its folder name", report.suite_title("khac", "demo") == "Test case khac")
        stub = {"env_prefix": "X", "default_url": "<địa chỉ>", "login": {"id_labels": ["<nhãn>"], "session_minutes": "<số>", "login_api": "/api/ok"}}
        check("config placeholders are found by key", config._placeholder_keys(stub) == ["default_url", "login.id_labels[0]", "login.session_minutes"],
              str(config._placeholder_keys(stub)))
        no_cap = config.Config("demo", {"env_prefix": "X", "default_url": "http://x", "login": {
            "id_labels": ["a"], "button_labels": ["b"], "login_api": "/a", "session_check_api": "/b", "session_minutes": 1}}, {})
        check("no cap in the config: deliberate wrong input is refused, no default number",
              no_cap.max_consecutive_failures is None and failure_counter.refusal_reason(no_cap) == failure_counter.NO_CAP)
        fake_table = [{"number": "1", "id": "TC-001"}, {"number": "2", "id": "TC-002"}, {"number": "3", "id": "TC-003"}]
        fake_results = {"1": {"status": "Đạt"}, "2": {"status": "Bỏ qua"}, "3": {"status": "Chưa chạy"}}
        good = {"headline": "Chưa thể nhận bản này: 1 trong 3 case đã Đạt, 2 case chưa có kết quả như nêu bên dưới.",
                "passed": ["TC-001 đăng nhập đúng vào được Danh sách việc"],
                "not_tested": [{"cases": "TC-002", "status": "Bỏ qua", "reason": "Bước làm của ca này làm hệ thống chặn đăng nhập, người kiểm thử tự làm."},
                               {"cases": "TC-003", "status": "Chưa chạy", "reason": "Chưa có script vì chưa rõ màn hình hiện lúc hết hạn phiên."}],
                "risks": [{"title": "Phiên hết hạn chưa kiểm", "detail": "Người dùng để yên lâu có thể bị đưa về form đăng nhập giữa lúc làm việc; chưa kiểm."}],
                "suggestion": "Đề xuất chạy lại TC-003 khi có câu trả lời của BA; nhận hay trả bản do người kiểm thử quyết."}
        check("a complete conclusion passes the validator", report.validate_conclusion("feature", fake_table, fake_results, good) == [],
              str(report.validate_conclusion("feature", fake_table, fake_results, good)))
        check("a feature run without a conclusion is refused", len(report.validate_conclusion("feature", fake_table, fake_results, None)) == 1)
        vague = dict(good, headline="Chưa thể nhận bản này vì còn một số lỗi và nhiều case chưa chạy xong.")
        check("vague wording is refused", any("chung chung" in x for x in report.validate_conclusion("feature", fake_table, fake_results, vague)))
        missing = dict(good, not_tested=good["not_tested"][:1])
        check("a case without a result must be listed", any("TC-003" in x for x in report.validate_conclusion("feature", fake_table, fake_results, missing)))
        wrong = dict(good, not_tested=[dict(good["not_tested"][0], status="Chưa chạy"), good["not_tested"][1]])
        check("the listed status must match the real status", any("TC-002" in x for x in report.validate_conclusion("feature", fake_table, fake_results, wrong)))
        check("a smoke run without a conclusion is refused too", len(report.validate_conclusion("smoke", fake_table, fake_results, None)) == 1)
        manual_dir = root / "testing" / "demo-manual"
        manual_dir.mkdir(parents=True)
        (manual_dir / "auto-config.json").write_text(json.dumps({"env_prefix": "M", "default_url": "http://127.0.0.1:1",
                                                                  "login": {"mode": "manual", "session_check_api": "/api/me", "session_minutes": 10}}), encoding="utf-8")
        manual_cfg = config.load("demo-manual")
        check("manual-login project needs only the session check, no form labels", manual_cfg.login_mode == "manual" and manual_cfg.id_labels == [])
        (manual_dir / "auto-config.json").write_text(json.dumps({"env_prefix": "M", "default_url": "http://127.0.0.1:1", "login": {"mode": "manual"}}), encoding="utf-8")
        try:
            config.load("demo-manual")
            missing_keys = False
        except config.ConfigError as error:
            missing_keys = "session_check_api" in str(error)
        check("manual-login config still requires the session check keys", missing_keys)
        check("run banner names project and address", "demo" in config.load("demo").banner() and "127.0.0.1" in config.load("demo").banner())
        video_html = bug_page._images_in_line("- Video: evidence/demo/chay-test/video/khong-co-tren-may-nay.webm", str(project))
        check("bug page embeds a video even when the file is not on this machine", "<video" in video_html, video_html[:80])
    finally:
        server.shutdown()
        shutil.rmtree(root, ignore_errors=True)
    print("\nRESULT:", "ALL OK" if not FAILED else f"{len(FAILED)} FAILED: {FAILED}")
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
