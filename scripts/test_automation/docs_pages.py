"""Trang HTML dễ xem cho tài liệu markdown của dự án (SRS, bảng soát requirement, câu hỏi BA, checklist, test case, truy vết…)
và trang tổng `testing/<dự-án>/index.html` link tới mọi tài liệu, kết quả chạy và bug.

- File md vẫn là bản gốc (AI đọc md). HTML sinh ra cạnh file md, đừng sửa tay: chạy `python -X utf8 scripts/build_docs.py`.
- Không dùng AI để sinh: chỉ là chương trình đổi md sang HTML và đọc số liệu từ file có sẵn, nên xem hay cập nhật đều 0 token.
- Giao diện (màu, font, bảng rộng, chế độ tối) lấy từ `theme.py`, dùng chung cho mọi dự án và mọi máy.
- Mọi dòng, mọi dòng bảng, mọi mục danh sách có neo `id="L<số dòng md>"`, nên link kiểu `dang-nhap.md#L66` (truy vết) nhảy đúng chỗ.
- Mã requirement (S01-AC02, R06, M06, E20), câu trả lời BA (TL-07), mã câu hỏi BA (B15), mã test case (TC-014) tự thành link tới đúng dòng định nghĩa.
- `sync()` sinh lại mọi trang (tài liệu, kết quả chạy, trang bug, trang tổng) và so với file đang có; `--check` dùng để đảm bảo không bao giờ cũ.
"""
import html
import os
import re
from pathlib import Path

from . import bug_page, config, theme
from . import report as report_mod
from . import summary_report as summary_mod

GENERATOR = '<meta name="generator" content="build_docs.py">'
_CELL_SPLIT = re.compile(r"(?<!\\)\|")
STATUSES = {"Đạt": "ok", "Không đạt": "bad", "Bị chặn": "warn", "Bỏ qua": "gray", "Chưa chạy": "gray", "Đạt kèm ý phụ sai": "warn", "Đạt kèm lỗi đã biết": "warn"}

GUIDE_PAGES = ["bat-dau", "cai-dat-may-moi", "chay-test-tu-dong"]  # docs/<tên>.md hiện ở mục "Hướng dẫn và quy ước chung" của trang tổng

DOC_LABELS = [("srs", "SRS"), ("bang-soat-requirement", "Bảng phân tích requirement"), ("phan-tich-requirement", "Phân tích requirement"),
              ("cau-hoi-cho-ba", "Câu hỏi cho BA"), ("checklist", "Checklist"), ("test-case", "Test case"), ("truy-vet", "Truy vết"),
              ("ket-qua-test-case", "Kết quả chạy")]

CODE_DEF = re.compile(r"^(?:([A-Z]{2,6})-)?(S\d{2}-AC\d{2}|[RME]\d{2})$")
CODE_RE = re.compile(r"(?<![\w./#-])((?:[A-Z]{2,6}-)?S\d{2}-AC\d{2}|(?:[A-Z]{2,6}-)?[RME]\d{2}|TL-\d{2}|TC-\d{3}|[ABC]\d{1,2})(?![\w-])")


# ---------------------------------------------------------------- tìm tài liệu
def projects():
    """Các dự án có thư mục testing/<dự-án> (có auto-config.json hoặc test case)."""
    t = config.ROOT / "testing"
    return [d.name for d in sorted(t.iterdir()) if d.is_dir() and ((d / "auto-config.json").exists() or any(d.glob("*/test-case.md")))]


def collect_sources(project):
    """Danh sách file md cần đổi sang HTML của một dự án."""
    root = config.ROOT
    found = []
    found += sorted((root / "srs" / project).glob("*.md"))
    t = root / "testing" / project
    found += [f for f in sorted(t.glob("*.md")) if f.name not in ("smoke-ket-qua.md", "test-summary-report.md") and not f.name.endswith("-ket-qua.md")]
    for sub in sorted(x for x in t.iterdir() if x.is_dir()):
        found += [f for f in sorted(sub.glob("*.md")) if f.name != "ket-qua-test-case.md"]
    e = root / "evidence" / project
    if e.exists():
        for f in sorted(e.rglob("*.md")):
            if not {"_src", "screenshots", "chay-test"} & set(f.relative_to(e).parts):
                found.append(f)
    found += shared_sources()
    return found


def shared_sources():
    """File md dùng chung, không thuộc dự án nào: quy ước `srs/*.md`, chiến lược và khuôn `testing/*.md`, hướng dẫn `docs/*.md`."""
    root = config.ROOT
    return [f for d in ("srs", "testing", "docs") for f in sorted((root / d).glob("*.md"))]


def feature_of(src, project):
    if project is None:   # trang dùng chung sinh khi chưa có dự án nào
        return None
    parts = src.parts
    if "features" in parts:
        return src.parent.name
    if "testing" in parts and src.parent.parent.name == project:
        return src.parent.name
    if "srs" in parts:
        return src.stem
    return None


# ---------------------------------------------------------------- chỉ mục mã (mã → file + neo)
def _first_cell(line):
    cells = _split_row(line)
    return re.sub(r'<a id="?[\w.-]+"?></a>|`', "", cells[0]).strip() if cells else ""


