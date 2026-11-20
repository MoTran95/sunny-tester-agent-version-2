#!/usr/bin/env python3
"""Ghi câu trả lời của BA (TL-xx) vào bảng soát + file câu hỏi bằng script, không viết code mới mỗi lần.

Làm phần MÁY MÓC của bước "Khi có câu trả lời"; phần cần hiểu nghĩa (đổi ❓ thành ✅ ở từng dòng, ghi
"khác hệ thống hiện tại") vẫn do người/AI sửa bằng Edit, script chỉ chỉ ra dòng cần sửa.

    python -X utf8 ghi-tl.py --bang-soat <bang-soat.md> --cau-hoi <cau-hoi.md> --nguon <requirement.md> --du-lieu tl.json [--thu]
    python -X utf8 ghi-tl.py --bang-soat <bang-soat.md> --chi-tong-ket [--thu]

`tl.json` (tiếng Việt thường, không dán cả bảng):
    {
      "ngay": "2026-11-19",                       # mặc định: hôm nay
      "lich_su": "Ghi TL-14 (B4)",                # thêm 1 dòng vào mục Lịch sử và sửa ô "Cập nhật gần nhất"; bỏ qua nếu không ghi
      "tl": [{
        "id": "TL-14",                            # bỏ trống thì lấy số kế tiếp
        "noi_dung": "Nguyên văn câu BA trả lời (kèm 'mình hiểu …' nếu có)",
        "nguon": "BA trả lời, người dùng chuyển lại trong chat",   # mặc định như vậy; script thêm ngày + "Chưa có link ticket…"
        "ap_dung": ["B4", "CART-S02-AC08"],      # câu hỏi (A1, B4…) và mã requirement
        "con_lai": "Khác hệ thống hiện tại: …",   # ô "Còn lại"; bỏ trống thì ghi —
        "tra_loi": {"B4": "câu trả lời nguyên văn"},          # chèn "**BA trả lời:** … (TL-14)" ở các dòng có câu B4 và điền vào file câu hỏi
        "so_voi_he_thong": {"B4": "khác. Hệ thống đang …"}    # (tùy chọn) dòng "So với hệ thống hiện tại" ở file câu hỏi
      }]
    }

Script làm: (1) thêm dòng TL vào mục "Câu trả lời đã nhận" kèm điểm nhảy `<a id="tl-xx">`; (2) chèn câu trả lời
vào cột "Câu hỏi gửi BA" của mọi dòng có câu đó (mục 5, 6); (3) thêm TL vào dòng "Đã có trả lời:" của danh sách
câu hỏi; (4) điền "Câu trả lời của BA" trong file câu hỏi; (5) tính lại các số ở mục Tổng kết đã kiểm được
(chỉ ✅, cả ✅ và ❓, chỉ ❓, tổng, theo TL, khác hệ thống); (6) thêm dòng lịch sử; (7) chạy kiem-tra.py; (8) in
các dòng bảng soát còn cần sửa tay. Chạy lại cùng dữ liệu thì bỏ qua phần đã ghi. `--thu`: không ghi file.
"""
import argparse
import datetime
import io
import json
import os
import re
import subprocess
import sys

SPLIT = re.compile(r"(?<!\\)\|")
SEPLINE = re.compile(r"^\|[\s\-:|]+\|$")
HERE = os.path.dirname(os.path.abspath(__file__))


EOL = {}  # đường dẫn -> kiểu xuống dòng của file gốc (giữ nguyên để git không báo cả file đổi)


def read(p):
    t = io.open(p, encoding="utf-8", newline="").read()
    EOL[p] = "\r\n" if "\r\n" in t else "\n"
    return t.replace("\r\n", "\n")


def write(p, t):
    io.open(p, "w", encoding="utf-8", newline="").write(t.replace("\n", EOL.get(p, "\n")))


def cells(line):
    return [c.strip() for c in SPLIT.split(line.strip())[1:-1]]


def esc(s):
    return " ".join(str(s).split()).replace("|", "\\|")


def set_cell(line, idx, new):
    parts = SPLIT.split(line.rstrip("\n"))
    parts[idx + 1] = " " + new + " "
    return "|".join(parts)


