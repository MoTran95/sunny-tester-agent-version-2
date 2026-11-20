#!/usr/bin/env python3
"""Khi một bug được chốt ĐÓNG: liệt kê mọi chỗ trong tài liệu của dự án còn nhắc mã bug đó, để cập nhật cho khỏi sót.

Quét file `.md` ở `testing/<dự-án>/` và `memories/modules/<dự-án>/` (dự án lấy từ đường dẫn file bug), bỏ file bug và kế hoạch re-test
của chính nó. Chỉ đọc, không sửa. Dòng có chữ gợi ý cần đổi được đánh dấu:
  - "lỗi đã biết" / "Đạt kèm": ca đang được miễn vì bug này, đổi lại thành Đạt (smoke, regression, test case);
  - "Bị chặn": ca chưa test được vì bug này, cần CHẠY LẠI;
  - "Không đạt": trạng thái test case/ lượt chạy còn ghi lỗi do bug này.
Việc đổi trạng thái do người dùng chốt; sửa file md nguồn rồi chạy `build_docs.py --all` và `kiem-tra-bo-nho.py`.

Ví dụ (từ gốc repo):
    python -X utf8 .claude/skills/lap-ke-hoach-retest/scripts/can-cap-nhat-khi-dong.py testing/<dự-án>/<tính-năng>/bug/BUG-001.md
"""
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[4]
HINTS = [
    (re.compile(r"lỗi đã biết|Đạt kèm", re.I), "đổi lại thành Đạt nếu ý này chỉ sai vì bug đã đóng"),
    (re.compile(r"Bị chặn", re.I), "CHẠY LẠI ca này (đang bị chặn bởi bug)"),
    (re.compile(r"Không đạt", re.I), "kiểm lại trạng thái, chạy lại ca"),
]


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 1
    bug = Path(sys.argv[1]).resolve()
    if not bug.exists():
        print(f"Không có file {bug}")
        return 1
    try:
        parts = bug.relative_to(ROOT / "testing").parts
    except ValueError:
        print("File bug phải nằm trong testing/<dự-án>/<tính-năng>/bug/")
        return 1
    slug, code = parts[0], bug.stem
    pattern = re.compile(rf"\b{re.escape(code)}\b")
    skip = {bug, bug.parent.parent / "retest" / f"{code}-ke-hoach.md"}

    files = sorted(list((ROOT / "testing" / slug).rglob("*.md")) + list((ROOT / "memories" / "modules" / slug).rglob("*.md")))
    total = 0
    for f in files:
        if f.resolve() in skip:
            continue
        hits = []
        for number, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if pattern.search(line):
                hint = next((h for rx, h in HINTS if rx.search(line)), "")
                hits.append((number, line.strip()[:170], hint))
        if hits:
            print(f"\n{f.relative_to(ROOT).as_posix()}")
            for number, snippet, hint in hits:
                print(f"  dòng {number}: {snippet}" + (f"\n      → {hint}" if hint else ""))
            total += len(hits)
    print(f"\n{total} chỗ nhắc {code} trong tài liệu của dự án {slug}." if total else f"\nKhông có chỗ nào nhắc {code} ngoài file bug.")
    print("Việc đổi trạng thái do người dùng chốt. Sửa md nguồn rồi chạy: build_docs.py --all, kiem-tra-bo-nho.py. "
          "Nhớ ghi trạng thái Đóng ở công cụ của team (không nằm trong kho này).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
