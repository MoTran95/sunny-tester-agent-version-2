#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Sinh test plan từ file nguồn + số liệu đọc từ tài liệu dự án + phiếu thông tin của người test.

  python -X utf8 .claude/skills/tao-test-plan/scripts/sinh-test-plan.py khoi-tao <dự-án>  # tạo test-plan-nguon.txt từ khuôn; ĐÃ CÓ thì KHÔNG ghi đè
  python -X utf8 .claude/skills/tao-test-plan/scripts/sinh-test-plan.py dat   <dự-án> khóa=giá trị ...  # ghi câu trả lời của người test vào test-plan-thong-tin.json (gộp, kiểm khóa, in cũ -> mới)
  python -X utf8 .claude/skills/tao-test-plan/scripts/sinh-test-plan.py sinh  <dự-án>   # ghi testing/<dự-án>/test-plan.md
  python -X utf8 .claude/skills/tao-test-plan/scripts/sinh-test-plan.py kiem  <dự-án>   # chỉ so: test-plan.md có khớp bản sinh không (mã 1 nếu lệch)
  python -X utf8 .claude/skills/tao-test-plan/scripts/sinh-test-plan.py gon   <dự-án>   # ghi test-plan-gon.md (bản gọn: bảng đầu + mục 1, 2, 3, 5, 9, 10)
  python -X utf8 .claude/skills/tao-test-plan/scripts/sinh-test-plan.py phieu <dự-án>   # ghi phiếu thông tin HTML để người test điền và tải file JSON

Vì sao có file nguồn: số liệu (số test case, mã requirement, bộ smoke/regression, độ phủ) và câu trả lời của người test KHÔNG gõ tay vào test plan.
  testing/<dự-án>/test-plan-nguon.txt   Claude viết (khuôn: assets/mau-test-plan-nguon.txt); chứa các dấu {{...}}
  testing/<dự-án>/test-plan-thong-tin.json   câu trả lời của người test (khóa -> chữ); thiếu khóa thì ô để `……………`
  testing/<dự-án>/test-plan.md          SINH RA, không sửa tay (sửa nguồn hoặc JSON rồi chạy `sinh`); `kiem` báo lệch nếu ai sửa tay hoặc số liệu nguồn đã đổi

Dấu trong file nguồn:
  {{o:khoa}} hoặc {{o:khoa|khoa_du_phong}}   ô người test điền (lấy từ JSON; không có thì `……………`)
  {{tc:thu-muc-tinh-nang}}                   "43 case: [test-case.md](thu-muc/test-case.md)"
  {{smoke}} {{regression}} {{tong-case}}     số bộ case (đếm từ smoke-test.md, regression-test.md, các test-case.md)
  {{truy-vet}}                               bảng mục 10 (requirement, test case, case chưa có, smoke, regression Tầng 1, link truy vết)
  {{do-phu}}                                 câu độ phủ requirement
  {{n-chua-co-case}}                         tổng số mã requirement chưa có test case
