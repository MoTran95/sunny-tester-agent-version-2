"""Giao diện chuẩn của báo cáo khám phá, dùng chung với giao diện thương hiệu của repo.

- CSS chuẩn: `assets/giao-dien-chuan.css` (bảng màu thương hiệu, cỡ chữ, bố cục).
- Font thương hiệu: Be Vietnam Pro (font tĩnh, mỗi độ đậm một file) lấy từ `docs/thuong-hieu/fonts/` (do `scripts/tai-font.py` tải),
  CẮT chỉ còn các ký tự thật sự có trong báo cáo rồi nhúng base64 → file nhẹ (khung xem trước giới hạn 512 KiB), giống hệt trên mọi máy.
  Thiếu font hoặc thiếu fontTools thì dùng font hệ thống và báo cảnh báo.
- Logo: theo `docs/thuong-hieu/brand.json` (`test_automation.theme`), đặt ở góc trái đầu báo cáo; tắt được bằng `logo_enabled: false`.
"""
import base64
import html as _html
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, '..', 'assets')
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
FONTS = os.path.join(ROOT, 'docs', 'thuong-hieu', 'fonts')
sys.path.insert(0, os.path.join(ROOT, 'scripts'))


def _manifest():
    f = os.path.join(FONTS, 'fonts.json')
    if not os.path.exists(f):
        return []
    try:
        return [m for m in json.load(io.open(f, encoding='utf-8')) if os.path.exists(os.path.join(FONTS, m['file']))]
    except (OSError, ValueError, KeyError):
        return []


def _ranges(spec):
    out = []
    for part in spec.split(','):
        part = part.strip().upper().replace('U+', '')
        if not part:
            continue
        lo, _, hi = part.partition('-')
        lo_i = int(lo.replace('?', '0'), 16)
        hi_i = int(hi, 16) if hi else int(lo.replace('?', 'F'), 16)
        out.append((lo_i, hi_i))
    return out


def _subset(path, codepoints, axes=None):
    """Cắt file woff2 còn các ký tự cần dùng. `axes`: giới hạn trục độ đậm (ví dụ {'wght': (400, 700)}) hoặc cố định thành bản tĩnh
    (ví dụ {'wght': 700, 'opsz': 36}) cho nhẹ. None nếu thiếu fontTools."""
    try:
        from fontTools import subset
        from fontTools.ttLib import TTFont
        from fontTools.varLib import instancer
    except ImportError:
        return None
    def build(with_axes):
        font = TTFont(path)
        if with_axes:
            font = instancer.instantiateVariableFont(font, with_axes)
        opts = subset.Options()
        opts.flavor = 'woff2'
        opts.layout_features = ['kern', 'ccmp', 'locl', 'mark', 'mkmk']   # đủ cho dấu tiếng Việt và căn cặp chữ, bỏ các tính năng không dùng
        sub = subset.Subsetter(opts)
        sub.populate(unicodes=sorted(codepoints))
        sub.subset(font)
        return font

    try:
        font = build(axes)
    except Exception:  # noqa: BLE001  (một số file con của font không có glyph 'space' nên fontTools không đổi trục được: giữ bản biến thiên)
        font = build(None)
    out = io.BytesIO()
    font.flavor = 'woff2'
    font.save(out)
    return out.getvalue()


def _faces(family, chars, warn, axes=None, weight=None, weights=None):
    """`weights`: chỉ lấy các file có độ đậm này (font tĩnh, mỗi độ đậm một file)."""
    css = []
    for m in _manifest():
        if m['family'] != family or m['style'] != 'normal' or (weights and m['weight'] not in weights):
            continue
        rng = _ranges(m['unicode_range'])
        need = {c for c in chars if any(lo <= c <= hi for lo, hi in rng)}
        if not need:
            continue
        path = os.path.join(FONTS, m['file'])
        data = _subset(path, need, axes)
        if data is None:
            data = open(path, 'rb').read()
            warn.append('thiếu fontTools: nhúng nguyên file font %s (nặng hơn); cài: pip install fonttools brotli' % m['file'])
        css.append('@font-face{font-family:"%s";font-style:normal;font-weight:%s;font-display:block;'
                   'src:url(data:font/woff2;base64,%s) format("woff2");unicode-range:%s}'
                   % (family, weight or m['weight'], base64.b64encode(data).decode('ascii'), m['unicode_range']))
    return css


