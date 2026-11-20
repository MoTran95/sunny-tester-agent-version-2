"""Bảng kết quả các lượt chạy bộ test (smoke, sau này regression) và trang HTML xem nhanh.

Dữ liệu gốc: `testing/<dự-án>/run-results/<bộ>.json` (chỉ thêm lượt mới, không sửa tay).
Từ đó script sinh ra (đừng sửa tay, chạy lại là ghi đè):
  - testing/<dự-án>/<bộ>-ket-qua.md
  - testing/<dự-án>/<bộ>-ket-qua.html
Bảng chính 6 cột: ID, Smoke case, Status, Evidence, Bug, Số lần chạy. "Số lần chạy" = số lượt đã có
kết luận Đạt/Không đạt cho case đó (đếm từ lịch sử, không ghi tay).
"""
import html
import json
import re
import time
from pathlib import Path

from . import config
from . import theme as theme_mod
from .theme import CSS_BASE as _CSS, JS_DRAG_SCROLL as _JS_DRAG_SCROLL, JS_THEME as _JS_THEME, LOGO_PATH, logo_data_uri as _logo_data_uri  # noqa: F401

PASS = "Đạt"
PASS_KNOWN_ISSUE = "Đạt kèm lỗi đã biết"
PASS_MINOR_FAIL = "Đạt kèm ý phụ sai"
FAIL = "Không đạt"
NO_VERDICT = "Không kết luận"
NOT_RUN = "Chưa chạy"
NO_SCRIPT = "Chưa có script"
HAS_VERDICT = {PASS, PASS_KNOWN_ISSUE, PASS_MINOR_FAIL, FAIL}
BLOCKED = "Bị chặn"
SKIPPED = "Bỏ qua"
ACCEPT_BUILD, REJECT_BUILD, INCOMPLETE = "Nhận build", "Trả build", "Chưa đủ kết luận"
ALL_PASS, HAS_FAIL, NOT_ALL_RUN = "Đạt toàn bộ", "Có case không đạt", "Chưa chạy hết"
SUITE_NAMES = {"smoke": "Smoke test", "regression": "Regression"}
MATRIX_RUNS = 8

_CELL_SPLIT = re.compile(r"(?<!\\)\|")


# ---------- đọc bảng smoke ----------
def read_smoke_table(cfg):
    """[{so, id, ten, ma_goc, tinh_nang, tc}] đọc từ bảng chính của smoke-test.md."""
    f = cfg.project_dir / "smoke-test.md"
    if not f.exists():
        raise config.ConfigError(f"Không có {f.relative_to(config.ROOT)}")
    entries, seen = [], set()
    for line in f.read_text(encoding="utf-8").splitlines():
        m_so = re.match(r"^\|\s*(\d+)\s*\|", line)
        m_ca = re.search(r"\[([^\]]+)\]\(([\w-]+)/test-case\.md#(tc-\d+)\)", line)
        if not (m_so and m_ca) or m_so.group(1) in seen:
            continue
        o = _CELL_SPLIT.split(line)
        seen.add(m_so.group(1))
        entries.append({"number": m_so.group(1), "id": f"SM-{int(m_so.group(1)):02d}", "title": o[2].strip(),
                   "source_ref": m_ca.group(1), "feature": m_ca.group(2), "tc": m_ca.group(3)})
    return sorted(entries, key=lambda x: int(x["number"]))


def read_feature_table(cfg, feature):
    """Bảng toàn bộ test case của một tính năng (đọc test-case.md theo TÊN cột): cùng dạng với read_smoke_table."""
    f = cfg.project_dir / feature / "test-case.md"
    if not f.exists():
        raise config.ConfigError(f"Không có {f.relative_to(config.ROOT)}")
    names, entries = None, []
    for line in f.read_text(encoding="utf-8").splitlines():
        if names is None and line.startswith("| Mã |"):
            names = [c.strip() for c in _CELL_SPLIT.split(line)[1:-1]]
        elif names:
            m = re.match(r'^\|\s*<a id="(tc-\d+)"></a>(TC-\d+)', line)
            if m:
                d = dict(zip(names, [c.strip() for c in _CELL_SPLIT.split(line)[1:-1]]))
                entries.append({"number": str(int(m.group(1)[3:])), "id": m.group(2), "title": d.get("Tình huống", "").replace("**", ""),
                                "source_ref": "Ưu tiên " + d.get("Ưu tiên", "?"), "feature": feature, "tc": m.group(1)})
    return sorted(entries, key=lambda x: int(x["number"]))


def is_regression(suite):
    """Bộ regression theo tầng: tên bộ dạng `regression-tang-1` (Tầng 1), `regression-tang-2`, `regression-tang-3`."""
    return suite.startswith("regression-tang-")


