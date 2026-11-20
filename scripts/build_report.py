#!/usr/bin/env python3
"""Ghi lượt chạy và sinh bảng kết quả (md + HTML) cho bộ smoke (sau này regression).

    # ghi lượt từ các file kết quả của run_tests.py (theo thứ tự thời gian), rồi sinh md + html
    python -X utf8 scripts/build_report.py add-run --build 1.3.0 \\
        --results-files evidence/<dự-án>/chay-test/result-A.json evidence/<dự-án>/chay-test/result-B.json \\
        --status "2=Đạt kèm lỗi đã biết" --bug "2=BUG-001" --note "..."

    # chỉ sinh lại md + html từ dữ liệu đã có (cũng dựng lại trang HTML của mọi file bug)
    python -X utf8 scripts/build_report.py build

    # sinh báo cáo tổng kết (testing/<dự-án>/test-summary-report.md và .html); --build chọn build, mặc định build của lượt mới nhất
    python -X utf8 scripts/build_report.py summary

    # chỉ dựng trang HTML cho các file bug (testing/<dự-án>/**/bug/BUG-*.md → BUG-*.html cạnh nó)
    python -X utf8 scripts/build_report.py bug-pages

Dùng --project <slug> (mặc định .du-an-hien-tai) và --suite smoke (mặc định).
Số trong --status/--bug/--blocked-by là số thứ tự ở cột # của bảng trong smoke-test.md (với --suite <tính-năng>: số của mã test case, TC-014 là 14).
Chạy cả bộ và tự ghi lượt: `python -X utf8 scripts/run_tests.py --smoke --record-run --build 1.3.0`.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_automation import report, config  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def _parse_pairs(s):
    """'2=Đạt,3=Đạt' hoặc '2=BUG-001' → dict (gộp nhiều giá trị cùng số bằng dấu +)."""
    import re

    pairs = {}
    # chỉ tách ở dấu phẩy đứng trước "số=", nên câu chú thích có dấu phẩy vẫn giữ nguyên
    for part in [p.strip() for p in re.split(r",(?=\s*\d+=)", s or "") if p.strip()]:
        number, _, value = part.partition("=")
        pairs[number.strip()] = value.strip()
    return pairs


def main():
    ap = argparse.ArgumentParser(description="Ghi lượt chạy và sinh bảng kết quả md + HTML")
    ap.add_argument("command", choices=["add-run", "build", "bug-pages", "summary"])
    ap.add_argument("--project")
    ap.add_argument("--suite", default="smoke", help="smoke (mặc định) hoặc slug tính năng, ví dụ dang-nhap: trang kết quả cho cả bộ test case của tính năng")
    ap.add_argument("--build")
    ap.add_argument("--results-files", nargs="+", help="các file result-*.json của run_tests.py, theo thứ tự thời gian")
    ap.add_argument("--run-by", default=None, help="người chạy; mặc định lấy từ .nguoi-test")
    ap.add_argument("--run-method", default="Tự động (Playwright)")
    ap.add_argument("--author", help="summary: người viết báo cáo tổng kết (mặc định: người chạy lượt mới nhất)")
    ap.add_argument("--note", default="")
    ap.add_argument("--status", help='ghi đè status theo số, ví dụ "2=Đạt kèm lỗi đã biết"')
    ap.add_argument("--error-images", help='ảnh đã tô đỏ chỗ lỗi theo số, ví dụ "2=evidence/.../anh-loi.png" (nhiều ảnh: nối bằng +)')
    ap.add_argument("--error-captions", help='câu mô tả lỗi ở bước nào dưới ảnh tô đỏ, theo số, ví dụ "2=Lỗi ở bước 5: ..."')
    ap.add_argument("--blocked-by", help='case chưa test được vì bug khác, theo số, ví dụ "14=BUG-007" (dùng cùng --status "14=Bị chặn")')
    ap.add_argument("--conclusion-file", help="file JSON kết luận và rủi ro (headline, passed, not_tested, risks, suggestion) để hiện ở trang kết quả")
    ap.add_argument("--bug", help='mã bug theo số, ví dụ "2=BUG-001" (nhiều mã cùng số: "2=BUG-001+BUG-002")')
    args = ap.parse_args()

    try:
        # bug-pages và summary chỉ sinh trang, không cần phần đăng nhập của auto-config.json
        cfg = config.load_for_docs(args.project) if args.command in ("bug-pages", "summary") else config.load(args.project)
        if args.command == "bug-pages":
            from test_automation import bug_page

            entries = bug_page.build_all(cfg)
            print("Đã sinh: " + (", ".join(str(x.relative_to(config.ROOT)) for x in entries) or "(không có file bug)"))
            return 0
        if args.command == "summary":
            from test_automation import summary_report

            rr = cfg.project_dir / "run-results"
            if not (rr.exists() and any(rr.glob("*.json"))):
                print(f"Chưa có lượt chạy nào ở testing/{cfg.project}/run-results/: chưa làm được báo cáo tổng kết. "
                      "Chạy test và ghi lượt trước (skill chay-test-tu-dong); không có số liệu thì không lập báo cáo.")
                return 2
            written = summary_report.build_pages(cfg, args.build, args.author)
            print("Đã sinh: " + (", ".join(str(x.relative_to(config.ROOT)) for x in written) or "(chưa có lượt chạy nào để tổng hợp)"))
            return 0
        if args.command == "build":
            md_file, html_file = report.build_pages(cfg, args.suite)
        else:
            if not args.build or not args.results_files:
                print("add-run cần --build và --results-files")
                return 2
            case_results, sources, timestamp = [], [], None
            for f in args.results_files:
                p = Path(f)
                data = json.loads(p.read_text(encoding="utf-8"))
                case_results += data["results"]
                sources.append(str(p.resolve().relative_to(config.ROOT)))
                timestamp = max(timestamp or "", data["timestamp"])
            bug = {number: v.split("+") for number, v in _parse_pairs(args.bug).items()}
            error_images = {number: v.split("+") for number, v in _parse_pairs(args.error_images).items()}
            error_captions = _parse_pairs(args.error_captions)
            blocked_by = {number: v.split("+") for number, v in _parse_pairs(args.blocked_by).items()}
            run_record = report.add_run(cfg, args.suite, args.build, case_results, run_by=args.run_by or config.default_author(), run_method=args.run_method,
                                          note=args.note, status_override=_parse_pairs(args.status), bug=bug, sources=sources, add_error_images=error_images, error_captions=error_captions,
                                          timestamp=timestamp, blocked_by=blocked_by,
                                          conclusion=json.loads(Path(args.conclusion_file).read_text(encoding='utf-8')) if args.conclusion_file else None)
            print(f"Đã ghi lượt {run_record['number']} (build {run_record['build']}): {run_record['verdict']}")
            md_file, html_file = report.page_files(cfg, args.suite)
    except (config.ConfigError, report.ConclusionError) as error:
        print(error)
        return 2
    print(f"Đã sinh: {md_file.relative_to(config.ROOT)} và {html_file.relative_to(config.ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
