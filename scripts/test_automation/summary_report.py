"""Báo cáo tổng kết kiểm thử của một dự án (md + HTML), KHÔNG có logo (người dùng dặn 2026-11-19: báo cáo gửi công ty không nên có logo): `testing/<dự-án>/test-summary-report.md` và `.html`.

Số liệu đọc hết từ file có sẵn (lượt chạy `run-results/*.json`, bug, truy vết); không tự quyết định nhận hay trả build.
Quyết định của người test và người duyệt build nằm ở `testing/<dự-án>/duyet-build.json`: trang HTML có form để điền, nút tải file
`duyet-build.json` về, người dùng đặt file vào đúng chỗ rồi chạy lại `build_docs.py` thì quyết định vào cả bản md lẫn HTML.
Quyết định gắn với số lượt của từng bộ test lúc duyệt; có lượt mới thì báo "đã lỗi thời".
Nội dung chỉ phụ thuộc dữ liệu (không dùng giờ hiện tại) để `build_docs.py --check` so sánh được.
"""
import html
import json
import os
import re

from . import bug_page, config, report as R

MD_NAME = "test-summary-report.md"
HTML_NAME = "test-summary-report.html"
APPROVAL_FILE = "duyet-build.json"
DECISIONS = ["Nhận build", "Không nhận build", "Nhận có điều kiện"]
DECISION_CLASS = {"Nhận build": "ok", "Không nhận build": "bad", "Nhận có điều kiện": "warn"}  # lớp badge; nút chọn dùng nut-<lớp> để không dính CSS badge

BUG_STATUS_NOTE = ("Trạng thái bug đọc từ mục `Trạng thái` trong file bug, do người test chốt sau khi re-test (skill lap-ke-hoach-retest). "
                   "Bug ghi \"Chưa ghi\" là chưa ai chốt trong kho; trạng thái chính thức nằm ở công cụ của team.").replace("`", "")

# Nhóm trạng thái để đếm theo tính năng
CATEGORIES = [("pass", "Đạt"), ("pass_issue", "Đạt kèm lỗi"), ("fail", "Không đạt"), ("open", "Bị chặn / Không kết luận"), ("skipped", "Bỏ qua"), ("not_run", "Chưa chạy")]


def category(status):
    if status == R.PASS:
        return "pass"
    if status in (R.PASS_KNOWN_ISSUE, R.PASS_MINOR_FAIL):
        return "pass_issue"
    if status == R.FAIL:
        return "fail"
    if status in (R.BLOCKED, R.NO_VERDICT):
        return "open"
    if status == R.SKIPPED:
        return "skipped"
    return "not_run"


def page_paths(cfg):
    return cfg.project_dir / MD_NAME, cfg.project_dir / HTML_NAME


def approval_path(cfg):
    return cfg.project_dir / APPROVAL_FILE


def read_approvals(cfg):
    f = approval_path(cfg)
    if not f.exists():
        return []
    data = json.loads(f.read_text(encoding="utf-8"))
    items = data.get("approvals", []) if isinstance(data, dict) else data
    return [x for x in items if isinstance(x, dict) and x.get("build")]


def has_any_run(cfg):
    return bool(_all_suites(cfg))


def _all_suites(cfg):
    """{tên bộ: (dữ liệu lượt, bảng case)} cho mọi bộ có lượt chạy; bỏ bộ không đọc được bảng case."""
    out = {}
    rr = cfg.project_dir / "run-results"
    for f in sorted(rr.glob("*.json")) if rr.exists() else []:
        data = R.read_results_data(cfg, f.stem)
        if not data["runs"]:
            continue
        try:
            out[f.stem] = (data, R.read_table(cfg, f.stem))
        except config.ConfigError:
            continue
    return out


def _suite_order(name):
    return (0 if name == "smoke" else 1 if R.is_regression(name) else 2, name)


def _rel(cfg, path):
    return os.path.relpath(path, cfg.project_dir).replace("\\", "/")


def _percent(a, b):
    return f"{round(100 * a / b)}%" if b else "—"


def _requirement_coverage(cfg, feature, names):
    """Đọc mục 1 của truy-vet.md của tính năng; không đọc được thì để trống (người đọc mở trang truy vết)."""
    f = cfg.project_dir / feature / "truy-vet.md"
    info = {"slug": feature, "name": names.get(feature, feature), "requirements": "—", "uncovered": "—", "state": "—", "href": None}
    if not f.exists():
        return info
    text = f.read_text(encoding="utf-8")
    info["href"] = f"{feature}/truy-vet.html"
    m = re.search(r"Mã requirement: (.+)", text)
    info["requirements"] = m.group(1).strip().rstrip(".") if m else "—"
    m = re.search(r"Mã SRS chưa có test case nào: (.+)", text)
    info["uncovered"] = m.group(1).strip().rstrip(".") if m else "—"
    m = re.search(r"Trạng thái test case: (.+)", text)
    info["state"] = m.group(1).strip().rstrip(".") if m else "—"
    return info


# ---------------------------------------------------------------- link mã (test case, bug, requirement)
CASE_CODE = re.compile(r"\b(TC-\d{3}|RG-\d{2}|SM-\d{2}|BUG-\d{3})\b")
REQ_CODE = re.compile(r"(?<![\w-])(S\d{2}-AC\d{2}|[RME]\d{2})(?![\w-])")


