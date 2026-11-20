"""Thanh điều hướng dùng chung cho mọi trang HTML của một dự án (người dùng chốt 2026-11-20).

Ba lớp:
  1. Trang con: thanh cố định trên cùng có `← Trang tổng` (nhảy đúng thẻ tính năng), đường dẫn Dự án › Tính năng › Trang,
     và menu nhảy nhanh tới Smoke / Regression / Test plan / Tổng kết / Hướng dẫn trên trang tổng.
  2. Trang con: dải tab chuyển giữa các trang cùng tính năng (hoặc cùng nhóm bộ test ở cấp dự án).
  3. Trang tổng: thanh menu ngang cố định (nút ☰ khi màn hẹp) + nút "↑ Lên đầu".

Khối được chèn ngay sau `<body>` giữa hai dấu `<!--dh-->` … `<!--/dh-->` nên chạy lại nhiều lần vẫn một khối.
Dùng biến màu có giá trị dự phòng để chạy cả trên báo cáo khám phá (CSS riêng, không có biến chung).
"""
import html
import os
import re
from pathlib import Path

from . import config

START, END = "<!--dh-->", "<!--/dh-->"
_STRIP = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
_BODY = re.compile(r"<body[^>]*>", re.I)
_TITLE = re.compile(r"<title>(.*?)</title>", re.S | re.I)

_CSS = (
    ".dh{position:sticky;top:0;z-index:4;background:var(--card,#F2EDE5);border-bottom:1px solid var(--line,#D1C9BB);"
    "font:14px/1.3 'Be Vietnam Pro',system-ui,sans-serif;color:var(--body,#463B34);padding:8px 140px 8px 16px;box-sizing:border-box}"
    ".dh *{box-sizing:border-box}.dh a,.dh b{text-decoration:none;white-space:nowrap}"
    ".dh-r{display:flex;align-items:center;gap:8px 14px;flex-wrap:wrap}"
    ".dh-back{padding:5px 12px;border-radius:999px;background:var(--coral,#C24E3A);color:#fff!important;font-weight:700}"
    ".dh-crumb{color:var(--muted,#6F6154);display:flex;flex-wrap:wrap;gap:0 6px;min-width:0}"
    ".dh-crumb a{color:var(--body,#463B34)}.dh-crumb a:hover{color:var(--coral,#C24E3A)}.dh-crumb b{color:var(--text,#3A2E26)}"
    ".dh-menu{display:flex;gap:4px 14px;flex-wrap:wrap;margin-left:auto}"
    ".dh-menu a{color:var(--body,#463B34);padding:3px 0;border-bottom:2px solid transparent}.dh-menu a:hover{color:var(--coral,#C24E3A);border-bottom-color:var(--coral,#C24E3A)}"
    ".dh-tabs{display:flex;gap:6px;overflow-x:auto;padding:8px 0 2px;margin-top:6px;border-top:1px dashed var(--line,#D1C9BB)}"
    ".dh-tabs a,.dh-tabs b{padding:4px 12px;border-radius:999px;border:1px solid var(--line,#D1C9BB);background:var(--bg,#E8DFD0);color:var(--body,#463B34);font-size:13px;flex:none}"
    ".dh-tabs b{background:var(--coral,#C24E3A);border-color:var(--coral,#C24E3A);color:#fff}.dh-tabs a:hover{border-color:var(--coral,#C24E3A);color:var(--coral,#C24E3A)}"
    ".dh-burger{display:none;margin-left:auto;padding:5px 12px;border:1px solid var(--line,#D1C9BB);border-radius:999px;background:var(--bg,#E8DFD0);color:inherit;font:inherit;cursor:pointer}"
    ".dh-top{position:fixed;right:18px;bottom:18px;z-index:6;display:none;padding:9px 14px;border:1px solid var(--line,#D1C9BB);border-radius:999px;background:var(--card,#F2EDE5);color:var(--body,#463B34);font:700 13px/1 inherit;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.2)}"
    "[id]{scroll-margin-top:96px}nav.top{top:var(--dh-h,0)!important}"
    "@media (max-width:760px){.dh{padding-right:130px}.dh-burger{display:inline-block}.dh-menu{display:none;width:100%;margin:6px 0 0}.dh.mo .dh-menu{display:flex}.dh-crumb{display:none}}"
    "@media print{.dh,.dh-top{display:none!important}}"
)
_JS = ("(function(){var d=document,t=d.getElementById('dh-top'),b=d.getElementById('dh-bg'),h=d.querySelector('.dh');"
       "if(b)b.onclick=function(){h.classList.toggle('mo')};"
       "function dat(){d.documentElement.style.setProperty('--dh-h',h.offsetHeight+'px')}dat();addEventListener('resize',dat);addEventListener('load',dat);if(b)b.addEventListener('click',dat);"
       "if(t){addEventListener('scroll',function(){t.style.display=scrollY>400?'block':'none'});t.onclick=function(){scrollTo({top:0,behavior:'smooth'})}}})();")


def _rel(from_dir, target):
    return os.path.relpath(target, from_dir).replace("\\", "/")