def build_code_index(project):
    """{(tính năng, mã): (file md, neo)}: nơi mỗi mã được định nghĩa, để mọi trang link tới đúng dòng."""
    root = config.ROOT
    codes = {}

    def put(feature, code, md, anchor):
        codes.setdefault((feature, code), (md, anchor))

    for srs in sorted((root / "srs" / project).glob("*.md")):
        feature = srs.stem
        for n, line in enumerate(srs.read_text(encoding="utf-8").splitlines(), 1):
            if line.startswith("|"):
                cell = _first_cell(line)
                m = CODE_DEF.match(cell)
                if m:
                    put(feature, cell, srs, f"L{n}")
                    put(feature, m.group(2), srs, f"L{n}")
    t = root / "testing" / project
    for d in sorted(x for x in t.iterdir() if x.is_dir()):
        feature = d.name
        bs = d / "bang-soat-requirement.md"
        if bs.exists():
            for n, line in enumerate(bs.read_text(encoding="utf-8").splitlines(), 1):
                if line.startswith("|") and re.match(r"^TL-\d{2}$", _first_cell(line)):
                    put(feature, _first_cell(line), bs, f"L{n}")
        ch = d / "cau-hoi-cho-ba.md"
        if ch.exists():
            for m in re.finditer(r'<a id="([a-c]\d{1,2})"></a>', ch.read_text(encoding="utf-8")):
                put(feature, m.group(1).upper(), ch, m.group(1))
        tc = d / "test-case.md"
        if tc.exists():
            for m in re.finditer(r'<a id="(tc-\d{3})"></a>', tc.read_text(encoding="utf-8")):
                put(feature, m.group(1).upper(), tc, m.group(1))
    return codes


class DocCtx:
    """Ngữ cảnh khi đổi một file md: file nguồn, tập file được đổi, chỉ mục mã, dòng đang xử lý."""

    def __init__(self, src, converted, codes=None, feature=None):
        self.src, self.converted, self.codes, self.feature, self.line = src, converted, codes or {}, feature, 0
        self.is_srs = "srs" in src.parts

    def code_href(self, token):
        target = self.codes.get((self.feature, token))
        if not target or (self.is_srs and re.match(r"^[ABC]\d", token)):
            return None
        md, anchor = target
        if md.resolve() == self.src.resolve() and anchor == f"L{self.line}":
            return None  # dòng định nghĩa chính nó: không tự link
        rel = os.path.relpath(md.with_suffix(".html"), self.src.parent).replace("\\", "/")
        return f"{rel}#{anchor}"


# ---------------------------------------------------------------- markdown → HTML
def _slug(text):
    s = re.sub(r"[^\w\- ]", "", re.sub(r"[`*_\[\]()]", "", text).lower(), flags=re.U).strip().replace(" ", "-")
    return s or "muc"


def _fix_link(url, src, converted):
    if re.match(r"^(https?:|mailto:|#)", url):
        return url
    path, sep, frag = url.partition("#")
    if path.endswith(".md"):
        target = (src.parent / path).resolve()
        generated = target.exists() and (target.stem.startswith("BUG-") or target.name in ("smoke-ket-qua.md", "ket-qua-test-case.md") or target.name.startswith("regression-tang-"))  # trang do build_report/bug_page sinh
        if target in converted or generated:
            return path[:-3] + ".html" + (sep + frag if sep else "")
    return url


def render_inline(text, ctx):
    holders = []

    def hold(h):
        holders.append(h)
        return f"\x00{len(holders) - 1}\x00"

    def code_span(m):
        inner = m.group(1)
        href = ctx.code_href(inner.strip()) if CODE_RE.fullmatch(inner.strip()) else None
        body = html.escape(inner, quote=False)
        return hold(f'<code><a class="ma" href="{href}">{body}</a></code>' if href else f"<code>{body}</code>")

    text = re.sub(r"`([^`]+)`", code_span, text)
    text = re.sub(r"<br\s*/?>", lambda m: hold("<br>"), text, flags=re.I)
    text = re.sub(r'<a id="?([\w.-]+)"?></a>', lambda m: hold(f'<a id="{m.group(1)}"></a>'), text)
    text = html.escape(text, quote=False)
    text = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", lambda m: hold(f'<img class="anh-md" src="{m.group(2)}" alt="{m.group(1)}">'), text)
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)",
                  lambda m: hold(f'<a href="{_fix_link(m.group(2), ctx.src, ctx.converted).replace(chr(34), "%22")}">{m.group(1)}</a>'), text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![*\w])\*([^*\s][^*]*?)\*(?![*\w])", r"<em>\1</em>", text)
    text = re.sub(r"(?<![=\"\w/>])(https?://[^\s<)\x00]+[^\s<).,;\x00])", lambda m: f'<a href="{m.group(1)}">{m.group(1)}</a>', text)

    def link_code(m):
        href = ctx.code_href(m.group(1))
        return hold(f'<a class="ma" href="{href}">{m.group(1)}</a>') if href else m.group(0)

    text = CODE_RE.sub(link_code, text)
    while "\x00" in text:
        text = re.sub(r"\x00(\d+)\x00", lambda m: holders[int(m.group(1))], text)
    return text


def _cell_html(cell, ctx):
    plain = re.sub(r"`", "", cell).strip()
    if plain in STATUSES:
        return f'<span class="badge {STATUSES[plain]}">{html.escape(plain)}</span>'
    return render_inline(cell.strip(), ctx) or "—"


def _split_row(line):
    cells = _CELL_SPLIT.split(line.strip())
    if cells and cells[0] == "":
        cells = cells[1:]
    if cells and cells[-1].strip() == "":
        cells = cells[:-1]
    return [c.replace("\\|", "|") for c in cells]


