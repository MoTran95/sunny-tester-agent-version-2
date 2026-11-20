#!/usr/bin/env python3
"""Kiểm mục 0 "Bảng phủ" của nhật ký khám phá: đã đủ để khỏi khám phá lại chưa.

Dùng:  python -X utf8 kiem-tra-bang-phu.py evidence/<hệ thống>/features/<feature>/bao-cao.md

Kết quả (in rất ngắn):
  ĐỦ          mọi dòng có trạng thái hợp lệ và có hàng nhật ký/lý do  -> không cần mở trình duyệt
              (ca "Chưa làm" kèm lý do thật như cần mật khẩu, chờ thời gian là ngoại lệ đã ghi, vẫn tính ĐỦ)
  CÒN THIẾU   in từng dòng còn trống / "Chưa có trong nhật ký" / thiếu lý do -> hỏi người dùng, không tự khám phá
  KHÔNG CÓ    nhật ký chưa có mục 0 -> dựng bảng từ các hàng sẵn có (không mở trình duyệt)
Thoát mã 0 nếu ĐỦ, mã 1 nếu CÒN THIẾU hoặc KHÔNG CÓ.
"""
import re
import sys
from pathlib import Path

OK = ("đã làm", "không áp dụng")
KNOWN = "chưa làm"
GAP = ("chưa có trong nhật ký",)


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    text = Path(sys.argv[1]).read_text(encoding="utf-8")
    m = re.search(r"^##\s*0\.[^\n]*\n(.*?)(?=^##\s|\Z)", text, re.S | re.M)
    if not m:
        print("KHÔNG CÓ: nhật ký chưa có mục '## 0. Bảng phủ'")
        return 1
    rows = []
    for line in m.group(1).split("\n"):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3 or set(cells[0]) <= set("-: ") or cells[0].lower().startswith("nhóm ca"):
            continue
        rows.append(cells[:3])
    if not rows:
        print("KHÔNG CÓ: mục 0 không có dòng nào")
        return 1
    gaps, known = [], []
    for name, status, why in rows:
        s = status.lower()
        if not s:
            gaps.append(f"- {name}: trạng thái trống")
        elif s.startswith(OK):
            if not why:
                gaps.append(f"- {name}: '{status}' nhưng thiếu hàng nhật ký/lý do")
        elif s.startswith(KNOWN):
            if why:
                known.append(name)
            else:
                gaps.append(f"- {name}: 'Chưa làm' nhưng thiếu lý do thật")
        elif s.startswith(GAP):
            gaps.append(f"- {name}: {status}" + (f" ({why})" if why else ""))
        else:
            gaps.append(f"- {name}: trạng thái '{status}' không hợp lệ (chỉ Đã làm / Chưa làm / Không áp dụng / Chưa có trong nhật ký)")
    if gaps:
        print(f"CÒN THIẾU ({len(gaps)}/{len(rows)} dòng):")
        print("\n".join(gaps))
        return 1
    print(f"ĐỦ: {len(rows)}/{len(rows)} dòng có trạng thái hợp lệ"
          + (f"; {len(known)} ca chưa làm có lý do thật (không khám phá lại): " + "; ".join(known) if known else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