def read_regression_table(cfg, suite):
    """Các case của MỘT tầng trong regression-test.md: cùng dạng với read_smoke_table.
    Mỗi dòng tầng có link [Tên · TC-005](thư-mục/test-case.md#tc-005); ID là RG-01, RG-02… theo thứ tự trong bảng; vùng nằm ở source_ref."""
    tang = f"Tầng {suite.rsplit('-', 1)[1]}"
    f = cfg.project_dir / "regression-test.md"
    if not f.exists():
        raise config.ConfigError(f"Không có {f.relative_to(config.ROOT)}")
    names = feature_names(cfg.project)
    entries, seen, cache = [], set(), {}
    for line in f.read_text(encoding="utf-8").splitlines():
        if not line.startswith(f"| {tang} |"):
            continue
        o = _CELL_SPLIT.split(line)
        vung = o[2].strip()
        for m in re.finditer(r"\[([^\]]+)\]\(([\w-]+)/test-case\.md#(tc-\d+)\)", o[3]):
            feature, tc = m.group(2), m.group(3)
            if (feature, tc) in seen:
                continue
            seen.add((feature, tc))
            if feature not in cache:
                cache[feature] = {e["tc"]: e for e in read_feature_table(cfg, feature)}
            goc = cache[feature].get(tc)
            title = (goc["title"] if goc else m.group(1)).strip()
            n = len(entries) + 1
            entries.append({"number": str(n), "id": f"RG-{n:02d}", "title": f"[{names.get(feature, feature)} · {tc.upper()}] {title}",
                            "source_ref": vung, "feature": feature, "tc": tc})
    return entries


def read_table(cfg, suite):
    if is_regression(suite):
        return read_regression_table(cfg, suite)
    return read_smoke_table(cfg) if suite == "smoke" else read_feature_table(cfg, suite)


def feature_names(project):
    """Tên hiển thị tiếng Việt của các tính năng, theo từng dự án: `testing/<dự-án>/ten-tinh-nang.json`
    (`{"dang-nhap": "Đăng nhập", …}`). Tính năng chưa khai thì hiện đúng tên thư mục."""
    f = config.ROOT / "testing" / project / "ten-tinh-nang.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}


def suite_title(suite, project=None):
    if is_regression(suite):
        return f"Regression Tầng {suite.rsplit('-', 1)[1]}"
    return SUITE_NAMES.get(suite) or f"Test case {feature_names(project).get(suite, suite) if project else suite}"


def case_label(suite):
    return "Smoke case" if suite == "smoke" else "Regression case" if is_regression(suite) else "Test case"


def page_dir(cfg, suite):
    return cfg.project_dir if suite == "smoke" or is_regression(suite) else cfg.project_dir / suite


def page_files(cfg, suite):
    d = page_dir(cfg, suite)
    if is_regression(suite):
        return (d / f"{suite}-ket-qua.md", d / f"{suite}-ket-qua.html")
    return (d / "smoke-ket-qua.md", d / "smoke-ket-qua.html") if suite == "smoke" else (d / "ket-qua-test-case.md", d / "ket-qua-test-case.html")


# ---------- dữ liệu lượt ----------
def results_data_path(cfg, suite):
    return cfg.project_dir / "run-results" / f"{suite}.json"


def read_results_data(cfg, suite):
    f = results_data_path(cfg, suite)
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    return {"project": cfg.project, "suite": suite, "runs": []}


def _normalize_path(path):
    return str(path).replace("\\", "/")


def _find_bug_file(cfg, code):
    pairs = sorted(cfg.project_dir.glob(f"**/bug/{code}.md"))
    return str(pairs[0].relative_to(config.ROOT)).replace("\\", "/") if pairs else None


