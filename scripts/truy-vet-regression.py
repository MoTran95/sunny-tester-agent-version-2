#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Truy vết bộ regression (testing/<dự-án>/regression-test.md) về test case gốc và requirement.

Dùng:
  python -X utf8 scripts/truy-vet-regression.py kiem <dự-án>
      CHỈ ĐỌC, in gọn vài dòng. So requirement và test case hiện tại với mốc đã chốt, rồi báo:
      - mã requirement đã đổi, và case nào dựa vào mã đó thuộc Tầng 1 hay vùng nào của Tầng 2
        (đó là gợi ý "đợt này nên chạy Tầng 1 + các vùng này");
      - test case đã sửa, test case mới chưa xếp tầng/vùng, test case không còn;
      - vấn đề cấu trúc (link hỏng, case trùng, case chưa thuộc tầng/vùng nào).
      Thoát mã 1 nếu có việc cần làm.
  python -X utf8 scripts/truy-vet-regression.py ghi-luot <dự-án> --tang "Tầng 1" --build "1.3.0" --ket-qua "dang-nhap/TC-005=Đạt,..." [--ghi-chu "..."]
      Ghi MỘT lượt chạy của một tầng vào mục "Lượt chạy" (case của tầng không nêu = Chưa chạy). Chỉ ghi khối này.
  python -X utf8 scripts/truy-vet-regression.py chot <dự-án> -m "đã làm gì" [--nguoi "Tên"]  (mặc định: .nguoi-test)
      Chốt mốc mới: "bộ regression hiện tại đã khớp test case và requirement hiện tại". Ghi dòng lịch sử,
      làm mới mục Truy vết (vùng -> mã requirement) và mốc. Chốt SAU khi đã chốt truy vết từng tính năng.

