#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Truy vết bộ smoke test (testing/<dự-án>/smoke-test.md) về test case gốc và requirement.

Dùng:
  python -X utf8 scripts/truy-vet-smoke.py kiem <dự-án>
      CHỈ ĐỌC, không ghi file, in gọn vài dòng. So test case gốc và requirement hiện tại với mốc smoke
      đã chốt: báo smoke case nào "Cần xem lại" (requirement mà test case gốc dựa vào đã đổi),
      "Test case đã sửa", "Test case không còn". Thoát mã 1 nếu có việc cần làm.
      Thời gian vượt mục tiêu chỉ là lưu ý, không phải lỗi (mục đích smoke quan trọng hơn thời gian).
      Cũng chỉ LƯU Ý (không phải lỗi): test case gốc có ⚠️ (đang lệch hệ thống), "cố ý nhập sai N lần", tác dụng phụ khó
      đảo ngược, không có mã requirement; requirement nháp; case chưa chạy thật; dòng 'Case mới'/'Ngoài repo' (không truy vết được).
  python -X utf8 scripts/truy-vet-smoke.py chot <dự-án> -m "đã làm gì" [--nguoi "Tên"]  (mặc định: .nguoi-test)
      Chốt mốc mới: "bộ smoke hiện tại đã khớp test case và requirement hiện tại". Thêm một dòng vào
      "Lịch sử tạo và cập nhật" và làm mới mục "Truy vết". Chốt sau khi đã chốt truy vết từng tính năng.

  python -X utf8 scripts/truy-vet-smoke.py ghi-luot <dự-án> --build "<số bản ở chân trang>" --ket-qua "1=Đạt,2=Không đạt,..." [--ghi-chu "..."]
      Ghi MỘT lượt chạy smoke (một build) vào mục "Lượt chạy" của smoke-test.md. Số trong --ket-qua là cột # của bảng;
      trạng thái ∈ Đạt, Đạt kèm lỗi đã biết, Không đạt, Bị chặn, Bỏ qua, Chưa chạy; case không nêu = Chưa chạy.
      Script tự tính quyết định (Nhận/Trả build) theo tiêu chí "Không đạt thì dừng". Chỉ ghi khối Lượt chạy.

Ví dụ: python -X utf8 scripts/truy-vet-smoke.py kiem <dự-án>

CHỈ MỘT FILE smoke. Nguồn sự thật là cột "Mã case gốc" của bảng 7 cột: mỗi ô có link dạng
[Tên module · TC-005](dang-nhap/test-case.md#tc-005); script đọc link để biết tính năng và test case.
Mốc nằm ngay trong smoke-test.md (một dòng chú thích HTML "SMOKE-MOC", người đọc không thấy), lịch sử
là bảng trong chính file; không có file trạng thái riêng. Mỗi tính năng cần có truy-vet-cau-hinh.json.
Cách tính "đổi" dùng lại hàm của scripts/truy-vet.py nên đồng nhất với truy vết của từng tính năng.
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

spec = importlib.util.spec_from_file_location("truy_vet", ROOT / "scripts" / "truy-vet.py")
tv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tv)

TV_START = "<!-- TRUY-VET:BAT-DAU (tự sinh bởi scripts/truy-vet-smoke.py, không sửa tay) -->"
TV_END = "<!-- TRUY-VET:KET-THUC -->"
LS_START = "<!-- LICH-SU:BAT-DAU (tự sinh bởi scripts/truy-vet-smoke.py, không sửa tay) -->"
LS_END = "<!-- LICH-SU:KET-THUC -->"
LC_START = "<!-- LUOT-CHAY:BAT-DAU (tự sinh bởi scripts/truy-vet-smoke.py ghi-luot, không sửa tay) -->"
LC_END = "<!-- LUOT-CHAY:KET-THUC -->"
TT_LUOT = ("Đạt", "Đạt kèm lỗi đã biết", "Không đạt", "Bị chặn", "Bỏ qua", "Chưa chạy")
MOC = re.compile(r"<!-- SMOKE-MOC: (\{.*?\}) -->")
PHU = re.compile(r"(?:[Bb]ấm|[Nn]hấn|[Cc]họn)[^.<]{0,40}(?:Gửi|Phê duyệt|Từ chối|Trả lại|Xóa|Xoá|Hủy|Thanh toán|Chuyển tiền)|\bSMS\b|\bemail\b|\bgửi (?:thư|tin)")
LINK = re.compile(r"\[([^\]]+)\]\(([^)#]+)#(tc-\d+)\)")
HANG_LS = re.compile(r"^\| \d{4}-\d\d-\d\d ", re.M)
PHAN = ("Cố định", "Theo build")


