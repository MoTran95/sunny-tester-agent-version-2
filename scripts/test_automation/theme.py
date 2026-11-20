"""Giao diện thương hiệu dùng chung cho MỌI trang HTML do script sinh ra (kết quả chạy, bug, tài liệu, trang tổng).

Một nơi duy nhất giữ: bảng màu (lấy mẫu từ ảnh thương hiệu), font, chế độ sáng/tối, bảng rộng có cột cố định và thanh cuộn ngang, logo.
Mọi dự án và mọi máy dùng cùng module này nên trang ra giống hệt nhau. Muốn đổi giao diện: sửa ở đây rồi chạy
`python -X utf8 scripts/build_docs.py --all` (sinh lại mọi trang). Mô tả thương hiệu: docs/thuong-hieu/README.md.

Font: ưu tiên font cục bộ trong `docs/thuong-hieu/fonts/` (tải bằng scripts/tai-font.py; chạy được khi không có mạng, giống hệt trên mọi máy);
chưa có thì lấy từ Google Fonts (cần mạng). Logo: `docs/thuong-hieu/logo-sunny-nhan-ra-nen-trong.png` (nhúng thẳng vào trang; chưa có thì bỏ qua).
"""
import base64
import os

from . import config

CSS_BASE = """
/* Màu lấy mẫu từ ảnh thương hiệu (đỏ #C24E3A, vàng #E8A53C, xanh #2E7D32, nâu #3A2E26); nền và thẻ hạ độ sáng cho đỡ chói.
   Chế độ tối theo hệ điều hành, có nút đổi tay (lưu trong trình duyệt). */
:root{color-scheme:light;--bg:#E8DFD0;--card:#F2EDE5;--text:#3A2E26;--body:#463B34;--muted:#6F6154;--line:#D1C9BB;--coral:#C24E3A;--amber:#D9902A;--amberbg:#F6E6C3;--amberfg:#8A5A0E;--warnline:#E6CC93;--green:#2E7D32;--greenbg:#E1EDE3;--greenline:#BBD6C2;--pinkbg:#F8E4DE;--pinkline:#E0B0A4;--graybg:#DCD4C6;--grayfg:#5F5246}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){color-scheme:dark;--bg:#251F1A;--card:#2E2721;--text:#F1E6D4;--body:#DCCFBE;--muted:#A89A8B;--line:#44392F;--coral:#EE8F7C;--amber:#E8A53C;--amberbg:#3A2F18;--amberfg:#EDBB62;--warnline:#5E4A22;--green:#86D08F;--greenbg:#1F3228;--greenline:#2F5A3E;--pinkbg:#3B2420;--pinkline:#6B3A32;--graybg:#38302A;--grayfg:#B8AA9A}:root:not([data-theme=light]) .brand img{background:#E8DFD0;border-radius:14px;padding:6px 14px}}
:root[data-theme=dark]{color-scheme:dark;--bg:#251F1A;--card:#2E2721;--text:#F1E6D4;--body:#DCCFBE;--muted:#A89A8B;--line:#44392F;--coral:#EE8F7C;--amber:#E8A53C;--amberbg:#3A2F18;--amberfg:#EDBB62;--warnline:#5E4A22;--green:#86D08F;--greenbg:#1F3228;--greenline:#2F5A3E;--pinkbg:#3B2420;--pinkline:#6B3A32;--graybg:#38302A;--grayfg:#B8AA9A}
:root[data-theme=dark] .brand img{background:#E8DFD0;border-radius:14px;padding:6px 14px}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--body);font:16px/1.65 "Be Vietnam Pro","Segoe UI",system-ui,sans-serif;padding:40px 16px 56px}
main{max-width:1100px;margin:0 auto}
.brand{text-align:left;margin:0 0 16px}.brand img{height:60px;width:auto;display:block}
.eyebrow{text-align:center;font-size:12px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:var(--amber);margin:0 0 10px}
h1{font:700 40px/1.15 "Be Vietnam Pro","Segoe UI",system-ui,sans-serif;color:var(--text);text-align:center;margin:0 0 8px}
h1 em{font-style:italic;color:var(--coral)}
h2{font:700 22px/1.3 "Be Vietnam Pro","Segoe UI",system-ui,sans-serif;color:var(--text);margin:36px 0 12px}
.sub{text-align:center;color:var(--muted);margin:0 0 26px;font-size:14px}
code{background:var(--graybg);padding:1px 6px;border-radius:5px;font-size:13px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 22px}
dl.meta{display:grid;grid-template-columns:max-content 1fr;gap:8px 24px;margin:0}
dl.meta dt{font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);padding-top:3px}
dl.meta dd{margin:0}
.wrap{overflow-x:auto;border:1px solid var(--line);border-radius:14px;background:var(--card)}
table{border-collapse:collapse;width:100%;min-width:640px}
th,td{padding:12px 16px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}
th{font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);background:var(--bg)}
tr:last-child td{border-bottom:0}
a{color:var(--coral);text-decoration-color:var(--pinkline);text-underline-offset:3px}
a:hover{text-decoration-color:var(--coral)}
.badge{display:inline-block;padding:3px 11px;border-radius:999px;font-size:13px;font-weight:700;white-space:nowrap;border:1px solid transparent}
.ok{background:var(--greenbg);color:var(--green);border-color:var(--greenline)}
.warn{background:var(--amberbg);color:var(--amberfg);border-color:var(--warnline)}
.bad{background:var(--pinkbg);color:var(--coral);border-color:var(--pinkline)}
.gray{background:var(--graybg);color:var(--grayfg);border-color:var(--line)}
.num{text-align:center}.nw{white-space:nowrap}
.small{font-size:13px;color:var(--muted)}
ul.ev{margin:0;padding-left:16px}
.note{font:400 18px/1.6 "Be Vietnam Pro","Segoe UI",system-ui,sans-serif;color:var(--text);text-align:center;border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:18px 8px;margin:36px 0 0}
main.rong{max-width:1840px}
.thumb.kiem{border-color:#1B8F3A}.cap-ok{color:var(--green);font-size:13px;font-weight:700;line-height:1.45;margin:6px 0 2px;max-width:230px}.vid{display:block;margin-top:6px;max-width:250px;border-radius:8px;background:#000}
.kl h3{font:700 16px/1.3 "Be Vietnam Pro","Segoe UI",system-ui,sans-serif;color:var(--text);margin:18px 0 6px}.kl p{margin:6px 0}.kl ul{margin:6px 0;padding-left:22px}.kl li{margin:5px 0}.kl-dau{font-size:17px;color:var(--text);font-weight:500}.kl-bang{min-width:0;width:100%}.kl-bang td{font-size:14.5px}
.lon table{min-width:1280px;border-collapse:separate;border-spacing:0}.lon td:nth-child(2){min-width:230px}
.khu-bang{position:relative}.lon{scrollbar-width:none;cursor:grab}.lon::-webkit-scrollbar{display:none}.lon.keo{cursor:grabbing;user-select:none}
.thanh-keo{position:sticky;bottom:0;z-index:6;overflow-x:auto;overflow-y:hidden;height:18px;background:var(--bg);border:1px solid var(--line);border-radius:10px;margin-top:6px}
.thanh-keo>div{height:1px}
.lon th:nth-child(1),.lon td:nth-child(1){position:sticky;left:0;z-index:2;background:var(--card);width:76px;min-width:76px}
.lon th:nth-child(2),.lon td:nth-child(2){position:sticky;left:76px;z-index:2;background:var(--card);box-shadow:3px 0 0 var(--line)}
.lon th:nth-child(1),.lon th:nth-child(2){background:var(--bg);z-index:3}
.goi-y{margin:0 0 8px;font-size:13px;color:var(--muted)}
.cap-loi{color:var(--coral);font-size:13px;font-weight:700;line-height:1.45;margin:6px 0 2px;max-width:230px}.cot-nho{font-size:13.5px;line-height:1.5;min-width:170px}.cot-nho div+div{margin-top:4px}.cot-nho code{font-size:12px}
.thuc-te .dung{color:var(--green)}.thuc-te .sai{color:var(--coral);font-weight:700}
ul.ev li.loi{list-style:none;margin:8px 0 0 -16px}.thumb{display:block;margin-top:6px;max-width:210px;border:3px solid #E5252A;border-radius:8px}
.theme{position:absolute;top:12px;right:12px;z-index:5;background:var(--card);color:var(--body);border:1px solid var(--line);border-radius:999px;padding:6px 14px;font:700 12px/1 inherit;font-family:inherit;letter-spacing:.06em;cursor:pointer}
.theme:hover{border-color:var(--coral);color:var(--coral)}
@media (max-width:600px){h1{font-size:30px}body{padding-top:28px}}
"""