class Linker:
    """Biến mã trong câu chữ thành link bấm được (md hoặc html): TC-nnn thành dòng test case, RG-nn/SM-nn thành test case gốc,
    BUG-nnn thành file bug, mã requirement (chỉ khi biết tính năng) thành dòng SRS. Mã không tìm được nơi định nghĩa thì giữ nguyên chữ."""

    def __init__(self, cfg, model):
        from . import docs_pages  # nhập trễ: docs_pages cũng nhập module này

        self.cfg = cfg
        self.index = docs_pages.build_code_index(cfg.project)
        self.names = {f["slug"]: f["name"] for f in model["features"]}
        self.case_map = model["case_map"]
        self.bugs = {b["code"]: b for b in model["bugs"]}

    def _href(self, feature, key, fmt):
        hit = self.index.get((feature, key))
        if not hit:
            return None
        md, anchor = hit
        rel = os.path.relpath(md, self.cfg.project_dir).replace("\\", "/")
        return f"{rel[:-3] + '.html' if fmt == 'html' else rel}#{anchor}"

    def _case(self, code, suite, before):
        if code.startswith(("RG-", "SM-")):
            for name in ([suite] if suite in self.case_map else []) + [k for k in self.case_map if k != suite]:
                hit = self.case_map[name].get(code)
                if hit:
                    return hit[0], hit[1].upper()
            return None
        if suite in self.names:  # bộ test case của một tính năng: TC-nnn thuộc tính năng đó
            return suite, code
        best = None  # bộ smoke/regression: chỉ link khi ngay trước mã có tên tính năng (hoặc phần đầu của tên), ví dụ "Khuyến nghị TC-001"
        tail = before.rstrip()[-60:]
        for slug, name in self.names.items():
            words = name.split()
            for k in range(len(words), 0, -1):
                if tail.endswith(" ".join(words[:k])):
                    if best is None or k > best[0]:
                        best = (k, slug)
                    break
        return (best[1], code) if best else None

    @staticmethod
    def _plain(text, fmt):
        return html.escape(text) if fmt == "html" else text

    @staticmethod
    def _anchor(label, href, fmt):
        return f'<a href="{html.escape(href)}">{html.escape(label)}</a>' if fmt == "html" else f"[{label}]({href})"

    def link(self, text, fmt, suite=None, feature=None):
        """feature=None: link mã test case và bug trong `text` (suite = bộ test chứa câu này); có feature: link mã requirement của tính năng đó."""
        out, pos = [], 0
        for m in (REQ_CODE if feature else CASE_CODE).finditer(text):
            out.append(self._plain(text[pos:m.start()], fmt))
            code, href = m.group(1), None
            if feature:
                href = self._href(feature, code, fmt)
            elif code.startswith("BUG-"):
                bug = self.bugs.get(code)
                href = (bug["href"] if fmt == "html" else bug["href_md"]) if bug else None
            else:
                target = self._case(code, suite, text[:m.start()])
                href = self._href(target[0], target[1], fmt) if target else None
            out.append(self._anchor(code, href, fmt) if href else self._plain(code, fmt))
            pos = m.end()
        out.append(self._plain(text[pos:], fmt))
        return "".join(out)

    def case_item(self, item, fmt):
        href = self._href(item["feature"], item["tc"].upper(), fmt)
        label = self._anchor(item["id"], href, fmt) if href else self._plain(item["id"], fmt)
        return label + (f' <span class="small">({html.escape(item["suite"])})</span>' if fmt == "html" else f" ({item['suite']})")