def anchors(path):
    return set(re.findall(r'<a id="([^"]+)"></a>', tv.read(path)))


def load_feature(rel_dir, du_an_dir, cache):
    """Đọc requirement + test case của một tính năng (đồng nhất cách tính với truy-vet.py)."""
    if rel_dir in cache:
        return cache[rel_dir]
    cfg_p = du_an_dir / rel_dir / "truy-vet-cau-hinh.json"
    if not cfg_p.exists():
        sys.exit(f"Chưa có {cfg_p}: tính năng này chưa làm truy vết")
    cfg = json.loads(tv.read(cfg_p))
    srs_t, bs_t = tv.read(ROOT / cfg["srs"]), tv.read(ROOT / cfg["bang_soat"])
    tc_t = tv.read(ROOT / cfg["test_case"])
    ck_t = tc_t if not cfg.get("checklist") else tv.read(ROOT / cfg["checklist"])
    cur = tv.parse_srs(srs_t, cfg["tien_to"])
    ba = tv.parse_ba(bs_t, cfg["tien_to"])
    for k, v in cur.items():
        v["ba_hash"] = tv.h([x for e in ba.get(k, {}).get("ba", []) for x in (e["text"], e["stt"])])
    cur.update(tv.parse_tl(bs_t))
    for k, v in cur.items():
        v["ten"] = cfg["ten_ngan"].get(k) or tv.cut(v["nghia"] or v["nguyen_van"], 40)
    f = dict(nhap=bool(re.search(r"chưa BA xác nhận|\(nháp", tc_t[:3000])), cfg=cfg, cur=cur, ck=tv.parse_tc(ck_t), tcs=tv.parse_tc(tc_t), bs=ROOT / cfg["bang_soat"], srs=ROOT / cfg["srs"],
             srs_ids=anchors(ROOT / cfg["srs"]), bs_ids=anchors(ROOT / cfg["bang_soat"]), tc_ids=anchors(ROOT / cfg["test_case"]))
    cache[rel_dir] = f
    return f


def row_hash(f, t):
    return tv.h([f["ck"].get(t, {}).get("row", ""), f["tcs"].get(t, {}).get("row", "")])


def parse_smoke(text, du_an_dir):
    """Đọc bảng 7 cột (tiêu đề bắt đầu '| # | Smoke case |') -> (danh sách dòng, vấn đề, tổng phút)."""
    rows, names, problems, tong, ngoai, tat_ca = [], None, [], 0.0, [], []
    for line in text.splitlines():
        if names is None:
            if line.startswith("| # | Smoke case |"):
                names = tv.cells(line)
            continue
        if not re.match(r"^\| \d+ \|", line):
            if rows and not line.startswith("|"):
                break
            continue
        c = tv.cells(line)
        if len(c) != len(names):
            problems.append(f"Dòng {c[0]}: có {len(c)} ô, tiêu đề có {len(names)} cột")
            continue
        d = dict(zip(names, c))
        tat_ca.append(d["#"])
        tm = re.search(r"(\d+(?:[,.]\d+)?)\s*phút", d["Thời gian ước tính"])
        if tm:
            tong += float(tm.group(1).replace(",", "."))
        else:
            problems.append(f"Dòng {d['#']}: cột Thời gian ước tính chưa có số phút")
        if d["Phần"] not in PHAN:
            problems.append(f"Dòng {d['#']}: cột Phần chỉ được ghi {PHAN}, hiện là '{d['Phần']}'")
        m = LINK.search(d["Mã case gốc"])
        if not m:
            cell = d["Mã case gốc"]
            if cell.startswith(("Case mới", "Ngoài repo")):
                ngoai.append(f"Dòng {d['#']} ({cell.split('·')[0].strip()}): chưa có test case gốc trong repo nên không truy vết được; kiểm tay khi requirement đổi")
            else:
                problems.append(f"Dòng {d['#']}: cột Mã case gốc chưa có link dạng [Tên · TC-005](thư-mục/test-case.md#tc-005); case mới ghi 'Case mới', case ngoài repo ghi 'Ngoài repo: <nguồn> · <mã>'")
            continue
        tc_dir = (du_an_dir / m.group(2)).resolve().parent.relative_to(du_an_dir).as_posix()
        rows.append(dict(n=d["#"], rel_dir=tc_dir, tc=m.group(3).upper(), nhan=m.group(1), key=f"{tc_dir}/{m.group(3).upper()}"))
    if names is None:
        sys.exit("Không thấy bảng 7 cột (tiêu đề '| # | Smoke case |')")
    return rows, problems, tong, ngoai, tat_ca


