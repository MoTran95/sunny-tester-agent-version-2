#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Truy vết requirement <-> checklist/test case của một tính năng.

Dùng:
  python -X utf8 scripts/truy-vet.py kiem <dự-án> <tính-năng>
      So requirement hiện tại với mốc đã chốt lần trước, báo mã nào đổi và test case nào
      cần xem lại, ghi lại truy-vet.md và khối "Lịch sử thay đổi" trong checklist/test case.
      Không đổi mốc. Thoát mã 1 nếu có việc cần làm.
  python -X utf8 scripts/truy-vet.py chot <dự-án> <tính-năng> -m "đã làm gì" [--doi checklist,test-case,requirement] [--ngay-ba YYYY-MM-DD]
      Chốt mốc mới: "test case hiện tại đã khớp requirement hiện tại". Ghi một dòng lịch sử.
  python -X utf8 scripts/truy-vet.py tra <dự-án> <tính-năng> --ma S02-AC07,R06,TL-11,TC-014 [--day-du]
      Chỉ ĐỌC, không ghi file. In gọn mọi thứ về vài mã: dòng SRS (theo tên cột), điều BA trả lời, hành vi
      hiện tại/chỗ còn mở, câu trả lời liên quan, test case và trạng thái truy vết. Dùng thay cho việc
      đọc cả SRS, bảng soát, test-case.md. Mã nhận cả có tiền tố (CART-R06) lẫn TC-14.

  python -X utf8 scripts/truy-vet.py khoi-tao <dự-án> <tính-năng> --tien-to <MÃ> --ten "<Tên tính năng>" [--srs <file SRS>]
      Tạo truy-vet-cau-hinh.json cho tính năng mới (đường dẫn mặc định: srs/<dự-án>/<tính-năng>.md,
      bảng soát và test-case.md trong testing/<dự-án>/<tính-năng>/) và ghi tên tính năng vào
      testing/<dự-án>/ten-tinh-nang.json (trang HTML, test plan hiện tên này). Không ghi đè cấu hình có sẵn.

Ví dụ: python -X utf8 scripts/truy-vet.py kiem <dự-án> <tính-năng>

Cần trong thư mục testing/<dự-án>/<tính-năng>/ file truy-vet-cau-hinh.json (đường dẫn, tiền tố mã,
tên ngắn của từng mã; tạo bằng lệnh khoi-tao). File trạng thái truy-vet-trang-thai.json do script tự tạo; không sửa tay.
Cách tính "mã đổi": băm nội dung dòng của mã trong SRS (bỏ cột bằng chứng/nhãn) và dòng TL trong
bảng soát (chỉ cột mã + nội dung trả lời). Đổi link, đổi ngày không làm mã bị tính là đổi.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CODE = r"(?:S\d\d-AC\d\d|R\d\d|M\d\d|TL-\d\d)"
TOKEN = re.compile(r"(?<![\w-])(" + CODE + r")(?!\w)")
START = "<!-- LICH-SU:BAT-DAU (tự sinh bởi scripts/truy-vet.py, không sửa tay) -->"
END = "<!-- LICH-SU:KET-THUC -->"


def git(*args):
    r = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True, encoding="utf-8")
    return r.stdout.strip()


def fmt_dt(iso, ngay=None):
    """2026-11-18 14:32:05 (+07:00); mốc cũ chỉ có ngày thì ghi "không rõ giờ", không bịa giờ."""
    if iso:
        return datetime.datetime.fromisoformat(iso).strftime("%Y-%m-%d %H:%M:%S") + f" ({iso[-6:]})"
    return f"{ngay} (không rõ giờ)"


def fmt_commit(e):
    c = e.get("commit_goc")
    if not c:
        return "—"
    return f"`{c}`" + (" + sửa chưa commit" if e.get("chua_commit") else "")


def cells(line):
    line = re.sub(r'<a id="[^"]*"></a>', "", line)  # thẻ neo để link tới dòng, không tính là nội dung
    return [c.strip() for c in line.strip().strip("|").split("|")]


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def h(parts):
    return hashlib.sha1("¦".join(norm(p) for p in parts).encode("utf-8")).hexdigest()[:12]


def cut(s, n=150):
    s = norm(s).replace("|", "¦")
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def read(p):
    return Path(p).read_text(encoding="utf-8")


def parse_srs(text, prefix):
    out = {}
    keep = {"S": 5, "R": 3, "M": 4}
    pat = re.compile(r'^\| (?:<a id="[^"]*"></a>)?`' + re.escape(prefix) + r"-(S\d\d-AC\d\d|R\d\d|M\d\d)` \|")
    for n, line in enumerate(text.splitlines(), 1):
        m = pat.match(line)
        if not m or m.group(1) in out:
            continue
        code = m.group(1)
        c = cells(line)
        k = keep[code[0]]
        nv = {"S": 4, "R": 2, "M": 2}[code[0]]
        out[code] = dict(hash=h(c[:k]), nghia=c[1] if len(c) > 1 else "", nguyen_van=c[nv] if len(c) > nv else "", dong=n)
    return out