"""
import argparse
import html
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))

BLANK = "……………"
TOKEN = re.compile(r"\{\{([^{}]+)\}\}")
GON_SECTIONS = {1, 2, 3, 5, 9, 10}
KHOA_FILE = Path(__file__).resolve().parents[1] / "references" / "khoa-thong-tin.json"


# ---------------------------------------------------------------- số liệu từ tài liệu dự án
def read(p):
    return p.read_text(encoding="utf-8")


def compress(nums):
    """[1,2,3,4,5,23,26] -> '001…005, 023, 026' (dải từ 3 mã liên tiếp trở lên)."""
    nums = sorted(set(nums))
    out, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        if j - i >= 2:
            out.append(f"{nums[i]:03d}…{nums[j]:03d}")
        else:
            out += [f"{n:03d}" for n in nums[i:j + 1]]
        i = j + 1
    return ", ".join(out)


def tc_list(nums):
    return f"TC-{compress(nums)}" if nums else ""


def facts(slug):
    from test_automation import docs_pages
    pdir = ROOT / "testing" / slug
    if not pdir.is_dir():
        sys.exit(f"Không có thư mục {pdir}")
    names = {}
    nf = pdir / "ten-tinh-nang.json"
    if nf.exists():
        names = json.loads(read(nf))
    index = docs_pages.build_code_index(slug)
    feats = []
    for d in sorted(x for x in pdir.iterdir() if x.is_dir() and (x / "test-case.md").exists()):
        n_tc = len(re.findall(r'^\|\s*<a id="tc-\d+"></a>', read(d / "test-case.md"), flags=re.M))
        f = dict(slug=d.name, name=names.get(d.name, d.name), n_tc=n_tc, n_srs=None, n_tl=None, uncovered=[], state=None, has_truyvet=False)
        tv = d / "truy-vet.md"
        if tv.exists():
            t = read(tv)
            f["has_truyvet"] = True
            m = re.search(r"Mã requirement: (\d+) trong SRS(?:, (\d+) câu trả lời)?", t)
            if m:
                f["n_srs"], f["n_tl"] = int(m.group(1)), int(m.group(2) or 0)
            m = re.search(r"Mã SRS chưa có test case nào: (.+)", t)
            if m and not m.group(1).strip().lower().startswith("không"):
                f["uncovered"] = [c.strip() for c in m.group(1).strip().rstrip(".").split(",") if c.strip()]
            m = re.search(r"Trạng thái test case: (.+)", t)
            f["state"] = m.group(1).strip().rstrip(".") if m else None
        feats.append(f)
    link = re.compile(r"\]\(([^)#\s]*?)([\w-]+)/test-case\.md#tc-(\d+)\)")
    smoke = dict(exists=False, rows=0, minutes=None, per={})
    sp = pdir / "smoke-test.md"
    if sp.exists():
        smoke["exists"] = True
        in_table = False
        for line in read(sp).splitlines():
            if line.startswith("| # | Smoke case |"):
                in_table = True
                continue
            if in_table:
                if not line.startswith("|"):
                    in_table = False
                elif re.match(r"^\| \d+ \|", line):
                    smoke["rows"] += 1
                    m = link.search(line)
                    if m:
                        smoke["per"].setdefault(m.group(2), []).append(int(m.group(3)))
            m = re.search(r"\*\*Tổng\*\* \| \*\*(\d+(?:,\d+)?)", line)
            if m:
                smoke["minutes"] = m.group(1)
    reg = dict(exists=False, t1=0, t2_vung=0, t2_case=0, per1={})
    rp = pdir / "regression-test.md"
    if rp.exists():
        reg["exists"] = True
        seen2 = set()
        in_table = False
        for line in read(rp).splitlines():
            if line.startswith("| Tầng | Vùng |"):
                in_table = True
                continue
            if not in_table:
                continue
            if not line.startswith("|"):
                break
            m = re.match(r"^\| (Tầng [12]) \|", line)
            if not m:
                continue
            ms = list(link.finditer(line))
            if m.group(1) == "Tầng 1":
                reg["t1"] += 1
                for x in ms:
                    reg["per1"].setdefault(x.group(2), []).append(int(x.group(3)))
            else:
                reg["t2_vung"] += 1
                for x in ms:
                    seen2.add((x.group(2), x.group(3)))
        reg["t2_case"] = len(seen2)
    return dict(pdir=pdir, feats=feats, smoke=smoke, reg=reg, index=index)


def rel_link(pdir, target):
    return os.path.relpath(target, pdir).replace("\\", "/")


# ---------------------------------------------------------------- mở rộng dấu
def expand(src, info, answers, used):
    pdir, feats = info["pdir"], info["feats"]
    total = sum(f["n_tc"] for f in feats)
    by = {f["slug"]: f for f in feats}

    def o(arg):
        keys = arg.split("|")
        used.add(keys[-1])   # phiếu chỉ hỏi khóa chung (cuối chuỗi dự phòng), không hỏi từng ô lịch
        for k in keys:
            v = (answers.get(k) or "").strip()
            if v:
                return v.replace("|", "\\|").replace("\n", " ")
        return BLANK

    def tc(slug):
        f = by.get(slug)
        if not f:
            sys.exit(f"{{{{tc:{slug}}}}}: không có tính năng '{slug}' có test-case.md")
        return f"{f['n_tc']} case: [test-case.md]({slug}/test-case.md)"

    def smoke():
        s = info["smoke"]
        if not s["exists"]:
            return "Chưa có `smoke-test.md`"
        t = f"[smoke-test.md](smoke-test.md): {s['rows']} case"
        return t + (f", khoảng {s['minutes']} phút" if s["minutes"] else "")

    def regression():
        r = info["reg"]
        if not r["exists"]:
            return "Chưa có `regression-test.md`"
        return (f"[regression-test.md](regression-test.md): Tầng 1 ({r['t1']} case lõi), Tầng 2 ({r['t2_vung']} vùng, {r['t2_case']} case), "
                f"Tầng 3 (toàn bộ {total} case)")

    def n_unc():
        return str(sum(len(f["uncovered"]) for f in feats))

    def do_phu():
        parts = []
        for f in feats:
            if f["n_srs"]:
                parts.append(f"{f['name']} {f['n_srs'] - len(f['uncovered'])}/{f['n_srs']}")
        return "; ".join(parts) + " mã requirement có test case" if parts else "Chưa có số liệu truy vết"

    def truy_vet():
        rows = ["| Tính năng | Requirement | Test case | Chưa có test case | Smoke | Regression Tầng 1 | Truy vết |", "|---|---|---|---|---|---|---|"]
        for f in feats:
            req = f"{f['n_srs']} mã, {f['n_tl']} câu trả lời của BA" if f["n_srs"] is not None else "Chưa có truy vết"
            unc = ", ".join(
                (f"[{c}]({rel_link(pdir, info['index'][(f['slug'], c)][0])}#{info['index'][(f['slug'], c)][1]})" if (f["slug"], c) in info["index"] else c)
                for c in f["uncovered"]) or "Không có"
            sm = info["smoke"]["per"].get(f["slug"], [])
            r1 = info["reg"]["per1"].get(f["slug"], [])
            rows.append(f"| {f['name']} | {req} | {f['n_tc']} | {unc} | {(str(len(sm)) + ' ca (' + tc_list(sm) + ')') if sm else '—'} | "
                        f"{(str(len(r1)) + ' ca (' + tc_list(r1) + ')') if r1 else '—'} | {'[mở](' + f['slug'] + '/truy-vet.md)' if f['has_truyvet'] else '—'} |")
        return "\n".join(rows)

    def one(m):
        tok = m.group(1).strip()
        if tok.startswith("o:"):
            return o(tok[2:])
        if tok.startswith("tc:"):
            return tc(tok[3:])
        simple = {"smoke": smoke, "regression": regression, "tong-case": lambda: str(total), "do-phu": do_phu,
                  "n-chua-co-case": n_unc, "truy-vet": truy_vet}
        if tok not in simple:
            sys.exit(f"Dấu không biết: {{{{{tok}}}}}")
        return simple[tok]()

    return TOKEN.sub(one, src)


def load_answers(slug, ten="test-plan"):
    p = ROOT / "testing" / slug / f"{ten}-thong-tin.json"
    if not p.exists():
        return {}
    data = json.loads(read(p))
    return {k: v for k, v in data.items() if not k.startswith("_")}


def render(slug, ten="test-plan"):
    nguon = ROOT / "testing" / slug / f"{ten}-nguon.txt"
    if not nguon.exists():
        sys.exit(f"Chưa có {nguon}. Sao `.claude/skills/tao-test-plan/assets/mau-test-plan-nguon.txt` sang đó rồi điền (xem SKILL.md bước 3).")
    info = facts(slug)
    used = set()
    src = re.sub(r"\A<!--.*?-->\s*", "", read(nguon), flags=re.S)   # khối chú thích hướng dẫn đầu file nguồn không vào bản sinh
    text = expand(src, info, load_answers(slug, ten), used)
    return text.strip("\n") + "\n", info, used   # bỏ cả dòng trống đầu file (sau khi xóa khối chú thích)


def gon(text, ten="test-plan"):
    """Giữ phần trước mục 1 (tiêu đề + bảng đầu) và các mục trong GON_SECTIONS, giữ số mục của bản đầy đủ."""
    parts = re.split(r"(?m)^(?=## \d+\. )", text)
    out = [parts[0].rstrip("\n") + "\n\n*Bản gọn của kế hoạch đầy đủ ([bản đầy đủ](" + ten + ".md)); các mục giữ số của bản đầy đủ để dễ đối chiếu.*\n"]
    for p in parts[1:]:
        n = int(re.match(r"## (\d+)\.", p).group(1))
        if n in GON_SECTIONS:
            out.append(p.rstrip("\n") + "\n")
    return "\n".join(out)


# ---------------------------------------------------------------- phiếu thông tin
def phieu(slug, used_keys, answers, ten="test-plan"):
    meta = json.loads(read(KHOA_FILE))
    groups = {"A": "A. Yêu cầu của đợt test", "B": "B. Tiêu chí kết thúc (do sếp hoặc công ty quyết)", "C": "C. Người và lịch", "D": "D. Môi trường và công cụ", "Z": "Khác"}
    by_group = {}
    for k in sorted(used_keys, key=lambda x: (meta.get(x, {}).get("thu_tu", 999), x)):
        g = meta.get(k, {}).get("nhom", "Z")
        by_group.setdefault(g, []).append(k)
    e = html.escape
    body = []
    for g in sorted(by_group):
        body.append(f"<h2>{e(groups.get(g, g))}</h2>")
        for k in by_group[g]:
            m = meta.get(k, {})
            val = answers.get(k, "")
            body.append(f'<label><span class="q">{e(m.get("nhan", k))}</span>' + (f'<span class="g">{e(m["goi_y"])}</span>' if m.get("goi_y") else "") +
                        f'<input type="text" data-k="{e(k)}" value="{e(val)}" placeholder="Chưa biết thì để trống"></label>')
    page = f"""<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Phiếu thông tin test plan — {e(slug)}</title><style>