def sections(lines):
    """Cho từng dòng: tiêu đề mục '## n.' đang đứng (chuỗi 3 ký tự đầu sau '## ')."""
    cur, out = "", []
    for l in lines:
        if l.startswith("## "):
            cur = l[3:6]
        out.append(cur)
    return out


def header_for(lines, i):
    j = i
    while j > 0 and not SEPLINE.match(lines[j].strip()):
        j -= 1
    return cells(lines[j - 1]) if j > 0 and SEPLINE.match(lines[j].strip()) else []


# Mã requirement ở ô đầu: có hoặc không có dấu `, có thể có thẻ neo <a id> phía trước (khuôn cho phép cả hai).
UNIT_CODE = re.compile(r'^(?:<a id="[^"]*"></a>\s*)?`?[A-Z][A-Z0-9]*-(S\d\d-AC\d\d|R\d\d|M\d\d)`?$')


def dem_tong_ket(lines, sec=None):
    """Đếm các số của mục Tổng kết từ bảng soát (mục 5, 6). Trả [(nhãn, số)], rỗng nếu không thấy đơn vị có mã nào.
    Dùng chung cho ghi-tl.py (sửa số) và kiem-tra.py (báo lệch)."""
    sec = sec or sections(lines)
    units, hdr = {}, None
    for i, l in enumerate(lines):
        if sec[i] not in ("5. ", "6. ") or not l.startswith("|") or SEPLINE.match(l.strip()):
            continue
        if i + 1 < len(lines) and SEPLINE.match(lines[i + 1].strip()):
            hdr = cells(l)
            continue
        c = cells(l)
        m = UNIT_CODE.match(c[0])
        if m and hdr and "Trạng thái" in hdr and len(c) == len(hdr):
            units.setdefault(m.group(1), []).append(c[hdr.index("Trạng thái")])
    ok = sum(1 for s in units.values() if any(x.startswith("✅") for x in s) and not any(x.startswith("❓") for x in s))
    both = sum(1 for s in units.values() if any(x.startswith("✅") for x in s) and any(x.startswith("❓") for x in s))
    only_q = sum(1 for s in units.values() if not any(x.startswith("✅") for x in s))
    tl = sum(1 for s in units.values() if any("theo TL" in x for x in s))
    khac = sum(1 for s in units.values() if any(("⚠️" in x or "khác TL" in x or "khác hệ thống" in x) for x in s))
    if not units:
        return []
    # Khuôn cũ đếm riêng AC (nhãn "AC chỉ có phần ✅", "Tổng AC"…): đếm trên các mã S..-AC.. để đối chiếu được cả bảng cũ
    ac = {k: v for k, v in units.items() if "-AC" in k}
    ok_ac = sum(1 for s in ac.values() if any(x.startswith("✅") for x in s) and not any(x.startswith("❓") for x in s))
    both_ac = sum(1 for s in ac.values() if any(x.startswith("✅") for x in s) and any(x.startswith("❓") for x in s))
    only_q_ac = sum(1 for s in ac.values() if not any(x.startswith("✅") for x in s))
    return [("Đơn vị chỉ có phần ✅", ok), ("Đơn vị có cả ✅ và ❓", both), ("Đơn vị chỉ có ❓", only_q),
            ("Tổng", len(units)), ("Đơn vị có dòng ✅ nhờ câu trả lời", tl), ("Trong đó có dòng khác hệ thống hiện tại", khac),
            ("AC chỉ có phần ✅", ok_ac), ("AC có cả ✅ và ❓", both_ac), ("AC chỉ có ❓", only_q_ac), ("Tổng AC", len(ac))]


def so_trong_tong_ket(lines, sec=None):
    """{nhãn trong want: (số dòng, ô số)} các dòng mục 4 khớp nhãn (nhãn 'Tổng' khớp cả 'Tổng (đơn vị có mã)')."""
    sec = sec or sections(lines)
    found = {}
    for i, l in enumerate(lines):
        if sec[i] != "4. " or not l.startswith("|"):
            continue
        c = cells(l)
        if len(c) > 1 and re.match(r"^\d+", c[1]):
            found[c[0]] = (i, c[1])
    return found


def _khop_nhan(cell, label):
    if label == "Tổng":
        return cell == "Tổng" or cell.startswith("Tổng (")
    return cell == label or cell.startswith(label + " ") or cell.startswith(label + "(")


