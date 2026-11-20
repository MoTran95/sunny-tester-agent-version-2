"""Trang HTML dễ xem cho file bug (`testing/<dự-án>/<tính-năng>/bug/BUG-nnn.md`).

- Mỗi mục là một thẻ có nút "Sao chép" (chép chữ thường của mục đó); nút "Sao chép cả bug" chép nguyên file md.
- Ảnh bằng chứng hiện thành ảnh nhỏ; ảnh tên có `-loi` (đã tô đỏ chỗ lỗi) có viền đỏ.
- Chữ `[Giả định: …]` được tô vàng để người duyệt thấy ngay.
File HTML nằm cạnh file md, tự sinh (đừng sửa tay): `python scripts/build_report.py build` hoặc `bug-pages`.
"""
import html
import os
import re
from pathlib import Path

from . import report as report_mod
from . import theme as theme_mod
from . import config

_CSS_BUG = """
.bar{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin:0 0 22px}
.btn{background:var(--card);color:var(--body);border:1px solid var(--line);border-radius:999px;padding:8px 16px;font:700 13px/1 inherit;font-family:inherit;cursor:pointer}
.btn:hover{border-color:var(--coral);color:var(--coral)}
.btn.chinh{background:var(--coral);border-color:var(--coral);color:#fff}
.btn.nho{padding:5px 12px;font-size:12px}
.chips{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:0 0 22px}
.chip{font-size:13px;color:var(--muted)}.chip b{color:var(--text)}
section.muc{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 22px;margin:0 0 14px}
section.muc header{display:flex;justify-content:space-between;align-items:center;gap:12px;margin:0 0 6px}
section.muc h2{margin:0;font-size:18px}
section.muc p{margin:8px 0}section.muc ul,section.muc ol{margin:8px 0;padding-left:22px}section.muc li{margin:4px 0}
blockquote{margin:0 0 20px;padding:10px 16px;border-left:4px solid var(--amber);background:var(--amberbg);color:var(--amberfg);border-radius:0 10px 10px 0}
.gd{background:var(--amberbg);color:var(--amberfg);border:1px solid var(--warnline);border-radius:6px;padding:0 6px;font-size:14px}
li.tick{list-style:none;margin-left:-22px}li.tick .o{display:inline-block;width:1.4em}
.anh{display:block;margin:4px 0;max-width:250px;border:1px solid var(--line);border-radius:8px}
.gal{display:flex;flex-wrap:wrap;gap:6px 18px;margin:6px 0 4px}.gal a{display:block}
.anh.loi{border:3px solid #E5252A}
.vid{display:block;max-width:420px;border-radius:8px;background:#000}
.nhan-loi{display:inline-block;background:#E5252A;color:#fff;font-size:11px;font-weight:700;padding:2px 7px;border-radius:5px;margin-right:6px}
.toast{position:fixed;left:50%;bottom:24px;transform:translateX(-50%);background:var(--text);color:var(--bg);padding:9px 18px;border-radius:999px;font-size:14px;opacity:0;transition:opacity .2s;pointer-events:none}
.toast.hien{opacity:1}
"""

_JS_COPY = """
function sao(btn){var t=btn.getAttribute('data-copy');var done=function(){var z=document.getElementById('toast');z.textContent='Đã sao chép';z.classList.add('hien');setTimeout(function(){z.classList.remove('hien')},1400)};
if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(t).then(done,function(){du(t,done)})}else{du(t,done)}}
function du(t,done){var a=document.createElement('textarea');a.value=t;a.style.position='fixed';a.style.opacity='0';document.body.appendChild(a);a.select();try{document.execCommand('copy');done()}catch(e){}document.body.removeChild(a)}
"""


def _plain_text(line):
    """Dòng md → chữ thường để dán (bỏ ** và dấu huyền, [chữ](đường dẫn) → chữ (đường dẫn))."""
    line = re.sub(r"\*\*(.+?)\*\*", r"\1", line)
    line = re.sub(r"`([^`]*)`", r"\1", line)
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: m.group(1) if m.group(2).startswith("#") else f"{m.group(1)} ({m.group(2)})", line)


def _md_to_html(url, bug_dir):
    """Link tới file md của repo (SRS, test case, bug khác…) → trang HTML sinh từ nó, giữ nguyên phần #neo."""
    if re.match(r"^(https?:|mailto:|#)", url):
        return url
    path, sep, frag = url.partition("#")
    if path.endswith(".md") and (Path(bug_dir) / path).resolve().exists():
        return path[:-3] + ".html" + sep + frag
    return url


