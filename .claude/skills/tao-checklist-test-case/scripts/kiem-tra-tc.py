#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Kiểm checklist và test case (đầu ra của skill tao-checklist-test-case).

  python -X utf8 kiem-tra-tc.py --test-case <test-case.md> [--nguon <requirement.md> --ma "<regex mã>" --tien-to CART]
      (FILE GỘP, cách mặc định từ 2026-11-18: một bảng 13 cột có cả Kỹ thuật; kiểm phần checklist và phần test case trong cùng file)
  python -X utf8 kiem-tra-tc.py --checklist <checklist.md> [--test-case <test-case.md>] [...]   (cách cũ, hai file)

Thoát mã 1 nếu có LỖI (cảnh báo thì không). Kiểm:
 Checklist : đủ 5 cột đúng tên; mã TC-001 liên tục, không trùng; Ưu tiên, Kỹ thuật thuộc danh sách; Nguồn bắt đầu bằng
             "Có trong tài liệu" hoặc "Suy luận" (không có Giả định); xếp Cao trước; (có --nguon) mọi mã requirement có dòng.
 Test case : đủ 12 cột đúng tên; mã khớp checklist 100%, không trùng, cùng thứ tự; Ưu tiên khớp checklist; Điều kiện trước,
             Dữ liệu test, Kết quả mong đợi không trống; Các bước đánh số 1,2,3 liên tục; không "như TC-xxx" hay nhắc mã TC khác;
             không có mã requirement (R, TL, S..-AC.., M..) trong Kết quả mong đợi; "Bước N" nằm trong số bước; Trạng thái thuộc
             danh sách; Tự động hóa là Chưa có / Có: <đường dẫn> / Không tự động được: <lý do>; ô có CẦN XÁC NHẬN phải có trong mục "Câu hỏi cho BA"; cảnh báo email thật, thiếu "Bước N".