def link_ma(f, c, du_an_dir, ten=True):
    """Mã requirement thành link: ưu tiên thẻ neo theo mã; chưa có neo thì link tới đúng dòng (#L<số dòng>, trang HTML có neo này)."""
    v = f["cur"].get(c)
    t = f" {v['ten']}" if v and ten else ""
    if not v:
        return f"{c}{t}"
    low = f"{f['cfg']['tien_to'].lower()}-{c.lower()}"
    if c.startswith("TL-"):
        return f"[{c}]({tv.rel(du_an_dir, f['bs'])}#{c.lower() if c.lower() in f['bs_ids'] else 'L' + str(v['dong'])}){t}"
    return f"[{c}]({tv.rel(du_an_dir, f['srs'])}#{low if low in f['srs_ids'] else 'L' + str(v['dong'])}){t}"


def ghi_file(sm_p, text, rows, info, cache, du_an_dir, moc_moi, hang_moi):
    """Chỉ chạy khi chốt: làm mới mục Truy vết, mốc (một dòng chú thích), thêm dòng lịch sử, dòng Cập nhật lần cuối."""
    T = ["| # | Test case gốc | Requirement mà test case dựa vào |", "|---|---|---|"]
    for r in rows:
        f = cache[r["rel_dir"]]
        codes = "<br>".join(link_ma(f, c, du_an_dir) for c in info[r["key"]]["ma"]) or "—"
        T.append(f"| {r['n']} | [{r['nhan']}]({r['rel_dir']}/test-case.md#{r['tc'].lower()}) | {codes} |")
    new = re.sub(re.escape(TV_START) + r".*?" + re.escape(TV_END), lambda m: "\n".join([TV_START] + T + [TV_END]), text, flags=re.S)
    cu = new.split(LS_START)[1].split(LS_END)[0]
    cu_dong = [l for l in cu.splitlines() if HANG_LS.match(l)]
    H = ["| Thời điểm | Việc | Người | Nội dung | Số case · tổng phút (ước lượng) | Commit |", "|---|---|---|---|---|---|", hang_moi] + cu_dong
    new = re.sub(re.escape(LS_START) + r".*?" + re.escape(LS_END), lambda m: "\n".join([LS_START] + H + [LS_END]), new, flags=re.S)
    moc = "<!-- SMOKE-MOC: " + json.dumps(dict(case=moc_moi), ensure_ascii=False, separators=(",", ":")) + " -->"
    new = MOC.sub(lambda m: moc, new) if MOC.search(new) else new.replace(LS_END, LS_END + "\n" + moc, 1)
    c = hang_moi.strip().strip("|").split("|")
    cap = f"| Cập nhật lần cuối | {c[0].strip()} ({c[1].strip().lower()}: {c[3].strip()}) |"
    if re.search(r"^\| Cập nhật lần cuối \|.*$", new, flags=re.M):
        new = re.sub(r"^\| Cập nhật lần cuối \|.*$", lambda m: cap, new, flags=re.M)
    else:
        new = re.sub(r"^(\| Ngày lập \|.*)$", lambda m: m.group(1) + "\n" + cap, new, count=1, flags=re.M)
    sm_p.write_text(new, encoding="utf-8")


