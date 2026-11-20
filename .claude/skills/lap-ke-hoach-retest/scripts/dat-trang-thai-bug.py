#!/usr/bin/env python3
"""Ghi (hoặc sửa) mục `## Trạng thái` trong file bug theo điều người dùng chốt; báo cáo tổng kết đọc mục này.

Mặc định chỉ in bản xem trước; thêm --ghi mới sửa file. Không tự suy ra trạng thái: người dùng nói Đóng / Mở lại thì mới ghi.
Công cụ của team vẫn là bản chính thức; mục này là bản ghi lại trong kho để báo cáo tổng kết và tong-hop-retest.py đọc.

Ví dụ (từ gốc repo):
    python -X utf8 .claude/skills/lap-ke-hoach-retest/scripts/dat-trang-thai-bug.py testing/<slug>/<tính-năng>/bug/BUG-001.md --trang-thai "Mở lại" --build 1.3.1
    ... --trang-thai Đóng --build 1.3.2 --ghi-chu "đã re-test đủ 3 tài khoản" --ghi

Trạng thái hợp lệ: Mở, Chờ re-test, Mở lại, Đóng.
Mục được đặt ngay trước `## Lịch sử re-test` nếu có, không thì cuối file; đã có mục `## Trạng thái` thì thay tại chỗ.
Sau khi ghi: chạy `python -X utf8 scripts/build_docs.py --all` (sinh lại trang bug và test summary).
"""
import argparse
import datetime
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

STATUSES = ("Mở", "Chờ re-test", "Mở lại", "Đóng")


def build_section(status, day, build, note):
    detail = f"Ngày {day}" + (f", build {build}" if build else ", chưa có số build") + (f". {note.strip().rstrip('.')}" if note else "") + "."
    return f"## Trạng thái\n**{status}.** {detail}\n"


def apply(text, section):
    """Thay mục `## Trạng thái` có sẵn, hoặc chèn trước `## Lịch sử re-test`, hoặc thêm cuối file."""
    lines = text.rstrip("\n").split("\n")
    start = next((i for i, l in enumerate(lines) if l.strip() == "## Trạng thái"), None)
    new = section.rstrip("\n").split("\n")
    if start is not None:
        end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
        tail = lines[end:]
        return "\n".join(lines[:start] + new + ([""] + tail if tail else [])) + "\n"
    at = next((i for i, l in enumerate(lines) if l.strip() == "## Lịch sử re-test"), None)
    if at is not None:
        return "\n".join(lines[:at] + new + [""] + lines[at:]) + "\n"
    return "\n".join(lines + [""] + new) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Ghi trạng thái bug do người dùng chốt")
    ap.add_argument("bug", help="file BUG-nnn.md")
    ap.add_argument("--trang-thai", required=True, choices=STATUSES)
    ap.add_argument("--build", help="số build lúc chốt (bỏ trống nếu chưa có)")
    ap.add_argument("--ngay", default=datetime.date.today().isoformat(), help="YYYY-MM-DD (mặc định hôm nay)")
    ap.add_argument("--ghi-chu", help="một câu ngắn, ví dụ lý do mở lại")
    ap.add_argument("--ghi", action="store_true", help="ghi vào file (không có thì chỉ xem trước)")
    args = ap.parse_args()

    path = Path(args.bug)
    if not path.exists() or not re.fullmatch(r"BUG-\d+\.md", path.name):
        print(f"Cần đường dẫn file bug dạng BUG-nnn.md, không tìm thấy: {path}")
        return 1
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.ngay):
        print("--ngay phải dạng YYYY-MM-DD")
        return 1
    old = path.read_text(encoding="utf-8")
    section = build_section(args.trang_thai, args.ngay, args.build, args.ghi_chu)
    new = apply(old, section)
    print(f"{path.name}: mục sẽ ghi:\n\n{section}")
    if new == old:
        print("(Không đổi gì: mục đã đúng như vậy.)")
        return 0
    if not args.ghi:
        print("Chỉ xem trước. Đúng rồi thì chạy lại thêm --ghi, rồi build_docs.py --all.")
        return 0
    path.write_text(new, encoding="utf-8")
    print(f"Đã ghi vào {path}. Chạy tiếp: python -X utf8 scripts/build_docs.py --all")
    return 0


if __name__ == "__main__":
    sys.exit(main())