def add_run(cfg, suite, build, case_results, run_by=None, run_method="Tự động (Playwright)",
              note="", status_override=None, bug=None, sources=None, timestamp=None, add_error_images=None, error_captions=None, blocked_by=None, conclusion=None):
    """Thêm một lượt vào dữ liệu rồi sinh lại md + html.

    ket_qua_ca: danh sách dict {ca: 'dang-nhap/tc-005', ket_luan, ly_do, anh: [...]} (định dạng file result-*.json),
    theo thứ tự thời gian; ca chạy sau thay ca trước nếu ca trước chưa có kết luận.
    ghi_de_status: {"2": "Đạt kèm lỗi đã biết"}; bug: {"2": ["BUG-001"]}; them_anh_loi: {"2": ["evidence/.../anh-loi.png"]}; chu_thich_loi: {"2": "Lỗi ở bước 5: ..."} (gắn cho mọi ảnh tô đỏ của case đó chưa có chú thích).
    Mỗi case lưu thêm `thuc_te` (các ý kiểm tra đúng/sai đã thấy) và `evidence_loi` (ảnh tô đỏ chỗ lỗi).
    """
    table = read_table(cfg, suite)
    by_case = {}
    for b in table:  # một test case có thể đứng ở nhiều dòng smoke: ghi cho tất cả
        by_case.setdefault((b["feature"], b["tc"]), []).append(b["number"])
    results = {b["number"]: {"status": NOT_RUN, "evidence": [], "evidence_error": [], "evidence_error_captions": {}, "video": [], "bug": [], "blocked_by": [], "note": "", "actual": []} for b in table}
    for kq in case_results:
        feature, _, tc = kq["case_id"].partition("/")
        for number in by_case.get((feature, tc), []):
            old = results[number]["status"]
            if old in HAS_VERDICT and kq["verdict"] not in HAS_VERDICT:
                continue  # giữ kết quả đã có kết luận
            results[number] = {
                "status": kq["verdict"] if kq["verdict"] not in (NO_SCRIPT,) else NOT_RUN,
                "evidence": [_normalize_path(a) for a in kq.get("images", [])],
                "evidence_error": [_normalize_path(a) for a in kq.get("error_images", [])],
                "evidence_error_captions": {_normalize_path(k): t for k, t in kq.get("error_image_captions", {}).items()},
                "video": [_normalize_path(a) for a in kq.get("videos", [])],
                "bug": [], "blocked_by": [], "note": kq.get("reason", ""),
                "actual": [{"kind": k["kind"], "title": k["title"], "passed": k["passed"], "note": k.get("note", "")} for k in kq.get("checks", [])],
            }
    for number, st in (status_override or {}).items():
        results[number]["status"] = st
    for number, entries in (add_error_images or {}).items():
        results[number]["evidence_error"] += [_normalize_path(a) for a in entries]
    for number, text in (error_captions or {}).items():
        for a in results[number]["evidence_error"]:
            results[number]["evidence_error_captions"].setdefault(a, text)
    for number, entries in (bug or {}).items():
        for code in entries:
            results[number]["bug"].append({"code": code, "path": _find_bug_file(cfg, code)})

    for number, entries in (blocked_by or {}).items():
        for code in entries:
            results[number]["blocked_by"].append({"code": code, "path": _find_bug_file(cfg, code)})

    problems = validate_conclusion(suite, table, results, conclusion)
    if problems:
        raise ConclusionError("Không ghi lượt vì kết luận chưa đạt:" + NL_JOIN + NL_JOIN.join("- " + x for x in problems))
    statuses = [v["status"] for v in results.values()]
    if suite == "smoke":
        verdict = REJECT_BUILD if FAIL in statuses else ACCEPT_BUILD if all(s in HAS_VERDICT for s in statuses) else INCOMPLETE
    else:
        verdict = HAS_FAIL if FAIL in statuses else ALL_PASS if all(s in HAS_VERDICT for s in statuses) else NOT_ALL_RUN

    data = read_results_data(cfg, suite)
    run_record = {
        "number": len(data["runs"]) + 1, "build": build,
        "timestamp": timestamp or time.strftime("%Y-%m-%d %H:%M:%S"),
        "run_by": run_by or config.default_author(), "run_method": run_method, "verdict": verdict, "note": note,
        "sources": [_normalize_path(n) for n in (sources or [])], "results": results,
    }
    if conclusion:
        run_record["conclusion"] = conclusion
    data["runs"].append(run_record)
    f = results_data_path(cfg, suite)
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    build_pages(cfg, suite)
    return run_record



def _updated_text(run):
    """Dòng 'Cập nhật lần cuối' (nếu lượt đã được chỉnh sau lúc chạy; khóa `updated_at` và `updated_note` trong dữ liệu lượt)."""
    if not run.get("updated_at"):
        return None
    return run["updated_at"] + (f" ({run['updated_note']})" if run.get("updated_note") else "")


def _updated_md(run):
    text = _updated_text(run)
    return [f"| Cập nhật lần cuối | {text} |"] if text else []


def _updated_html(run, e):
    text = _updated_text(run)
    return [("Cập nhật lần cuối", e(text))] if text else []


NL_JOIN = chr(10)


class ConclusionError(ValueError):
    """Kết luận và rủi ro chưa đạt yêu cầu: không ghi lượt."""


# Cụm chung chung bị cấm trong kết luận (người kiểm thử cần số liệu cụ thể để đánh giá).
VAGUE_PATTERNS = [r"một số (lỗi|case|ca|bug|chỗ)", r"một vài", r"\bvài (lỗi|case|ca|bug|chỗ)", r"nhiều (lỗi|case|ca|bug|chỗ)", r"v\.v", r"\betc\b", r"và các (lỗi|ca|case) khác"]