def _render_table(rows, ctx):
    """rows: [(số dòng md, [ô])]; hàng 0 là tiêu đề, hàng 1 là dòng gạch ngăn."""
    header, body = rows[0][1], rows[2:]
    n = len(header)
    wide = n >= 6
    ctx.line = rows[0][0]
    empty_head = all(not h.strip() for h in header)
    out = [f'<div class="khu-bang" id="L{rows[0][0]}"><div class="wrap' + (" lon" if wide else "") + '"><table>']
    if not empty_head:
        out.append("<thead><tr>" + "".join(f"<th>{render_inline(h.strip(), ctx)}</th>" for h in header) + "</tr></thead>")
    out.append("<tbody>")
    for ln, r in body:
        ctx.line = ln
        cells = (r + [""] * n)[:n]
        out.append(f'<tr id="L{ln}">' + "".join(f'<td class="cot-nho">{_cell_html(c, ctx)}</td>' if wide else f"<td>{_cell_html(c, ctx)}</td>" for c in cells) + "</tr>")
    out.append('</tbody></table></div><div class="thanh-keo"><div></div></div></div>')
    return "".join(out)


_LIST_RE = re.compile(r"^(\s*)([-*]|\d+\.)\s+(.*)$")


def _render_list(items, ctx):
    """items: [(dòng, độ thụt, kiểu, chữ)] → HTML lồng nhau theo độ thụt."""
    out, stack = [], []
    for line, indent, kind, text in items:
        ctx.line = line
        tag = "ol" if kind[0].isdigit() else "ul"
        while stack and indent < stack[-1][0]:
            out.append(f"</li></{stack.pop()[1]}>")
        if stack and indent == stack[-1][0] and stack[-1][1] != tag:
            out.append(f"</li></{stack.pop()[1]}>")   # đổi kiểu danh sách ở cùng mức: mở danh sách mới
        if stack and indent == stack[-1][0]:
            out.append("</li>")
        elif not stack or indent > stack[-1][0]:
            stack.append((indent, tag))
            out.append(f"<{tag}>")
        out.append(f'<li id="L{line}">{render_inline(text, ctx)}')
    while stack:
        out.append(f"</li></{stack.pop()[1]}>")
    return "".join(out)


