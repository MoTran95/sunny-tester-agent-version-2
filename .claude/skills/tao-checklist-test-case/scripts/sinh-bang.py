#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Sinh file checklist.md và test-case.md từ dữ liệu JSON, để không phải gõ tay bảng Markdown (hay vỡ cột).

  python -X utf8 sinh-bang.py gop --du-lieu <dl.json> --ra <test-case.md> [--nguoi-viet "Tên"] [--ghi-de]
      (CÁCH MẶC ĐỊNH từ 2026-11-18: MỘT file, mỗi dòng gồm cả phần checklist và phần chi tiết test case)
  python -X utf8 sinh-bang.py checklist --du-lieu <dl.json> --ra <checklist.md> [--ghi-de]      (cách cũ, hai file)
  python -X utf8 sinh-bang.py test-case --du-lieu <dl.json> --checklist <checklist.md> --ra <test-case.md>
                                        [--nguoi-viet "Tên"] [--ghi-de]

Định dạng JSON xem assets/mau-du-lieu-gop.json (gop). Lệnh checklist/test-case là cách hai file cũ, không dùng nữa (khuôn JSON của chúng đã bỏ 2026-11-19).
- gop: mã TC-001... đánh theo thứ tự sau khi xếp Cao, Trung bình, Thấp. Ca có sẵn "ma" thì giữ mã đó (dùng khi cập nhật);
  ca chưa có "ma" lấy số kế tiếp. Bốn cột ghi khi chạy được GIỮ LẠI theo mã nếu file đã có.
- checklist: mã TC-001... đánh theo thứ tự sau khi xếp Cao, Trung bình, Thấp (giữ thứ tự nhập trong cùng mức).
- test-case: Tình huống, Ưu tiên, Nguồn lấy NGUYÊN VĂN từ checklist theo mã. Ba cột ghi khi chạy test
  (Kết quả thực tế, Trạng thái, Người viết, Tự động hóa) được GIỮ LẠI theo mã nếu file test-case đã có; không bao giờ ghi đè.
- File đã có: nếu có cặp dấu <!-- BANG-TC:BAT-DAU --> ... <!-- BANG-TC:KET-THUC --> thì chỉ thay bảng giữa hai dấu;
  nếu không có dấu thì dừng, trừ khi có --ghi-de (ghi lại cả file; vẫn giữ ba cột ghi khi chạy).
