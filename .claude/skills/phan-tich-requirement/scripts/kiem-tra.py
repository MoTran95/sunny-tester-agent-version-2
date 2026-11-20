#!/usr/bin/env python3
"""Soát đầu ra của skill phan-tich-requirement (bảng soát + file câu hỏi cho BA).

Cách chạy:
    python -X utf8 kiem-tra.py --nguon <requirement.md> --bang-soat <bang-soat.md> \
        [--cau-hoi <cau-hoi-cho-ba.md>] [--ma "<regex mã>"] [--tu-cam "tiến hành,nhằm"]

    Tìm nhanh các dòng cần sửa khi ghi câu trả lời (không cần đọc cả bảng):
    python -X utf8 kiem-tra.py --nguon <requirement.md> --bang-soat <bang-soat.md> --tim A4,TL-04

Kiểm:
  1. Mọi bảng Markdown: mỗi dòng có đúng số cột của dòng tiêu đề (bắt lỗi escape `|` sai).
  2. Cột cuối có tiêu đề chứa "Trích": mọi đoạn trong “…” phải có trong requirement, nguyên văn.
  3. --ma: mọi mã tìm thấy trong requirement phải có mặt trong bảng soát.
  4. File câu hỏi: mỗi khối `## A1.` có đủ trường (Hỏi, Mình đang hiểu; phần C: Cần xem/Cần làm, Mình đang hiểu).
  5. Bảng soát khớp file câu hỏi: bảng soát chỉ ghi `**A1. <tiêu đề>** (<nhóm>)`, cộng câu BA đã trả lời
     (`**BA trả lời:** … (TL-xx)`) nếu có; tiêu đề phải đúng chữ như ở file câu hỏi, nhóm phải đúng phần
     (A/B/C). Bảng soát chép lại nội dung câu hỏi (Hỏi, Mình đang hiểu, Cần xem, Nếu không tìm ra…) là lỗi:
     nội dung đó chỉ nằm ở file câu hỏi. Câu BA trả lời thiếu mã TL: lỗi. Câu hỏi không có dòng nào trong
     bảng soát: cảnh báo.
  6. Mã TL-xx nhắc trong bảng soát phải có dòng ở bảng "Câu trả lời đã nhận".
  7. Cảnh báo: từ dịch máy, mã nội bộ (CH-xx, KN-xx, Mxx, Rxx) lọt vào nội dung câu hỏi.
Thoát mã 1 nếu có lỗi; cảnh báo không làm thất bại.
"""
import argparse
import io
import os
import re
import sys

BT = chr(96)
SPLIT = re.compile(r"(?<!\\)\|")
SEP = re.compile(r"^\|\s*:?-{2,}")
DEFAULT_TU_CAM = ["tiến hành", "nhằm", "đối với", "dựa trên", "thực hiện việc", "kết quả mong đợi"]
INTERNAL_CODE = re.compile(r"\b(?:CH|KN)-\d\d\b|\bM\d\d\b|\bR\d\d\b")
NHOM = {"A": "🚨 Hỏi BA ngay", "B": "📋 Hỏi BA sau (gom lại)", "C": "🔍 Tự kiểm tra trên hệ thống trước"}
TITLE_IN_CELL = re.compile(r"\*\*([ABC]\d+)\. (.+?)\*\* \(([^)]*\)?)\)")
OLD_FIELDS = re.compile(r"\*\*(Hỏi|Mình đang hiểu|Cần xem|Cần làm|Nếu [^:*]*?hỏi BA):\*\*")
BA_ANSWER = re.compile(r"\*\*BA trả lời[^*]*:\*\*(.*?)(?:<br>|$)")


def read(path):
    return io.open(path, encoding="utf-8").read()


def cells(line):
    parts = SPLIT.split(line.strip())
    return [c.strip().replace("\\|", "|") for c in parts[1:-1]]