def render_markdown(md, src, converted, codes=None, feature=None):
    """→ (html thân trang, tiêu đề, [(mức, id, chữ)] của các đề mục)."""
    ctx = DocCtx(src, converted, codes, feature)
    lines = md.splitlines()
    out, heads, used, title = [], [], set(), ""
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        stripped = line.strip()
        ln = i + 1
        if not stripped:
            i += 1
            continue
        if stripped.startswith("<!--"):
            while i < len(lines) and "-->" not in lines[i]:
                i += 1
            i += 1
            continue
        if stripped.startswith("```"):
            i += 1
            code = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1
            out.append(f'<pre id="L{ln}"><code>{html.escape(chr(10).join(code), quote=False)}</code></pre>')
            continue
        m = re.match(r'^<a id="?([\w.-]+)"?></a>\s*$', stripped)
        if m:
            out.append(f'<a id="{m.group(1)}"></a>')
            i += 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            level, text = len(m.group(1)), m.group(2).strip()
            sid = base = _slug(text)
            n = 2
            while sid in used:
                sid, n = f"{base}-{n}", n + 1
            used.add(sid)
            if level == 1 and not title:
                title = re.sub(r"[`*]", "", text)
            if 2 <= level <= 3:
                heads.append((level, sid, re.sub(r"[`*]", "", text)))
            ctx.line = ln
            out.append(f'<h{level} id="{sid}"><a id="L{ln}"></a>{render_inline(text, ctx)}</h{level}>')
            i += 1
            continue
        if re.match(r"^([-*_])\1{2,}$", stripped):
            out.append(f'<hr id="L{ln}">')
            i += 1
            continue
        if stripped.startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|[\s:|-]+\|?\s*$", lines[i + 1]):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append((i + 1, _split_row(lines[i])))
                i += 1
            out.append(_render_table(rows, ctx))
            continue
        if stripped.startswith(">"):
            block = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                block.append(lines[i].strip().lstrip(">").strip())
                i += 1
            ctx.line = ln
            out.append(f'<blockquote id="L{ln}">' + "<br>".join(render_inline(b, ctx) for b in block if b) + "</blockquote>")
            continue
        if _LIST_RE.match(line):
            items = []
            while i < len(lines):
                cur = lines[i].rstrip()
                lm = _LIST_RE.match(cur)
                if lm:
                    items.append([i + 1, len(lm.group(1).replace("\t", "    ")), lm.group(2), lm.group(3)])
                elif cur.strip() and cur.startswith(" ") and items:
                    items[-1][3] += " " + cur.strip()
                elif not cur.strip():
                    j = i + 1
                    while j < len(lines) and not lines[j].strip():
                        j += 1
                    if j < len(lines) and _LIST_RE.match(lines[j].rstrip()):
                        i = j
                        continue
                    break
                else:
                    break
                i += 1
            out.append(_render_list([tuple(x) for x in items], ctx))
            continue
        para = [stripped]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,4}\s|\||>|-{3,}$|<!--|```)", lines[i].strip()) and not _LIST_RE.match(lines[i].rstrip()):
            para.append(lines[i].strip())
            i += 1
        ctx.line = ln
        out.append(f'<p id="L{ln}">{render_inline(" ".join(para), ctx)}</p>')
    return "".join(out), title, heads


# ---------------------------------------------------------------- khung trang
_CSS_DOC = """
main.rong{max-width:1840px}
.doc h1{text-align:left;font-size:34px;margin:6px 0 14px}.doc h2{margin:34px 0 10px;padding-top:6px;border-top:1px solid var(--line)}.doc h3{font:700 18px/1.3 "Be Vietnam Pro","Segoe UI",system-ui,sans-serif;color:var(--text);margin:24px 0 8px}
.doc p,.doc ul,.doc ol,.doc blockquote{max-width:1100px}.doc ul,.doc ol{padding-left:24px}.doc li{margin:4px 0}
.doc blockquote{margin:14px 0;padding:10px 16px;border-left:4px solid var(--amber);background:var(--amberbg);color:var(--amberfg);border-radius:0 10px 10px 0}
.doc hr{border:0;border-top:1px solid var(--line);margin:26px 0}.doc pre{background:var(--graybg);padding:12px 16px;border-radius:10px;overflow-x:auto;font-size:13px}.doc pre code{background:none;padding:0}
.anh-md{max-width:100%;border:1px solid var(--line);border-radius:8px}
.khu-bang{margin:12px 0 18px}
.doc table{min-width:0}.doc .lon table{min-width:1280px}
a.ma{font-weight:700;text-decoration-style:dotted}
[id^=L]{scroll-margin-top:90px}tr:target td,li:target,p:target,blockquote:target{background:var(--amberbg)!important;outline:2px solid var(--amber);outline-offset:-2px}
tr:target td:first-child{box-shadow:inset 5px 0 0 var(--amber)}
tr.dich td,li.dich,p.dich,blockquote.dich{background:var(--amberbg)!important;outline:2px solid var(--amber);outline-offset:-2px}tr.dich td:first-child{box-shadow:inset 5px 0 0 var(--amber)}
.nav-doc{display:flex;flex-wrap:wrap;gap:6px 8px;margin:0 0 18px;font-size:14px}.nav-doc a,.nav-doc b{padding:5px 12px;border-radius:999px;border:1px solid var(--line);background:var(--card);text-decoration:none;color:var(--body)}
.nav-doc b{background:var(--coral);border-color:var(--coral);color:#fff}.nav-doc a:hover{border-color:var(--coral);color:var(--coral)}
.muc-luc{margin:0 0 16px;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px 18px}.muc-luc summary{cursor:pointer;font-weight:700}
.muc-luc ul{margin:8px 0 4px;padding-left:20px;columns:2;column-gap:36px}.muc-luc li{margin:3px 0;break-inside:avoid}
.loc{display:flex;gap:10px;align-items:center;margin:0 0 16px}.loc input{flex:1;max-width:520px;padding:9px 14px;border:1px solid var(--line);border-radius:999px;background:var(--card);color:var(--body);font:inherit}
.loc span{color:var(--muted);font-size:13px}
tr.an{display:none}
.the{display:grid;grid-template-columns:repeat(auto-fill,minmax(420px,1fr));gap:16px;margin:12px 0 8px}
.the .card h3{margin:0 0 4px;font:700 20px/1.3 "Be Vietnam Pro","Segoe UI",system-ui,sans-serif;color:var(--text)}
.the .card h4{margin:14px 0 6px;font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.links{display:flex;flex-wrap:wrap;gap:6px}.links a{padding:4px 11px;border-radius:999px;border:1px solid var(--line);background:var(--bg);text-decoration:none;font-size:13.5px}.links a:hover{border-color:var(--coral)}
.links .none{padding:4px 11px;border-radius:999px;border:1px dashed var(--line);color:var(--muted);font-size:13.5px}
.bar-tt{display:flex;height:14px;border-radius:7px;overflow:hidden;border:1px solid var(--line);background:var(--graybg)}.bar-tt i{display:block;height:100%}
.bar-tt .s-ok{background:var(--green)}.bar-tt .s-bad{background:var(--coral)}.bar-tt .s-warn{background:var(--amber)}.bar-tt .s-gray{background:var(--graybg)}
.chu-thich{display:flex;flex-wrap:wrap;gap:4px 14px;margin:6px 0 0;font-size:13px;color:var(--muted)}
.bugs{margin:4px 0 0;padding:0;list-style:none}.bugs li{margin:5px 0;font-size:14px}
.so-lieu{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:0 0 6px}.so-lieu div{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 16px}.so-lieu b{display:block;font:700 26px/1.1 "Be Vietnam Pro","Segoe UI",system-ui,sans-serif;color:var(--text)}.so-lieu span{font-size:13px;color:var(--muted)}
@media (max-width:700px){.the{grid-template-columns:1fr}.muc-luc ul{columns:1}}
"""

_JS_HASH = ("function hl(){document.querySelectorAll('.dich').forEach(function(x){x.classList.remove('dich')});var h=decodeURIComponent(location.hash.slice(1));if(!h)return;"
            "var e=document.getElementById(h);if(!e)return;e.classList.add('dich');e.scrollIntoView({block:'center'})}"
            "document.addEventListener('DOMContentLoaded',function(){hl();addEventListener('hashchange',hl)});")

_JS_FILTER = _JS_HASH + ("document.addEventListener('DOMContentLoaded',function(){var q=document.getElementById('loc-q');if(!q)return;var c=document.getElementById('loc-n');"
              "q.addEventListener('input',function(){var v=q.value.trim().toLowerCase(),n=0,t=0;document.querySelectorAll('.doc tbody tr').forEach(function(r){t++;"
              "var ok=!v||r.textContent.toLowerCase().indexOf(v)>=0;r.classList.toggle('an',!ok);if(ok)n++});c.textContent=v?(n+' / '+t+' dòng'):''})});")


_CSS_CLEAN = "mark.trong{background:var(--amberbg);color:var(--amberfg);border:1px dashed var(--amber);border-radius:5px;padding:0 6px;font-weight:700}@media print{#theme,.in-pdf{display:none!important}main.rong{max-width:none}body{background:#fff}}.in-pdf{display:inline-block;margin:0 0 14px;padding:8px 16px;border:1px solid var(--line);border-radius:999px;background:var(--card);color:var(--body);font:inherit;cursor:pointer}"


def _page(title, body, page_dir, nav_html="", toc_html="", has_table=False, project=None, clean=False):
    """`clean=True`: tài liệu gửi ra ngoài (test plan): KHÔNG logo, KHÔNG thanh điều hướng nội bộ, KHÔNG dòng "trang tự sinh"; có nút In / Lưu PDF."""
    flt = ('<div class="loc"><input id="loc-q" type="search" placeholder="Lọc dòng trong các bảng (gõ chữ hoặc mã)…"><span id="loc-n"></span></div>' if has_table else "")
    head = theme.page_head(title, page_dir, _CSS_DOC + (_CSS_CLEAN if clean else "")).replace("<head>", "<head>" + GENERATOR, 1).replace("</script></head>", f"</script><script>{_JS_FILTER}</script></head>", 1)
    if clean:
        body = re.sub(r"(…{2,})", r'<mark class="trong"></mark>', body)   # ô chờ điền nổi bật để người đọc thấy ngay chỗ còn trống
        return (head + '<body><button id="theme" class="theme" type="button">Chế độ tối</button><main class="rong doc">'
                '<button class="in-pdf" type="button" onclick="window.print()">In / Lưu PDF</button>' + toc_html + body + '</main></body></html>')
    return (head + '<body><button id="theme" class="theme" type="button">Chế độ tối</button><main class="rong doc">'
            + theme.brand_html(project) + nav_html + toc_html + flt + body +
            '<p class="small" style="margin-top:36px">Trang tự sinh từ file markdown bằng <code>scripts/build_docs.py</code>; không sửa tay, hãy sửa file md rồi chạy lại.</p></main></body></html>')


def _rel(from_dir, target):
    return os.path.relpath(target, from_dir).replace("\\", "/")


def feature_docs(project, feature, exists):
    """[(nhãn, đường dẫn HTML)] các tài liệu của một tính năng, theo thứ tự đọc. `exists(path)` cho biết trang HTML có (hoặc sẽ có)."""
    root = config.ROOT
    t = root / "testing" / project / feature
    cand = {"srs": root / "srs" / project / f"{feature}.html"}
    for key in ("bang-soat-requirement", "phan-tich-requirement", "cau-hoi-cho-ba", "checklist", "test-case", "truy-vet", "ket-qua-test-case"):
        cand[key] = t / f"{key}.html"
    out = [(label, cand[key]) for key, label in DOC_LABELS if key in cand and exists(cand[key])]
    # tài liệu khác của tính năng (không có trong danh sách trên) cũng phải có link từ trang tổng
    known = {Path(x).name for x in cand.values()}
    for md in sorted(t.glob("*.md")) if t.exists() else []:
        page = md.with_suffix(".html")
        if page.name not in known and exists(page):
            out.append((_doc_title(md), page))
    fdir = root / "evidence" / project / "features" / feature
    # báo cáo khám phá dạng HTML (sơ đồ, ảnh khoanh nút) của tính năng: đặt ngay trong thẻ tính năng, nhãn dễ nhận
    for rep in sorted(fdir.glob("*.html")) if fdir.exists() else []:
        if rep.name != "bao-cao.html" and exists(rep):
            out.append(("Báo cáo khám phá (sơ đồ, ảnh khoanh nút)", rep))
    log = fdir / "bao-cao.html"
    if exists(log):
        out.append(("Nhật ký khám phá", log))
    return out


def _doc_title(md):
    """Tiêu đề cấp 1 của file md (bỏ dấu #), không có thì tên file."""
    try:
        for line in md.read_text(encoding="utf-8").splitlines()[:15]:
            if line.startswith("# "):
                return re.sub(r"[`*]", "", line[2:]).strip()
    except OSError:
        pass
    return md.stem