def validate_conclusion(suite, table, results, conclusion):
    """Kiểm kết luận và rủi ro theo quy tắc đã chốt (xem skill chay-test-tu-dong, references/quy-tac-da-chot.md mục 5). Trả danh sách lỗi."""
    problems = []
    if not conclusion:
        # Bắt buộc với mọi bộ, kể cả smoke (2026-11-19: thiếu thì báo cáo tổng kết mất dòng của smoke).
        problems.append("thiếu kết luận và rủi ro (--conclusion-file): bắt buộc cho mọi lượt (smoke, regression, tính năng)")
        return problems
    for key, kind in (("headline", str), ("passed", list), ("not_tested", list), ("risks", list), ("suggestion", str)):
        if not isinstance(conclusion.get(key), kind):
            problems.append(f"thiếu hoặc sai kiểu khóa `{key}` ({kind.__name__})")
    if problems:
        return problems
    if len(conclusion["headline"].strip()) < 30:
        problems.append("`headline` quá ngắn: viết một câu đầy đủ nói được nhận hay trả và vì sao")
    if len(conclusion["suggestion"].strip()) < 20:
        problems.append("`suggestion` quá ngắn")
    texts = [("headline", conclusion["headline"]), ("suggestion", conclusion["suggestion"])]
    texts += [(f"passed[{i}]", str(x)) for i, x in enumerate(conclusion["passed"])]
    for i, item in enumerate(conclusion["not_tested"]):
        if not all(str(item.get(k, "")).strip() for k in ("cases", "status", "reason")):
            problems.append(f"not_tested[{i}] thiếu `cases`, `status` hoặc `reason`")
            continue
        if len(str(item["reason"]).strip()) < 20:
            problems.append(f"not_tested[{i}].reason quá ngắn: nói rõ vì sao chưa có kết quả")
        texts.append((f"not_tested[{i}].reason", str(item["reason"])))
    for i, risk in enumerate(conclusion["risks"]):
        if not str(risk.get("title", "")).strip() or len(str(risk.get("detail", "")).strip()) < 30:
            problems.append(f"risks[{i}] cần `title` và `detail` (nói chuyện gì xảy ra với người dùng, đã hay chưa kiểm)")
            continue
        texts += [(f"risks[{i}].title", str(risk["title"])), (f"risks[{i}].detail", str(risk["detail"]))]
    for where, text in texts:
        for pattern in VAGUE_PATTERNS:
            m = re.search(pattern, text, re.I)
            if m:
                problems.append(f"{where} có cụm chung chung `{m.group(0)}`: thay bằng số liệu cụ thể")
                break
    # mọi ca chưa có kết quả phải được nêu đúng trạng thái trong not_tested
    listed = {}
    for item in conclusion["not_tested"]:
        for code in re.findall(r"[A-Za-z]+-\d+", str(item.get("cases", ""))):
            listed[code.upper()] = str(item.get("status", "")).strip()
    for b in table:
        status = results[b["number"]]["status"]
        if status in HAS_VERDICT:
            continue
        code = str(b.get("id", "")).upper()
        if code and code not in listed:
            problems.append(f"{code} đang `{status}` nhưng không được nêu trong `not_tested` (liệt kê từng mã, không viết khoảng)")
        elif code and listed[code] != status:
            problems.append(f"{code} đang `{status}` nhưng `not_tested` ghi `{listed[code]}`")
    return problems


def read_test_case(cfg, feature, tc):
    """{'buoc': ..., 'mong_doi': ...} lấy từ dòng test case gốc (đọc theo TÊN cột, nên file 12 hay 13 cột đều được)."""
    f = cfg.project_dir / feature / "test-case.md"
    if not f.exists():
        return {"steps": "", "expected": ""}
    column_names = None
    for line in f.read_text(encoding="utf-8").splitlines():
        if column_names is None and line.startswith("| Mã |"):
            column_names = [c.strip() for c in _CELL_SPLIT.split(line)[1:-1]]
        elif column_names and f'id="{tc}"' in line:
            o = [c.strip() for c in _CELL_SPLIT.split(line)[1:-1]]
            d = dict(zip(column_names, o))
            return {"steps": d.get("Các bước", ""), "expected": d.get("Kết quả mong đợi", "")}
    return {"steps": "", "expected": ""}


_BR = re.compile(r"<br\s*/?>")


def _cell_lines(o):
    """Ô trong bảng md (các dòng ngăn bằng <br>) → danh sách dòng chữ thường (bỏ dấu huyền)."""
    return [x.replace("`", "").strip() for x in _BR.split(o or "") if x.strip()]


def _cell_html(o):
    """Ô md → HTML: mỗi dòng một đoạn, chữ trong dấu huyền thành <code>."""
    out = []
    for line in _BR.split(o or ""):
        line = line.strip()
        if line:
            out.append("<div>" + re.sub(r"`([^`]+)`", lambda m: f"<code>{m.group(1)}</code>", html.escape(line, quote=False).replace("`", "`")) + "</div>")
    return "".join(out) or "—"


def _actual_lines(v):
    """Kết quả thực tế của một case → [(dung, chữ)] từ các ý kiểm tra đã chạy; không có thì dùng ghi chú của lượt."""
    out = []
    for k in v.get("actual", []):
        plain = k["title"].replace("`", "") + (" (ý phụ)" if k["kind"] == "minor" else "")
        if k.get("note"):
            plain += " — " + k["note"].replace("`", "")
        out.append((k["passed"], plain))
    if not out and v.get("note"):
        out.append((None, v["note"]))
    return out