def tong_ket(lines, sec, notes):
    """Tính lại các số đã kiểm được và sửa số đầu ô ở mục Tổng kết."""
    want = dem_tong_ket(lines, sec)
    if not want:
        notes.append("Tổng kết: không thấy dòng nào có mã requirement ở bảng soát (mục 5, 6) nên KHÔNG sửa số nào; kiểm khuôn bảng")
        return
    n_doi = 0
    for i, l in enumerate(lines):
        if sec[i] != "4. " or not l.startswith("|"):
            continue
        c = cells(l)
        for label, val in want:
            if c and _khop_nhan(c[0], label) and len(c) > 1 and re.match(r"^\d+", c[1]):
                if int(re.match(r"^\d+", c[1]).group(0)) != val:
                    lines[i] = set_cell(l, 1, re.sub(r"^\d+", str(val), c[1], count=1))
                    n_doi += 1
                    notes.append(f"Tổng kết: '{label}' đổi {c[1][:12]} → {val}")
    v = dict(want)
    notes.append(f"Tổng kết đã tính lại: chỉ ✅ {v['Đơn vị chỉ có phần ✅']}, cả hai {v['Đơn vị có cả ✅ và ❓']}, chỉ ❓ {v['Đơn vị chỉ có ❓']}, "
                 f"tổng {v['Tổng']}, theo TL {v['Đơn vị có dòng ✅ nhờ câu trả lời']}, khác {v['Trong đó có dòng khác hệ thống hiện tại']}"
                 + (" (không số nào đổi)" if not n_doi else ""))
    notes.append("Hai số 'dòng suy ra' và 'mục không mã ở phụ lục' không tính tự động: đếm tay nếu có đổi.")