def render_doc(project, src, converted, codes, exists):
    md = src.read_text(encoding="utf-8")
    feature = feature_of(src, project)
    body, title, heads = render_markdown(md, src, converted, codes, feature)
    out = src.with_suffix(".html")
    root = config.ROOT
    parts = ['<nav class="nav-doc">']
    if project in src.parts:   # tài liệu dùng chung (docs/, srs/*.md) không gắn với một dự án: không có link về trang tổng
        parts.append(f'<a href="{_rel(src.parent, root / "testing" / project / "index.html")}">← Trang tổng</a>')
    if feature:
        for label, p in feature_docs(project, feature, exists):
            parts.append(f"<b>{html.escape(label)}</b>" if p == out else f'<a href="{_rel(src.parent, p)}">{html.escape(label)}</a>')
    parts.append("</nav>")
    toc = ""
    if len(heads) >= 4:
        toc = '<details class="muc-luc"><summary>Mục lục</summary><ul>' + "".join(f'<li><a href="#{i}">{html.escape(t)}</a></li>' for lv, i, t in heads if lv == 2) + "</ul></details>"
    # tài liệu dùng chung (docs/, srs/*.md, testing/*.md) luôn dùng thương hiệu chung của repo để sinh ra giống nhau ở mọi dự án
    clean = src.stem.startswith(("test-plan", "_template-test-plan"))   # test plan là tài liệu gửi sếp/công ty: không logo (người dùng dặn 2026-11-19)
    return out, _page(title or src.stem, body, src.parent, "".join(parts), toc, has_table="<table>" in body, project=project if project in src.parts else None, clean=clean)