def parse_tl(text):
    out = {}
    for n, line in enumerate(text.splitlines(), 1):
        m = re.match(r"^\| (TL-\d\d) \|", line)
        if not m or m.group(1) in out:
            continue
        c = cells(line)
        out[m.group(1)] = dict(hash=h(c[:2]), nghia="", nguyen_van=c[1] if len(c) > 1 else "", dong=n)
    return out


def parse_ba(text, prefix):
    """Gom, theo từng mã SRS, các dòng của bảng soát: điều BA trả lời, hệ thống hiện tại, chỗ còn mở."""
    out = {}
    pat = re.compile(r'^\| (?:<a id="[^"]*"></a>)?`' + re.escape(prefix) + r"-(S\d\d-AC\d\d|R\d\d|M\d\d)` \|")
    in5 = False
    for line in text.splitlines():
        if line.startswith("## "):
            in5 = line.startswith("## 5.") or line.startswith("## 6.")
        m = pat.match(line)
        if not in5 or not m:
            continue
        c = cells(line)
        if len(c) < 6:
            continue
        s, o = c[3], out.setdefault(m.group(1), dict(ba=[], hien_tai=[], chua_chot=[], khac=False))
        khac = "khác hệ thống" in s or "có thể khác" in s
        refs = sorted(set(re.findall(r"TL-\d\d", s)))
        if s.startswith("❓"):
            q = re.search(r"\*\*([ABC]\d+)\.", c[4])
            o["chua_chot"].append(q.group(1) if q else "?")
        elif "hành vi hiện tại" in s:
            o["hien_tai"].append(c[2])
        elif "Suy ra" in s or "theo TL" in s:
            o["ba"].append(dict(text=c[2], refs=refs, suy_ra="Suy ra" in s, stt=s))
            o["khac"] = o["khac"] or khac
    return out


EXEC_COLS = {"Kết quả thực tế", "Trạng thái", "Người viết", "Tự động hóa"}  # người chạy test điền; không tính là "thay đổi thiết kế"


def parse_tc(text):
    """Đọc bảng đầu tiên có tiêu đề bắt đầu bằng "| Mã |", theo TÊN cột (không theo vị trí).
    Ba cột ghi khi chạy (Kết quả thực tế, Trạng thái, Người viết) không vào dấu vết "row", để điền kết quả
    không làm test case bị tính là đã sửa."""
    out, names = {}, None
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
            sys.exit(f"{m.group(1)}: có {len(c)} ô, tiêu đề bảng có {len(names)} cột")
        d = dict(zip(names, c))
        if "Nguồn" not in d:
            sys.exit("Bảng không có cột Nguồn")
        design = [v for k, v in d.items() if k not in EXEC_COLS]
        out[m.group(1)] = dict(tinh_huong=d.get("Tình huống", ""), uu_tien=d.get("Ưu tiên", ""), nguon=d["Nguồn"], auto=d.get("Tự động hóa", ""),
                               ma=sorted(set(TOKEN.findall(d["Nguồn"]))), row=norm("|".join(design)), cot=d)
    return out


SEP = re.compile(r"^\|[\s\-:|]+\|$")


def row_dict(text, n):
    """Dòng số n (từ 1) của bảng Markdown -> {tên cột: nội dung}, tên cột lấy từ dòng tiêu đề của bảng đó."""
    lines = text.splitlines()
    i = n - 1
    j = i
    while j > 0 and not SEP.match(lines[j].strip()):
        j -= 1
    names = cells(lines[j - 1]) if j > 0 and SEP.match(lines[j].strip()) else []
    c = cells(lines[i])
    if len(names) != len(c):
        names = [f"cột {k + 1}" for k in range(len(c))]
    return dict(zip(names, c))


def show_cells(d, n, skip=("Mã", "ID")):
    for k, v in d.items():
        if k in skip or not v.strip() or v.strip() in ("—", "-"):
            continue
        v = re.sub(r"<a id=\"[^\"]*\"></a>", "", v).replace("<br>", " / ")
        print(f"    {k}: {norm(v) if n is None else cut(v, n)}")


def date_in(text, label):
    m = re.search(re.escape(label) + r"[^0-9]{0,10}(\d{4}-\d\d-\d\d)", text)
    return m.group(1) if m else "?"


def rel(frm_dir, target):
    return os.path.relpath(target, frm_dir).replace("\\", "/")