def build_model(cfg, build=None, author=None):
    suites = _all_suites(cfg)
    names = R.feature_names(cfg.project)
    model = {"project": cfg.project, "url": cfg.url, "empty": not suites}
    if not suites:
        return model
    if build is None:
        newest = max((run["timestamp"], run["build"]) for data, _ in suites.values() for run in data["runs"])
        build = newest[1]
    model["build"] = build
    latest, old_builds = {}, {}
    for name, (data, table) in sorted(suites.items(), key=lambda x: _suite_order(x[0])):
        runs = [r for r in data["runs"] if r["build"] == build]
        if runs:
            latest[name] = (max(runs, key=lambda r: r["number"]), table)
        else:
            old_builds[name] = data["runs"][-1]["build"]
    model["latest"] = {k: v[0] for k, v in latest.items()}
    model["old_builds"] = old_builds
    model["based_on"] = {k: v[0]["number"] for k, v in latest.items()}
    all_runs = sorted(((r, name, suites[name][1]) for name in latest for r in suites[name][0]["runs"] if r["build"] == build), key=lambda x: x[0]["timestamp"])
    model["author"] = author or max(latest.values(), key=lambda x: x[0]["timestamp"])[0]["run_by"]
    model["date_from"] = min(r["timestamp"] for r, _, _ in all_runs)
    model["date_to"] = max(r["timestamp"] for r, _, _ in all_runs)

    testers = {}
    for name, (run, _) in latest.items():
        t = testers.setdefault(run["run_by"], {"methods": [], "runs": []})
        if run["run_method"] not in t["methods"]:
            t["methods"].append(run["run_method"])
        t["runs"].append(f"{R.suite_title(name, cfg.project)} (lượt {run['number']})")
    model["testers"] = testers

    # Kết quả mới nhất của từng test case trong build này (kết luận thật thắng "Bị chặn/Không kết luận"; lượt sau thắng lượt trước)
    status = {}
    for run, name, table in all_runs:
        for entry in table:
            v = run["results"].get(entry["number"])
            if not v:
                continue
            key = (entry["feature"], entry["tc"])
            new = v["status"]
            cur = status.get(key)
            if new in R.HAS_VERDICT or (new in (R.BLOCKED, R.NO_VERDICT, R.SKIPPED) and (cur is None or cur not in R.HAS_VERDICT)):
                status[key] = new
    features = []
    for d in sorted(x for x in cfg.project_dir.iterdir() if x.is_dir() and (x / "test-case.md").exists()):
        table = R.read_feature_table(cfg, d.name)
        counts = {k: 0 for k, _ in CATEGORIES}
        for e in table:
            counts[category(status.get((d.name, e["tc"]), R.NOT_RUN))] += 1
        features.append({"slug": d.name, "name": names.get(d.name, d.name), "total": len(table), "counts": counts})
    model["features"] = features

    rows = []
    for name, (run, _) in latest.items():
        page = R.page_files(cfg, name)[1]
        rows.append({"suite": name, "title": R.suite_title(name, cfg.project), "run": run, "counts": R._count_statuses(run), "href": _rel(cfg, page)})
    model["suite_rows"] = rows

    bug_files = sorted(cfg.project_dir.glob("**/bug/BUG-*.md"))
    found = {}
    for name, (run, table) in latest.items():
        ids = {b["number"]: b["id"] for b in table}
        entries = {b["number"]: b for b in table}
        for number, v in run["results"].items():
            for x in v.get("bug", []):
                found.setdefault(x["code"], [])
                entry = entries[number]
                item = {"id": ids[number], "feature": entry["feature"], "tc": entry["tc"], "suite": R.suite_title(name, cfg.project)}
                if item not in found[x["code"]]:
                    found[x["code"]].append(item)
    bugs = []
    for f in bug_files:
        code = f.stem
        status, status_note = bug_page.read_status(f.read_text(encoding="utf-8"))
        bugs.append({"code": code, "title": R._bug_title(cfg, code), "severity": R._bug_severity(cfg, code) or "—", "status": status, "status_note": status_note,
                     "found": found.get(code, []), "href": _rel(cfg, f.with_suffix(".html")), "href_md": _rel(cfg, f)})
    model["bugs"] = bugs
    model["case_map"] = {name: {b["id"]: (b["feature"], b["tc"]) for b in table} for name, (_, table) in suites.items()}

    model["coverage"] = [_requirement_coverage(cfg, f["slug"], names) for f in features]
    model["headlines"], model["not_tested"], model["risks"], model["suggestions"] = [], [], [], []
    for name, (run, _) in latest.items():
        k = run.get("conclusion")
        title = R.suite_title(name, cfg.project)
        if not k:
            continue
        model["headlines"].append((name, title, k.get("headline", "")))
        model["not_tested"] += [{"suite": title, "slug": name, **x} for x in k.get("not_tested", [])]
        model["risks"] += [{"suite": title, "slug": name, **x} for x in k.get("risks", [])]
        if k.get("suggestion"):
            model["suggestions"].append((name, title, k["suggestion"]))

    totals = {k: sum(f["counts"][k] for f in features) for k, _ in CATEGORIES}
    model["totals"] = totals
    model["total_cases"] = sum(f["total"] for f in features)

    model["approvals"] = read_approvals(cfg)
    model["record"] = next((a for a in model["approvals"] if a["build"] == build), None)
    return model


def staleness(model, record):
    """('current'|'stale'|'other_build', [lý do]) cho một quyết định đã ghi."""
    if record["build"] != model["build"]:
        return "other_build", []
    based = record.get("based_on") or {}
    reasons = []
    for name, number in model["based_on"].items():
        if based.get(name) != number:
            reasons.append(f"{R.suite_title(name, model['project'])}: lúc duyệt là lượt {based.get(name, 'chưa có')}, nay là lượt {number}")
    return ("stale" if reasons else "current"), reasons


def _validity_text(state):
    return {"current": "Còn hiệu lực", "stale": "Đã lỗi thời", "other_build": "Build khác"}[state]


def _facts_sentence(model):
    t = model["totals"]
    ran = t["pass"] + t["pass_issue"] + t["fail"]
    parts = [f"Tổng {model['total_cases']} test case của {len(model['features'])} tính năng: {ran} đã có kết luận ({_percent(ran, model['total_cases'])}), trong đó {t['pass']} Đạt, {t['pass_issue']} Đạt kèm lỗi, {t['fail']} Không đạt; "
             f"{t['open']} bị chặn hoặc chưa kết luận được, {t['skipped']} bỏ qua, {t['not_run']} chưa chạy."]
    open_bugs = [b for b in model["bugs"] if b["found"]]
    parts.append(f"{len(open_bugs)} bug được ghi nhận trong các lượt của build này (tổng {len(model['bugs'])} bug đã ghi).")
    if model["bugs"]:
        parts.append("Trạng thái bug: " + _status_counts_text(model["bugs"]) + ".")
    return " ".join(parts)


def _status_counts_text(bugs):
    """Ví dụ '2 Đóng, 1 Mở lại, 4 Chưa ghi' theo thứ tự cố định."""
    order = list(bug_page.BUG_STATUSES) + [bug_page.STATUS_UNSET]
    counts = {}
    for b in bugs:
        counts[b["status"]] = counts.get(b["status"], 0) + 1
    names = [s for s in order if s in counts] + [s for s in counts if s not in order]
    return ", ".join(f"{counts[s]} {s}" for s in names)