def tables(text):
    lines = text.split("\n")
    out = []
    i = 0
    while i < len(lines):
        if lines[i].startswith("|") and i + 1 < len(lines) and SEP.match(lines[i + 1]):
            header = cells(lines[i])
            rows = []
            j = i + 2
            while j < len(lines) and lines[j].startswith("|"):
                rows.append((j + 1, cells(lines[j])))
                j += 1
            out.append((i + 1, header, rows))
            i = j
        else:
            i += 1
    return out


def clean(t):
    t = t.strip()
    t = re.sub(r"\n\s*\n- ", "; ", t)
    t = re.sub(r"\n- ", "; ", t)
    t = re.sub(r"\s*\n\s*", " ", t)
    return t


def parse_questions(text):
    """Trả về {id: {title, van, hieu, xem, hoi, raw}}."""
    out = {}
    for blk in re.split(r"\n(?=## [ABC]\d+\. )", text):
        m = re.match(r"## ([ABC]\d+)\. (.+)", blk)
        if not m:
            continue
        nid, title = m.group(1), m.group(2).strip()
        d = {"title": title, "raw": blk}
        if nid[0] in "AB":
            mm = re.search(r"\*\*Hỏi:\*\* (.*?)(?:\n\n|\Z)", blk, re.S)
            d["van"] = clean(mm.group(1)) if mm else ""
            mm = re.search(r"\*\*Mình đang hiểu:\*\*\s*(.*?)(?=\n\n\*\*|\n\n\*Mã cũ|\Z)", blk, re.S)
            d["hieu"] = clean(mm.group(1)) if mm else ""
        else:
            for key, lab in [("xem", "Cần xem|Cần làm"), ("hieu", "Mình đang hiểu"),
                             ("hoi", "Nếu [^:*]*?hỏi BA")]:
                mm = re.search(r"- \*\*(?:%s):\*\* (.*)" % lab, blk)
                d[key] = clean(mm.group(1)) if mm else ""
        out[nid] = d
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nguon", required=True)
    ap.add_argument("--bang-soat", required=True)
    ap.add_argument("--cau-hoi")
    ap.add_argument("--ma", help="regex của mã requirement cần phủ, ví dụ CART-S\\d\\d-AC\\d\\d")
    ap.add_argument("--tu-cam", help="danh sách từ cảnh báo, cách nhau dấu phẩy (mặc định: từ dịch máy hay gặp)")
    ap.add_argument("--tim", help="chỉ liệt kê các dòng bảng soát nhắc tới những mã này (ví dụ A4,TL-04,CART-R06), rồi thoát")
    a = ap.parse_args()

    errors, warns = [], []
    src = read(a.nguon)
    bs = read(a.bang_soat)
    ch_text = read(a.cau_hoi) if a.cau_hoi else None

    if a.tim:
        keys = [k.strip() for k in a.tim.split(",") if k.strip()]
        for line_no, header, rows in tables(bs):
            for ln, row in rows:
                line = " | ".join(row)
                hit = [k for k in keys if re.search(r"(?<![\w-])" + re.escape(k) + r"(?![\w])", line)]
                if hit:
                    status = row[3] if len(row) > 3 else ""
                    print(f"dòng {ln}: {row[0] if row else ''} | {status[:60]} | khớp: {', '.join(hit)}")
        return 0

    # 1. bảng
    for name, txt in [("bảng soát", bs)] + ([("câu hỏi", ch_text)] if ch_text else []):
        n_tab = 0
        for line_no, header, rows in tables(txt):
            n_tab += 1
            for ln, row in rows:
                if len(row) != len(header):
                    errors.append(f"[{name}] dòng {ln}: {len(row)} cột, tiêu đề có {len(header)} (kiểm dấu | trong ô)")
        print(f"- {name}: {n_tab} bảng")

    # 2. trích dẫn
    n_quote = 0
    for line_no, header, rows in tables(bs):
        if not header or "Trích" not in header[-1]:
            continue
        for ln, row in rows:
            cell = row[-1] if row else ""
            quotes = re.findall(r"“(.+?)”", cell)
            if not quotes and cell not in ("", "—"):
                warns.append(f"[bảng soát] dòng {ln}: cột trích không có đoạn nào trong “…”")
            for q in quotes:
                n_quote += 1
                if q not in src:
                    errors.append(f"[bảng soát] dòng {ln}: trích không khớp nguyên văn: “{q[:80]}…”")
    print(f"- trích dẫn đã so: {n_quote}")

    # 3. phủ mã
    if a.ma:
        codes = sorted(set(re.findall(a.ma, src)))
        missing = [c for c in codes if c not in bs]
        print(f"- mã trong requirement: {len(codes)}, thiếu trong bảng soát: {len(missing)}")
        for c in missing:
            errors.append(f"[phủ mã] chưa có trong bảng soát: {c}")

    # 4, 5, 6. câu hỏi
    if ch_text:
        qs = parse_questions(ch_text)
        groups = {"A": 0, "B": 0, "C": 0}
        for nid, d in qs.items():
            groups[nid[0]] += 1
            if nid[0] in "AB":
                if not d["van"]:
                    errors.append(f"[câu hỏi {nid}] thiếu trường **Hỏi:**")
                if not d["hieu"]:
                    errors.append(f"[câu hỏi {nid}] thiếu trường **Mình đang hiểu:**")
            else:
                if not d["xem"]:
                    errors.append(f"[câu hỏi {nid}] thiếu **Cần xem:** (hoặc **Cần làm:**)")
                if not d["hieu"]:
                    warns.append(f"[câu hỏi {nid}] chưa có **Mình đang hiểu:** (chấp nhận được nếu đây là việc mình tự làm, không cần đoán)")
        print(f"- câu hỏi: A {groups['A']}, B {groups['B']}, C {groups['C']}")

        # 5. khớp bảng soát: chỉ tiêu đề + nhóm, không chép nội dung câu hỏi
        seen = set()
        for line_no, header, rows in tables(bs):
            for ln, row in rows:
                for cell in row:
                    if not re.match(r"\*\*[ABC]\d+\. ", cell):
                        continue
                    if OLD_FIELDS.search(cell):
                        errors.append(f"[bảng soát] dòng {ln}: chép lại nội dung câu hỏi ('{OLD_FIELDS.search(cell).group(1)}'); "
                                      "chỉ ghi **<số câu>. <tiêu đề>** (<nhóm>), nội dung để ở file câu hỏi")
                    for mm in BA_ANSWER.finditer(cell):
                        if not re.search(r"TL-\d\d", mm.group(0)):
                            errors.append(f"[bảng soát] dòng {ln}: câu BA trả lời thiếu mã TL-xx để tra về mục 'Câu trả lời đã nhận'")
                    for m in TITLE_IN_CELL.finditer(cell):
                        nid, title, nhom = m.group(1), m.group(2).strip(), m.group(3)
                        seen.add(nid)
                        if nid not in qs:
                            errors.append(f"[bảng soát] dòng {ln}: câu {nid} không có trong file câu hỏi")
                            continue
                        if title != qs[nid]["title"]:
                            errors.append(f"[bảng soát] dòng {ln}: tiêu đề câu {nid} lệch file câu hỏi: “{title[:60]}”")
                        if nhom != NHOM[nid[0]]:
                            errors.append(f"[bảng soát] dòng {ln}: câu {nid} ghi nhóm '{nhom}', đúng ra là '{NHOM[nid[0]]}'")
        print(f"- câu hỏi có mặt trong bảng soát: {len(seen)}/{len(qs)}")
        for nid in sorted(set(qs) - seen, key=lambda x: (x[0], int(x[1:]))):
            warns.append(f"[bảng soát] câu {nid} không có dòng nào nhắc tới (bỏ qua nếu câu đã bỏ hoặc là câu chung)")

    # 6. mã TL
    defined = set()
    for line_no, header, rows in tables(bs):
        if header and header[0] == "Mã":
            for ln, row in rows:
                if row and re.fullmatch(r"TL-\d\d", row[0]):
                    defined.add(row[0])
    used = set(re.findall(r"TL-\d\d", bs))
    for t in sorted(used - defined):
        errors.append(f"[bảng soát] nhắc {t} nhưng bảng 'Câu trả lời đã nhận' không có dòng {t}")
    print(f"- câu trả lời TL đã ghi: {len(defined)}")

    # 8. một mã nằm trên nhiều dòng: dòng thứ hai trở đi không được chép lại ô Tình huống (cột 2) hay ô trích (cột cuối)
    n_dup = 0
    for line_no, header, rows in tables(bs):
        first = {}
        for ln, row in rows:
            if len(row) < 3 or not re.match(r"^%s[^%s]+%s$" % (BT, BT, BT), row[0]):
                continue
            cur = (row[1], row[-1])
            if row[0] not in first:
                first[row[0]] = [(ln, cur)]
                continue
            for pl, prev in first[row[0]]:
                if row[1] and row[1] == prev[0]:
                    errors.append(f"[bảng soát] dòng {ln}: {row[0]} chép lại ô Tình huống của dòng {pl}; "
                                  "dòng thứ hai trở đi ghi ngắn, ví dụ '**Phần còn chưa rõ** của dòng trên'")
                    n_dup += 1
                    break
            for pl, prev in first[row[0]]:
                if row[-1] not in ("", "—") and row[-1] == prev[1]:
                    errors.append(f"[bảng soát] dòng {ln}: {row[0]} chép lại ô trích của dòng {pl}; ghi '—' ở dòng thứ hai trở đi")
                    n_dup += 1
                    break
            first[row[0]].append((ln, cur))
    print(f"- ô chép lại giữa các dòng cùng mã: {n_dup}")

    if ch_text:

        # 6. cảnh báo giọng văn
        tu_cam = [t.strip() for t in a.tu_cam.split(",")] if a.tu_cam else DEFAULT_TU_CAM
        for nid, d in qs.items():
            body = " ".join(str(d.get(k, "")) for k in ("van", "hieu", "xem", "hoi"))
            raw_body = re.sub(r"\*Mã cũ:.*?\*", "", d["raw"])
            for t in tu_cam:
                if t and t in raw_body:
                    warns.append(f"[câu hỏi {nid}] có từ nghe dịch máy: '{t}'")
            if INTERNAL_CODE.search(body):
                warns.append(f"[câu hỏi {nid}] có mã nội bộ trong nội dung câu hỏi: {INTERNAL_CODE.search(body).group(0)}")

    # 7. số ở mục Tổng kết khớp bảng soát (cùng cách đếm với ghi-tl.py; chỉ xét các nhãn khuôn có số đếm được)
    import importlib.util
    spec = importlib.util.spec_from_file_location("ghi_tl", os.path.join(os.path.dirname(os.path.abspath(__file__)), "ghi-tl.py"))
    gtl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gtl)
    bs_lines = bs.replace("\r\n", "\n").split("\n")
    want = gtl.dem_tong_ket(bs_lines)
    n_tk = 0
    for cell, (i, val) in gtl.so_trong_tong_ket(bs_lines).items():
        for label, n in want:
            if gtl._khop_nhan(cell, label):
                n_tk += 1
                have = int(re.match(r"^\d+", val).group(0))
                if have != n:
                    errors.append(f"[bảng soát] dòng {i + 1}: Tổng kết '{cell}' ghi {have}, đếm từ bảng ra {n} "
                                  f"(sửa bằng ghi-tl.py --chi-tong-ket)")
    print(f"- số ở Tổng kết đã đối chiếu: {n_tk}")

    print()
    for w in warns:
        print("CẢNH BÁO:", w)
    for e in errors:
        print("LỖI:", e)
    print(f"\nKết quả: {len(errors)} lỗi, {len(warns)} cảnh báo")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