JS_DRAG_SCROLL = ("document.addEventListener('DOMContentLoaded',function(){document.querySelectorAll('.khu-bang').forEach(function(k){"
           "var w=k.querySelector('.wrap'),p=k.querySelector('.thanh-keo'),i=p.firstElementChild,t=w.querySelector('table'),a=false;"
           "function dat(){i.style.width=t.scrollWidth+'px';p.style.display=(w.scrollWidth>w.clientWidth+2)?'block':'none'}dat();addEventListener('resize',dat);"
           "p.addEventListener('scroll',function(){if(a){a=false;return}a=true;w.scrollLeft=p.scrollLeft});"
           "w.addEventListener('scroll',function(){if(a){a=false;return}a=true;p.scrollLeft=w.scrollLeft});"
           "var x0=0,s0=0,d=false;w.addEventListener('mousedown',function(e){if(e.target.closest('a,button,img')||e.button!==0)return;d=true;x0=e.clientX;s0=w.scrollLeft;w.classList.add('keo')});"
           "addEventListener('mouseup',function(){d=false;w.classList.remove('keo')});"
           "addEventListener('mousemove',function(e){if(d)w.scrollLeft=s0-(e.clientX-x0)})})});")

JS_THEME = "(function(){var r=document.documentElement;try{var t=localStorage.getItem('smoke-theme');if(t)r.setAttribute('data-theme',t)}catch(e){}document.addEventListener('DOMContentLoaded',function(){var b=document.getElementById('theme');function eff(){var t=r.getAttribute('data-theme');return t||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light')}function lab(){b.textContent=eff()==='dark'?'Chế độ sáng':'Chế độ tối'}lab();b.onclick=function(){var n=eff()==='dark'?'light':'dark';r.setAttribute('data-theme',n);try{localStorage.setItem('smoke-theme',n)}catch(e){}lab()}})})();"