def _status_text(b):
    return b["status"] + (f" ({b['status_note']})" if b["status_note"] else "")


# ---------------------------------------------------------------- md
def _md_cell(text):
    return str(text).replace("|", "\\|").replace("\n", "<br>")


def _md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    out += ["| " + " | ".join(_md_cell(c) for c in r) + " |" for r in rows]
    return out


def _person_rows(record, key, fields):
    block = (record or {}).get(key) or {}
    return [(label, block.get(f) or "(chưa điền)") for label, f in fields]


def build_md(cfg, model):
    if model["empty"]:
        return "# Báo cáo tổng kết kiểm thử\n\nChưa có lượt chạy nào để tổng hợp.\n"
    p = model["project"]
    lk = Linker(cfg, model)
    d = ["# Báo cáo tổng kết kiểm thử", "",
         "> File tự sinh bằng `scripts/build_docs.py` từ các lượt chạy, bug và truy vết; đừng sửa tay. Quyết định của người test và người duyệt nằm ở "
         f"`testing/{p}/{APPROVAL_FILE}` (điền trên trang HTML rồi tải file về). Bản dễ xem và có nút in PDF: `test-summary-report.html`.", "",
         "## 1. Thông tin chung", ""]
    tester_rows = [f"{name}: {', '.join(t['methods'])} ({'; '.join(t['runs'])})" for name, t in model["testers"].items()]
    d += _md_table(["Mục", "Nội dung"], [
        ("Dự án", p), ("Build", model["build"]), ("Môi trường", model["url"]), ("Thời gian test", f"{model['date_from']} đến {model['date_to']}"),
        ("Người viết báo cáo", model["author"]), ("Người test", "<br>".join(tester_rows)),
        ("Phạm vi", "Smoke, regression và test case theo từng tính năng: " + ", ".join(f["name"] for f in model["features"]))])
    if model["old_builds"]:
        d += ["", "Chưa có lượt nào ở build này: " + "; ".join(f"{R.suite_title(n, p)} (lượt mới nhất ở build {b})" for n, b in model["old_builds"].items()) + "."]
    d += ["", "## 2. Kết luận", "", "**Tình trạng theo số liệu.** " + _facts_sentence(model), ""]
    d += [f"- {t}: {lk.link(h, 'md', slug)}" for slug, t, h in model["headlines"]] or ["- Các lượt chưa có phần Kết luận và rủi ro."]
    d += ["", "**Đề xuất của người test** (nhận build / không nhận / nhận có điều kiện):", ""]
    d += _md_table(["Mục", "Nội dung"], _person_rows(model["record"], "tester", [("Đề xuất", "decision"), ("Lý do", "reason"), ("Ngày", "date")]))
    d += ["", "## 3. Kết quả theo tính năng", "",
          "Mỗi test case lấy kết quả mới nhất trong các lượt của build này (smoke, regression, test case tính năng). Tỉ lệ đạt tính trên số đã có kết luận."]
    d += [""] + _md_table(["Tính năng", "Tổng"] + [n for _, n in CATEGORIES] + ["Đã chạy", "Tỉ lệ đạt"], [
        (f["name"], f["total"], *[f["counts"][k] for k, _ in CATEGORIES], _percent(f["counts"]["pass"] + f["counts"]["pass_issue"] + f["counts"]["fail"], f["total"]),
         _percent(f["counts"]["pass"] + f["counts"]["pass_issue"], f["counts"]["pass"] + f["counts"]["pass_issue"] + f["counts"]["fail"])) for f in model["features"]])
    d += ["", "## 4. Kết quả theo bộ test", ""]
    d += _md_table(["Bộ test", "Lượt", "Thời điểm", "Kết quả", "Kết luận", "Trang kết quả"], [
        (r["title"], r["run"]["number"], r["run"]["timestamp"], r["counts"], r["run"]["verdict"], f"[mở]({r['href']})") for r in model["suite_rows"]])
    d += ["", "## 5. Bug", ""]
    d += (_md_table(["Bug", "Tiêu đề", "Mức độ nghiêm trọng", "Trạng thái", "Case thấy lỗi ở build này"], [(f"[{b['code']}]({b['href_md']})", b["title"], b["severity"], _status_text(b), "; ".join(lk.case_item(i, "md") for i in b["found"]) or "—") for b in model["bugs"]])
          if model["bugs"] else ["Chưa có bug nào được ghi."])
    d += ["", BUG_STATUS_NOTE, "", "## 6. Độ phủ requirement", ""]
    d += _md_table(["Tính năng", "Mã requirement", "Mã chưa có test case", "Trạng thái test case", "Truy vết"], [
        (c["name"], c["requirements"], lk.link(c["uncovered"], "md", feature=c["slug"]), c["state"], f"[mở]({c['href']})" if c["href"] else "—") for c in model["coverage"]])
    d += ["", "## 7. Rủi ro còn lại", ""]
    if model["not_tested"]:
        d += ["**Chưa có kết quả và vì sao**", ""] + _md_table(["Bộ test", "Case", "Trạng thái", "Lý do"], [(x["suite"], lk.link(x["cases"], "md", x["slug"]), x["status"], lk.link(x["reason"], "md", x["slug"])) for x in model["not_tested"]]) + [""]
    d += [f"- **{lk.link(x['title'], 'md', x['slug'])}** ({x['suite']}). {lk.link(x['detail'], 'md', x['slug'])}" for x in model["risks"]] or ["Các lượt chưa ghi rủi ro nào."]
    d += ["", "## 8. Đề xuất bước tiếp theo", ""]
    d += [f"- {t}: {lk.link(text, 'md', slug)}" for slug, t, text in model["suggestions"]] or ["Các lượt chưa ghi đề xuất."]
    d += ["", "## 9. Duyệt build", "", "Người duyệt điền trên trang HTML (mục 9), tải file `duyet-build.json`, đặt vào " f"`testing/{p}/` rồi chạy lại `python -X utf8 scripts/build_docs.py`.", ""]
    rec = model["record"]
    if rec:
        state, reasons = staleness(model, rec)
        d += [f"Trạng thái quyết định: **{_validity_text(state)}**" + (" (" + "; ".join(reasons) + ")" if reasons else "") + ".", ""]
    d += _md_table(["Mục", "Nội dung"], _person_rows(rec, "approver", [("Người duyệt", "name"), ("Chức danh", "title"), ("Quyết định", "decision"), ("Điều kiện kèm theo", "conditions"), ("Ghi chú", "note"), ("Ngày duyệt", "date")]))
    others = [a for a in model["approvals"] if a is not rec]
    if others:
        d += ["", "**Các lần duyệt khác**", ""] + _md_table(["Build", "Người duyệt", "Quyết định", "Ngày"], [(a["build"], (a.get("approver") or {}).get("name", ""), (a.get("approver") or {}).get("decision", ""), (a.get("approver") or {}).get("date", "")) for a in others])
    d += ["", "## Phụ lục: trang kết quả từng lượt", ""] + [f"- [{r['title']}]({r['href']})" for r in model["suite_rows"]] + [""]
    return "\n".join(d)