# ---------------------------------------------------------------- trang tổng
def _status_counts(test_case_file):
    names, counts = None, {}
    if not test_case_file.exists():   # tính năng mới chỉ có SRS, chưa có test case
        return counts
    for line in test_case_file.read_text(encoding="utf-8").splitlines():
        if names is None and line.startswith("| Mã |"):
            names = [c.strip() for c in _CELL_SPLIT.split(line)[1:-1]]
        elif names and re.match(r'^\|\s*<a id="tc-\d+"></a>', line):
            d = dict(zip(names, [c.strip() for c in _CELL_SPLIT.split(line)[1:-1]]))
            st = d.get("Trạng thái", "Chưa chạy") or "Chưa chạy"
            counts[st] = counts.get(st, 0) + 1
    return counts


def _links(from_dir, items):
    if not items:
        return '<div class="links"><span class="none">Chưa có</span></div>'
    return '<div class="links">' + "".join(f'<a href="{_rel(from_dir, p)}">{html.escape(l)}</a>' for l, p in items) + "</div>"


def _bar(counts):
    total = sum(counts.values()) or 1
    order = ["Đạt", "Không đạt", "Bị chặn", "Bỏ qua", "Chưa chạy"]
    segs = "".join(f'<i class="s-{STATUSES.get(k, "gray")}" style="width:{100 * counts[k] / total:.1f}%" title="{html.escape(k)}: {counts[k]}"></i>' for k in order if counts.get(k))
    legend = "".join(f'<span><span class="badge {STATUSES.get(k, "gray")}">{html.escape(k)}</span> {counts[k]}</span>' for k in order if counts.get(k))
    return f'<div class="bar-tt">{segs}</div><div class="chu-thich">{legend}</div>'