def _inline(line, bug_dir):
    e = html.escape(line, quote=False)
    e = re.sub(r"\[Giả định: (.+?)\]", lambda m: f'<span class="gd">Giả định: {m.group(1)}</span>', e)
    e = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", e)
    e = re.sub(r"`([^`]+)`", r"<code>\1</code>", e)
    e = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: f'<a href="{html.escape(_md_to_html(m.group(2), bug_dir))}">{m.group(1)}</a>', e)
    return e


def _images_in_line(line, bug_dir):
    """Tìm đường dẫn ảnh (tính từ gốc repo) trong dòng; trả về HTML ảnh nhỏ (viền đỏ nếu tên có -loi)."""
    out = []
    for m in re.finditer(r"`?((?:evidence|docs)/[^\s`]+?\.(?:png|webm))`?", line):
        from_root = m.group(1)
        f = config.ROOT / from_root
        rel = os.path.relpath(f, bug_dir).replace("\\", "/")
        if from_root.endswith(".webm"):
            # Video nằm trong `evidence/**/video/` (gitignore, chỉ có ở máy đã chạy test): vẫn nhúng dù file chưa có,
            # để trang sinh ra giống hệt ở mọi máy (nếu chọn theo file có thật thì máy khác sinh lại sẽ mất khung video).
            out.append(f'<div><video class="vid" controls preload="metadata" src="{html.escape(rel)}"></video><div class="small">Video: {html.escape(Path(from_root).name)}</div></div>')
            continue
        if not f.exists():
            continue
        if "-kiem" in Path(from_root).name:
            out.append(f'<a href="{html.escape(rel)}" target="_blank" rel="noopener"><span class="nhan-loi" style="background:#1B8F3A">Ảnh kiểm tra</span>'
                       f'<img class="anh" style="border:3px solid #1B8F3A" src="{html.escape(rel)}" alt="{html.escape(Path(from_root).name)}"></a>')
            continue
        error = "-loi" in Path(from_root).name
        out.append(f'<a href="{html.escape(rel)}" target="_blank" rel="noopener">'
                  f'{"<span class=nhan-loi>Tô đỏ chỗ lỗi</span>" if error else ""}<img class="anh{" loi" if error else ""}" src="{html.escape(rel)}" alt="{html.escape(Path(from_root).name)}"></a>')
    return f'<div class="gal">{"".join(out)}</div>' if out else ""


def render_section(md_lines, bug_dir):
    """Danh sách dòng md của một mục → (html thân, chữ thuong để sao chép)."""
    out, plain, goto = [], [], None  # mo: 'ul' | 'ol' | None

    def close_list():
        nonlocal goto
        if goto:
            out.append(f"</{goto}>")
            goto = None

    for line in md_lines:
        t = line.rstrip()
        if not t.strip():
            close_list()
            continue
        m_tick = re.match(r"^- \[( |x)\] (.*)$", t)
        m_ul = re.match(r"^- (.*)$", t)
        m_ol = re.match(r"^\d+\. (.*)$", t)
        if m_tick or m_ul or m_ol:
            kind = "ol" if m_ol else "ul"
            if goto != kind:
                close_list()
                out.append(f"<{kind}>")
                goto = kind
            content = (m_tick or m_ul or m_ol).groups()[-1]
            images = _images_in_line(content, bug_dir)
            if m_tick:
                sign = "☑" if m_tick.group(1) == "x" else "☐"
                out.append(f'<li class="tick"><span class="o">{sign}</span>{_inline(content, bug_dir)}{images}</li>')
            else:
                out.append(f"<li>{_inline(content, bug_dir)}{images}</li>")
            plain.append(("- " if m_ul or m_tick else re.match(r"^\d+\. ", t).group(0)) + _plain_text(content))
        else:
            close_list()
            out.append(f"<p>{_inline(t, bug_dir)}</p>")
            plain.append(_plain_text(t))
    close_list()
    return "".join(out), "\n".join(plain).strip()


# Trạng thái bug do người dùng chốt, ghi ở mục `## Trạng thái` của file bug (xem skill lap-ke-hoach-retest, script dat-trang-thai-bug.py).
# Công cụ của team vẫn là bản chính thức; mục này là bản ghi lại trong kho để báo cáo tổng kết đọc.
BUG_STATUSES = {"Mở": "bad", "Chờ re-test": "warn", "Mở lại": "bad", "Đóng": "ok"}
STATUS_UNSET = "Chưa ghi"