"""
import argparse
import re
import sys
from pathlib import Path

PRI = ["Cao", "Trung bình", "Thấp"]
KT = ["EP", "BVA", "Bảng quyết định", "Chuyển trạng thái", "Use case", "Đoán lỗi"]
CK_HEAD = ["Mã", "Tình huống", "Ưu tiên", "Kỹ thuật", "Nguồn"]
GOP_HEAD = ["Mã", "Tình huống", "Ưu tiên", "Kỹ thuật", "Điều kiện trước", "Các bước", "Dữ liệu test", "Kết quả mong đợi",
            "Nguồn", "Kết quả thực tế", "Trạng thái", "Người viết", "Tự động hóa"]
TC_HEAD = ["Mã", "Tình huống", "Ưu tiên", "Điều kiện trước", "Các bước", "Dữ liệu test", "Kết quả mong đợi", "Nguồn",
           "Kết quả thực tế", "Trạng thái", "Người viết", "Tự động hóa"]
TRANG_THAI = ["Chưa chạy", "Đạt", "Không đạt", "Bị chặn", "Bỏ qua"]
# Mã requirement dạng thường gặp; dùng để cấm trong "Kết quả mong đợi"
MA_CAM = re.compile(r"(?<![\w-])(?:TL-?\d+|R\d{1,3}|M\d{1,3}|S\d\d-AC\d\d|[A-Z]{2,8}-(?:S\d\d-AC\d\d|R\d\d|M\d\d|AC\d\d))(?![\w])")

loi, canh_bao = [], []


def L(msg):
    loi.append(msg)


def W(msg):
    canh_bao.append(msg)


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def read_table(text, where):
    names, rows, order = None, {}, []
    for line in text.splitlines():
        if names is None:
            if line.startswith("| Mã |"):
                names = cells(line)
            continue
        m = re.match(r'^\| (?:<a id="[^"]*"></a>)?(TC-\d+) \|', line)
        if not m:
            continue
        c = cells(line)
        if len(c) != len(names):
            L(f"{where} {m.group(1)}: có {len(c)} ô, tiêu đề có {len(names)} cột")
            continue
        if m.group(1) in rows:
            L(f"{where}: mã {m.group(1)} xuất hiện hai lần")
        rows[m.group(1)] = dict(zip(names, c))
        order.append(m.group(1))
    if names is None:
        L(f"{where}: không thấy bảng có tiêu đề bắt đầu bằng '| Mã |'")
    return names, rows, order


def kiem_checklist(path, nguon, ma_re, tien_to, gop=False):
    t = Path(path).read_text(encoding="utf-8")
    names, rows, order = read_table(t, "Test case (gộp)" if gop else "Checklist")
    dau = GOP_HEAD if gop else CK_HEAD
    if names is not None and names != dau:
        L(f"{'File gộp' if gop else 'Checklist'}: cột phải đúng thứ tự {dau}, hiện là {names}")
    nums = [int(x[3:]) for x in order]
    if nums != list(range(1, len(nums) + 1)):
        L("Checklist: mã TC phải liên tục từ TC-001 theo đúng thứ tự dòng")
    for m, r in rows.items():
        if r.get("Ưu tiên") not in PRI:
            L(f"Checklist {m}: Ưu tiên '{r.get('Ưu tiên')}' không thuộc {PRI}")
        if r.get("Kỹ thuật") not in KT:
            L(f"Checklist {m}: Kỹ thuật '{r.get('Kỹ thuật')}' phải đúng một trong {KT}")
        ng = r.get("Nguồn", "")
        if not ng.startswith(("Có trong tài liệu", "Suy luận")):
            L(f"Checklist {m}: Nguồn phải bắt đầu bằng 'Có trong tài liệu' hoặc 'Suy luận' (Giả định không vào bảng chính)")
        if ng.startswith("Suy luận") and len(ng) < 40:
            W(f"Checklist {m}: dòng Suy luận nên có một câu lý do đủ rõ")
        if not r.get("Tình huống"):
            L(f"Checklist {m}: Tình huống trống")
    # Dòng thêm sau khi requirement đổi lấy số kế tiếp (không đổi mã cũ) nên xếp cuối bảng, không theo thứ tự ưu tiên.
    # Khai báo ở bảng đầu file: "| Dòng thêm sau khi requirement đổi | TC-042, TC-043 (...) |"
    them_sau = set()
    mm = re.search(r"\|\s*Dòng thêm sau[^|]*\|([^|]*)\|", t)
    if mm:
        them_sau = set(re.findall(r"TC-\d+", mm.group(1)))
    pr = [PRI.index(r["Ưu tiên"]) for k, r in rows.items() if r.get("Ưu tiên") in PRI and k not in them_sau]
    if pr != sorted(pr):
        L("Checklist: dòng Cao phải xếp trước, rồi Trung bình, rồi Thấp")
    if nguon and ma_re:
        src = Path(nguon).read_text(encoding="utf-8")
        codes = sorted(set(re.findall(ma_re, src)))
        blob = " ".join(r.get("Nguồn", "") for r in rows.values())
        thieu = []
        for c in codes:
            short = re.sub(r"^" + re.escape(tien_to) + r"-", "", c) if tien_to else c
            if not re.search(r"(?<![\w-])" + re.escape(short) + r"(?![\w])", blob):
                thieu.append(c)
        if thieu:
            L(f"Checklist: {len(thieu)} mã requirement chưa có dòng nào: {', '.join(thieu)}")
        print(f"  Phủ requirement: {len(codes) - len(thieu)}/{len(codes)} mã")
    print(f"  Checklist: {len(rows)} dòng " + ", ".join(f"{p} {sum(1 for r in rows.values() if r.get('Ưu tiên') == p)}" for p in PRI))
    return rows, order


def kiem_test_case(path, ck_rows, ck_order):
    t = Path(path).read_text(encoding="utf-8")
    names, rows, order = read_table(t, "Test case")
    if names is not None:
        thieu = [c for c in TC_HEAD if c not in names]
        if thieu:
            L(f"Test case: thiếu cột {thieu}")
    if ck_rows is not None:
        if set(rows) != set(ck_rows):
            L(f"Test case: mã lệch checklist: chỉ ở checklist {sorted(set(ck_rows)-set(rows))}, chỉ ở test case {sorted(set(rows)-set(ck_rows))}")
        if order != ck_order:
            W("Test case: thứ tự mã khác checklist")
    sec = re.search(r"^## Câu hỏi cho BA\s*$(.*?)(?=^## |\Z)", t, re.S | re.M)
    cau_hoi = sec.group(1) if sec else ""
    if not sec:
        L('Test case: thiếu mục "## Câu hỏi cho BA" (không có câu hỏi thì ghi "Không có.")')
    for m, r in rows.items():
        for k in ("Điều kiện trước", "Dữ liệu test", "Kết quả mong đợi", "Nguồn", "Tình huống"):
            if not r.get(k, "").strip():
                L(f"Test case {m}: cột {k} trống")
        if ck_rows and m in ck_rows:
            if r.get("Ưu tiên") != ck_rows[m].get("Ưu tiên"):
                L(f"Test case {m}: Ưu tiên khác checklist")
            if r.get("Tình huống") != ck_rows[m].get("Tình huống"):
                W(f"Test case {m}: Tình huống không giống nguyên văn checklist")
            if r.get("Nguồn") != ck_rows[m].get("Nguồn"):
                W(f"Test case {m}: Nguồn không giống checklist")
        steps = [s for s in r.get("Các bước", "").split("<br>") if s.strip()]
        nums = []
        for s in steps:
            mm = re.match(r"^(\d+)\.\s", s)
            nums.append(int(mm.group(1)) if mm else -1)
        if not steps or nums != list(range(1, len(steps) + 1)):
            L(f"Test case {m}: Các bước phải đánh số 1, 2, 3… liên tục, mỗi bước một dòng")
        ket = r.get("Kết quả mong đợi", "")
        for k, v in r.items():
            if k in ("Mã", "Tự động hóa", "Kết quả thực tế", "Trạng thái", "Người viết"):
                # tên script đặt theo mã TC; cột ghi khi chạy được nhắc ca khác ("cùng lỗi với TC-001"), quy tắc tự đứng chỉ cho phần thiết kế
                continue
            if re.search(r"\b(như|giống|xem|theo)\s+TC-\d+", v, re.I) or re.search(r"TC-\d+", v):
                L(f"Test case {m}: cột {k} nhắc mã TC khác (mỗi case phải tự đứng)")
        if MA_CAM.search(ket):
            L(f"Test case {m}: Kết quả mong đợi có mã requirement '{MA_CAM.search(ket).group(0)}' (mã chỉ ghi ở cột Nguồn)")
        for mm in re.finditer(r"Bước (\d+)(?: đến bước (\d+))?", ket):
            for g in (mm.group(1), mm.group(2)):
                if g and int(g) > len(steps):
                    L(f"Test case {m}: kết quả nhắc 'Bước {g}' nhưng chỉ có {len(steps)} bước")
        if len(steps) > 1 and "Bước" not in ket:
            W(f"Test case {m}: kết quả mong đợi nên ghi rõ ở bước nào (có {len(steps)} bước)")
        if r.get("Trạng thái") not in TRANG_THAI:
            L(f"Test case {m}: Trạng thái '{r.get('Trạng thái')}' không thuộc {TRANG_THAI}")
        if not r.get("Người viết", "").strip():
            W(f"Test case {m}: Người viết trống")
        au = r.get("Tự động hóa", "").strip()
        if not au.startswith(("Chưa có", "Có:", "Không tự động được:")):
            L(f"Test case {m}: Tự động hóa phải bắt đầu bằng Chưa có, Có: <đường dẫn> hoặc Không tự động được: <lý do>")
        elif au.startswith("Có:"):
            duong = au[3:].strip().strip("`").strip()
            if not duong or not Path(duong).exists():
                W(f"Test case {m}: script {duong} không tồn tại (đường dẫn tính từ gốc repo)")
        elif au.startswith("Không tự động được:") and len(au) < 28:
            W(f"Test case {m}: ghi lý do vì sao không tự động được")
        for em in re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", r.get("Dữ liệu test", "") + " " + r.get("Các bước", "")):
            em = em.rstrip(".")
            if not em.lower().endswith("@example.com"):
                W(f"Test case {m}: email '{em}' không phải dữ liệu giả @example.com")
        cxn = any("CẦN XÁC NHẬN" in v for k, v in r.items() if k not in ("Kết quả thực tế",))
        if cxn and m not in cau_hoi:
            L(f"Test case {m}: có CẦN XÁC NHẬN nhưng mục Câu hỏi cho BA không nhắc {m}")
    dem = {}
    for r in rows.values():
        dem[r.get("Trạng thái", "?")] = dem.get(r.get("Trạng thái", "?"), 0) + 1
    print(f"  Test case: {len(rows)} case; trạng thái: " + ", ".join(f"{k} {v}" for k, v in sorted(dem.items())))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--checklist", help="bỏ trống = file gộp (chỉ cần --test-case)")
    ap.add_argument("--test-case")
    ap.add_argument("--nguon")
    ap.add_argument("--ma", help="biểu thức chính quy của mã requirement trong file nguồn, ví dụ CART-(?:S\\d\\d-AC\\d\\d|R\\d\\d|M\\d\\d)")
    ap.add_argument("--tien-to", default="", help="tiền tố mã bỏ đi trong cột Nguồn, ví dụ CART")
    a = ap.parse_args()
    print("Kiểm checklist/test case")
    if not a.checklist:
        if not a.test_case:
            sys.exit("Cần --test-case (file gộp) hoặc --checklist")
        _, gop_order = kiem_checklist(a.test_case, a.nguon, a.ma, a.tien_to, gop=True)
        kiem_test_case(a.test_case, None, gop_order)
    else:
        ck_rows, ck_order = kiem_checklist(a.checklist, a.nguon, a.ma, a.tien_to)
        if a.test_case:
            kiem_test_case(a.test_case, ck_rows, ck_order)
    for w in canh_bao:
        print("  CẢNH BÁO:", w)
    for e in loi:
        print("  LỖI:", e)
    print(f"Kết quả: {len(loi)} lỗi, {len(canh_bao)} cảnh báo")
    sys.exit(1 if loi else 0)


if __name__ == "__main__":
    main()