# ---------------------------------------------------------------- HTML
_CSS = """
.tg{display:grid;grid-template-columns:max-content 1fr;gap:6px 22px;margin:0}.tg dt{font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);padding-top:3px}.tg dd{margin:0}
.so{display:flex;flex-wrap:wrap;gap:12px;margin:14px 0}.so div{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px 18px;min-width:120px}.so b{display:block;font:700 26px/1.2 "Be Vietnam Pro","Segoe UI",system-ui,sans-serif;color:var(--text)}.so span{font-size:13px;color:var(--muted)}
.chon{display:flex;flex-wrap:wrap;gap:10px;margin:6px 0 14px}.nut{position:relative}.nut input{position:absolute;opacity:0;inset:0;cursor:pointer}.nut span{display:inline-block;padding:9px 18px;border-radius:999px;border:2px solid var(--line);background:var(--card);font-weight:700;cursor:pointer;color:var(--body)}
.nut input:focus-visible+span{outline:3px solid var(--amber)}.nut-ok input:checked+span{background:var(--greenbg);border-color:var(--green);color:var(--green)}.nut-bad input:checked+span{background:var(--pinkbg);border-color:var(--coral);color:var(--coral)}.nut-warn input:checked+span{background:var(--amberbg);border-color:var(--amber);color:var(--amberfg)}
.form{display:grid;grid-template-columns:max-content 1fr;gap:10px 18px;align-items:start}.form label.t{font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);padding-top:9px}
.form input[type=text],.form input[type=date],.form textarea{width:100%;max-width:640px;padding:8px 12px;border:1px solid var(--line);border-radius:10px;background:var(--bg);color:var(--text);font:inherit}.form textarea{min-height:76px;resize:vertical}
.hanh-dong{display:flex;flex-wrap:wrap;gap:10px;margin:16px 0 6px}.hanh-dong button{padding:9px 18px;border-radius:999px;border:1px solid var(--line);background:var(--card);color:var(--body);font:700 14px/1 inherit;font-family:inherit;cursor:pointer}.hanh-dong button.chinh{background:var(--coral);border-color:var(--coral);color:#fff}.hanh-dong button:hover{border-color:var(--coral)}
.tb{min-height:22px;font-size:14px;color:var(--muted)}.tb.loi{color:var(--coral);font-weight:700}
.canh-bao{background:var(--amberbg);border:1px solid var(--warnline);color:var(--amberfg);border-radius:12px;padding:10px 16px;margin:0 0 14px}
.min table{min-width:0}
@page{size:A4;margin:14mm}
@media print{.theme,.hanh-dong,.tb,.khong-in{display:none!important}body{padding:0;background:#fff}main,main.rong{max-width:none}.wrap{overflow:visible;border-radius:6px}table{min-width:0}th,td{padding:6px 8px;font-size:12px}tr{break-inside:avoid}h2,h3{break-after:avoid}.card{break-inside:auto}.form,.chon{break-inside:avoid}.nut input:not(:checked)+span{display:none}.chon{margin:2px 0 8px}.form input,.form textarea{border:0;border-bottom:1px solid #999;border-radius:0;background:none;max-width:none}}
"""