def read_status(md_text):
    """(trạng thái, chi tiết) từ mục `## Trạng thái` của file bug; không có mục thì (STATUS_UNSET, '')."""
    m = re.search(r"^## Trạng thái\s*\n+\s*\*\*([^*]+?)\.?\*\*[ \t]*([^\n]*)", md_text, re.M)
    if not m:
        return STATUS_UNSET, ""
    return m.group(1).strip(), m.group(2).strip()


def status_badge(status):
    cls = BUG_STATUSES.get(status, "gray")
    return f'<span class="badge {cls}">{html.escape(status)}</span>'


def _section_badge(title, content):
    """Severity/Priority: lấy chữ in đậm đầu tiên làm huy hiệu."""
    m = re.search(r"\*\*([^*]+?)\.?\*\*", content)
    if not m:
        return ""
    v = m.group(1).strip()
    cls = "bad" if v.lower() in ("critical", "major", "cao", "nghiêm trọng", "lớn", "nặng") else "warn" if v.lower() in ("minor", "trung bình", "nhỏ") else "gray"
    return f'<span class="chip">{html.escape(title)}: <span class="badge {cls}">{html.escape(v)}</span></span>'


def render_one(md_path):
    md = Path(md_path)
    line = md.read_text(encoding="utf-8").splitlines()
    heading = next((d[2:].strip() for d in line if d.startswith("# ")), md.stem)
    bug_code = md.stem
    # tách mục
    preamble, section, current = [], [], None
    for d in line:
        if d.startswith("# "):
            continue
        if d.startswith("## "):
            current = [d[3:].strip(), []]
            section.append(current)
        elif current is None:
            preamble.append(d)
        else:
            current[1].append(d)
    e = html.escape
    parts = md.resolve().parts
    project = parts[parts.index("testing") + 1] if "testing" in parts else None
    chips = []
    for title, content in section:
        if title in ("Mức độ nghiêm trọng", "Severity"):
            chips.append(_section_badge("Mức độ nghiêm trọng", "\n".join(content)))
        elif title in ("Mức độ ưu tiên đề xuất", "Priority đề xuất"):
            chips.append(_section_badge("Mức độ ưu tiên", "\n".join(content)))
        elif title == "Trạng thái":
            st = read_status(md.read_text(encoding="utf-8"))[0]
            chips.insert(0, f'<span class="chip">Trạng thái: {status_badge(st)}</span>')
        elif title == "Tần suất":
            chips.append(f'<span class="chip">Tần suất: <b>{e(_plain_text(" ".join(x for x in content if x.strip())).rstrip("."))}</b></span>')
    p = ['<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">',
         f"<title>{e(bug_code)} {e(_plain_text(heading))}</title>",
         theme_mod.font_head(md.parent),
         f"<style>{report_mod._CSS}{_CSS_BUG}</style><script>{report_mod._JS_THEME}{_JS_COPY}</script></head><body>"
         '<button id="theme" class="theme" type="button">Chế độ tối</button><main>',
         theme_mod.brand_html(project),
         f'<p class="eyebrow">Bug report · {e(bug_code)}</p>',
         f"<h1 style=\"font-size:30px\">{e(_plain_text(heading))}</h1>",
         f'<div class="chips">{"".join(chips)}</div>',
         f'<div class="bar"><button class="btn chinh" type="button" onclick="sao(this)" data-copy="{e(_plain_text(heading))}">Sao chép tiêu đề</button>'
         f'<button class="btn" type="button" onclick="sao(this)" data-copy="{e(md.read_text(encoding="utf-8"))}">Sao chép cả bug (md)</button></div>']
    assumption, _ = render_section([d for d in preamble if d.strip()], md.parent)
    if assumption:
        p.append(f"<blockquote>{assumption}</blockquote>")
    for title, content in section:
        body_html, plain = render_section(content, md.parent)
        p.append(f'<section class="muc"><header><h2>{e(title)}</h2>'
                 f'<button class="btn nho" type="button" onclick="sao(this)" data-copy="{e(title + chr(10) + plain)}">Sao chép</button></header>{body_html}</section>')
    p.append('<div id="toast" class="toast"></div></main></body></html>')
    return md.with_suffix(".html"), "".join(p)


def build_one(md_path):
    out, text = render_one(md_path)
    out.write_text(text, encoding="utf-8")
    return out


def render_all(cfg):
    """{đường dẫn html: nội dung} của mọi file bug (chưa ghi)."""
    return dict(render_one(f) for f in sorted(cfg.project_dir.glob("**/bug/BUG-*.md")))


def build_all(cfg):
    return [build_one(f) for f in sorted(cfg.project_dir.glob("**/bug/BUG-*.md"))]