def tra(a, cfg, srs_t, bs_t, cur, ba, tcs, ma_st, tc_st, tc_of, problems):
    """In gọn mọi thứ liên quan tới vài mã (SRS, theo BA, test case, trạng thái) để khỏi đọc cả file."""
    n = None if a.day_du else 420
    pre = cfg["tien_to"] + "-"
    want = [x.strip() for x in a.ma.split(",") if x.strip()]
    if not want:
        sys.exit("Cần --ma, ví dụ: --ma S02-AC07,R06,TL-11,TC-014")
    tl_refs = lambda c: [k for k, v in cur.items() if k.startswith("TL") and re.search(re.escape(pre + c) + r"(?!\w)", v["nguyen_van"] + " " + row_dict(bs_t, v["dong"]).get("Áp dụng cho", ""))]
    for raw in want:
        c = raw.upper().removeprefix(pre.upper())
        mt = re.fullmatch(r"TC-?(\d+)", c)
        if mt:
            c = f"TC-{int(mt.group(1)):03d}"
        print(f"\n=== {c} ===")
        if c in tcs:
            t = tcs[c]
            print(f"  Test case — trạng thái truy vết: {tc_st.get(c)}")
            show_cells(t["cot"], n)
            for m in t["ma"]:
                if m in cur:
                    print(f"  → {m} ({cur[m]['ten']}): {ma_st.get(m)}")
            continue
        if c.startswith("TL-") and c in cur:
            print(f"  Câu trả lời của BA (bảng soát dòng {cur[c]['dong']}):")
            show_cells(row_dict(bs_t, cur[c]["dong"]), n)
            ap_ = [m for m in cur if not m.startswith("TL") and re.search(re.escape(pre + m) + r"(?!\w)", row_dict(bs_t, cur[c]["dong"]).get("Áp dụng cho", ""))]
        elif c in cur:
            print(f"  {cur[c]['ten']} — trạng thái requirement: {ma_st.get(c)} (SRS dòng {cur[c]['dong']})")
            show_cells(row_dict(srs_t, cur[c]["dong"]), n)
            o = ba.get(c)
            if o:
                for e in o["ba"]:
                    print(f"  Theo BA{' (suy ra)' if e['suy_ra'] else ''}: {cut(e['text'], n or 99999)} [{', '.join(e['refs']) or 'suy ra từ SRS'}]")
                for x in o["hien_tai"]:
                    print(f"  Hành vi hiện tại: {cut(x, n or 99999)}")
                if o["khac"]:
                    print("  ⚠️ Khác hệ thống hiện tại (nghi lỗi nếu BA xác nhận)")
                if o["chua_chot"]:
                    print(f"  Còn mở: {', '.join(sorted(set(o['chua_chot'])))}")
            qua_tl = set()
            for k in tl_refs(c):
                print(f"  Câu trả lời liên quan {k}: {cut(row_dict(bs_t, cur[k]['dong']).get('Nội dung trả lời', ''), n or 99999)}")
                qua_tl |= set(tc_of.get(k, []))
            ap_ = []
        else:
            print("  Không có mã này trong SRS, bảng soát hay test case.")
            continue
        ts = tc_of.get(c, []) if c in cur and not c.startswith("TL") else sorted({t for m in ap_ for t in tc_of.get(m, [])} | set(tc_of.get(c, [])))
        print(f"  Test case ({len(ts)}):" if ts else "  Test case: ⚠️ chưa có" if not c.startswith("TL") else "  Test case: —")
        for t in ts:
            print(f"    {t} [{tc_st.get(t)}] {cut(tcs[t]['tinh_huong'], 110)}")
        if c in cur and not c.startswith("TL") and qua_tl - set(ts):
            print("  Test case dùng câu trả lời liên quan (không ghi mã này): " + ", ".join(sorted(qua_tl - set(ts))))
    for p in problems:
        print("VẤN ĐỀ chung:", p)
    return 0


def _bo_gio(text):
    """Bỏ phần chỉ đổi theo giờ chạy (dòng 'Lần chạy gần nhất', '(chạy <giờ>)') để biết nội dung có đổi thật không."""
    text = re.sub(r"(?m)^\| Lần chạy gần nhất \|.*$", "", text)
    return re.sub(r"\(chạy [^)]*\)", "(chạy)", text)


def write_if_changed(path, text, read_only=False):
    """Chỉ ghi khi nội dung đổi thật (không tính giờ chạy) để không tạo thay đổi giả trong git; read_only thì không ghi."""
    old = read(path) if path.exists() else None
    if read_only or (old is not None and _bo_gio(old) == _bo_gio(text)):
        return False
    path.write_text(text, encoding="utf-8")
    return True