def render_index(project, exists):
    cfg = config.load_for_docs(project)  # trang tổng không cần phần đăng nhập của auto-config.json
    root = config.ROOT
    tdir = cfg.project_dir
    e = html.escape
    # tính năng hiện ở trang tổng khi đã có test case HOẶC đã có SRS (giai đoạn đầu chưa có test case vẫn phải có link tới SRS và nhật ký khám phá)
    features = [d for d in sorted(tdir.iterdir()) if d.is_dir() and ((d / "test-case.md").exists() or (root / "srs" / project / f"{d.name}.md").exists())]
    names = report_mod.feature_names(project)
    version = cfg.test_data.get("version", "")
    cards, total_tc, total_bug, total_ran, total_fail = [], 0, 0, 0, 0
    for d in features:
        f = d.name
        counts = _status_counts(d / "test-case.md")
        n = sum(counts.values())
        total_tc += n
        total_ran += counts.get("Đạt", 0) + counts.get("Không đạt", 0)
        total_fail += counts.get("Không đạt", 0)
        auto = len(list((d / "auto").glob("tc-*.py"))) if (d / "auto").exists() else 0
        bugs = sorted((d / "bug").glob("BUG-*.md")) if (d / "bug").exists() else []
        total_bug += len(bugs)
        data = report_mod.read_results_data(cfg, f)
        last = data["runs"][-1] if data["runs"] else None
        run_line = (f'Lượt {last["number"]} ({e(last["timestamp"][:10])}, bản {e(last["build"])}): {report_mod._verdict_badge(last["verdict"])}' if last else "Chưa có lượt chạy ghi lại")
        bug_items = "".join(
            f'<li><a href="{_rel(tdir, b.with_suffix(".html"))}">{e(b.stem)}</a> <span class="badge gray">{e(report_mod._bug_severity(cfg, b.stem) or "?")}</span> {e(report_mod._bug_title(cfg, b.stem))}</li>' for b in bugs) or "<li>Chưa có bug</li>"
        cards.append(
            f'<div class="card" id="tn-{e(f)}"><h3>{e(names.get(f, f))}</h3><div class="small">{n} test case · {auto} có script tự động</div>'
            f"<h4>Tài liệu</h4>{_links(tdir, feature_docs(project, f, exists))}"
            f"<h4>Tiến độ test case</h4>{_bar(counts)}"
            f"<h4>Lượt chạy gần nhất</h4><div>{run_line}</div>"
            f'<h4>Bug đã ghi ({len(bugs)})</h4><ul class="bugs">{bug_items}</ul></div>')
    smoke_card = ""
    if (tdir / "smoke-test.md").exists():
        sdata = report_mod.read_results_data(cfg, "smoke")
        srun = sdata["runs"][-1] if sdata["runs"] else None
        links = [("Bộ smoke test", tdir / "smoke-test.html"), ("Kết quả smoke", tdir / "smoke-ket-qua.html")]
        n_smoke = len(report_mod.read_smoke_table(cfg))
        srun_line = (f'Lượt {srun["number"]} ({e(srun["timestamp"][:10])}, bản {e(srun["build"])}): {report_mod._verdict_badge(srun["verdict"])}; {e(report_mod._count_statuses(srun))}' if srun else "Chưa có lượt chạy ghi lại")
        smoke_card = f'<div class="card" id="smoke"><h3>Bộ smoke test</h3><div class="small">{n_smoke} case chọn từ các test case</div><h4>Tài liệu</h4>{_links(tdir, [x for x in links if exists(x[1])])}<h4>Lượt chạy gần nhất</h4><div>{srun_line}</div></div>'
    regression_card = ""
    if (tdir / "regression-test.md").exists():
        rg_lines, rg_links = [], [("Bộ regression test", tdir / "regression-test.html")]
        for n in (1, 2, 3):
            page = tdir / f"regression-tang-{n}-ket-qua.html"
            if not page.exists():
                continue
            rg_links.append((f"Kết quả Tầng {n}", page))
            rdata = report_mod.read_results_data(cfg, f"regression-tang-{n}")
            rrun = rdata["runs"][-1] if rdata["runs"] else None
            if rrun:
                rg_lines.append(f'Tầng {n}, lượt {rrun["number"]} ({e(rrun["timestamp"][:10])}, bản {e(rrun["build"])}): {report_mod._verdict_badge(rrun["verdict"])}; {e(report_mod._count_statuses(rrun))}')
        rg_run = "<br>".join(rg_lines) or "Chưa có lượt chạy ghi lại"
        n_t1 = len(report_mod.read_regression_table(cfg, "regression-tang-1"))
        regression_card = (f'<div class="card" id="regression"><h3>Bộ regression test</h3><div class="small">Ba tầng: lõi ({n_t1} case), vùng bị ảnh hưởng, toàn bộ</div>'
                           f'<h4>Tài liệu</h4>{_links(tdir, [x for x in rg_links if exists(x[1])])}<h4>Lượt chạy gần nhất</h4><div>{rg_run}</div></div>')
    plan_pages = sorted({p.with_suffix(".html") for p in tdir.glob("test-plan*.md")} | set(tdir.glob("test-plan*.html")))
    plan_items = [(("Phiếu điền thông tin test plan" if p.stem.endswith("-phieu") else _doc_title(p.with_suffix(".md"))), p)
                  for p in plan_pages if exists(p)]
    plan_card = (f'<div class="card" id="test-plan"><h3>Kế hoạch kiểm thử (test plan)</h3><div class="small">Bản đầy đủ, bản gọn, phiếu điền thông tin</div>'
                 f'<h4>Tài liệu</h4>{_links(tdir, plan_items)}</div>') if plan_items else ""
    summary_card = ""
    if exists(tdir / "test-summary-report.html"):
        summary_card = ('<div class="card" id="bao-cao-tong-ket"><h3>Báo cáo tổng kết kiểm thử</h3><div class="small">Tổng hợp mọi lượt chạy của build mới nhất; có form người test và người duyệt build, nút in PDF</div>'
                        f'<h4>Tài liệu</h4>{_links(tdir, [("Báo cáo tổng kết kiểm thử", tdir / "test-summary-report.html")])}</div>')
    ev = root / "evidence" / project
    ev_items = [(f"Báo cáo khám phá: {p.stem}", p) for p in sorted(ev.glob("*.html"))] if ev.exists() else []
    if (ev / "features").exists():
        for p in sorted((ev / "features").glob("*/*.html")):
            ev_items.append((f"{names.get(p.parent.name, p.parent.name)}: {p.stem}", p))
        for p in sorted((ev / "features").glob("*/bao-cao.md")):
            ev_items.append((f"Nhật ký khám phá: {names.get(p.parent.name, p.parent.name)}", p.with_suffix(".html")))
    seen, ev_unique = set(), []
    for label, p in ev_items:
        if p not in seen and exists(p):
            seen.add(p)
            ev_unique.append((label, p))
    # Hướng dẫn chung cho người đọc: chỉ hai trang này (người dùng chốt 2026-11-19; tài liệu nội bộ, khuôn,
    # đánh giá skill không đưa lên trang tổng vì người khác không cần đọc)
    guide = [(_doc_title(root / "docs" / f"{name}.md"), root / "docs" / f"{name}.html") for name in GUIDE_PAGES]
    # tài liệu khác ở gốc testing/<dự-án>/ (ví dụ file đối chiếu sách với một tính năng) chưa có link ở thẻ nào khác
    linked = "".join(cards) + plan_card + summary_card + smoke_card + regression_card
    extra = [(_doc_title(p), p.with_suffix(".html")) for p in sorted(tdir.glob("*.md"))
             if exists(p.with_suffix(".html")) and f'href="{_rel(tdir, p.with_suffix(".html"))}' not in linked]
    other = (f'<div class="card" id="huong-dan"><h3>Khám phá hệ thống và hướng dẫn</h3><h4>Báo cáo khám phá</h4>{_links(tdir, ev_unique)}'
             + (f'<h4>Tài liệu khác của dự án</h4>{_links(tdir, extra)}' if extra else "")
             + f'<h4>Hướng dẫn và quy ước chung</h4>{_links(tdir, [x for x in guide if exists(x[1])])}</div>')
    stats = ('<div class="so-lieu">' + "".join(f"<div><b>{v}</b><span>{k}</span></div>" for k, v in (
        ("tính năng có test case", len(features)), ("test case", total_tc), ("đã chạy có kết luận", total_ran), ("không đạt", total_fail), ("bug đã ghi", total_bug))) + "</div>")
    system = f'<a href="{e(cfg.url)}/">{e(cfg.url)}</a>' if cfg.url else "chưa khai địa chỉ (điền <code>auto-config.json</code> trước khi chạy test tự động)"
    body = (f'<h1>Trang tổng · {e(project)}</h1><p class="small">Hệ thống: {system}' + (f" · bản test {e(version)}" if version else "") +
            ". Mọi số liệu đọc từ file có sẵn; sau khi sửa tài liệu hoặc chạy test, chạy lại <code>python -X utf8 scripts/build_docs.py</code> để cập nhật.</p>"
            + stats + '<h2 id="tinh-nang">Từng tính năng</h2><div class="the">' + "".join(cards) + "</div>"
            + '<h2 id="bo-test">Kế hoạch, bộ smoke, regression và tài liệu chung</h2><div class="the">' + plan_card + summary_card + smoke_card + regression_card + other + "</div>")
    return tdir / "index.html", _page(f"Trang tổng {project}", body, tdir, project=project)