# ---------- tính toán ----------
def run_count(data, number):
    return sum(1 for l in data["runs"] if l["results"].get(number, {}).get("status") in HAS_VERDICT)


def _count_statuses(run_record):
    counts = {}
    for v in run_record["results"].values():
        counts[v["status"]] = counts.get(v["status"], 0) + 1
    return ", ".join(f"{n} {s}" for s, n in counts.items())


def _link(cfg, suite, path_from_root):
    """Đường dẫn tương đối từ thư mục chứa trang kết quả tới file tính từ gốc repo."""
    import os

    return os.path.relpath(config.ROOT / path_from_root, page_dir(cfg, suite)).replace("\\", "/")


def _bug_href(cfg, suite, x, ext):
    return _link(cfg, suite, x["path"]).removesuffix(".md") + ext


def _bug_cell_md(cfg, suite, v):
    lines = [f"[{x['code']}]({_bug_href(cfg, suite, x, '.md')})" if x["path"] else x["code"] for x in v["bug"]]
    lines += ["Bị chặn bởi " + (f"[{x['code']}]({_bug_href(cfg, suite, x, '.md')})" if x["path"] else x["code"]) for x in v.get("blocked_by", [])]
    return "<br>".join(lines) or "—"


def _bug_cell_html(cfg, suite, v):
    e = html.escape

    def one(x):
        return f'<a href="{e(_bug_href(cfg, suite, x, ".html"))}">{e(x["code"])}</a>' if x["path"] else e(x["code"])

    parts = []
    if v["bug"]:
        parts.append(", ".join(one(x) for x in v["bug"]))
    if v.get("blocked_by"):
        parts.append('<div class="small">Bị chặn bởi ' + ", ".join(one(x) for x in v["blocked_by"]) + "</div>")
    return "".join(parts) or "—"


# ---------- Markdown ----------
def build_md(cfg, suite, data, table):
    title = suite_title(suite, cfg.project)
    d = ["# Kết quả chạy " + title.lower() + f" — {cfg.project}", "",
         "> File tự sinh từ `testing/%s/run-results/%s.json` bằng `scripts/build_report.py` — đừng sửa tay, chạy lại là ghi đè. Bản dễ xem: `%s`." % (cfg.project, suite, page_files(cfg, suite)[1].name), ""]
    if not data["runs"]:
        d += ["Chưa có lượt chạy nào.", ""]
        return "\n".join(d)
    new_text = data["runs"][-1]
    d += ["| | |", "|---|---|",
          f"| Build | **{new_text['build']}** |", f"| Lượt | {new_text['number']} / {len(data['runs'])} (lượt mới nhất) |",
          f"| Thời điểm | {new_text['timestamp']} |", *_updated_md(new_text), f"| Người chạy | {new_text['run_by']} |",
          f"| Cách chạy | {new_text['run_method']} |", f"| Kết luận | **{new_text['verdict']}** |",
          f"| Ghi chú | {new_text['note'] or '—'} |", ""]
    d += _conclusion_md(new_text)
    d += ["## Kết quả lượt mới nhất", "",
          f"| ID | {case_label(suite)} | Các bước | Kết quả mong đợi | Status | Evidence | Bug | Số lần chạy |", "|---|---|---|---|---|---|---|---|"]
    for b in table:
        v = new_text["results"][b["number"]]
        test_case = read_test_case(cfg, b["feature"], b["tc"])
        ev = [f"[{Path(a).name}]({_link(cfg, suite, a)})" for a in v["evidence"]]
        ev += [f"🔴 [{Path(a).name}]({_link(cfg, suite, a)}) (tô đỏ chỗ lỗi)" + (f": {v.get('evidence_error_captions', {}).get(a)}" if v.get("evidence_error_captions", {}).get(a) else "")
               for a in v.get("evidence_error", [])]
        ev += [f"🎬 [{Path(a).name}]({_link(cfg, suite, a)}) (video quay lại ca)" for a in v.get("video", [])]
        bug_cell = _bug_cell_md(cfg, suite, v)
        steps = "<br>".join(_cell_lines(test_case["steps"])) or "—"
        expected = "<br>".join(_cell_lines(test_case["expected"])) or "—"
        case_title = f"{b['title']} ({b['source_ref']})"
        d.append(f"| {b['id']} | {case_title} | {steps} | {expected} | {v['status']} | {'<br>'.join(ev) or '—'} | {bug_cell} | {run_count(data, b['number'])} |")
    d += ["", "## Lịch sử các lượt", "",
          "| Lượt | Build | Thời điểm | Người chạy | Kết quả | Kết luận |", "|---|---|---|---|---|---|"]
    for l in reversed(data["runs"]):
        d.append(f"| {l['number']} | {l['build']} | {l['timestamp']} | {l['run_by']} | {_count_statuses(l)} | {l['verdict']} |")
    entries = data["runs"][-MATRIX_RUNS:]
    d += ["", f"## Từng case qua các lượt (tối đa {MATRIX_RUNS} lượt gần nhất)", "",
          "| ID | " + " | ".join(f"Lượt {l['number']} ({l['build']})" for l in entries) + " |",
          "|---|" + "---|" * len(entries)]
    for b in table:
        d.append(f"| {b['id']} | " + " | ".join(l["results"].get(b["number"], {}).get("status", NOT_RUN) for l in entries) + " |")
    d += ["", "Các bước và Kết quả mong đợi lấy từ test case gốc. Bị chặn: chưa test được vì bug khác (xem cột Bug). Số lần chạy: số lượt có kết luận Đạt, Đạt kèm lỗi đã biết, Đạt kèm ý phụ sai hoặc Không đạt; lượt Không kết luận và Chưa chạy không tính.", ""]
    return "\n".join(d)