def context(project, path):
    """(loại, tính năng) của một trang: loại 'tong' | 'tinh-nang' | 'du-an' | None (không thuộc dự án)."""
    root = config.ROOT
    try:
        parts = Path(path).resolve().relative_to(root.resolve()).parts
    except ValueError:
        return None, None
    if len(parts) < 3 or parts[1] != project or "_src" in parts:
        return None, None
    top = parts[0]
    if top == "testing":
        if len(parts) == 3:
            return ("tong", None) if parts[2] == "index.html" else ("du-an", None)
        return "tinh-nang", parts[2]
    if top == "srs":
        return "tinh-nang", Path(parts[2]).stem
    if top == "evidence" and len(parts) >= 5 and parts[2] == "features":
        return "tinh-nang", parts[3]
    return None, None


def _tdir(project):
    return config.ROOT / "testing" / project


def _menu_items(project, exists):
    """Mục menu nhảy nhanh tới trang tổng: (nhãn, điểm neo), chỉ mục có thật."""
    t = _tdir(project)
    items = [("Từng tính năng", "tinh-nang")]
    if exists(t / "smoke-test.html"):
        items.append(("Smoke", "smoke"))
    if exists(t / "regression-test.html"):
        items.append(("Regression", "regression"))
    if any(exists(p) for p in t.glob("test-plan*.html")) or any(t.glob("test-plan*.md")):
        items.append(("Test plan", "test-plan"))
    if exists(t / "test-summary-report.html"):
        items.append(("Tổng kết", "bao-cao-tong-ket"))
    items.append(("Hướng dẫn", "huong-dan"))
    return items


def _project_tabs(project, exists):
    """Tab cho trang ở cấp dự án (smoke, regression, test plan, tổng kết)."""
    t = _tdir(project)
    cand = [("Bộ smoke test", t / "smoke-test.html"), ("Kết quả smoke", t / "smoke-ket-qua.html"), ("Bộ regression test", t / "regression-test.html")]
    cand += [(f"Kết quả regression tầng {n}", t / f"regression-tang-{n}-ket-qua.html") for n in (1, 2, 3)]
    cand += [("Test plan", p) for p in sorted(t.glob("test-plan*.html")) if not p.stem.endswith("-phieu")]
    cand.append(("Báo cáo tổng kết kiểm thử", t / "test-summary-report.html"))
    return [(l, p) for l, p in cand if exists(p)]


def render(project, path, text, exists, names, feature_tabs):
    """Trả `text` đã chèn khối điều hướng (hoặc `text` nguyên vẹn nếu trang không thuộc dự án / là tài liệu gửi ngoài)."""
    text = _STRIP.sub("", text)
    kind, feature = context(project, path)
    if kind is None or Path(path).stem.startswith(("test-plan", "_template-test-plan")) or not _BODY.search(text):
        return text
    path = Path(path)
    here = path.parent
    e = html.escape
    index = _tdir(project) / "index.html"
    m = _TITLE.search(text)
    page_title = e(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip()) if m else e(path.stem)
    menu = "".join(f'<a href="{_rel(here, index)}#{a}">{e(l)}</a>' for l, a in _menu_items(project, exists))
    if kind == "tong":
        links = '<a href="#top">Tổng quan</a>' + "".join(f'<a href="#{a}">{e(l)}</a>' for l, a in _menu_items(project, exists))
        bar = (f'<div class="dh" id="top"><div class="dh-r"><b>{e(project)}</b><button class="dh-burger" id="dh-bg" type="button">☰ Menu</button>'
               f'<nav class="dh-menu" style="margin-left:14px">{links}</nav></div></div>')
    else:
        if kind == "tinh-nang":
            back = f"{_rel(here, index)}#tn-{feature}"
            fname = e(names.get(feature, feature))
            crumb = f'<a href="{_rel(here, index)}">{e(project)}</a> › <a href="{back}">{fname}</a> › <b>{page_title}</b>'
            tabs = feature_tabs(feature)
        else:
            back = _rel(here, index)
            crumb = f'<a href="{back}">{e(project)}</a> › <b>{page_title}</b>'
            tabs = _project_tabs(project, exists)
        tab_html = "".join(f"<b>{e(l)}</b>" if Path(p).resolve() == path.resolve() else f'<a href="{_rel(here, p)}">{e(l)}</a>' for l, p in tabs)
        bar = (f'<div class="dh"><div class="dh-r"><a class="dh-back" href="{back}">← Trang tổng</a>'
               f'<span class="dh-crumb">{crumb}</span><button class="dh-burger" id="dh-bg" type="button">☰ Menu</button><nav class="dh-menu">{menu}</nav></div>'
               + (f'<div class="dh-tabs">{tab_html}</div>' if tabs else "") + "</div>")
    block = f'{START}<style>{_CSS}</style>{bar}<button class="dh-top" id="dh-top" type="button">↑ Lên đầu</button><script>{_JS}</script>{END}'
    return _BODY.sub(lambda mo: mo.group(0) + block, text, count=1)