def ghi_luot(a, text, tat_ca, sm_p):
    if LC_START not in text or LC_END not in text:
        sys.exit('smoke-test.md chưa có mục "Lượt chạy" (cặp dấu LUOT-CHAY): thêm từ khuôn mẫu của skill tao-smoke-test')
    if not a.build.strip():
        sys.exit('Cần --build "<số bản đọc ở chân trang hệ thống>"')
    if not a.ket_qua.strip():
        sys.exit('Cần --ket-qua "1=Đạt,2=Không đạt,..."')
    st = {n: "Chưa chạy" for n in tat_ca}
    for phan in a.ket_qua.split(","):
        if "=" not in phan:
            sys.exit(f"--ket-qua sai ở '{phan.strip()}': mỗi mục dạng số=trạng thái")
        n, v = (x.strip() for x in phan.split("=", 1))
        if n not in st:
            sys.exit(f"Số {n} không có trong bảng smoke (có: {', '.join(tat_ca)})")
        if v not in TT_LUOT:
            sys.exit(f"Trạng thái '{v}' không hợp lệ; chọn một trong {TT_LUOT}")
        st[n] = v
    khong = [n for n in tat_ca if st[n] == "Không đạt"]
    chan = [n for n in tat_ca if st[n] == "Bị chặn"]
    chua = [n for n in tat_ca if st[n] in ("Chưa chạy", "Bỏ qua")]
    if khong:
        qd = f"Trả build (dừng tại case {khong[0]})"
    elif chan:
        qd = f"Chưa kết luận (case {', '.join(chan)} bị chặn, không chạy được)"
    elif chua:
        qd = f"Chưa kết luận (chưa chạy đủ: case {', '.join(chua)})"
    else:
        qd = "Nhận build"
    nhom = {}
    for n in tat_ca:
        nhom.setdefault(st[n], []).append(n)
    kq = f"Đạt cả {len(tat_ca)}" if list(nhom) == ["Đạt"] else "; ".join(f"{k}: {', '.join(v)}" for k, v in sorted(nhom.items(), key=lambda kv: TT_LUOT.index(kv[0])))
    canh = []
    if "Đạt kèm lỗi đã biết" in st.values() and "goại lệ" not in text:
        canh.append('có case "Đạt kèm lỗi đã biết" nhưng bảng tiêu chí trả build không ghi ngoại lệ nào; kiểm lại')
    now = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    ghi_chu = (a.ghi_chu.strip() or "—").replace("|", "¦")
    hang = f"| {tv.fmt_dt(now)} | {a.build.strip()} | {a.nguoi} | {kq} | {qd} | {ghi_chu} |"
    cu = text.split(LC_START)[1].split(LC_END)[0]
    cu_dong = [l for l in cu.splitlines() if HANG_LS.match(l)]
    H = ["| Thời điểm | Build (số bản ở chân trang) | Người chạy | Kết quả (số là cột # của bảng) | Quyết định | Ghi chú |", "|---|---|---|---|---|---|", hang] + cu_dong
    new = re.sub(re.escape(LC_START) + r".*?" + re.escape(LC_END), lambda m: "\n".join([LC_START] + H + [LC_END]), text, flags=re.S)
    sm_p.write_text(new, encoding="utf-8")
    print(f"[ghi-luot] build {a.build.strip()}: {kq} -> {qd}")
    for c in canh:
        print("  (lưu ý)", c)


