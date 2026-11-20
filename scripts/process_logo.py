#!/usr/bin/env python3
"""Tạo bản logo nền trong suốt, nhỏ gọn, để nhúng vào trang kết quả (smoke-ket-qua.html).

    python -X utf8 scripts/process_logo.py            # đọc logo gốc ghi trong docs/thuong-hieu/brand.json (mặc định logo-sunny-nhan-ra.png)
    python -X utf8 scripts/process_logo.py --width 420 # đổi chiều rộng (mặc định 420 px)

Nền trắng chuyển thành trong suốt (để đặt lên nền kem không bị hộp trắng), màu logo giữ nguyên. Logo đã có nền trong suốt thì giữ nền đó,
dọn chấm nhiễu li ti và cắt phần trống quanh logo.
Chạy một lần khi đổi logo, cần Pillow (`pip install Pillow`).
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_automation import theme  # noqa: E402

BRAND = theme.load_brand()   # đường dẫn logo gốc và logo nhúng lấy từ docs/thuong-hieu/brand.json
SOURCE = ROOT / BRAND["logo_source"]
DEST = ROOT / BRAND["logo"]


def process(src, dest, width=420):
    """Nền trắng → trong suốt; logo đã có nền trong suốt thì giữ và chỉ dọn các chấm nhiễu li ti còn sót quanh logo."""
    from PIL import Image, ImageChops, ImageFilter

    original = Image.open(src)
    if original.mode == "RGBA" and original.getchannel("A").getextrema()[0] < 250:
        im = original.copy()
        alpha = im.getchannel("A")
        solid = alpha.point(lambda v: 255 if v >= 128 else 0)
        opened = solid.filter(ImageFilter.MinFilter(9)).filter(ImageFilter.MaxFilter(9))   # bỏ chấm nhỏ hơn khoảng 9 điểm ảnh
        keep = opened.filter(ImageFilter.MaxFilter(7))                                      # chừa viền khử răng cưa quanh hình giữ lại
        im.putalpha(ImageChops.darker(alpha, keep))
        im = im.crop(im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox())   # cắt phần trống quanh logo
        im = im.resize((width, max(1, round(im.height * width / im.width))), Image.LANCZOS)
    else:
        im = original.convert("RGB")
        im = im.resize((width, max(1, round(im.height * width / im.width))), Image.LANCZOS)
        r, g, b = im.split()
        darkest = ImageChops.darker(ImageChops.darker(r, g), b)  # kênh tối nhất mỗi điểm; 255 = trắng tinh
        im.putalpha(darkest.point(lambda v: min(255, (255 - v) * 255 // 40)))  # gần trắng → trong suốt, đủ đậm → giữ nguyên
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "PNG", optimize=True)
    return im.size


def main():
    ap = argparse.ArgumentParser(description="Tạo logo nền trong suốt cho trang kết quả")
    ap.add_argument("--width", type=int, default=420)
    args = ap.parse_args()
    if not SOURCE.exists():
        print(f"Chưa có logo gốc. Đặt file vào {SOURCE.relative_to(ROOT)} rồi chạy lại.")
        return 2
    size = process(SOURCE, DEST, args.width)
    print(f"Đã tạo {DEST.relative_to(ROOT)} {size[0]}x{size[1]}. Chạy `scripts/build_report.py build` để cập nhật trang.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