BRAND_FILE = "docs/thuong-hieu/brand.json"
DEFAULT_BRAND = {
    "name": "Sunny Nhận Ra",                                      # tên thương hiệu (chữ thay thế của logo)
    "logo": "docs/thuong-hieu/logo-sunny-nhan-ra-nen-trong.png",  # logo nhúng vào trang (nền trong suốt, nên rộng 400 đến 500 px)
    "logo_source": "docs/thuong-hieu/logo-sunny-nhan-ra.png",     # logo gốc để scripts/process_logo.py tạo ra bản nhúng
    "logo_enabled": True,                                         # false = không hiện logo
}
LOGO_PATH = DEFAULT_BRAND["logo"]
_MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".svg": "image/svg+xml", ".webp": "image/webp"}


def load_brand(project=None):
    """Cấu hình thương hiệu: mặc định (Sunny) < `docs/thuong-hieu/brand.json` (chung cả repo) < `testing/<dự-án>/brand.json` (riêng một dự án).

    Chỉ cần ghi các khóa muốn đổi. Đường dẫn tính từ gốc repo. Dùng khi người khác dùng bộ công cụ này cho thương hiệu của họ.
    """
    import json

    brand = dict(DEFAULT_BRAND)
    files = [config.ROOT / BRAND_FILE]
    if project:
        files.append(config.ROOT / "testing" / project / "brand.json")
    for f in files:
        if f.exists():
            try:
                brand.update({k: v for k, v in json.loads(f.read_text(encoding="utf-8")).items() if k in DEFAULT_BRAND})
            except (OSError, ValueError):
                pass
    return brand


def logo_data_uri(project=None):
    """Nhúng logo thẳng vào trang (gửi file đi không thiếu logo); tắt, thiếu file hoặc định dạng lạ thì bỏ qua."""
    import base64

    brand = load_brand(project)
    if not brand["logo_enabled"]:
        return None
    f = config.ROOT / brand["logo"]
    mime = _MIME.get(f.suffix.lower())
    if not f.exists() or not mime:
        return None
    return f"data:{mime};base64," + base64.b64encode(f.read_bytes()).decode("ascii")


def brand_html(project=None):
    """Khối logo ở góc trái đầu trang (chuỗi rỗng nếu không có logo)."""
    import html

    uri = logo_data_uri(project)
    return f'<div class="brand"><img src="{uri}" alt="{html.escape(load_brand(project)["name"])}"></div>' if uri else ""


FONTS_DIR = "docs/thuong-hieu/fonts"
GOOGLE_FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">'
)
def font_head(page_dir):
    """Thẻ nạp font cho trang nằm ở `page_dir`: font cục bộ nếu có `docs/thuong-hieu/fonts/fonts.json` (do scripts/tai-font.py tạo,
    đủ tập ký tự gồm tiếng Việt), ngược lại Google Fonts (cần mạng)."""
    import json

    fonts = config.ROOT / FONTS_DIR
    manifest = fonts / "fonts.json"
    if not manifest.exists():
        return GOOGLE_FONTS
    try:
        items = [m for m in json.loads(manifest.read_text(encoding="utf-8")) if (fonts / m["file"]).exists()]
    except (OSError, ValueError, KeyError):
        items = []
    if not items:
        return GOOGLE_FONTS
    rules = "".join(
        f"@font-face{{font-family:'{m['family']}';font-style:{m['style']};font-weight:{m['weight']};font-display:swap;"
        f"src:url('{os.path.relpath(fonts / m['file'], page_dir).replace(chr(92), '/')}') format('woff2');unicode-range:{m['unicode_range']}}}"
        for m in items)
    return f"<style>{rules}</style>"


def page_head(title, page_dir, extra_css=""):
    """Phần <head> chung: meta, tiêu đề, font, CSS, JS đổi sáng/tối và kéo ngang."""
    import html

    return ('<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f"<title>{html.escape(title)}</title>{font_head(page_dir)}<style>{CSS_BASE}{extra_css}</style>"
            f"<script>{JS_THEME}{JS_DRAG_SCROLL}</script></head>")