# ---------- HTML ----------






def _badge(status):
    cls = {PASS: "ok", PASS_KNOWN_ISSUE: "warn", PASS_MINOR_FAIL: "warn", FAIL: "bad", BLOCKED: "warn"}.get(status, "gray")
    return f'<span class="badge {cls}">{html.escape(status)}</span>'


def _verdict_badge(verdict):
    cls = "ok" if verdict in (ACCEPT_BUILD, ALL_PASS) else "bad" if verdict in (REJECT_BUILD, HAS_FAIL) else "gray"
    return f'<span class="badge {cls}">{html.escape(verdict)}</span>'


def _bug_severity(cfg, code):
    path = _find_bug_file(cfg, code)
    if not path:
        return ""
    text = (config.ROOT / path).read_text(encoding="utf-8")
    m = re.search(r"## Mức độ nghiêm trọng\s*\n+\*\*([^*]+?)\.?\*\*", text)
    return m.group(1).strip() if m else ""


def _conclusion_counts(run_record):
    c = {}
    for v in run_record["results"].values():
        c[v["status"]] = c.get(v["status"], 0) + 1
    total = len(run_record["results"])
    ran = sum(n for st, n in c.items() if st in HAS_VERDICT)
    return total, ran, c


def _conclusion_html(run_record):
    """Thẻ 'Kết luận và rủi ro': số liệu tự tính + phần người soát viết (headline, đã kiểm, chưa kiểm được, rủi ro, đề xuất)."""
    k = run_record.get("conclusion")
    if not k:
        return ""
    e = html.escape
    total, ran, counts = _conclusion_counts(run_record)
    parts = ['<h2>Kết luận và rủi ro</h2><div class="card kl">',
             f'<p class="kl-dau">{e(k.get("headline", ""))}</p>',
             f'<p class="small">Số liệu lượt này: {ran} trên {total} case đã có kết quả ({round(100 * ran / total)}%): '
             + e(", ".join(f"{n} {st}" for st, n in counts.items())) + ".</p>"]
    if k.get("passed"):
        parts.append("<h3>Đã kiểm và đạt</h3><ul>" + "".join(f"<li>{e(x)}</li>" for x in k["passed"]) + "</ul>")
    if k.get("not_tested"):
        parts.append('<h3>Chưa có kết quả và vì sao</h3><table class="kl-bang"><thead><tr><th>Case</th><th>Trạng thái</th><th>Lý do</th></tr></thead><tbody>'
                     + "".join(f"<tr><td class='nw'>{e(x['cases'])}</td><td>{_badge(x['status'])}</td><td>{e(x['reason'])}</td></tr>" for x in k["not_tested"]) + "</tbody></table>")
    if k.get("risks"):
        parts.append("<h3>Rủi ro để người kiểm thử đánh giá</h3><ul>" + "".join(f"<li><strong>{e(x['title'])}.</strong> {e(x['detail'])}</li>" for x in k["risks"]) + "</ul>")
    if k.get("suggestion"):
        parts.append(f'<h3>Đề xuất (người kiểm thử hoặc PO quyết định)</h3><p>{e(k["suggestion"])}</p>')
    parts.append("</div>")
    return "".join(parts)


def _conclusion_md(run_record):
    k = run_record.get("conclusion")
    if not k:
        return []
    total, ran, counts = _conclusion_counts(run_record)
    d = ["## Kết luận và rủi ro", "", k.get("headline", ""), "",
         f"Số liệu lượt này: {ran} trên {total} case đã có kết quả ({round(100 * ran / total)}%): " + ", ".join(f"{n} {st}" for st, n in counts.items()) + ".", ""]
    if k.get("passed"):
        d += ["**Đã kiểm và đạt**", ""] + [f"- {x}" for x in k["passed"]] + [""]
    if k.get("not_tested"):
        d += ["**Chưa có kết quả và vì sao**", "", "| Case | Trạng thái | Lý do |", "|---|---|---|"] + [f"| {x['cases']} | {x['status']} | {x['reason']} |" for x in k["not_tested"]] + [""]
    if k.get("risks"):
        d += ["**Rủi ro để người kiểm thử đánh giá**", ""] + [f"- **{x['title']}.** {x['detail']}" for x in k["risks"]] + [""]
    if k.get("suggestion"):
        d += ["**Đề xuất (người kiểm thử hoặc PO quyết định)**", "", k["suggestion"], ""]
    return d