Dấu `|` trong nội dung ô được đổi thành `¦` (escape từng ô, không escape cả dòng).
"""
import argparse
import datetime
import json
import re
import sys
from pathlib import Path

PRI = ["Cao", "Trung bình", "Thấp"]
KT = ["EP", "BVA", "Bảng quyết định", "Chuyển trạng thái", "Use case", "Đoán lỗi"]
START = "<!-- BANG-TC:BAT-DAU (bảng test case; tiêu đề cột là cố định để script đọc) -->"
END = "<!-- BANG-TC:KET-THUC -->"
CK_HEAD = ["Mã", "Tình huống", "Ưu tiên", "Kỹ thuật", "Nguồn"]
GOP_HEAD = ["Mã", "Tình huống", "Ưu tiên", "Kỹ thuật", "Điều kiện trước", "Các bước", "Dữ liệu test", "Kết quả mong đợi",
            "Nguồn", "Kết quả thực tế", "Trạng thái", "Người viết", "Tự động hóa"]
TC_HEAD = ["Mã", "Tình huống", "Ưu tiên", "Điều kiện trước", "Các bước", "Dữ liệu test", "Kết quả mong đợi", "Nguồn",
           "Kết quả thực tế", "Trạng thái", "Người viết", "Tự động hóa"]


def esc(s):
    return re.sub(r"\s+", " ", str(s).replace("|", "¦")).strip()


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def neo(ma):
    """Ô Mã của test case: thẻ neo để link tới đúng dòng (smoke-test.md, truy vết), script truy vết không tính thẻ này là nội dung."""
    return f'<a id="{ma.lower()}"></a>{ma}'


def table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += ["| " + " | ".join(r) + " |" for r in rows]
    return out


def read_table(text):
    """Đọc bảng đầu tiên có tiêu đề bắt đầu bằng '| Mã |' → (tên cột, {mã: {tên cột: giá trị}})."""
    names, rows = None, {}
    for line in text.splitlines():
        if names is None:
            if line.startswith("| Mã |"):
                names = cells(line)
            continue
        m = re.match(r'^\| (?:<a id="[^"]*"></a>)?(TC-\d+) \|', line)
        if m:
            c = cells(line)
            if len(c) == len(names):
                rows[m.group(1)] = dict(zip(names, c))
    return names, rows


def block_rows(text, marker_start=START, marker_end=END):
    return marker_start in text and marker_end in text


def lines_of(items):
    return [str(x) for x in (items or [])]


def paragraphs(items):
    out = []
    for p in items or []:
        out += [p, ""]
    return out


def write_file(path, content, ghi_de, bang_lines):
    """Ghi file mới, hoặc chỉ thay bảng giữa hai dấu nếu file đã có dấu."""
    p = Path(path)
    if p.exists():
        old = p.read_text(encoding="utf-8")
        if START in old and END in old:
            new = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda m: "\n".join([START] + bang_lines + [END]), old, flags=re.S)
            p.write_text(new, encoding="utf-8")
            return "thay bảng giữa hai dấu, giữ nguyên phần còn lại"
        if not ghi_de:
            sys.exit(f"{p} đã có và không có dấu BANG-TC; dùng --ghi-de nếu thật sự muốn ghi lại cả file")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return "ghi file mới"


def lenh_checklist(a):
    d = json.loads(Path(a.du_lieu).read_text(encoding="utf-8"))
    dong = d["dong"]
    for i, r in enumerate(dong, 1):
        if r["uu_tien"] not in PRI:
            sys.exit(f"dòng {i}: ưu tiên '{r['uu_tien']}' không thuộc {PRI}")
        if r["ky_thuat"] not in KT:
            sys.exit(f"dòng {i}: kỹ thuật '{r['ky_thuat']}' không thuộc {KT}")
        if not r["nguon"].startswith(("Có trong tài liệu", "Suy luận")):
            sys.exit(f"dòng {i}: nguồn phải bắt đầu bằng 'Có trong tài liệu' hoặc 'Suy luận' (Giả định không vào bảng chính)")
    dong = sorted(dong, key=lambda r: PRI.index(r["uu_tien"]))
    rows = [[f"TC-{i:03d}", esc(r["tinh_huong"]), r["uu_tien"], r["ky_thuat"], esc(r["nguon"])] for i, r in enumerate(dong, 1)]
    bang = table(CK_HEAD, rows)
    dem = {p: sum(1 for r in rows if r[2] == p) for p in PRI}
    L = [f"# Checklist test — {d['tieu_de']}", "", "| | |", "|---|---|",
         f"| Ngày lập | {d.get('ngay') or datetime.date.today().isoformat()} |",
         f"| Hệ thống | {esc(d['he_thong'])} |", f"| Nguồn | {esc(d['nguon_doc'])} |",
         "| Chỉ làm | Checklist. Chưa viết bước chi tiết |", ""]
    L += paragraphs(d.get("ghi_chu_dau"))
    L += [START] + bang + [END, ""]
    if d.get("cau_hoi"):
        L += ["## Câu hỏi cho BA"] + [f"{i}. {c}" for i, c in enumerate(d["cau_hoi"], 1)] + [""]
    if d.get("chua_dua_vao"):
        L += ["## Chưa đưa vào"] + [f"- {c}" for c in d["chua_dua_vao"]] + [""]
    L += ["## Tự kiểm", f"- {len(rows)} dòng: Cao {dem['Cao']}, Trung bình {dem['Trung bình']}, Thấp {dem['Thấp']}. Chạy `kiem-tra-tc.py` để kiểm đầy đủ.", ""]
    print(write_file(a.ra, "\n".join(L), a.ghi_de, bang), f"({len(rows)} dòng) → {a.ra}")


def lenh_test_case(a):
    d = json.loads(Path(a.du_lieu).read_text(encoding="utf-8"))
    ck_text = Path(a.checklist).read_text(encoding="utf-8")
    _, ck = read_table(ck_text)
    if not ck:
        sys.exit("Không đọc được bảng checklist")
    ca = {c["ma"]: c for c in d["ca"]}
    if len(ca) != len(d["ca"]):
        sys.exit("Có mã test case trùng trong dữ liệu")
    if set(ca) != set(ck):
        sys.exit(f"Mã test case lệch checklist: chỉ ở checklist {sorted(set(ck)-set(ca))}, chỉ ở dữ liệu {sorted(set(ca)-set(ck))}")
    keep = {}
    p = Path(a.ra)
    if p.exists():
        _, old = read_table(p.read_text(encoding="utf-8"))
        keep = {m: (r.get("Kết quả thực tế", " "), r.get("Trạng thái", "Chưa chạy"), r.get("Người viết", a.nguoi_viet), r.get("Tự động hóa", "Chưa có")) for m, r in old.items()}
    rows = []
    for ma in sorted(ck):
        c, k = ca[ma], ck[ma]
        tt, tv, nv, au = keep.get(ma, (" ", "Chưa chạy", a.nguoi_viet, "Chưa có"))
        rows.append([neo(ma), k["Tình huống"], k["Ưu tiên"], "<br>".join(esc(x) for x in c["dieu_kien"]),
                     "<br>".join(f"{i}. {esc(x)}" for i, x in enumerate(c["buoc"], 1)),
                     "<br>".join(esc(x) for x in c["du_lieu"]), "<br>".join(esc(x) for x in c["ket_qua"]),
                     k["Nguồn"], tt or " ", tv, nv, au or "Chưa có"])
    bang = table(TC_HEAD, rows)
    L = [f"# Test case chi tiết — {d['tieu_de']}", "", "| | |", "|---|---|",
         f"| Ngày lập | {d.get('ngay') or datetime.date.today().isoformat()} |",
         f"| Hệ thống | {esc(d['he_thong'])} |", f"| Nguồn | {esc(d['nguon_doc'])} |",
         f"| Tình trạng | {esc(d.get('tinh_trang', 'Chưa chạy thử trên hệ thống'))} |", ""]
    L += paragraphs(d.get("ghi_chu_dau"))
    L += [START] + bang + [END, ""]
    L += ["## Câu hỏi cho BA"] + ([f"{i}. {c}" for i, c in enumerate(d.get("cau_hoi", []), 1)] or ["Không có."]) + [""]
    if d.get("ghi_nhan_rieng"):
        L += ["## Ghi nhận riêng (không tự gộp, xóa hay thêm test case)"] + [f"- {c}" for c in d["ghi_nhan_rieng"]] + [""]
    L += ["## Tự kiểm", f"- {len(rows)} test case. Chạy `kiem-tra-tc.py` để kiểm đầy đủ.", ""]
    print(write_file(a.ra, "\n".join(L), a.ghi_de, bang), f"({len(rows)} test case, giữ {len(keep)} bộ ba cột ghi khi chạy) → {a.ra}")


def lenh_gop(a):
    d = json.loads(Path(a.du_lieu).read_text(encoding="utf-8"))
    ca = d["ca"]
    for i, r in enumerate(ca, 1):
        if r["uu_tien"] not in PRI:
            sys.exit(f"ca {i}: ưu tiên '{r['uu_tien']}' không thuộc {PRI}")
        if r["ky_thuat"] not in KT:
            sys.exit(f"ca {i}: kỹ thuật '{r['ky_thuat']}' không thuộc {KT}")
        if not r["nguon"].startswith(("Có trong tài liệu", "Suy luận")):
            sys.exit(f"ca {i}: nguồn phải bắt đầu bằng 'Có trong tài liệu' hoặc 'Suy luận' (Giả định không vào bảng chính)")
        for k in ("dieu_kien", "buoc", "du_lieu", "ket_qua"):
            if not r.get(k):
                sys.exit(f"ca {i}: thiếu '{k}'")
    co_ma = [r for r in ca if r.get("ma")]
    chua = sorted((r for r in ca if not r.get("ma")), key=lambda r: PRI.index(r["uu_tien"]))
    nxt = max([int(r["ma"][3:]) for r in co_ma], default=0)
    for r in chua:
        nxt += 1
        r["ma"] = f"TC-{nxt:03d}"
    ma_list = [r["ma"] for r in ca]
    if len(set(ma_list)) != len(ma_list):
        sys.exit("Có mã test case trùng trong dữ liệu")
    ca = sorted(ca, key=lambda r: int(r["ma"][3:]))
    keep = {}
    p = Path(a.ra)
    if p.exists():
        _, old = read_table(p.read_text(encoding="utf-8"))
        keep = {m: (r.get("Kết quả thực tế", " "), r.get("Trạng thái", "Chưa chạy"), r.get("Người viết", a.nguoi_viet), r.get("Tự động hóa", "Chưa có")) for m, r in old.items()}
    rows = []
    for c in ca:
        tt, tv, nv, au = keep.get(c["ma"], (" ", "Chưa chạy", a.nguoi_viet, "Chưa có"))
        rows.append([neo(c["ma"]), esc(c["tinh_huong"]), c["uu_tien"], c["ky_thuat"], "<br>".join(esc(x) for x in c["dieu_kien"]),
                     "<br>".join(f"{i}. {esc(x)}" for i, x in enumerate(c["buoc"], 1)),
                     "<br>".join(esc(x) for x in c["du_lieu"]), "<br>".join(esc(x) for x in c["ket_qua"]),
                     esc(c["nguon"]), tt or " ", tv, nv, au or "Chưa có"])
    bang = table(GOP_HEAD, rows)
    dem = {pr: sum(1 for r in rows if r[2] == pr) for pr in PRI}
    L = [f"# Test case (gồm checklist) — {d['tieu_de']}", "", "| | |", "|---|---|",
         f"| Ngày lập | {d.get('ngay') or datetime.date.today().isoformat()} |",
         f"| Hệ thống | {esc(d['he_thong'])} |", f"| Nguồn | {esc(d['nguon_doc'])} |",
         f"| Tình trạng | {esc(d.get('tinh_trang', 'Chưa chạy thử trên hệ thống'))} |", ""]
    L += paragraphs(d.get("ghi_chu_dau"))
    L += [START] + bang + [END, ""]
    L += ["## Câu hỏi cho BA"] + ([f"{i}. {c}" for i, c in enumerate(d.get("cau_hoi", []), 1)] or ["Không có."]) + [""]
    if d.get("chua_dua_vao"):
        L += ["## Chưa đưa vào (phần chưa chốt, không viết theo yêu cầu)"] + [f"- {c}" for c in d["chua_dua_vao"]] + [""]
    if d.get("ghi_nhan_rieng"):
        L += ["## Ghi nhận riêng (không tự gộp, xóa hay thêm test case)"] + [f"- {c}" for c in d["ghi_nhan_rieng"]] + [""]
    L += ["## Tự kiểm", f"- {len(rows)} test case: Cao {dem['Cao']}, Trung bình {dem['Trung bình']}, Thấp {dem['Thấp']}. Chạy `kiem-tra-tc.py` để kiểm đầy đủ.", ""]
    print(write_file(a.ra, "\n".join(L), a.ghi_de, bang), f"({len(rows)} test case, giữ {len(keep)} bộ cột ghi khi chạy) → {a.ra}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="lenh", required=True)
    g = sub.add_parser("gop")
    g.add_argument("--du-lieu", required=True)
    g.add_argument("--ra", required=True)
    g.add_argument("--nguoi-viet", default=None)
    g.add_argument("--ghi-de", action="store_true")
    c = sub.add_parser("checklist")
    c.add_argument("--du-lieu", required=True)
    c.add_argument("--ra", required=True)
    c.add_argument("--ghi-de", action="store_true")
    t = sub.add_parser("test-case")
    t.add_argument("--du-lieu", required=True)
    t.add_argument("--checklist", required=True)
    t.add_argument("--ra", required=True)
    t.add_argument("--nguoi-viet", default=None)
    t.add_argument("--ghi-de", action="store_true")
    a = ap.parse_args()
    if getattr(a, "nguoi_viet", "x") is None:
        # Tên người test của máy này: `.nguoi-test` ở gốc repo (không ghi cứng tên ai).
        sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts"))
        from test_automation.config import default_author
        a.nguoi_viet = default_author()
    {"gop": lenh_gop, "checklist": lenh_checklist, "test-case": lenh_test_case}[a.lenh](a)


if __name__ == "__main__":
    main()