def tao_bang_tl(lines, notes):
    """Bảng soát chưa có câu trả lời nào: bỏ dòng "Chưa có câu trả lời nào.", bảo đảm mục 3 có tiêu đề bảng.
    Trả số dòng mà dòng TL mới sẽ chèn NGAY SAU (dòng gạch phân cách của bảng)."""
    sec = sections(lines)
    idx = [i for i, l in enumerate(lines) if sec[i] == "3. "]
    if not idx:
        sys.exit("Không thấy mục '## 3. Câu trả lời đã nhận' trong bảng soát (khuôn assets/mau-bang-soat.md)")
    for i in reversed(idx):
        if "Chưa có câu trả lời nào" in lines[i]:
            del lines[i]
    sec = sections(lines)
    idx = [i for i, l in enumerate(lines) if sec[i] == "3. "]
    for i in idx:
        if lines[i].startswith("| Mã |") and i + 1 < len(lines) and SEPLINE.match(lines[i + 1].strip()):
            return i + 1
    head = idx[0]  # dòng "## 3. ..."
    lines[head + 1:head + 1] = ["| Mã | Nội dung trả lời | Nguồn | Áp dụng cho | Còn lại |", "|---|---|---|---|---|"]
    notes.append("Mục 3: chưa có bảng câu trả lời, đã dựng bảng")
    return head + 2


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bang-soat", required=True)
    ap.add_argument("--cau-hoi")
    ap.add_argument("--nguon", help="requirement (để chạy kiem-tra.py)")
    ap.add_argument("--du-lieu")
    ap.add_argument("--chi-tong-ket", action="store_true")
    ap.add_argument("--thu", action="store_true", help="không ghi file, chỉ báo sẽ làm gì")
    ap.add_argument("--khong-kiem", action="store_true", help="không chạy kiem-tra.py")
    a = ap.parse_args()

    bs = read(a.bang_soat)
    lines = bs.split("\n")
    notes, warns = [], []
    ch_text = read(a.cau_hoi) if a.cau_hoi else None
    ch = ch_text.split("\n") if ch_text is not None else None
    touched = []  # (số dòng, ghi chú) các dòng bảng soát liên quan, để người sửa tay
    data = {}
    if not a.chi_tong_ket:
        if not a.du_lieu:
            sys.exit("Cần --du-lieu tl.json (hoặc --chi-tong-ket)")
        data = json.loads(read(a.du_lieu))
    today = data.get("ngay") or datetime.date.today().isoformat()
    sec = sections(lines)

    for tl in data.get("tl", []):
        for k in ("noi_dung", "ap_dung"):
            if not tl.get(k):
                sys.exit(f"Thiếu '{k}' trong một mục tl")
        # ---- 1. dòng TL ở mục 3 ----
        rows = [i for i, l in enumerate(lines) if re.match(r"^\| TL-\d\d \|", l)]
        if not rows:
            rows = [tao_bang_tl(lines, notes)]  # câu trả lời đầu tiên: dựng bảng mục 3 (chỉ có dòng tiêu đề)
            sec = sections(lines)
        have = {re.match(r"^\| (TL-\d\d) \|", lines[i]).group(1) for i in rows if re.match(r"^\| TL-\d\d \|", lines[i])}
        tid = tl.get("id") or "TL-%02d" % (max([int(x[3:]) for x in have] or [0]) + 1)
        if tid in have:
            notes.append(f"{tid} đã có ở mục 3: bỏ qua việc thêm dòng (không ghi đè)")
        else:
            qs = [x for x in tl["ap_dung"] if re.fullmatch(r"[ABC]\d+", x)]
            codes = [f"`{x}`" for x in tl["ap_dung"] if x not in qs]
            apd = ", ".join(qs) + ("; " if qs and codes else "") + ", ".join(codes)
            nguon = tl.get("nguon") or "BA trả lời, người dùng chuyển lại trong chat"
            row = (f"| {tid} | {esc(tl['noi_dung'])} | {esc(nguon)}, {today}. Chưa có link ticket hay kênh chung | {apd} | "
                   f"{esc(tl.get('con_lai') or '—')} <a id=\"{tid.lower()}\"></a> |")
            lines.insert(rows[-1] + 1, row)
            sec = sections(lines)
            notes.append(f"Mục 3: thêm dòng {tid}")
        # ---- 2. câu BA trả lời ở các dòng bảng soát ----
        for q, text in (tl.get("tra_loi") or {}).items():
            n_row = 0
            for i, l in enumerate(lines):
                if sec[i] not in ("5. ", "6. ") or not l.startswith("|") or f"**{q}." not in l:
                    continue
                hdr = header_for(lines, i)
                if "Câu hỏi gửi BA" not in hdr:
                    continue
                c = cells(l)
                idx = hdr.index("Câu hỏi gửi BA")
                segs = c[idx].split("<br>")
                s0 = next((k for k, s in enumerate(segs) if s.startswith(f"**{q}.")), None)
                if s0 is None:
                    continue
                e = s0 + 1
                while e < len(segs) and segs[e].startswith("**BA trả lời"):
                    e += 1
                n_row += 1
                if any(f"({tid})" in s for s in segs[s0 + 1:e]):
                    continue
                segs.insert(e, f"**BA trả lời:** {esc(text)} ({tid})")
                lines[i] = set_cell(l, idx, "<br>".join(segs))
            notes.append(f"Câu {q}: chèn câu trả lời vào {n_row} dòng bảng soát" + ("" if n_row else "  ⚠️ không thấy dòng nào có câu này"))
            if not n_row:
                warns.append(f"Không thấy câu {q} ở cột 'Câu hỏi gửi BA' (kiểm lại mã câu hỏi)")
            # ---- 3. danh sách câu hỏi (mục 7) ----
            for i, l in enumerate(lines):
                if re.match(r"^- \*\*" + re.escape(q) + r"\. ", l) and tid not in l:
                    lines[i] = (l.rstrip() + f", {tid}") if "Đã có trả lời:" in l else (l.rstrip() + f" Đã có trả lời: {tid}")
            # ---- 4. file câu hỏi ----
            if ch is not None:
                st = next((k for k, l in enumerate(ch) if re.match(r"^## " + re.escape(q) + r"\. ", l)), None)
                if st is None:
                    warns.append(f"File câu hỏi không có '## {q}.'")
                else:
                    en = next((k for k in range(st + 1, len(ch)) if ch[k].startswith("## ")), len(ch))
                    k = next((k for k in range(st, en) if ch[k].startswith("**Câu trả lời của BA:**")), None)
                    line_new = f"**Câu trả lời của BA:** {' '.join(str(text).split())} ({tid}, {today})"
                    if k is None:
                        warns.append(f"Câu {q} ở file câu hỏi chưa có dòng '**Câu trả lời của BA:**': thêm tay")
                    elif tid in ch[k]:
                        pass
                    elif "______" in ch[k]:
                        ch[k] = line_new
                        notes.append(f"File câu hỏi: điền câu trả lời cho {q}")
                    else:
                        ch.insert(k + 1, "")
                        ch.insert(k + 2, line_new.replace("Câu trả lời của BA:", "Câu trả lời của BA (bổ sung):", 1))
                        notes.append(f"File câu hỏi: thêm câu trả lời bổ sung cho {q}")
                    sv = (tl.get("so_voi_he_thong") or {}).get(q)
                    if sv and k is not None and not any(ch[x].startswith("**So với hệ thống hiện tại:**") for x in range(st, en)):
                        kk = next((x for x in range(k, min(k + 4, len(ch))) if tid in ch[x] and ch[x].startswith("**Câu trả lời")), k)
                        ch.insert(kk + 1, "")
                        ch.insert(kk + 2, f"**So với hệ thống hiện tại:** {' '.join(str(sv).split())}")
        # ---- dòng cần sửa tay ----
        keys = [x for x in tl["ap_dung"]]
        for i, l in enumerate(lines):
            if sec[i] in ("5. ", "6. ") and l.startswith("|") and not SEPLINE.match(l.strip()):
                if any(re.search(r"(?<![\w-])" + re.escape(k) + r"(?![\w])", l) for k in keys if re.fullmatch(r"[ABC]\d+", k)) or \
                        any(re.match(r"^\| `" + re.escape(k) + r"` \|", l) for k in keys if not re.fullmatch(r"[ABC]\d+", k)):
                    c = cells(l)
                    hdr = header_for(lines, i)
                    stt = c[hdr.index("Trạng thái")] if "Trạng thái" in hdr and len(c) == len(hdr) else "?"
                    touched.append((i + 1, c[0][:32], stt[:46]))

    # ---- 5. tổng kết ----
    sec = sections(lines)
    tong_ket(lines, sec, notes)
    # ---- 6. lịch sử ----
    if data.get("lich_su"):
        hit = next((i for i, l in enumerate(lines) if l.startswith("## ") and "Lịch sử" in l), None)
        if hit is not None:
            last = max((i for i in range(hit, len(lines)) if lines[i].startswith("| ")), default=None)
            if last is not None and not any(data["lich_su"] in lines[i] for i in range(hit, len(lines))):
                lines.insert(last + 1, f"| {today} | {esc(data['lich_su'])} |")
                notes.append("Mục Lịch sử: thêm 1 dòng")
        for i, l in enumerate(lines[:20]):
            if l.startswith("| Cập nhật gần nhất |") and esc(data["lich_su"]) not in l:
                old = cells(l)[1]  # giữ nội dung cũ, không làm mất lịch sử đã ghi tay
                lines[i] = f"| Cập nhật gần nhất | {today} ({esc(data['lich_su'])}). Trước đó: {old} |"

    # ---- ghi và kiểm ----
    new_bs = "\n".join(lines)
    if a.thu:
        print("[--thu] không ghi file.")
    else:
        if new_bs != bs:
            write(a.bang_soat, new_bs)
        if ch is not None and "\n".join(ch) != ch_text:
            write(a.cau_hoi, "\n".join(ch))
    for n in notes:
        print(" •", n)
    for w in warns:
        print(" ⚠️", w)
    rc = 0
    if not a.khong_kiem and not a.thu and a.nguon:
        cmd = [sys.executable, "-X", "utf8", os.path.join(HERE, "kiem-tra.py"), "--nguon", a.nguon, "--bang-soat", a.bang_soat]
        if a.cau_hoi:
            cmd += ["--cau-hoi", a.cau_hoi]
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        tail = [x for x in r.stdout.strip().splitlines() if x.strip()][-6:]
        print("kiem-tra.py:", "đạt" if r.returncode == 0 else "CÓ LỖI")
        for x in tail:
            print("   ", x)
        rc = r.returncode
    if touched:
        print("Dòng bảng soát liên quan, cần xem có phải đổi ❓ → ✅ / ghi 'khác hệ thống hiện tại' (sửa bằng Edit):")
        for n, c0, stt in touched:
            print(f"   dòng {n}: {c0} — {stt}")
    return rc or (1 if warns else 0)


if __name__ == "__main__":
    sys.exit(main())