def khoi_tao(a, d, cfg_p):
    """Tạo cấu hình truy vết cho một tính năng; ghi tên tính năng vào ten-tinh-nang.json của dự án."""
    if not a.tien_to or not a.ten:
        sys.exit("khoi-tao cần --tien-to <MÃ> và --ten \"<Tên tính năng>\"")
    srs = a.srs or f"srs/{a.du_an}/{a.tinh_nang}.md"
    if not (ROOT / srs).exists():
        sys.exit(f"Chưa có SRS {srs}: viết SRS trước (skill srs-from-website) hoặc truyền --srs")
    if cfg_p.exists():
        print(f"Đã có {cfg_p.relative_to(ROOT)}: không ghi đè.")
    else:
        d.mkdir(parents=True, exist_ok=True)
        rel_d = f"testing/{a.du_an}/{a.tinh_nang}"
        cfg = {"ten_tinh_nang": a.ten, "tien_to": a.tien_to.upper(), "srs": srs,
               "bang_soat": f"{rel_d}/bang-soat-requirement.md", "test_case": f"{rel_d}/test-case.md", "ten_ngan": {}}
        cfg_p.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Đã tạo {cfg_p.relative_to(ROOT)} (tên ngắn từng mã để trống: script tự cắt từ SRS; muốn đẹp hơn thì điền 'ten_ngan').")
    names_p = ROOT / "testing" / a.du_an / "ten-tinh-nang.json"
    names = json.loads(read(names_p)) if names_p.exists() and read(names_p).strip() else {}
    if names.get(a.tinh_nang) != a.ten:
        names[a.tinh_nang] = a.ten
        names_p.write_text(json.dumps(names, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Đã ghi tên tính năng vào {names_p.relative_to(ROOT)}: {a.tinh_nang} = {a.ten}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("lenh", choices=["kiem", "chot", "tra", "khoi-tao"])
    ap.add_argument("du_an")
    ap.add_argument("tinh_nang")
    ap.add_argument("--ma", default="", help="với lệnh tra: các mã cần xem, cách nhau dấu phẩy (S02-AC07,R06,TL-11,TC-014)")
    ap.add_argument("--day-du", action="store_true", help="với lệnh tra: không rút gọn nội dung ô")
    ap.add_argument("-m", "--mo-ta", default="")
    ap.add_argument("--doi", default="checklist,test-case")
    ap.add_argument("--ngay", default=None, help="chỉ dùng khi thử: ép ngày, không ghi giờ")
    ap.add_argument("--ngay-ba", default=None, help="ngày BA trả lời (YYYY-MM-DD), nếu biết")
    ap.add_argument("--chi-doc", action="store_true", help="với lệnh kiem: không ghi file nào, chỉ in (dùng trong kiem-tra-bo-nho.py)")
    ap.add_argument("--tien-to", help="với lệnh khoi-tao: mã feature trong SRS, ví dụ CART")
    ap.add_argument("--ten", help="với lệnh khoi-tao: tên tính năng cho người đọc")
    ap.add_argument("--srs", help="với lệnh khoi-tao: đường dẫn SRS (mặc định srs/<dự-án>/<tính-năng>.md)")
    a = ap.parse_args()

    d = ROOT / "testing" / a.du_an / a.tinh_nang
    cfg_p = d / "truy-vet-cau-hinh.json"
    st_p = d / "truy-vet-trang-thai.json"
    if a.lenh == "khoi-tao":
        return khoi_tao(a, d, cfg_p)
    if not cfg_p.exists():
        sys.exit(f"Chưa có {cfg_p.relative_to(ROOT)}. Tạo bằng: python -X utf8 scripts/truy-vet.py khoi-tao "
                 f"{a.du_an} {a.tinh_nang} --tien-to <MÃ> --ten \"<Tên tính năng>\"")
    cfg = json.loads(read(cfg_p))
    srs_t, bs_t = read(ROOT / cfg["srs"]), read(ROOT / cfg["bang_soat"])
    # Cấu hình không có khóa "checklist" = file gộp (checklist nằm chung bảng test case, từ 2026-11-18)
    gop = not cfg.get("checklist")
    tc_t = read(ROOT / cfg["test_case"])
    ck_t = tc_t if gop else read(ROOT / cfg["checklist"])

    cur = parse_srs(srs_t, cfg["tien_to"])
    tls = parse_tl(bs_t)
    ba = parse_ba(bs_t, cfg["tien_to"])
    for k, v in cur.items():
        if not k.startswith("TL"):
            v["ba_hash"] = h([x for e in ba.get(k, {}).get("ba", []) for x in (e["text"], e["stt"])])
    cur.update(tls)
    for k, v in cur.items():
        v["ten"] = cfg.get("ten_ngan", {}).get(k) or cut(v["nghia"] or v["nguyen_van"], 40)
    ck = parse_tc(ck_t)
    tcs = parse_tc(tc_t)

    state = json.loads(read(st_p)) if st_p.exists() else {"ma": {}, "tc": {}, "lich_su": [], "nguon_chot": {}}
    dua_tren = dict(srs=date_in(srs_t, "Cập nhật lần cuối"), bang_soat=date_in(bs_t, "Cập nhật gần nhất"),
                    tl_cuoi=max(tls, default="?"))

    problems = []
    # Checklist và test case phải khớp nhau
    if not gop and set(ck) != set(tcs):
        problems.append(f"Checklist và test case lệch mã TC: chỉ ở checklist {sorted(set(ck)-set(tcs))}, chỉ ở test case {sorted(set(tcs)-set(ck))}")
    for k in ([] if gop else sorted(set(ck) & set(tcs))):
        if tcs[k]["uu_tien"] and ck[k]["uu_tien"] != tcs[k]["uu_tien"]:
            problems.append(f"{k}: ưu tiên ở checklist \"{ck[k]['uu_tien']}\" khác test case \"{tcs[k]['uu_tien']}\"")
        if ck[k]["ma"] != tcs[k]["ma"]:
            problems.append(f"{k}: mã nguồn ở checklist {ck[k]['ma']} khác test case {tcs[k]['ma']}")
    # Mã requirement trạng thái
    def st_ma(code):
        base = state["ma"].get(code)
        if code not in cur:
            return "Đã bỏ khỏi nguồn" if base else None
        if base is None:
            return "Mới"
        return "Đã đổi" if why(code) else "Không đổi"

    def why(code):
        base, v = state["ma"].get(code), cur.get(code)
        if not base or not v:
            return []
        r = []
        if base["hash"] != v["hash"]:
            r.append("nội dung SRS" if not code.startswith("TL") else "nội dung câu trả lời")
        if "ba_hash" in base and base["ba_hash"] != v.get("ba_hash"):
            r.append("phần theo BA trong bảng soát")
        return r

    all_codes = sorted(set(cur) | set(state["ma"]), key=lambda c: (c.startswith("TL"), c))
    ma_st = {c: st_ma(c) for c in all_codes}
    tc_of = {c: [] for c in all_codes}
    for t in sorted(tcs):
        for c in tcs[t]["ma"]:
            tc_of.setdefault(c, []).append(t)
            ma_st.setdefault(c, "Không có trong nguồn")
    # Mã dùng trong TC mà không có trong SRS/bảng soát
    for c, v in ma_st.items():
        if v == "Không có trong nguồn":
            problems.append(f"Mã {c} được dùng ở test case nhưng không có trong SRS/bảng soát")
    srs_codes = [c for c in all_codes if not c.startswith("TL") and c in cur]
    chua_co_tc = [c for c in srs_codes if not tc_of.get(c)]

    def row_h(t):
        return h([ck.get(t, {}).get("row", ""), tcs.get(t, {}).get("row", "")])

    def st_tc(t):
        b = state["tc"].get(t)
        if b is None or b.get("da_bo"):
            return "Mới, chưa chốt"
        doi = [c for c in tcs[t]["ma"] if ma_st.get(c) in ("Đã đổi", "Đã bỏ khỏi nguồn")]
        sua = b["row_hash"] != row_h(t)
        if doi:
            return "Cần xem lại" + (" (đã sửa, chưa chốt)" if sua else "")
        if sua:
            return "Đã sửa, chưa chốt"
        return "Còn đúng"

    tc_st = {t: st_tc(t) for t in sorted(tcs)}
    tc_bo = sorted(t for t in state["tc"] if t not in tcs and not state["tc"][t].get("da_bo"))
    ma_doi = [c for c, v in ma_st.items() if v in ("Đã đổi", "Đã bỏ khỏi nguồn")]
    ma_moi = [c for c, v in ma_st.items() if v == "Mới"]

    if a.lenh == "tra":
        return tra(a, cfg, srs_t, bs_t, cur, ba, tcs, ma_st, tc_st, tc_of, problems)

    now = None if a.ngay else datetime.datetime.now().astimezone()
    now_iso = now.isoformat(timespec="seconds") if now else None
    today = a.ngay or now.date().isoformat()
    if a.lenh == "chot":
        if not a.mo_ta.strip():
            sys.exit('Cần -m "đã làm gì" để ghi vào lịch sử.')
        if problems:
            print("Chưa chốt được, còn vấn đề:")
            for p in problems:
                print(" -", p)
            sys.exit(1)
        tc_moi = [t for t in tcs if t not in state["tc"] or state["tc"][t].get("da_bo")]
        tc_sua = [t for t in tcs if t in state["tc"] and not state["tc"][t].get("da_bo") and state["tc"][t]["row_hash"] != row_h(t)]
        for c, v in cur.items():
            old = state["ma"].get(c)
            doi = not old or old["hash"] != v["hash"] or old.get("ba_hash") != v.get("ba_hash")
            state["ma"][c] = dict(hash=v["hash"], ba_hash=v.get("ba_hash"), ngay_chot=today if doi else old["ngay_chot"])
        for c in [c for c in state["ma"] if c not in cur]:
            del state["ma"][c]
        for t in tcs:
            old = state["tc"].get(t)
            if not old or old.get("da_bo"):
                state["tc"][t] = dict(tao=today, sua=today, row_hash=row_h(t), ma=tcs[t]["ma"])
            else:
                state["tc"][t] = dict(tao=old["tao"], sua=today if old["row_hash"] != row_h(t) else old["sua"], row_hash=row_h(t), ma=tcs[t]["ma"])
        for t in tc_bo:
            state["tc"][t]["da_bo"] = today
        state["lich_su"].append(dict(ngay=today, thoi_diem=now_iso, commit_goc=git("rev-parse", "--short", "HEAD") or None, chua_commit=bool(git("status", "--porcelain")), ngay_ba=a.ngay_ba, doi=[x.strip() for x in a.doi.split(",") if x.strip()], noi_dung=a.mo_ta.strip(),
                                     dua_tren=dua_tren, ma_doi=ma_doi, ma_moi=ma_moi, tc_moi=tc_moi, tc_sua=tc_sua, tc_bo=tc_bo))
        state["nguon_chot"] = dua_tren
        st_p.write_text(json.dumps(state, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        # tính lại sau chốt
        ma_st = {c: "Không đổi" for c in cur}
        for c in tc_of:
            ma_st.setdefault(c, "Không đổi")
        tc_st = {t: "Còn đúng" for t in tcs}
        ma_doi, ma_moi, tc_bo = [], [], []

    # ---------- sinh truy-vet.md ----------
    out_dir = d
    link = lambda p, n: f"[{Path(p).name} dòng {n}]({rel(out_dir, ROOT / p)}#L{n})"
    tc_neo = set(re.findall(r'<a id="([^"]+)"></a>', tc_t))

    def lk_ma(c):
        """Mã requirement thành link tới đúng dòng trong SRS (hoặc bảng soát nếu là TL); không có thì để chữ thường."""
        v = cur.get(c)
        if not v:
            return c
        p = cfg["bang_soat"] if c.startswith("TL") else cfg["srs"]
        return f"[{c}]({rel(out_dir, ROOT / p)}#L{v['dong']})"

    def lk_tc(x):
        """Mã test case thành link tới đúng dòng trong test-case.md (cần thẻ neo ở ô Mã)."""
        return f"[{x}]({rel(out_dir, ROOT / cfg['test_case'])}#{x.lower()})" if x.lower() in tc_neo else x
    cnt = {}
    for v in tc_st.values():
        k = v.split(" (")[0]
        cnt[k] = cnt.get(k, 0) + 1
    L = []
    L.append(f"# Truy vết — {cfg['ten_tinh_nang']}\n")
    L.append("*File này do `scripts/truy-vet.py` tự sinh, đừng sửa tay. Muốn đổi thì sửa nguồn rồi chạy lại script.*\n")
    L.append("| | |\n|---|---|")
    L.append(f"| Lần chạy gần nhất | {fmt_dt(now_iso, today)} ({'chốt mốc mới' if a.lenh == 'chot' else 'chỉ kiểm, chưa đổi mốc'}) |")
    L.append(f"| Requirement | {cfg['srs']} (cập nhật {dua_tren['srs']}); bảng soát (cập nhật {dua_tren['bang_soat']}), câu trả lời đến {dua_tren['tl_cuoi']} |")
    if gop:
        L.append(f"| Test case (đã gồm checklist) | [test-case.md]({rel(out_dir, ROOT / cfg['test_case'])}) |")
    else:
        L.append(f"| Checklist, test case | [checklist.md]({rel(out_dir, ROOT / cfg['checklist'])}), [test-case.md]({rel(out_dir, ROOT / cfg['test_case'])}) |")
    nc = state.get("nguon_chot") or {}
    L.append(f"| Mốc đã chốt | {fmt_dt(state['lich_su'][-1].get('thoi_diem'), state['lich_su'][-1]['ngay']) if state['lich_su'] else 'chưa chốt lần nào'}" +
             (f" (khi đó: SRS {nc.get('srs')}, bảng soát {nc.get('bang_soat')}, TL đến {nc.get('tl_cuoi')})" if nc else "") + " |\n")
    L.append("## 1. Tóm tắt")
    L.append(f"- Mã requirement: {len(srs_codes)} trong SRS, {len([c for c in cur if c.startswith('TL')])} câu trả lời (TL). Test case: {len(tcs)}.")
    L.append("- Trạng thái test case: " + (", ".join(f"{k} {v}" for k, v in sorted(cnt.items())) or "chưa có"))
    L.append(f"- Mã requirement đã đổi so với mốc đã chốt: {', '.join(ma_doi) or 'không có'}; mã mới: {', '.join(ma_moi) or 'không có'}.")
    L.append(f"- Mã SRS chưa có test case nào: {', '.join(chua_co_tc) or 'không có'}.")
    L.append(f"- Test case đã bỏ khỏi file: {', '.join(tc_bo) or 'không có'}.")
    L.append("- Vấn đề khác: " + ("; ".join(problems) if problems else "không có") + "\n")
    L.append("## 2. Khi requirement đổi, làm gì")
    L.append(f"1. Sửa SRS hoặc ghi câu trả lời mới của BA vào bảng soát (như mọi lần).")
    L.append(f"2. Chạy `python -X utf8 scripts/truy-vet.py kiem {a.du_an} {a.tinh_nang}`. Script liệt kê mã đã đổi và các test case chuyển sang **Cần xem lại**.")
    L.append(("3. Mở từng test case đó (bảng 6 dưới đây), sửa test case cho khớp (checklist nằm chung bảng)." if gop else "3. Mở từng test case đó (bảng 6 dưới đây), sửa checklist và test case cho khớp."))
    L.append(f"4. Chạy `python -X utf8 scripts/truy-vet.py chot {a.du_an} {a.tinh_nang} -m \"đã làm gì, vì sao\"`. Script ghi một dòng lịch sử và chốt mốc mới.")
    L.append("5. Muốn xem từng chữ đã đổi, dùng lịch sử git (commit sau mỗi lần chốt).\n")
    L.append("## 3. Bảng tra mã")
    L.append("Mã trong cột Nguồn của checklist và test case bỏ tiền tố `" + cfg["tien_to"] + "-`. `S01-AC02` là story 1, tình huống 2; `R` là quy tắc; `M` là thông báo; `TL` là câu trả lời của BA.\n")
    L.append("| Mã | Tên ngắn | Nguyên văn (rút gọn) | Mở ở đâu |\n|---|---|---|---|")
    for c in all_codes:
        if c not in cur:
            continue
        v = cur[c]
        where = link(cfg["bang_soat"], v["dong"]) if c.startswith("TL") else link(cfg["srs"], v["dong"])
        L.append(f"| {c} | {v['ten']} | {cut(v['nguyen_van'])} | {where} |")
    L.append("")
    L.append("## 4. Yêu cầu theo BA của từng mã SRS")
    L.append("Gom từ bảng soát (mục 5, 6) để mỗi mã SRS có chỗ ghi điều BA trả lời, kể cả khi SRS (bản quan sát hệ thống 1.3.0) ghi khác. "
             "Test case viết theo cột \"Theo BA\"; chỗ có ⚠️ là nghi lỗi của hệ thống, chưa phải lỗi đã xác nhận. "
             "SRS không bị sửa.\n")
    L.append("| Mã | Tên ngắn | Theo BA (hoặc suy ra) | Hệ thống 1.3.0 hiện tại | Còn mở |\n|---|---|---|---|---|")
    for c in srs_codes:
        o = ba.get(c, dict(ba=[], hien_tai=[], chua_chot=[], khac=False))
        if o["ba"]:
            tb = "<br>".join(
                ("Suy ra: " if e["suy_ra"] else "") + cut(e["text"], 320) +
                (" (" + ", ".join(e["refs"]) + ")" if e["refs"] else " (suy ra từ SRS)" if e["suy_ra"] else "") for e in o["ba"])
        else:
            tb = "Chưa có câu trả lời riêng của BA; theo SRS"
        if o["khac"]:
            ht = "⚠️ Khác. " + ("<br>".join(cut(x, 260) for x in o["hien_tai"]) if o["hien_tai"] else "Xem dòng theo BA ở cột bên cạnh")
        else:
            ht = "Không có điểm khác đã biết"
        L.append(f"| {lk_ma(c)} | {cur[c]['ten']} | {tb} | {ht} | {', '.join(sorted(set(o['chua_chot']))) or '—'} |")
    L.append("")
    L.append("## 5. Từ requirement tới test case")
    L.append("| Mã | Tên ngắn | Trạng thái requirement | Test case |\n|---|---|---|---|")
    for c in all_codes:
        ts = tc_of.get(c, [])
        stt = ma_st.get(c) or ""
        if c in cur:
            tname = cur[c]["ten"]
        else:
            tname = cfg.get("ten_ngan", {}).get(c, "")
        if not ts:
            tshow = "⚠️ chưa có test case" if (not c.startswith("TL") and c in cur) else "—"
        else:
            tshow = f"{len(ts)}: " + ", ".join(lk_tc(x) for x in ts)
        L.append(f"| {lk_ma(c)} | {tname} | {stt} | {tshow} |")
    L.append("")
    L.append("## 6. Từ test case tới requirement")
    L.append("| Mã | Tình huống | Ưu tiên | Mã requirement dùng | Trạng thái | Tạo | Sửa lần cuối | Tự động hóa |\n|---|---|---|---|---|---|---|---|")
    for t in sorted(tcs):
        b = state["tc"].get(t, {})
        au = (tcs[t].get("auto") or "—").replace("|", "¦")
        if tc_st[t].startswith("Cần xem lại") and au.startswith("Có"):
            au = "⚠️ script cần xem lại · " + au
        ms = ", ".join(f"{lk_ma(c)} ({cur[c]['ten']})" if c in cur else c for c in tcs[t]["ma"]) or "—"
        L.append(f"| {lk_tc(t)} | {cut(tcs[t]['tinh_huong'], 90)} | {ck.get(t, {}).get('uu_tien', '')} | {ms} | {tc_st[t]} | {b.get('tao', '—') if not b.get('da_bo') else '—'} | {b.get('sua', '—') if not b.get('da_bo') else '—'} | {au} |")
    L.append("")
    L.append("## 7. Lịch sử thay đổi")
    L.append("Ghi mỗi lần chạy `chot`. **Thời điểm chốt** là giờ máy lúc bấm chốt (kèm múi giờ), không phải giờ BA trả lời hay giờ requirement đổi; mốc cũ chỉ có ngày thì ghi \"không rõ giờ\". **Commit gốc** là commit đang đứng lúc chốt (\"+ sửa chưa commit\" nghĩa là còn thay đổi chưa commit); muốn xem từng chữ đã đổi, dùng git. **Ngày BA trả lời** chỉ ghi khi biết.\n")
    L.append("| Thời điểm chốt (giờ máy) | Commit gốc | Ngày BA trả lời | Đối tượng | Nội dung | Dựa trên | Mã requirement đổi | Test case mới / sửa / bỏ |\n|---|---|---|---|---|---|---|---|")
    for e in state["lich_su"]:
        dt = e.get("dua_tren", {})
        L.append(f"| {fmt_dt(e.get('thoi_diem'), e['ngay'])} | {fmt_commit(e)} | {e.get('ngay_ba') or '—'} | {', '.join(e['doi'])} | {cut(e['noi_dung'], 300)} | SRS {dt.get('srs')}; bảng soát {dt.get('bang_soat')}; TL đến {dt.get('tl_cuoi')} | "
                 f"{', '.join(e.get('ma_doi', []) + [x + ' (mới)' for x in e.get('ma_moi', [])]) or '—'} | "
                 f"mới {len(e.get('tc_moi', []))}; sửa {', '.join(e.get('tc_sua', [])) or 0}; bỏ {', '.join(e.get('tc_bo', [])) or 0} |")
    if not state["lich_su"]:
        L.append("| (chưa có) | | | | | | | |")
    write_if_changed(d / "truy-vet.md", "\n".join(L) + "\n", a.chi_doc)

    # ---------- chèn khối lịch sử vào checklist / test case ----------
    for kind, key in (("checklist", "checklist"), ("test-case", "test_case")):
        if gop and kind == "checklist":
            continue
        p = ROOT / cfg[key]
        t = read(p)
        B = [START, "## Lịch sử thay đổi",
             f"Dựa trên: SRS cập nhật {dua_tren['srs']}; bảng soát cập nhật {dua_tren['bang_soat']}; câu trả lời của BA đến {dua_tren['tl_cuoi']}. "
             f"Trạng thái truy vết (chạy {fmt_dt(now_iso, today)}): " + (", ".join(f"{k} {v}" for k, v in sorted(cnt.items())) or "chưa có") +
             ". Chi tiết từng test case và bảng tra mã: [truy-vet.md](truy-vet.md).", "",
             "| Thời điểm chốt (giờ máy) | Commit gốc | Nội dung | Test case mới / sửa / bỏ |", "|---|---|---|---|"]
        rows = [e for e in state["lich_su"] if kind in e["doi"] or "requirement" in e["doi"]]
        for e in rows:
            B.append(f"| {fmt_dt(e.get('thoi_diem'), e['ngay'])} | {fmt_commit(e)} | {cut(e['noi_dung'], 300)} | mới {len(e.get('tc_moi', []))}; sửa {', '.join(e.get('tc_sua', [])) or 0}; bỏ {', '.join(e.get('tc_bo', [])) or 0} |")
        if not rows:
            B.append("| (chưa có) | | | |")
        B.append(END)
        blk = "\n".join(B)
        if START in t and END in t:
            t = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda m: blk, t, flags=re.S)
        else:
            t = t.rstrip("\n") + "\n\n" + blk + "\n"
        write_if_changed(p, t, a.chi_doc)

    # ---------- in ra console ----------
    print(f"[{a.lenh}] {a.du_an}/{a.tinh_nang}  {fmt_dt(now_iso, today)}")
    print("  Trạng thái test case:", ", ".join(f"{k} {v}" for k, v in sorted(cnt.items())))
    if ma_doi:
        print("  Mã requirement đã đổi:", ", ".join(f"{c} ({'; '.join(why(c)) or 'đã bỏ khỏi nguồn'})" for c in ma_doi))
        for t in sorted(tcs):
            if tc_st.get(t, "").startswith("Cần xem lại"):
                print("   -", t, "xem lại vì:", ", ".join(c for c in tcs[t]["ma"] if ma_st.get(c) in ("Đã đổi", "Đã bỏ khỏi nguồn")))
    if ma_moi:
        print("  Mã requirement mới:", ", ".join(ma_moi))
    if chua_co_tc:
        print("  Mã SRS chưa có test case:", ", ".join(chua_co_tc))
    if tc_bo:
        print("  Test case đã bỏ khỏi file:", ", ".join(tc_bo))
    for p in problems:
        print("  VẤN ĐỀ:", p)
    print("  Chỉ đọc, không ghi file." if a.chi_doc else f"  truy-vet.md: {(d / 'truy-vet.md').relative_to(ROOT)}")
    sm = ROOT / "testing" / a.du_an / "smoke-test.md"
    if sm.exists() and f"{a.tinh_nang}/test-case.md#" in read(sm) and (a.lenh == "chot" or ma_doi or any(v != "Còn đúng" for v in tc_st.values())):
        print(f"  Smoke test có dùng test case của tính năng này: chạy `python -X utf8 scripts/truy-vet-smoke.py kiem {a.du_an}` để xem smoke có cần cập nhật không.")
    rg = ROOT / "testing" / a.du_an / "regression-test.md"
    if rg.exists() and f"{a.tinh_nang}/test-case.md#" in read(rg) and (a.lenh == "chot" or ma_doi or any(v != "Còn đúng" for v in tc_st.values())):
        print(f"  Bộ regression có dùng test case của tính năng này: chạy `python -X utf8 scripts/truy-vet-regression.py kiem {a.du_an}` để xem tầng/vùng nào cần chạy lại hoặc cập nhật.")
    can_xem = sum(1 for v in tc_st.values() if v != "Còn đúng")
    print(f"  TÓM TẮT: ma_doi={len(ma_doi)} can_xem_lai={can_xem} tc_bo={len(tc_bo)} van_de={len(problems)}")
    bad = ma_doi or chua_co_tc or tc_bo or problems or any(v != "Còn đúng" for v in tc_st.values())
    sys.exit(1 if bad and a.lenh == "kiem" else 0)


if __name__ == "__main__":
    main()
