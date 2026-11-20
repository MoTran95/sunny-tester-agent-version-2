#!/usr/bin/env python3
"""Tô khung đỏ lên ảnh bằng chứng để chỉ chỗ lỗi (ảnh gốc giữ nguyên, ra file mới có đuôi `-loi`).

    python -X utf8 scripts/mark_error.py <ảnh.png> --box 1067,14,1122,30
    python -X utf8 scripts/mark_error.py <ảnh.png> --box 100,200,300,240 --box 500,60,640,90 --nhan "LỖI"

--box x1,y1,x2,y2 là góc trên-trái và dưới-phải của chữ cần khoanh (điểm ảnh); khung được nới thêm vài điểm.
Với test tự động, không cần dùng công cụ này: khai `mark_text="chữ lỗi"` trong check_main/check_minor thì lúc chạy
script tự chụp thêm ảnh có khung đỏ (xem docs/chay-test-tu-dong.md). Cần Pillow.
"""
import argparse
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

RED = (229, 37, 42)


def to_do(path, box, label="LỖI", dest=None):
    from PIL import Image, ImageDraw, ImageFont

    src = Path(path)
    im = Image.open(src).convert("RGBA")
    cls = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(cls)
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 13)
    except OSError:
        font = ImageFont.load_default()
    for x1, y1, x2, y2 in box:
        x1, y1, x2, y2 = x1 - 6, y1 - 5, x2 + 6, y2 + 5
        d.rounded_rectangle((x1, y1, x2, y2), radius=6, fill=RED + (40,), outline=RED + (255,), width=3)
        if label:
            width = d.textlength(label, font=font) + 12
            label_y = y1 - 22 if y1 - 22 >= 2 else y2 + 5  # sát mép trên thì đặt nhãn dưới khung
            d.rounded_rectangle((x1, label_y, x1 + width, label_y + 19), radius=4, fill=RED + (255,))
            d.text((x1 + 6, label_y + 2), label, font=font, fill=(255, 255, 255, 255))
    out = Image.alpha_composite(im, cls).convert("RGB")
    dest = Path(dest) if dest else src.with_name(src.stem + "-loi" + src.suffix)
    out.save(dest, "PNG", optimize=True)
    return dest


def main():
    ap = argparse.ArgumentParser(description="Tô khung đỏ chỗ lỗi trên ảnh bằng chứng")
    ap.add_argument("images")
    ap.add_argument("--box", action="append", required=True, help="x1,y1,x2,y2 (có thể dùng nhiều lần)")
    ap.add_argument("--label", default="LỖI", help="chữ trên nhãn đỏ (để trống nếu không muốn nhãn)")
    ap.add_argument("--out", help="đường dẫn file kết quả (mặc định: tên gốc + -loi)")
    args = ap.parse_args()
    box = [tuple(int(x) for x in k.split(",")) for k in args.box]
    print(f"Đã tạo: {to_do(args.images, box, args.label, args.out)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