def _bug_title(cfg, code):
    path = _find_bug_file(cfg, code)
    if not path:
        return ""
    first = (config.ROOT / path).read_text(encoding="utf-8").splitlines()[0]
    return first.lstrip("# ").replace("`", "").strip()


def _bug_summary_html(cfg, suite, run_record, table):
    """Bảng 'Bug đã mở': mỗi bug, tiêu đề, case thấy lỗi, case bị chặn vì bug đó."""
    e = html.escape
    ids = {b["number"]: b["id"] for b in table}
    found, blocked = {}, {}
    for number, v in run_record["results"].items():
        for x in v["bug"]:
            found.setdefault(x["code"], []).append(ids[number])
        for x in v.get("blocked_by", []):
            blocked.setdefault(x["code"], []).append(ids[number])
    codes = sorted(set(found) | set(blocked))
    if not codes:
        return ""
    rows = []
    for code in codes:
        path = _find_bug_file(cfg, code)
        link = f'<a href="{e(_link(cfg, suite, path).removesuffix(".md") + ".html")}">{e(code)}</a>' if path else e(code)
        rows.append(f"<tr><td class='nw'>{link}</td><td>{e(_bug_title(cfg, code))}</td><td>{e(_bug_severity(cfg, code) or '—')}</td><td>{e(', '.join(found.get(code, [])) or '—')}</td><td>{e(', '.join(blocked.get(code, [])) or '—')}</td></tr>")
    return ('<h2>Bug đã mở</h2><div class="wrap"><table><thead><tr><th>Bug</th><th>Tiêu đề</th><th>Mức độ nghiêm trọng</th><th>Case thấy lỗi</th><th>Case bị chặn vì bug này</th></tr></thead><tbody>'
            + "".join(rows) + "</tbody></table></div>")