def _text_of(page_html):
    """Chữ nhìn thấy của trang (bỏ khối base64 và thẻ) để biết cần giữ ký tự nào."""
    t = re.sub(r'data:[^")\s]{200,}', '', page_html)
    return _html.unescape(re.sub(r'<[^>]+>', ' ', t))


def font_css(page_html, warn):
    """Be Vietnam Pro độ đậm 400 và 700 (chữ 600 trình duyệt dùng bản 700), chỉ giữ ký tự thật dùng trong trang; giữ báo cáo dưới 512 KiB."""
    body_chars = {ord(c) for c in _text_of(page_html)} | {32} | {ord(c) for c in '☐→·—…“”‘’'}
    heads = ' '.join(_html.unescape(re.sub(r'<[^>]+>', '', h)) for h in re.findall(r'<h[1-3][^>]*>(.*?)</h[1-3]>', page_html, flags=re.S))
    head_chars = {ord(c) for c in heads} | set(range(48, 58)) | {32}
    if not _manifest():
        warn.append('chưa có font thương hiệu ở docs/thuong-hieu/fonts: dùng font hệ thống (chạy scripts/tai-font.py)')
        return ''
    return chr(10).join(_faces('Be Vietnam Pro', body_chars, warn, weights=('400',))
                     + _faces('Be Vietnam Pro', body_chars | head_chars, warn, weights=('700',)))


def project_of(path):
    parts = os.path.abspath(path).replace('\\', '/').split('/')
    for key in ('evidence', 'testing', 'srs'):
        if key in parts and parts.index(key) + 1 < len(parts) - 1:
            return parts[parts.index(key) + 1]
    return None


def brand_block(project=None):
    """Khối logo góc trái theo docs/thuong-hieu/brand.json, thu nhỏ còn cao 112 px dạng PNG bảng màu (~6 KB) để báo cáo vẫn dưới 512 KiB."""
    try:
        from test_automation import theme
        brand = theme.load_brand(project)
        if not brand['logo_enabled']:
            return ''
        path = os.path.join(ROOT, brand['logo'])
        if not os.path.exists(path):
            return ''
        from PIL import Image
        im = Image.open(path).convert('RGBA')
        im = im.resize((max(1, round(im.width * 112 / im.height)), 112), Image.LANCZOS)
        buf = io.BytesIO()
        im.quantize(colors=96, method=Image.FASTOCTREE).save(buf, 'PNG', optimize=True)   # logo phẳng ít màu: PNG bảng màu nhẹ hơn WebP
        return '<div class="brand"><img src="data:image/png;base64,%s" alt="%s"></div>' % (base64.b64encode(buf.getvalue()).decode('ascii'), _html.escape(brand['name']))
    except Exception:  # noqa: BLE001  (thiếu thư viện/Pillow hoặc file lỗi: bỏ logo, không làm hỏng build)
        return ''


def std_block():
    """Khối <style id="giao-dien-chuan">: CSS chuẩn + chỗ giữ cho font (điền sau bằng embed_fonts khi đã biết đủ chữ của trang)."""
    css = io.open(os.path.join(ASSETS, 'giao-dien-chuan.css'), encoding='utf-8').read()
    return '<style id="giao-dien-chuan">' + chr(10) + '/*FONTS*/' + chr(10) + css + '</style>'


def embed_fonts(page_html, warn):
    """Điền font (đã cắt theo chữ thật của trang) vào chỗ giữ của khối giao diện chuẩn."""
    return page_html.replace('/*FONTS*/', font_css(page_html, warn), 1)


def add_logo(page_html, project=None):
    """Chèn logo (góc trái) đầu khối hero nếu báo cáo chưa có và thương hiệu bật logo."""
    block = brand_block(project)
    if not block or 'class="brand"' in page_html:
        return page_html
    return re.sub(r'(<header class="hero">\s*<div class="wrapper">)', lambda m: m.group(1) + block, page_html, count=1)