body{{font:16px/1.55 "Segoe UI",Arial,sans-serif;background:#faf6ee;color:#3a2f27;margin:0}}main{{max-width:860px;margin:0 auto;padding:28px 18px 60px}}
h1{{font-size:26px;margin:0 0 6px}}h2{{font-size:18px;margin:30px 0 10px;border-top:1px solid #ddd0bd;padding-top:14px}}p.n{{color:#6b5b4e;margin:0 0 8px}}
label{{display:block;margin:0 0 14px}}.q{{display:block;font-weight:600}}.g{{display:block;font-size:13.5px;color:#6b5b4e}}
input{{width:100%;box-sizing:border-box;margin-top:4px;padding:9px 12px;border:1px solid #cdbfab;border-radius:8px;font:inherit;background:#fff}}
button{{padding:10px 20px;border:0;border-radius:999px;background:#d9603f;color:#fff;font:600 16px inherit;cursor:pointer}}
</style></head><body><main><h1>Phiếu thông tin cho test plan</h1>
<p class="n">Dự án: <b>{e(slug)}</b>. Điền những gì bạn đã biết, chỗ nào chưa biết thì để trống (test plan sẽ giữ ô trống để điền sau).</p>
<p class="n">Bấm <b>Tải file</b>, lưu file <code>{e(ten)}-thong-tin.json</code> vào thư mục <code>testing/{e(slug)}/</code> rồi nhờ Claude chạy lại test plan (hoặc tự chạy lệnh sinh).</p>
{''.join(body)}
<p><button type="button" id="tai">Tải file</button></p></main>
<script>document.getElementById('tai').onclick=function(){{var o={{}};document.querySelectorAll('input[data-k]').forEach(function(i){{var v=i.value.trim();if(v)o[i.dataset.k]=v}});
var b=new Blob([JSON.stringify(o,null,2)],{{type:'application/json'}});var a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='{ten}-thong-tin.json';a.click()}};</script></body></html>"""
    out = ROOT / "testing" / slug / f"{ten}-phieu.html"
    out.write_text(page, encoding="utf-8")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("lenh", choices=["khoi-tao", "dat", "sinh", "kiem", "gon", "phieu"])
    ap.add_argument("project")
    ap.add_argument("pairs", nargs="*", help="với lệnh dat: các cặp khóa=giá trị")
    ap.add_argument("--ten", default="test-plan", help="tên file không đuôi, ví dụ test-plan-1.4.0 để giữ nhiều bản; mặc định test-plan")
    a = ap.parse_args()
    pdir = ROOT / "testing" / a.project
    if a.lenh == "khoi-tao":
        dst = pdir / f"{a.ten}-nguon.txt"
        if dst.exists():
            print(f"Đã có {dst}: KHÔNG ghi đè. Sửa trực tiếp file đó rồi chạy `sinh`.")
            return 0
        if not pdir.is_dir():
            sys.exit(f"Không có thư mục {pdir}")
        dst.write_text(read(Path(__file__).resolve().parents[1] / "assets" / "mau-test-plan-nguon.txt"), encoding="utf-8", newline="\n")
        print(f"Đã tạo {dst} từ khuôn. Thay các chỗ <…> bằng nội dung từ tài liệu dự án.")
        return 0
    if a.lenh == "dat":
        meta = json.loads(read(KHOA_FILE))
        jf = pdir / f"{a.ten}-thong-tin.json"
        cur = json.loads(read(jf)) if jf.exists() else {}
        if not a.pairs:
            sys.exit("Cú pháp: dat <dự-án> khóa=giá trị [khóa=giá trị …]. Khóa hợp lệ: " + ", ".join(sorted(meta)) + ", lN_bd, lN_han (N = 1..7)")
        for pr in a.pairs:
            if "=" not in pr:
                sys.exit(f"'{pr}' không có dạng khóa=giá trị")
            k, v = pr.split("=", 1)
            k = k.strip()
            if k not in meta and not re.fullmatch(r"l\d+_(bd|han)", k):
                sys.exit(f"Khóa không biết: {k}. Khóa hợp lệ: " + ", ".join(sorted(meta)) + ", lN_bd, lN_han")
            old = cur.get(k)
            if v.strip():
                cur[k] = v.strip()
            else:
                cur.pop(k, None)
            print(f"{k}: {old!r} -> {cur.get(k)!r}")
        jf.write_text(json.dumps(cur, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        print(f"Đã ghi {jf}. Đọc lại các dòng trên cho người test xác nhận, rồi chạy `sinh`.")
        return 0
    text, info, used = render(a.project, a.ten)
    if a.lenh == "sinh":
        (pdir / f"{a.ten}.md").write_text(text, encoding="utf-8", newline="\n")
        left = text.count(BLANK)
        print(f"Đã ghi {pdir / (a.ten + '.md')} ({left} ô còn `{BLANK}`)")
        for f in info["feats"]:
            if f["state"] and not f["state"].startswith("Còn đúng"):
                print(f"LƯU Ý: truy vết {f['slug']} đang '{f['state']}': chạy truy-vet.py kiem trước khi tin số liệu")
    elif a.lenh == "kiem":
        cur = pdir / f"{a.ten}.md"
        if not cur.exists() or read(cur).replace("\r\n", "\n") != text:
            print(f"LỆCH: {a.ten}.md khác bản sinh từ nguồn (có người sửa tay, hoặc số liệu/câu trả lời đã đổi). Chạy lại `sinh`; muốn đổi nội dung thì sửa test-plan-nguon.txt hoặc test-plan-thong-tin.json.")
            return 1
        print(f"Khớp: {a.ten}.md đúng bản sinh từ nguồn, số liệu và câu trả lời.")
    elif a.lenh == "gon":
        (pdir / f"{a.ten}-gon.md").write_text(gon(text, a.ten), encoding="utf-8", newline="\n")
        print(f"Đã ghi {pdir / (a.ten + '-gon.md')}")
    else:
        print(f"Đã ghi {phieu(a.project, used, load_answers(a.project, a.ten), a.ten)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