_JS = """
(function(){
var el=document.getElementById('du-lieu');if(!el)return;
var D=JSON.parse(el.textContent),KEY='duyet-'+D.project+'-'+D.build;
function $(i){return document.getElementById(i)}
var inputs=[].slice.call(document.querySelectorAll('[data-k]'));
function get(o,p){var a=p.split('.');for(var i=0;i<a.length;i++){if(!o)return '';o=o[a[i]]}return o==null?'':o}
function put(o,p,v){var a=p.split('.');for(var i=0;i<a.length-1;i++){o=o[a[i]]=o[a[i]]||{}}o[a[a.length-1]]=v}
function read(){var r={};inputs.forEach(function(x){if(x.type==='radio'){if(x.checked)put(r,x.dataset.k,x.value)}else put(r,x.dataset.k,x.value)});return r}
function fill(r){inputs.forEach(function(x){var v=get(r,x.dataset.k);if(x.type==='radio')x.checked=(x.value===v);else x.value=v})}
function msg(t,bad){var m=$('tb');m.textContent=t;m.className='tb'+(bad?' loi':'')}
function sync(){var r=read(),a=r.approver||{};var show=a.decision==='Nhận có điều kiện'||(a.conditions||'').trim()!=='';$('hang-dk-nhan').style.display=show?'':'none';$('d-dk').style.display=show?'':'none'}
var saved=null;D.approvals.forEach(function(a){if(a.build===D.build)saved=a});
var draft=null;try{draft=JSON.parse(localStorage.getItem(KEY)||'null')}catch(e){}
var start=draft||saved||{};
if(!(start.tester&&start.tester.name)){start.tester=start.tester||{};start.tester.name=D.author}
fill(start);sync();
if(draft)msg('Đang hiện bản nháp lưu trong trình duyệt này, chưa tải về file.');
inputs.forEach(function(x){x.addEventListener('input',change);x.addEventListener('change',change)});
function change(){sync();try{localStorage.setItem(KEY,JSON.stringify(read()));msg('Đã lưu nháp trong trình duyệt. Bấm Tải file duyệt để đưa vào repo.')}catch(e){}}
function today(){var d=new Date(),p=function(n){return String(n).padStart(2,'0')};return d.getFullYear()+'-'+p(d.getMonth()+1)+'-'+p(d.getDate())}
$('tai').onclick=function(){
 var r=read(),a=r.approver||{},t=r.tester||{};
 if(!a.decision&&!t.decision){msg('Chưa chọn quyết định nào để lưu.',1);return}
 if(a.decision&&!(a.name||'').trim()){msg('Cần điền tên người duyệt.',1);return}
 if(a.decision==='Nhận có điều kiện'&&!(a.conditions||'').trim()){msg('Chọn "Nhận có điều kiện" thì cần ghi điều kiện kèm theo.',1);return}
 if(a.decision&&!a.date){a.date=today();r.approver=a}
 if(t.decision&&!t.date){t.date=today();r.tester=t}
 fill(r);r.build=D.build;r.based_on=D.based_on;
 var list=D.approvals.filter(function(x){return x.build!==D.build});list.push(r);
 var blob=new Blob([JSON.stringify({approvals:list},null,2)+'\\n'],{type:'application/json'}),u=URL.createObjectURL(blob),l=document.createElement('a');
 l.href=u;l.download='duyet-build.json';document.body.appendChild(l);l.click();l.remove();URL.revokeObjectURL(u);
 try{localStorage.removeItem(KEY)}catch(e){}
 msg('Đã tải duyet-build.json. Đặt file vào '+D.dir+' (ghi đè file cũ), rồi chạy lại build_docs.py. Nếu trình duyệt đổi tên thành duyet-build (1).json thì đổi lại cho đúng.')};
$('xoa').onclick=function(){try{localStorage.removeItem(KEY)}catch(e){}fill(saved||{tester:{name:D.author}});sync();msg('Đã bỏ bản nháp, trở về nội dung trong file.')};
var prevTheme=null;
$('in').onclick=function(){window.print()};$('in2').onclick=function(){window.print()};
window.addEventListener('beforeprint',function(){prevTheme=document.documentElement.getAttribute('data-theme');document.documentElement.setAttribute('data-theme','light');[].forEach.call(document.querySelectorAll('textarea'),function(x){x.style.height='auto';x.style.height=x.scrollHeight+'px'})});
window.addEventListener('afterprint',function(){if(prevTheme)document.documentElement.setAttribute('data-theme',prevTheme);else document.documentElement.removeAttribute('data-theme')});
})();
"""


def _e(x):
    return html.escape(str(x))


def _radios(name):
    return '<div class="chon">' + "".join(
        f'<label class="nut nut-{DECISION_CLASS[d]}"><input type="radio" name="{name}" data-k="{name}" value="{_e(d)}"><span>{_e(d)}</span></label>' for d in DECISIONS) + "</div>"


