#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Liệt kê gọn test case của một dự án để chọn smoke, không phải đọc cả file test-case.md.

  python -X utf8 .claude/skills/tao-smoke-test/scripts/liet-ke-tc.py <dự-án> [--tinh-nang <thư-mục>] [--cao]

Mỗi dòng: Mã | Ưu tiên | cờ | số bước | ~phút | Tình huống (cắt 110 ký tự).
~phút = số bước x 18 giây, làm tròn 0,5 phút (ước lượng thô, chưa gồm chờ cố định; để mọi phiên ước lượng cùng một cách).
Cờ (suy ra từ cột của test case, không chép tay):
  ⚠️   cột Nguồn có dấu ⚠️: hệ thống đang làm khác kết quả mong đợi (smoke sẽ Không đạt cho tới khi sửa)
  SAI-N cột Điều kiện trước có "cố ý nhập sai N lần": có thể kích hoạt giới hạn/khóa tài khoản
  CHO   cột Các bước có "Chờ ... phút": phải chờ lâu
  PHU   Các bước/Kết quả có tác dụng phụ khó đảo ngược (bấm Gửi/Phê duyệt/Từ chối/Xóa/Thanh toán, SMS, email)
Dòng đầu mỗi module: số case, số case đã chạy thật (Đạt/Không đạt), và NGUỒN NHÁP nếu requirement ghi "chưa BA xác nhận".
--cao: chỉ in test case ưu tiên Cao.
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PHU = re.compile(r"(?:[Bb]ấm|[Nn]hấn|[Cc]họn)[^.<]{0,40}(?:Gửi|Phê duyệt|Từ chối|Trả lại|Xóa|Xoá|Hủy|Thanh toán|Chuyển tiền)|\bSMS\b|\bemail\b|\bgửi (?:thư|tin)")
TC = re.compile(r'^\| (?:<a id="[^"]*"></a>)?(TC-\d+) \|')


def cells(line):
    line = re.sub(r'<a id="[^"]*"></a>', "", line)
    return [c.strip() for c in line.strip().strip("|").split("|")]


def doc(path):
    names, out = None, []
    for line in path.read_text(encoding="utf-8").splitlines():
        if names is None:
            if line.startswith("| Mã |"):
                names = cells(line)
            continue
        if not TC.match(line):
            continue
        c = cells(line)
        if len(c) == len(names):
            out.append(dict(zip(names, c)))
    return out


def srs_nhap(test_case_file):
    """SRS của tính năng ghi Tình trạng là nháp hoặc chưa xác nhận (bảng đầu SRS theo khuôn srs/_template.md)."""
    import json
    srs = None
    cfg = test_case_file.parent / "truy-vet-cau-hinh.json"
    if cfg.exists():
        try:
            srs = ROOT / json.loads(cfg.read_text(encoding="utf-8")).get("srs", "")
        except ValueError:
            srs = None
    if not srs or not srs.is_file():
        srs = ROOT / "srs" / test_case_file.parent.parent.name / (test_case_file.parent.name + ".md")
    if not srs.is_file():
        return False
    for line in srs.read_text(encoding="utf-8").splitlines()[:30]:
        if line.startswith("| Tình trạng |"):
            if re.search(r"đã (?:có )?xác nhận", line, re.I) and not re.search(r"chưa (?:có )?xác nhận", line, re.I):
                return False   # "nháp, đã có xác nhận của BA" không còn là nguồn nháp
            return bool(re.search(r"nháp|chưa (?:có )?xác nhận", line, re.I))
    return False


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("du_an")
    ap.add_argument("--tinh-nang", default=None)
    ap.add_argument("--cao", action="store_true")
    a = ap.parse_args()
    base = ROOT / "testing" / a.du_an
    files = sorted(base.glob("*/test-case.md"))
    if a.tinh_nang:
        files = [f for f in files if f.parent.name == a.tinh_nang]
    if not files:
        sys.exit(f"Không thấy testing/{a.du_an}/*/test-case.md")
    for f in files:
        rows = doc(f)
        nhap = (" | NGUỒN NHÁP (requirement chưa BA xác nhận)"
                if re.search(r"chưa BA xác nhận|\(nháp", f.read_text(encoding="utf-8")[:3000]) or srs_nhap(f) else "")
        chay = sum(1 for r in rows if r.get("Trạng thái") in ("Đạt", "Không đạt"))
        print(f"== {f.parent.name} ({len(rows)} test case, đã chạy thật {chay}) — {f.relative_to(ROOT).as_posix()}{nhap}")
        for r in rows:
            if a.cao and r.get("Ưu tiên") != "Cao":
                continue
            co = []
            if "⚠️" in r.get("Nguồn", ""):
                co.append("⚠️")
            m = re.search(r"cố ý nhập sai (\d+) lần", r.get("Điều kiện trước", ""))
            if m:
                co.append(f"SAI-{m.group(1)}")
            if re.search(r"[Cc]hờ[^.<]{0,40}phút", r.get("Các bước", "")):
                co.append("CHO")
            if PHU.search(r.get("Các bước", "") + " " + r.get("Kết quả mong đợi", "")):
                co.append("PHU")
            n = len(re.findall(r"(?:^|<br>)\d+\.\s", r.get("Các bước", "")))
            ph = max(0.5, round(n * 18 / 60 * 2) / 2)
            th = re.sub(r"[`*]", "", r.get("Tình huống", ""))
            th = th if len(th) <= 110 else th[:109] + "…"
            print(f"{r['Mã']} | {r.get('Ưu tiên', '?')} | {' '.join(co) or '-'} | {n}b | ~{ph:g}p | {th}")


if __name__ == "__main__":
    main()