CHỈ MỘT FILE regression. Nguồn sự thật là bảng có tiêu đề '| Tầng | Vùng | Mã case gốc ...':
  - Tầng 1: mỗi dòng một case; Tầng 2: mỗi dòng một vùng, ô Mã case gốc chứa nhiều link; Tầng 3: một dòng, không link
    (Tầng 3 = toàn bộ test case của các tính năng đã làm truy vết, nên không liệt kê).
  - Link dạng [Tên module · TC-005](thư-mục/test-case.md#tc-005).
Mọi test case của mọi tính năng có truy-vet-cau-hinh.json phải thuộc Tầng 1 hoặc một vùng của Tầng 2; case mới thêm vào
test-case.md mà chưa xếp thì `kiem` báo vấn đề. Cách tính "đổi" dùng lại hàm của scripts/truy-vet.py và truy-vet-smoke.py.
"""
import argparse
import datetime
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
def _default_author():
    """Tên người test của máy này: `.nguoi-test` (xem scripts/test_automation/config.py)."""
    sys.path.insert(0, str(ROOT / "scripts"))
    from test_automation.config import default_author
    return default_author()

spec = importlib.util.spec_from_file_location("truy_vet_smoke", ROOT / "scripts" / "truy-vet-smoke.py")
sm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sm)
tv = sm.tv

TV_START = "<!-- TRUY-VET:BAT-DAU (tự sinh bởi scripts/truy-vet-regression.py, không sửa tay) -->"
TV_END = "<!-- TRUY-VET:KET-THUC -->"
LS_START = "<!-- LICH-SU:BAT-DAU (tự sinh bởi scripts/truy-vet-regression.py, không sửa tay) -->"
LS_END = "<!-- LICH-SU:KET-THUC -->"
LC_START = "<!-- LUOT-CHAY:BAT-DAU (tự sinh bởi scripts/truy-vet-regression.py ghi-luot, không sửa tay) -->"
LC_END = "<!-- LUOT-CHAY:KET-THUC -->"
TT_LUOT = ("Đạt", "Đạt kèm ý phụ sai", "Không đạt", "Không kết luận", "Bị chặn", "Bỏ qua", "Chưa chạy")
MOC = re.compile(r"<!-- REGRESSION-MOC: (\{.*?\}) -->")
HANG_LS = sm.HANG_LS
LINK = sm.LINK
TANG = ("Tầng 1", "Tầng 2", "Tầng 3")
CHAN = re.compile(r"cố ý nhập sai (\d+) lần")


def parse_regression(text, du_an_dir):
    """Đọc bảng tầng -> (danh sách dòng, vấn đề). Mỗi dòng: tang, vung, cases=[(rel_dir, TC, nhãn)]."""
    names, rows, problems = None, [], []
    for line in text.splitlines():
        if names is None:
            if line.startswith("| Tầng | Vùng |"):
                names = tv.cells(line)
            continue
        if not line.startswith("|"):
            if rows:
                break
            continue
        if re.match(r"^\|\s*-", line):
            continue
        c = tv.cells(line)
        if len(c) != len(names):
            problems.append(f"Dòng '{c[0]} · {c[1] if len(c) > 1 else ''}': có {len(c)} ô, tiêu đề có {len(names)} cột")
            continue
        d = dict(zip(names, c))
        tang = d["Tầng"]
        if tang not in TANG:
            problems.append(f"Cột Tầng chỉ được ghi {TANG}, hiện là '{tang}'")
            continue
        cases = []
        for m in LINK.finditer(d["Mã case gốc"]) if "Mã case gốc" in d else []:
            rd = (du_an_dir / m.group(2)).resolve().parent.relative_to(du_an_dir).as_posix()
            cases.append((rd, m.group(3).upper(), m.group(1)))
        if tang == "Tầng 3" and cases:
            problems.append("Dòng Tầng 3 không được liệt kê case (Tầng 3 = toàn bộ test case)")
        if tang == "Tầng 1" and len(cases) != 1:
            problems.append(f"Tầng 1 mỗi dòng một case, dòng '{d['Vùng']}' có {len(cases)} link")
        if tang == "Tầng 2" and not cases:
            problems.append(f"Dòng Tầng 2 '{d['Vùng']}' chưa có link case nào")
        rows.append(dict(tang=tang, vung=d["Vùng"], cases=cases))
    if names is None:
        sys.exit("Không thấy bảng tầng (tiêu đề '| Tầng | Vùng | Mã case gốc | ...')")
    if not any(r["tang"] == "Tầng 3" for r in rows):
        problems.append("Thiếu dòng Tầng 3 (toàn bộ), dù chỉ đề xuất khi có lý do")
    return rows, problems


def universe(du_an_dir):
    return [d.name for d in sorted(du_an_dir.iterdir()) if d.is_dir() and (d / "truy-vet-cau-hinh.json").exists()]


def snapshot(f):
    return dict(codes={c: [v["hash"], v.get("ba_hash")] for c, v in f["cur"].items()},
                tc={t: sm.row_hash(f, t) for t in f["tcs"]})


def code_changed(f, base):
    ch = set()
    for c in set(f["cur"]) | set(base["codes"]):
        cu, b = f["cur"].get(c), base["codes"].get(c)
        if (cu is None) != (b is None) or (cu is not None and [cu["hash"], cu.get("ba_hash")] != list(b)):
            ch.add(c)
    return ch


def ghi_file(path, text, rows, cache, moc_moi, hang_moi, du_an_dir):
    gom = {}
    for r in rows:
        if r["tang"] == "Tầng 3":
            continue
        g = gom.setdefault((r["tang"], r["vung"]), dict(n=0, ma=set()))
        for rd, t, _ in r["cases"]:
            g["n"] += 1
            g["ma"].update((rd, c) for c in cache[rd]["tcs"][t]["ma"])
    T = ["| Tầng | Vùng | Số case | Mã requirement mà các case dựa vào (bấm để mở đúng dòng trong tài liệu) |", "|---|---|---|---|"]
    for (tang, vung), g in gom.items():
        codes = "<br>".join(sm.link_ma(cache[rd], c, du_an_dir) for rd, c in sorted(g["ma"], key=lambda x: (x[0], x[1]))) or "—"
        T.append(f"| {tang} | {vung} | {g['n']} | {codes} |")
    new = re.sub(re.escape(TV_START) + r".*?" + re.escape(TV_END), lambda m: "\n".join([TV_START] + T + [TV_END]), text, flags=re.S)
    cu = [l for l in new.split(LS_START)[1].split(LS_END)[0].splitlines() if HANG_LS.match(l)]
    H = ["| Thời điểm | Việc | Người | Nội dung | Số case Tầng 1 · Tầng 2 · tất cả | Commit |", "|---|---|---|---|---|---|", hang_moi] + cu
    new = re.sub(re.escape(LS_START) + r".*?" + re.escape(LS_END), lambda m: "\n".join([LS_START] + H + [LS_END]), new, flags=re.S)
    moc = "<!-- REGRESSION-MOC: " + json.dumps(dict(f=moc_moi), ensure_ascii=False, separators=(",", ":")) + " -->"
    new = MOC.sub(lambda m: moc, new) if MOC.search(new) else new.replace(LS_END, LS_END + "\n" + moc, 1)
    c = hang_moi.strip().strip("|").split("|")
    cap = f"| Cập nhật lần cuối | {c[0].strip()} ({c[1].strip().lower()}: {c[3].strip()}) |"
    if re.search(r"^\| Cập nhật lần cuối \|.*$", new, flags=re.M):
        new = re.sub(r"^\| Cập nhật lần cuối \|.*$", lambda m: cap, new, flags=re.M)
    else:
        new = re.sub(r"^(\| Ngày lập \|.*)$", lambda m: m.group(1) + "\n" + cap, new, count=1, flags=re.M)
    path.write_text(new, encoding="utf-8")


def ghi_luot(a, text, rows, rg_p):
    """Ghi MỘT lượt chạy của một tầng vào mục "Lượt chạy" (không đụng mốc và lịch sử)."""
    if LC_START not in text:
        sys.exit('regression-test.md chưa có mục "Lượt chạy" (cặp dấu LUOT-CHAY): thêm từ khuôn mẫu của skill de-xuat-regression')
    if not a.build.strip() or not a.ket_qua.strip() or a.tang not in TANG:
        sys.exit('Cần --tang "Tầng 1|Tầng 2|Tầng 3", --build "<số bản>" và --ket-qua "dang-nhap/TC-005=Đạt,..."')
    muc_tieu = [f"{rd}/{t}" for r in rows if r["tang"] == a.tang for rd, t, _ in r["cases"]]
    st = {}
    for phan in a.ket_qua.split(","):
        if "=" not in phan:
            sys.exit(f"--ket-qua sai ở '{phan.strip()}': mỗi mục dạng <tính-năng>/<TC-xxx>=<trạng thái>")
        k, v = (x.strip() for x in phan.split("=", 1))
        k = k.rsplit("/", 1)[0] + "/" + k.rsplit("/", 1)[1].upper()
        if v not in TT_LUOT:
            sys.exit(f"Trạng thái '{v}' không hợp lệ; chọn một trong {TT_LUOT}")
        if k not in muc_tieu and a.tang != "Tầng 3":
            sys.exit(f"{k} không thuộc {a.tang} trong bảng (thuộc: {', '.join(muc_tieu) or 'không có'})")
        st[k] = v
    for k in muc_tieu:
        st.setdefault(k, "Chưa chạy")
    try:  # tên hiển thị của tính năng, theo dự án (testing/<dự-án>/ten-tinh-nang.json)
        ten_tn = json.loads((ROOT / "testing" / a.du_an / "ten-tinh-nang.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        ten_tn = {}
    nhom = {}
    for k in muc_tieu:
        rd, _, tc = k.partition("/")
        nhom.setdefault(st[k], []).append(f"{ten_tn[rd]} {tc}" if rd in ten_tn else k)
    kq = "; ".join(f"{k} ({len(v)}): {', '.join(v)}" for k, v in sorted(nhom.items(), key=lambda kv: TT_LUOT.index(kv[0])))
    xau = [k for k in ("Không đạt", "Bị chặn") if k in nhom]
    chua = [k for k in ("Không kết luận", "Chưa chạy", "Bỏ qua") if k in nhom]
    qd = "Có case không đạt" if "Không đạt" in nhom else ("Chưa kết luận hết" if chua or "Bị chặn" in nhom else "Đạt toàn bộ")
    now = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    hang = f"| {tv.fmt_dt(now)} | {a.tang} | {a.build.strip()} | {a.nguoi} | {kq} | {qd} | {(a.ghi_chu.strip() or '—').replace('|', '¦')} |"
    cu = [l for l in text.split(LC_START)[1].split(LC_END)[0].splitlines() if HANG_LS.match(l)]
    H = ["| Thời điểm | Phạm vi | Build (số bản ở chân trang) | Người chạy | Kết quả | Kết luận | Ghi chú |", "|---|---|---|---|---|---|---|", hang] + cu
    rg_p.write_text(re.sub(re.escape(LC_START) + r".*?" + re.escape(LC_END), lambda m: "\n".join([LC_START] + H + [LC_END]), text, flags=re.S), encoding="utf-8")
    print(f"[ghi-luot] {a.tang}, build {a.build.strip()}: {qd}")


def luot_gan_nhat(text):
    if LC_START not in text:
        return None
    for l in text.split(LC_START)[1].split(LC_END)[0].splitlines():
        if HANG_LS.match(l):
            c = [x.strip() for x in l.strip().strip("|").split("|")]
            return f"{c[0]}, {c[1]}, build {c[2]}: {c[5]}"
    return "chưa có lượt chạy nào"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("lenh", choices=["kiem", "chot", "ghi-luot"])
    ap.add_argument("du_an")
    ap.add_argument("-m", "--mo-ta", default="")
    ap.add_argument("--nguoi", default=None)
    ap.add_argument("--tang", default="", help="với ghi-luot: Tầng 1, Tầng 2 hoặc Tầng 3")
    ap.add_argument("--build", default="", help="với ghi-luot: số bản đọc ở chân trang hệ thống")
    ap.add_argument("--ket-qua", default="", help="với ghi-luot: dang-nhap/TC-005=Đạt,gio-hang/TC-001=Không đạt,...")
    ap.add_argument("--ghi-chu", default="", help="với ghi-luot: quan sát cụ thể, mã bug...")
    ap.add_argument("--ngay", default=None, help="chỉ dùng khi thử: ép ngày, không ghi giờ")
    a = ap.parse_args()
    if getattr(a, "nguoi", "x") is None:
        a.nguoi = _default_author()

    du_an_dir = ROOT / "testing" / a.du_an
    rg_p = du_an_dir / "regression-test.md"
    text = tv.read(rg_p)
    rows, problems = parse_regression(text, du_an_dir)
    if a.lenh == "ghi-luot":
        return ghi_luot(a, text, rows, rg_p)
    mm = MOC.search(text)
    state = json.loads(mm.group(1)) if mm else {"f": {}}
    cache, luu_y = {}, []

    loc, dem = {}, {}
    for r in rows:
        for rd, t, _ in r["cases"]:
            k = f"{rd}/{t}"
            if k in loc:
                problems.append(f"Test case {k} xuất hiện hai lần ({loc[k][0]} · {loc[k][1]} và {r['tang']} · {r['vung']})")
            loc[k] = (r["tang"], r["vung"])
            dem[r["tang"]] = dem.get(r["tang"], 0) + 1
    feats = universe(du_an_dir)
    for rd in feats:
        sm.load_feature(rd, du_an_dir, cache)
    for k, (tang, vung) in loc.items():
        rd, t = k.rsplit("/", 1)
        if rd not in cache:
            problems.append(f"{k}: tính năng chưa có truy-vet-cau-hinh.json")
        elif t not in cache[rd]["tcs"]:
            problems.append(f"{k} ({tang} · {vung}): test case không còn trong test-case.md, bỏ khỏi bảng hoặc đổi mã")
        elif t.lower() not in cache[rd]["tc_ids"]:
            problems.append(f"{k}: test-case.md không có thẻ neo #{t.lower()}")

    thieu, moi, sua, doi_ma = [], [], [], {}
    for rd, f in cache.items():
        base = state["f"].get(rd)
        for t in f["tcs"]:
            k = f"{rd}/{t}"
            if k not in loc:
                thieu.append(k)
            if base is not None and t not in base["tc"]:
                moi.append(k)
            elif base is not None and base["tc"][t] != sm.row_hash(f, t) and k in loc:
                sua.append(k)
        if base is None:
            continue
        ch = code_changed(f, base)
        if ch:
            for t, v in f["tcs"].items():
                hit = sorted(set(v["ma"]) & ch)
                if hit:
                    doi_ma[f"{rd}/{t}"] = hit
        doi_ma[f"__ma__{rd}"] = sorted(ch)
        if f["nhap"]:
            luu_y.append(f"{rd}: requirement nháp, chưa BA xác nhận; case Không đạt thì kiểm lại test case trước khi kết luận")
    for k in thieu:
        problems.append(f"{k}: chưa xếp vào Tầng 1 hoặc vùng nào của Tầng 2 (thêm vào bảng; Tầng 3 tự gồm mọi case)")
    for k, (tang, vung) in loc.items():
        rd, t = k.rsplit("/", 1)
        if rd not in cache or t not in cache[rd]["tcs"]:
            continue
        cot = cache[rd]["tcs"][t].get("cot", {})
        if tang == "Tầng 1":
            if "⚠️" in cot.get("Nguồn", ""):
                luu_y.append(f"{k} (Tầng 1): test case gốc đánh dấu ⚠️ (hệ thống đang làm khác kết quả mong đợi); cần cách xử lý ghi ở bảng Tầng 1")
            sai = CHAN.search(cot.get("Điều kiện trước", ""))
            if sai:
                luu_y.append(f"{k} (Tầng 1): cố ý nhập sai {sai.group(1)} lần, có thể kích hoạt khóa/chặn, không hợp Tầng 1")
            if sm.PHU.search(cot.get("Các bước", "") + " " + cot.get("Kết quả mong đợi", "")):
                luu_y.append(f"{k} (Tầng 1): có tác dụng phụ khó đảo ngược (gửi SMS/email, phê duyệt/từ chối, xóa, thanh toán)")
    chua = sum(1 for k in loc if k.rsplit('/', 1)[0] in cache and cache[k.rsplit('/', 1)[0]]["tcs"].get(k.rsplit('/', 1)[1], {}).get("cot", {}).get("Trạng thái") not in ("Đạt", "Không đạt"))
    if chua:
        luu_y.append(f"{chua}/{len(loc)} case trong bảng chưa chạy thật: kết quả mong đợi chưa được kiểm trên hệ thống")

    if a.lenh == "chot":
        if not a.mo_ta.strip():
            sys.exit('Cần -m "đã làm gì" để ghi vào lịch sử.')
        if problems:
            print("Chưa chốt được, còn vấn đề:")
            for p in problems:
                print(" -", p)
            sys.exit(1)
        now = None if a.ngay else datetime.datetime.now().astimezone()
        now_iso = now.isoformat(timespec="seconds") if now else None
        today = a.ngay or now.date().isoformat()
        loai = "Cập nhật" if HANG_LS.search(text.split(LS_START)[-1]) else "Tạo"
        ghi = []
        if moi and loai != "Tạo":
            ghi.append("thêm " + ", ".join(moi))
        xem = sorted({k for k in doi_ma if not k.startswith("__ma__")} | set(sua))
        xem = [k for k in xem if k in loc]
        if xem:
            ghi.append("xem lại/sửa " + ", ".join(xem))
        nd = a.mo_ta.strip() + (f" ({'; '.join(ghi)})" if ghi else "")
        e = dict(commit_goc=tv.git("rev-parse", "--short", "HEAD") or None, chua_commit=bool(tv.git("status", "--porcelain")))
        tong = sum(1 for k in (f"{rd}/{t}" for rd, f in cache.items() for t in f["tcs"]))
        hang_moi = f"| {tv.fmt_dt(now_iso, today)} | {loai} | {a.nguoi} | {nd} | {dem.get('Tầng 1', 0)} · {sum(v for k, v in dem.items() if k == 'Tầng 2')} · {tong} | {tv.fmt_commit(e)} |"
        ghi_file(rg_p, text, rows, cache, {rd: snapshot(f) for rd, f in cache.items()}, hang_moi, du_an_dir)
        print(f"[chot] {a.du_an}/regression-test.md: đã ghi mốc, lịch sử và mục Truy vết")
        return

    if not state["f"]:
        problems.append("Chưa có mốc (chưa chốt lần nào): chạy `chot` sau khi bảng đã xong")
    n_bug = len(re.findall(r"\| Bug lọt production ", text))
    print(f"[kiem] {a.du_an}/regression-test.md: Tầng 1 {dem.get('Tầng 1', 0)} case, Tầng 2 {dem.get('Tầng 2', 0)} case, tất cả {sum(len(f['tcs']) for f in cache.values())} case"
          + (f"; {n_bug} dòng có case sinh từ bug lọt production" if n_bug else ""))
    viec = False
    lg = luot_gan_nhat(text)
    if lg:
        print(f"  Lượt chạy gần nhất: {lg}")
    for rd in feats:
        ch = doi_ma.get(f"__ma__{rd}", [])
        if ch:
            print(f"  Mã requirement đã đổi ở {rd}: {', '.join(ch)}")
    hit = {k: v for k, v in doi_ma.items() if not k.startswith("__ma__")}
    if hit:
        viec = True
        vung_chay, t1 = {}, []
        for k, ma in sorted(hit.items()):
            where = loc.get(k)
            if where is None:
                print(f"  - {k}: dựa vào {', '.join(ma)} (chưa xếp tầng/vùng)")
            elif where[0] == "Tầng 1":
                t1.append(k)
                print(f"  - {k} (Tầng 1): dựa vào {', '.join(ma)}: cần xem lại")
            else:
                vung_chay.setdefault(where[1], []).append(k)
                print(f"  - {k} ({where[0]} · {where[1]}): dựa vào {', '.join(ma)}: cần xem lại")
        print("  Gợi ý phạm vi đợt này (suy ra từ requirement đổi, không phải từ build): Tầng 1" + (" + vùng " + "; ".join(vung_chay) if vung_chay else ""))
    for k in sua:
        viec = True
        print(f"  - {k} ({loc[k][0]} · {loc[k][1]}): test case đã sửa")
    for k in moi:
        viec = True
        print(f"  - {k}: test case mới, chưa chốt")
    for p in problems:
        print("  !", p)
    for p in luu_y:
        print("  (lưu ý)", p)
    if viec or problems:
        sys.exit(1)
    print("  Còn đúng: không mã requirement hay test case nào đổi so với mốc")


if __name__ == "__main__":
    main()
