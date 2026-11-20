#!/usr/bin/env python3
"""Sinh MỌI trang HTML của dự án từ file md và dữ liệu có sẵn, rồi (nếu --check) báo trang nào đang cũ.

Gồm: tài liệu md (SRS, bảng soát, câu hỏi BA, checklist, test case, truy vết, nhật ký khám phá, hướng dẫn), bảng kết quả smoke và
kết quả test case, trang bug, và trang tổng `testing/<dự-án>/index.html`. Không dùng AI: chỉ là chương trình đổi định dạng và đọc số liệu.

    python -X utf8 scripts/build_docs.py                  # dự án trong .du-an-hien-tai
    python -X utf8 scripts/build_docs.py --all            # mọi dự án
    python -X utf8 scripts/build_docs.py --check          # không ghi, so nội dung: thoát mã 1 nếu có trang cũ hoặc chưa có
    python -X utf8 scripts/build_docs.py --all --stage    # sinh rồi `git add` các trang đã đổi (dùng trong pre-commit)

File md và dữ liệu (run-results/*.json, bug/*.md) là bản gốc: sửa rồi chạy lại, đừng sửa HTML. Giao diện: scripts/test_automation/theme.py.
"""
import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_automation import config, docs_pages  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="Sinh trang HTML cho tài liệu, kết quả chạy, bug và trang tổng")
    ap.add_argument("--project")
    ap.add_argument("--all", action="store_true", help="mọi dự án trong testing/")
    ap.add_argument("--check", action="store_true", help="chỉ so sánh với file đang có, không ghi (thoát mã 1 nếu có trang cũ)")
    ap.add_argument("--stage", action="store_true", help="sau khi sinh, git add các trang đã đổi")
    args = ap.parse_args()
    try:
        names = docs_pages.projects() if args.all else [args.project or config.current_project()]
        if args.all and not names:   # chưa có dự án nào (bộ lõi mới xuất): vẫn sinh trang dùng chung docs/, srs/, testing/
            names = [None]
        total_changed, total_skipped = [], []
        for project in names:
            changed, skipped = docs_pages.sync(project, write=not args.check)
            total_changed += changed
            total_skipped += skipped
    except config.ConfigError as error:
        print(error)
        return 2
    rel = lambda p: p.relative_to(config.ROOT)  # noqa: E731
    for s in total_skipped:
        print(f"  (bỏ qua, có file HTML làm tay trùng tên: {rel(s)})")
    unlinked = [x for project in names for x in docs_pages.UNLINKED.get(project, [])]
    for f in unlinked[:15]:
        print(f"  LỖI: trang tổng index.html chưa có link tới {rel(f)} (người dùng chỉ mở trang tổng là phải tới được mọi trang)")
    if args.check:
        if unlinked:
            return 1
        if total_changed:
            print(f"{len(total_changed)} trang HTML đang cũ hoặc chưa có. Chạy: python -X utf8 scripts/build_docs.py" + (" --all" if args.all else ""))
            for f in total_changed[:10]:
                print("  -", rel(f))
            return 1
        print("Mọi trang HTML (tài liệu, kết quả, bug, trang tổng) đều khớp với file nguồn, và đều có link từ trang tổng.")
        return 0
    print(f"Đã cập nhật {len(total_changed)} trang HTML/md sinh tự động ({len([n for n in names if n])} dự án).")
    if args.stage and total_changed:
        subprocess.run(["git", "add", "--"] + [str(rel(f)) for f in total_changed], cwd=config.ROOT, check=False)
        print("Đã git add các trang vừa cập nhật.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