def luot_gan_nhat(text):
    if LC_START not in text or LC_END not in text:
        return None
    for l in text.split(LC_START)[1].split(LC_END)[0].splitlines():
        if HANG_LS.match(l):
            c = [x.strip() for x in l.strip().strip("|").split("|")]
            return f"{c[0]}, build {c[1]}: {c[3]} -> {c[4]}"
    return "chưa có lượt chạy nào"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("lenh", choices=["kiem", "chot", "ghi-luot"])
    ap.add_argument("du_an")
    ap.add_argument("-m", "--mo-ta", default="")
    ap.add_argument("--nguoi", default=None)
    ap.add_argument("--build", default="", help="với ghi-luot: số bản đọc ở chân trang hệ thống")
    ap.add_argument("--ket-qua", default="", help="với ghi-luot: 1=Đạt,2=Không đạt,...")
    ap.add_argument("--ghi-chu", default="", help="với ghi-luot: quan sát cụ thể, mã bug...")
    ap.add_argument("--ngay", default=None, help="chỉ dùng khi thử: ép ngày, không ghi giờ")
    a = ap.parse_args()
    if getattr(a, "nguoi", "x") is None:
        a.nguoi = _default_author()

    du_an_dir = ROOT / "testing" / a.du_an
    sm_p = du_an_dir / "smoke-test.md"
    text = tv.read(sm_p)
    rows, problems, tong, ngoai, tat_ca = parse_smoke(text, du_an_dir)
    if a.lenh == "ghi-luot":
        return ghi_luot(a, text, tat_ca, sm_p)
    mm = MOC.search(text)
    state = json.loads(mm.group(1)) if mm else {"case": {}}
    cache = {}

    luu_y = list(ngoai)
    mx = re.search(r"Thời gian mục tiêu[^|]*\|\s*\*{0,2}(?:khoảng\s*)?(\d+(?:[,.]\d+)?)\s*phút", text)
    if mx and tong > float(mx.group(1).replace(",", ".")):
        luu_y.append(f"Tổng {tong:g} phút vượt mục tiêu {mx.group(1)} phút (chưa kể chuẩn bị chung). Chỉ là lưu ý: giữ case nếu cần cho mục đích smoke, ghi lý do")
    keys = [r["key"] for r in rows]
    for k in {k for k in keys if keys.count(k) > 1}:
        problems.append(f"Test case {k} xuất hiện hai lần trong smoke")

    info = {}
    for r in rows:
        f = load_feature(r["rel_dir"], du_an_dir, cache)
        t = r["tc"]
        if t.lower() not in f["tc_ids"]:
            problems.append(f"Dòng {r['n']}: link tới #{t.lower()} nhưng test-case.md không có thẻ neo này")
        if t not in f["tcs"]:
            info[r["key"]] = dict(st="Test case không còn", doi=[], ma=[])
            continue
        cot = f["tcs"][t].get("cot", {})
        if "⚠️" in cot.get("Nguồn", ""):
            luu_y.append(f"Dòng {r['n']} ({r['key']}): test case gốc đánh dấu ⚠️ (hệ thống đang làm khác kết quả mong đợi), smoke sẽ Không đạt cho tới khi sửa; cần cách xử lý ghi ở tiêu chí trả build")
        sai = re.search(r"cố ý nhập sai (\d+) lần", cot.get("Điều kiện trước", ""))
        if sai:
            luu_y.append(f"Dòng {r['n']} ({r['key']}): test case gốc cố ý nhập sai {sai.group(1)} lần, có thể kích hoạt giới hạn/khóa tài khoản, không hợp smoke")
        ma = f["tcs"][t]["ma"]
        if PHU.search(cot.get("Các bước", "") + " " + cot.get("Kết quả mong đợi", "")):
            luu_y.append(f"Dòng {r['n']} ({r['key']}): test case gốc có tác dụng phụ khó đảo ngược (gửi SMS/email, phê duyệt/từ chối, xóa, thanh toán); chỉ chạy trên môi trường thử và khi người dùng đồng ý")
        if not ma:
            luu_y.append(f"Dòng {r['n']} ({r['key']}): cột Nguồn của test case gốc không có mã requirement nào, truy vết sẽ không bắt được thay đổi requirement")
        base = state["case"].get(r["key"])
        if base is None:
            info[r["key"]] = dict(st="Mới, chưa chốt", doi=[], ma=ma)
            continue
        doi = []
        for c in sorted(set(ma) | set(base["ma"])):
            cu, b = f["cur"].get(c), base["ma"].get(c)
            if cu is None and b is not None:
                doi.append(f"{c} (đã bỏ khỏi nguồn)")
            elif b is None and cu is not None:
                doi.append(f"{c} (mã mới ở test case)")
            elif cu is not None and [cu["hash"], cu.get("ba_hash")] != list(b):
                doi.append(c)
        sua = base["r"] != row_hash(f, t)
        st = "Cần xem lại" if doi else ("Test case đã sửa" if sua else "Còn đúng")
        if doi and sua:
            st = "Cần xem lại (test case cũng đã sửa)"
        info[r["key"]] = dict(st=st, doi=doi, ma=ma)
    for rd, ft in cache.items():
        if ft["nhap"]:
            luu_y.append(f"{rd}: requirement nháp, chưa BA xác nhận. Lượt chạy đầu là lượt hiệu chuẩn: case Không đạt thì kiểm lại test case trước khi kết luận trả build")
    chua = sum(1 for r in rows if cache[r["rel_dir"]]["tcs"].get(r["tc"], {}).get("cot", {}).get("Trạng thái") not in ("Đạt", "Không đạt"))
    if chua:
        luu_y.append(f"{chua}/{len(rows)} case gốc chưa chạy thật: kết quả mong đợi chưa được kiểm trên hệ thống")
    bo = [k for k in state["case"] if k not in keys]

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
        moi = [k for k in keys if k not in state["case"]]
        xem = [k for k in keys if info[k]["st"].startswith(("Cần xem lại", "Test case đã sửa"))]
        moc_moi = {}
        for r in rows:
            f = cache[r["rel_dir"]]
            ma_h = {c: [f["cur"][c]["hash"], f["cur"].get(c, {}).get("ba_hash")] for c in f["tcs"][r["tc"]]["ma"] if c in f["cur"]}
            moc_moi[r["key"]] = dict(r=row_hash(f, r["tc"]), ma=ma_h)
        loai = "Cập nhật" if HANG_LS.search(text.split(LS_START)[-1]) else "Tạo"
        ghi = []
        if moi and loai != "Tạo":
            ghi.append("thêm " + ", ".join(moi))
        if xem:
            ghi.append("xem lại/sửa " + ", ".join(xem))
        if bo:
            ghi.append("bỏ " + ", ".join(bo))
        nd = a.mo_ta.strip() + (f" ({'; '.join(ghi)})" if ghi else "")
        e = dict(commit_goc=tv.git("rev-parse", "--short", "HEAD") or None, chua_commit=bool(tv.git("status", "--porcelain")))
        hang_moi = f"| {tv.fmt_dt(now_iso, today)} | {loai} | {a.nguoi} | {nd} | {len(rows)} case · {tong:g} phút | {tv.fmt_commit(e)} |"
        info = {k: dict(st="Còn đúng", doi=[], ma=v["ma"]) for k, v in info.items()}
        bo = []
        ghi_file(sm_p, text, rows, info, cache, du_an_dir, moc_moi, hang_moi)

    cnt = {}
    for i in info.values():
        k = i["st"].split(" (")[0]
        cnt[k] = cnt.get(k, 0) + 1
    print(f"[{a.lenh}] {a.du_an}/smoke-test.md: {len(rows)} case, {tong:g} phút ước lượng; " + ", ".join(f"{k} {v}" for k, v in sorted(cnt.items())))
    viec = [r for r in rows if info[r["key"]]["st"] != "Còn đúng"]
    for r in viec:
        i = info[r["key"]]
        print(f"  - Dòng {r['n']} ({r['key']}): {i['st']}" + (f" — đổi {', '.join(i['doi'])}" if i["doi"] else ""))
    lg = luot_gan_nhat(text)
    if lg and a.lenh == "kiem":
        print(f"  Lượt chạy gần nhất: {lg}")
    for k in bo:
        print(f"  - {k}: đã bỏ khỏi smoke")
    for p in problems:
        print("  !", p)
    for p in luu_y:
        print("  (lưu ý)", p)
    if a.lenh == "kiem" and (viec or bo or problems):
        sys.exit(1)


if __name__ == "__main__":
    main()