def build_html(cfg, suite, data, table):
    e = html.escape
    title = suite_title(suite, cfg.project)
    p = [f'<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
         f"<title>Kết quả {e(title)} {e(cfg.project)}</title>"
         + theme_mod.font_head(page_dir(cfg, suite)) +
         f"<style>{_CSS}</style><script>{_JS_THEME}{_JS_DRAG_SCROLL}</script></head><body><button id=\"theme\" class=\"theme\" type=\"button\">Chế độ tối</button><main class=\"rong\">",
         theme_mod.brand_html(cfg.project),
         f'<p class="eyebrow">Kết quả chạy {e(title.lower())}</p>',
         f"<h1>Lượt chạy của <em>{e(cfg.project)}</em></h1>",
         '<p class="sub">Trang tự sinh từ file dữ liệu bằng <code>scripts/build_report.py</code>; không sửa tay.</p>']
    if not data["runs"]:
        p.append("<p>Chưa có lượt chạy nào.</p></main></body></html>")
        return "".join(p)
    new_text = data["runs"][-1]
    p.append('<div class="card"><dl class="meta">')
    for k, v in (("Build", f"<strong>{e(new_text['build'])}</strong>"), ("Lượt", f"{new_text['number']} / {len(data['runs'])} (mới nhất)"),
                 ("Thời điểm", e(new_text["timestamp"])), *_updated_html(new_text, e), ("Người chạy", e(new_text["run_by"])), ("Cách chạy", e(new_text["run_method"])),
                 ("Kết quả", e(_count_statuses(new_text))), ("Kết luận", _verdict_badge(new_text["verdict"])),
                 ("Ghi chú", e(new_text["note"]) or "—")):
        p.append(f"<dt>{k}</dt><dd>{v}</dd>")
    p.append("</dl></div>")
    p.append(_conclusion_html(new_text))
    p.append(f'<h2>Kết quả lượt mới nhất</h2><p class="goi-y">Trang rộng gần hết màn hình, bảng tự co theo bề rộng. Nếu màn hình hẹp vẫn phải kéo ngang: dùng thanh cuộn luôn hiện ở cuối màn hình, hoặc giữ chuột trái kéo trên bảng, hoặc giữ Shift và lăn chuột. Hai cột ID và {case_label(suite)} được giữ cố định bên trái.</p><div class="khu-bang"><div class="wrap lon"><table><thead><tr><th>ID</th><th>{case_label(suite)}</th><th>Các bước</th><th>Kết quả mong đợi</th>'
             '<th>Status</th><th>Evidence</th><th>Bug</th><th class="num">Số lần chạy</th></tr></thead><tbody>')
    for b in table:
        v = new_text["results"][b["number"]]
        test_case = read_test_case(cfg, b["feature"], b["tc"])
        ev = "".join(
            (f'<li class="loi"><span class="badge ok">Ảnh kiểm tra</span><div class="cap-ok">Khung xanh: đã kiểm và đạt. Khung đỏ: sai.</div>'
             f'<a href="{e(_link(cfg, suite, a))}" target="_blank" rel="noopener"><img class="thumb kiem" src="{e(_link(cfg, suite, a))}" alt="{e(Path(a).name)}"></a></li>')
            if "-kiem" in Path(a).name else
            f'<li><a href="{e(_link(cfg, suite, a))}" target="_blank" rel="noopener">{e(Path(a).name)}</a></li>' for a in v["evidence"])
        ev += "".join(
            f'<li class="loi"><span class="badge bad">Ảnh tô đỏ chỗ lỗi</span>'
            + (f'<div class="cap-loi">{e(v.get("evidence_error_captions", {}).get(a, ""))}</div>' if v.get("evidence_error_captions", {}).get(a) else "")
            + f'<a href="{e(_link(cfg, suite, a))}" target="_blank" rel="noopener">'
            f'<img class="thumb" src="{e(_link(cfg, suite, a))}" alt="{e(Path(a).name)}"></a></li>' for a in v.get("evidence_error", []))
        ev += "".join(f'<li class="loi"><span class="badge warn">Video quay lại ca</span><video class="vid" controls preload="none" src="{e(_link(cfg, suite, a))}"></video>'
                      f'<a href="{e(_link(cfg, suite, a))}" target="_blank" rel="noopener">{e(Path(a).name)}</a></li>' for a in v.get("video", []))
        ev = f'<ul class="ev">{ev}</ul>' if ev else "—"
        bug_cell = _bug_cell_html(cfg, suite, v)
        p.append(f'<tr><td class="nw">{e(b["id"])}</td><td>{e(b["title"].replace(chr(96), ""))}<div class="small">{e(b["source_ref"])}</div></td>'
                 f'<td class="cot-nho">{_cell_html(test_case["steps"])}</td><td class="cot-nho">{_cell_html(test_case["expected"])}</td>'
                 f'<td>{_badge(v["status"])}</td><td>{ev}</td><td>{bug_cell}</td><td class="num">{run_count(data, b["number"])}</td></tr>')
    p.append("</tbody></table></div><div class=\"thanh-keo\"><div></div></div></div>")
    if suite != "smoke":
        p.append(_bug_summary_html(cfg, suite, new_text, table))
    p.append('<h2>Lịch sử các lượt</h2><div class="wrap"><table><thead><tr><th>Lượt</th><th>Build</th><th>Thời điểm</th><th>Người chạy</th><th>Kết quả</th><th>Kết luận</th></tr></thead><tbody>')
    for l in reversed(data["runs"]):
        p.append(f"<tr><td>{l['number']}</td><td>{e(l['build'])}</td><td>{e(l['timestamp'])}</td><td>{e(l['run_by'])}</td>"
                 f"<td>{e(_count_statuses(l))}</td><td>{_verdict_badge(l['verdict'])}</td></tr>")
    p.append("</tbody></table></div>")
    entries = data["runs"][-MATRIX_RUNS:]
    p.append(f"<h2>Từng case qua các lượt <span class='small'>(tối đa {MATRIX_RUNS} lượt gần nhất)</span></h2><div class='wrap'><table><thead><tr><th>ID</th>"
             + "".join(f"<th>Lượt {l['number']}<div class='small'>{e(l['build'])}</div></th>" for l in entries) + "</tr></thead><tbody>")
    for b in table:
        p.append(f"<tr><td class='nw'>{e(b['id'])}</td>" + "".join(f"<td>{_badge(l['results'].get(b['number'], {}).get('status', NOT_RUN))}</td>" for l in entries) + "</tr>")
    p.append("</tbody></table></div>")
    p.append('<p class="note">Các bước và Kết quả mong đợi lấy từ test case gốc. Bị chặn: chưa test được vì bug khác (xem cột Bug). Số lần chạy: số lượt có kết luận Đạt, Đạt kèm lỗi đã biết, Đạt kèm ý phụ sai hoặc Không đạt. '
             "Lượt Không kết luận (script lỗi, phiên hết hạn, thiếu dữ liệu) và Chưa chạy không tính.</p></main></body></html>")
    return "".join(p)


def render_pages(cfg, suite="smoke"):
    """Sinh (chưa ghi) trang md + html kết quả của một bộ: {đường dẫn: nội dung}."""
    data = read_results_data(cfg, suite)
    table = read_table(cfg, suite)
    md_file, html_file = page_files(cfg, suite)
    return {md_file: build_md(cfg, suite, data, table), html_file: build_html(cfg, suite, data, table)}


def build_pages(cfg, suite="smoke"):
    pages = render_pages(cfg, suite)
    for path, text in pages.items():
        path.write_text(text, encoding="utf-8")
    from . import bug_page

    bug_page.build_all(cfg)  # mỗi BUG-nnn.md có trang BUG-nnn.html cạnh nó
    return page_files(cfg, suite)