def _table(headers, rows, cls="wrap", hide=()):
    """hide: số thứ tự cột (từ 0) chỉ có ích khi xem trên máy (link tới trang khác), ẩn khi in."""
    mark = lambda i: ' class="khong-in"' if i in hide else ""  # noqa: E731
    head = "".join(f"<th{mark(i)}>{h}</th>" for i, h in enumerate(headers))
    body = "".join("<tr>" + "".join(f"<td{mark(i)}>{c}</td>" for i, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<div class="{cls}"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def _badge(text, cls):
    return f'<span class="badge {cls}">{_e(text)}</span>'


def build_html(cfg, model):
    from . import theme as theme_mod

    title = f"Báo cáo tổng kết kiểm thử {model['project']}"
    head = theme_mod.page_head(title, cfg.project_dir, _CSS)
    if model["empty"]:
        return head + '<body><main class="rong">' + "<h1>Báo cáo tổng kết kiểm thử</h1><p>Chưa có lượt chạy nào để tổng hợp.</p></main></body></html>"
    p, e = model["project"], _e
    lk = Linker(cfg, model)
    t = model["totals"]
    ran = t["pass"] + t["pass_issue"] + t["fail"]
    out = [head, '<body><button id="theme" class="theme" type="button">Chế độ tối</button><main class="rong">',
           "<h1>Báo cáo tổng kết kiểm thử</h1>",
           '<div class="hanh-dong"><button type="button" id="in">In / Lưu PDF</button></div>']

    out.append("<h2>1. Thông tin chung</h2><div class=\"card\"><dl class=\"tg\">")
    testers = "<br>".join(f"<strong>{e(n)}</strong>: {e(', '.join(x['methods']))} <span class='small'>({e('; '.join(x['runs']))})</span>" for n, x in model["testers"].items())
    for k, v in (("Dự án", e(p)), ("Build", f"<strong>{e(model['build'])}</strong>"), ("Môi trường", f"<a href='{e(model['url'])}/'>{e(model['url'])}</a>"),
                 ("Thời gian test", f"{e(model['date_from'])} đến {e(model['date_to'])}"), ("Người viết báo cáo", e(model["author"])), ("Người test", testers),
                 ("Phạm vi", e("Smoke, regression và test case theo từng tính năng: " + ", ".join(f["name"] for f in model["features"])))):
        out.append(f"<dt>{k}</dt><dd>{v}</dd>")
    out.append("</dl>")
    if model["old_builds"]:
        out.append('<p class="small">Chưa có lượt nào ở build này: ' + e("; ".join(f"{R.suite_title(n, p)} (lượt mới nhất ở build {b})" for n, b in model["old_builds"].items())) + ".</p>")
    out.append("</div>")

    out.append("<h2>2. Kết luận</h2>")
    out.append('<div class="so">' + "".join(f"<div><b>{v}</b><span>{k}</span></div>" for k, v in (
        ("test case", model["total_cases"]), (f"đã có kết luận ({_percent(ran, model['total_cases'])})", ran), ("Đạt (cả kèm lỗi)", t["pass"] + t["pass_issue"]), ("Không đạt", t["fail"]),
        ("bị chặn / chưa kết luận", t["open"]), ("chưa chạy / bỏ qua", t["not_run"] + t["skipped"]), ("bug đã ghi", len(model["bugs"])))) + "</div>")
    out.append(f'<div class="card"><p><strong>Tình trạng theo số liệu.</strong> {e(_facts_sentence(model))}</p><ul>'
               + ("".join(f"<li><strong>{e(t)}:</strong> {lk.link(h, 'html', slug)}</li>" for slug, t, h in model["headlines"]) or "<li>Các lượt chưa có phần Kết luận và rủi ro.</li>") + "</ul>"
               '<h3>Đề xuất của người test</h3><p class="small">Đề xuất dựa trên số liệu; quyết định cuối cùng ở mục 9.</p>'
               + _radios("tester.decision") +
               '<div class="form"><label class="t" for="t-ly-do">Lý do</label><textarea id="t-ly-do" data-k="tester.reason"></textarea>'
               '<label class="t" for="t-ten">Người đề xuất</label><input type="text" id="t-ten" data-k="tester.name">'
               '<label class="t" for="t-ngay">Ngày</label><input type="date" id="t-ngay" data-k="tester.date"></div></div>')

    out.append("<h2>3. Kết quả theo tính năng</h2><p class=\"small\">Mỗi test case lấy kết quả mới nhất trong các lượt của build này (smoke, regression, test case tính năng). Tỉ lệ đạt tính trên số đã có kết luận.</p>")
    out.append(_table(["Tính năng", "Tổng"] + [n for _, n in CATEGORIES] + ["Đã chạy", "Tỉ lệ đạt"], [
        (f"<strong>{e(f['name'])}</strong>", f["total"], *[f["counts"][k] for k, _ in CATEGORIES],
         _percent(f["counts"]["pass"] + f["counts"]["pass_issue"] + f["counts"]["fail"], f["total"]),
         _percent(f["counts"]["pass"] + f["counts"]["pass_issue"], f["counts"]["pass"] + f["counts"]["pass_issue"] + f["counts"]["fail"])) for f in model["features"]]))

    out.append("<h2>4. Kết quả theo bộ test</h2>")
    out.append(_table(["Bộ test", "Lượt", "Thời điểm", "Kết quả", "Kết luận", "Chi tiết"], [
        (e(r["title"]), r["run"]["number"], e(r["run"]["timestamp"]), e(r["counts"]), R._verdict_badge(r["run"]["verdict"]), f'<a href="{e(r["href"])}">Mở trang kết quả</a>') for r in model["suite_rows"]], hide=(5,)))

    out.append("<h2>5. Bug</h2>")
    out.append(_table(["Bug", "Tiêu đề", "Mức độ nghiêm trọng", "Trạng thái", "Case thấy lỗi ở build này"], [
        (f'<a href="{e(b["href"])}">{e(b["code"])}</a>', e(b["title"]), e(b["severity"]),
         bug_page.status_badge(b["status"]) + (f' <span class="small">{e(b["status_note"])}</span>' if b["status_note"] else ""),
         "; ".join(lk.case_item(i, "html") for i in b["found"]) or "—") for b in model["bugs"]]) if model["bugs"] else "<p>Chưa có bug nào được ghi.</p>")
    out.append(f'<p class="small">{e(BUG_STATUS_NOTE)}</p>')

    out.append("<h2>6. Độ phủ requirement</h2>")
    out.append(_table(["Tính năng", "Mã requirement", "Mã chưa có test case", "Trạng thái test case", "Truy vết"], [
        (e(c["name"]), e(c["requirements"]), lk.link(c["uncovered"], "html", feature=c["slug"]), e(c["state"]), f'<a href="{e(c["href"])}">Mở truy vết</a>' if c["href"] else "—") for c in model["coverage"]], hide=(4,)))

    out.append("<h2>7. Rủi ro còn lại</h2>")
    if model["not_tested"]:
        out.append("<h3>Chưa có kết quả và vì sao</h3>" + _table(["Bộ test", "Case", "Trạng thái", "Lý do"], [(e(x["suite"]), lk.link(x["cases"], "html", x["slug"]), R._badge(x["status"]), lk.link(x["reason"], "html", x["slug"])) for x in model["not_tested"]]))
    out.append('<div class="card"><ul>' + ("".join(f"<li><strong>{lk.link(x['title'], 'html', x['slug'])}</strong> <span class='small'>({e(x['suite'])})</span>. {lk.link(x['detail'], 'html', x['slug'])}</li>" for x in model["risks"]) or "<li>Các lượt chưa ghi rủi ro nào.</li>") + "</ul></div>")

    out.append("<h2>8. Đề xuất bước tiếp theo</h2><div class=\"card\"><ul>" + ("".join(f"<li><strong>{e(t)}:</strong> {lk.link(text, 'html', slug)}</li>" for slug, t, text in model["suggestions"]) or "<li>Các lượt chưa ghi đề xuất.</li>") + "</ul></div>")

    out.append("<h2>9. Duyệt build</h2>")
    rec = model["record"]
    if rec:
        state, reasons = staleness(model, rec)
        if state == "stale":
            out.append('<div class="canh-bao"><strong>Quyết định đã ghi đã lỗi thời.</strong> Sau khi duyệt có lượt chạy mới: ' + e("; ".join(reasons)) + ". Xem lại rồi duyệt lại nếu cần.</div>")
    out.append('<div class="card"><p class="small khong-in">Người duyệt điền, chọn quyết định rồi bấm Tải file duyệt.</p><p class="small">Trang này ghi nhận quyết định, không thay chữ ký hay quy trình duyệt của công ty.</p>'
               + _radios("approver.decision") +
               '<div class="form"><label class="t" for="d-ten">Người duyệt</label><input type="text" id="d-ten" data-k="approver.name">'
               '<label class="t" for="d-chuc">Chức danh</label><input type="text" id="d-chuc" data-k="approver.title">'
               '<label class="t" for="d-dk" id="hang-dk-nhan">Điều kiện kèm theo</label><textarea id="d-dk" data-k="approver.conditions"></textarea>'
               '<label class="t" for="d-ghi">Ghi chú</label><textarea id="d-ghi" data-k="approver.note"></textarea>'
               '<label class="t" for="d-ngay">Ngày duyệt</label><input type="date" id="d-ngay" data-k="approver.date"></div>'
               '<div class="hanh-dong"><button type="button" class="chinh" id="tai">Tải file duyệt</button><button type="button" id="xoa">Bỏ bản nháp</button><button type="button" id="in2" onclick="document.getElementById(\'in\').click()">In / Lưu PDF</button></div>'
               '<p class="tb" id="tb" role="status"></p></div>')
    if model["approvals"]:
        rows = []
        for a in sorted(model["approvals"], key=lambda x: (x["build"], (x.get("approver") or {}).get("date", "")), reverse=True):
            ap = a.get("approver") or {}
            state, _ = staleness(model, a)
            rows.append((e(a["build"]), e(ap.get("name", "—")), _badge(ap["decision"], DECISION_CLASS.get(ap["decision"], "gray")) if ap.get("decision") else "—", e(ap.get("date", "—")),
                         _badge(_validity_text(state), {"current": "ok", "stale": "warn", "other_build": "gray"}[state])))
        out.append("<h3>Các lần duyệt đã ghi</h3>" + _table(["Build", "Người duyệt", "Quyết định", "Ngày", "Hiệu lực"], rows))
    out.append('<div class="khong-in"><h2>Phụ lục: trang kết quả từng lượt</h2><ul>' + "".join(f'<li><a href="{e(r["href"])}">{e(r["title"])}</a></li>' for r in model["suite_rows"]) + "</ul></div>")

    data = {"project": p, "build": model["build"], "based_on": model["based_on"], "author": model["author"], "approvals": model["approvals"], "dir": f"testing/{p}/"}
    out.append('<script type="application/json" id="du-lieu">' + json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + "</script>")
    out.append(f"<script>{_JS}</script></main></body></html>")
    return "".join(out)


def render_pages(cfg, build=None, author=None):
    """Sinh (chưa ghi) trang md + html: {đường dẫn: nội dung}. Dự án chưa có lượt chạy nào thì không sinh gì."""
    model = build_model(cfg, build, author)
    if model["empty"]:
        return {}
    md_file, html_file = page_paths(cfg)
    return {md_file: build_md(cfg, model), html_file: build_html(cfg, model)}


def build_pages(cfg, build=None, author=None):
    pages = render_pages(cfg, build, author)
    for path, text in pages.items():
        path.write_text(text, encoding="utf-8")
    return list(pages)