# ---------------------------------------------------------------- sinh và so sánh
def render_all(project):
    """Sinh (chưa ghi) mọi trang của dự án → ({đường dẫn: nội dung}, [file md bị bỏ qua vì có HTML làm tay trùng tên])."""
    sources = collect_sources(project)
    # Link tới md của MỌI dự án đều đổi sang html (không chỉ dự án đang xét): trang dùng chung (docs/, testing/*.md) được sinh
    # trong lượt của từng dự án, nếu mỗi lượt đổi link một kiểu thì trang đổi theo dự án hiện tại và --check báo cũ mãi.
    converted = {s.resolve() for p in projects() for s in collect_sources(p)} | {s.resolve() for s in sources}
    codes = build_code_index(project)
    pages, skipped, outs = {}, [], []
    for s in sources:
        out = s.with_suffix(".html")
        if out.exists() and GENERATOR not in out.read_text(encoding="utf-8", errors="ignore")[:900]:
            skipped.append(s)
            continue
        outs.append((s, out))
    cfg = config.load_for_docs(project)  # trang bug, kết quả, báo cáo tổng kết không cần phần đăng nhập
    if cfg is not None:
        rr = cfg.project_dir / "run-results"
        for f in sorted(rr.glob("*.json")) if rr.exists() else []:
            try:
                pages.update(report_mod.render_pages(cfg, f.stem))
            except config.ConfigError:
                continue
        pages.update(bug_page.render_all(cfg))
        pages.update(summary_mod.render_pages(cfg))
    planned = {o for _, o in outs} | set(pages)

    def exists(p):
        return p in planned or Path(p).exists()

    for s, out in outs:
        pages.update([render_doc(project, s, converted, codes, exists)])
    index_path, index_text = render_index(project, exists)
    if index_path is not None:
        pages[index_path] = index_text
        UNLINKED[project] = _unlinked(project, index_path, index_text, planned)
    return pages, skipped


UNLINKED = {}  # dự án -> [trang HTML của dự án mà trang tổng chưa có link], do render_all tính


def render_shared():
    """Chỉ trang dùng chung (docs/, srs/*.md, testing/*.md), không gắn dự án. Dùng khi repo chưa có dự án nào
    (ví dụ bộ lõi mới xuất bằng `xuat-bo-loi.py`); có dự án thì các trang này được sinh trong `render_all` của dự án."""
    sources = shared_sources()
    converted = {s.resolve() for s in sources}
    pages, skipped = {}, []
    for s in sources:
        out = s.with_suffix(".html")
        if out.exists() and GENERATOR not in out.read_text(encoding="utf-8", errors="ignore")[:900]:
            skipped.append(s)
            continue
        pages.update([render_doc(None, s, converted, {}, lambda p: Path(p).exists())])
    return pages, skipped


def _unlinked(project, index_path, index_text, planned):
    """Trang HTML của dự án (testing/, srs/, evidence/ của dự án; bỏ thư mục nguồn `_src`) mà trang tổng không link tới.
    Người dùng chỉ mở trang tổng là tới được mọi trang, nên trang nào thiếu link là lỗi."""
    root = config.ROOT
    hrefs = {os.path.normpath(os.path.join(index_path.parent, h.split("#")[0]))
             for h in re.findall(r'href="([^"#:]+?\.html)(?:#[^"]*)?"', index_text)}
    pages = set(p for p in planned if str(p).endswith(".html"))
    for folder in (root / "testing" / project, root / "srs" / project, root / "evidence" / project):
        if folder.exists():
            pages |= set(folder.rglob("*.html"))
    out = []
    for p in sorted(pages):
        rel_parts = Path(p).relative_to(root).parts
        if len(rel_parts) < 2 or rel_parts[1] != project or "_src" in rel_parts or Path(p).name == "index.html":
            continue
        if os.path.normpath(str(p)) not in hrefs:
            out.append(Path(p))
    return out


def sync(project, write=True):
    """Sinh lại mọi trang rồi so với file đang có. Trả ([file đổi hoặc chưa có], [md bị bỏ qua]); `write=False` chỉ so sánh."""
    pages, skipped = render_all(project) if project is not None else render_shared()
    changed = []
    for path, text in pages.items():
        old = path.read_text(encoding="utf-8") if path.exists() else None
        if old != text:
            changed.append(path)
            if write:
                path.write_text(text, encoding="utf-8")
    return changed, skipped
