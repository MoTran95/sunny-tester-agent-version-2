#!/usr/bin/env python3
"""Tải font thương hiệu (Be Vietnam Pro, giấy phép SIL OFL; đổi từ Fraunces + Hanken Grotesk ngày 2026-11-19 vì dấu tiếng Việt hiển thị lỗi) từ Google Fonts về `docs/thuong-hieu/fonts/`
để các trang HTML dùng font cục bộ, giống hệt trên mọi máy kể cả khi không có mạng.

    python -X utf8 scripts/tai-font.py

Chỉ chạy khi người dùng đồng ý tải. Script lấy CSS của Google Fonts (bản biến thiên, đủ các tập ký tự gồm tiếng Việt), tải từng
file .woff2 và ghi `fonts.json` (họ font, độ đậm, kiểu, dải ký tự, tên file); `theme.py` đọc `fonts.json` để nạp font.
Chạy lại là ghi đè. Sau đó chạy `python -X utf8 scripts/build_docs.py --all` để các trang dùng font cục bộ.
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "docs" / "thuong-hieu" / "fonts"
CSS_URL = "https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"  # để Google trả woff2


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    css = get(CSS_URL).decode("utf-8")
    blocks = re.findall(r"/\*\s*([\w-]+)\s*\*/\s*@font-face\s*\{(.*?)\}", css, flags=re.S)
    if not blocks:
        print("Không đọc được CSS từ Google Fonts.")
        return 1
    DEST.mkdir(parents=True, exist_ok=True)
    manifest, total = [], 0
    for subset, body in blocks:
        fam = re.search(r"font-family:\s*'([^']+)'", body).group(1)
        style = re.search(r"font-style:\s*(\w+)", body).group(1)
        weight = re.search(r"font-weight:\s*([\d ]+)", body).group(1).strip()
        rng = re.search(r"unicode-range:\s*([^;]+);", body).group(1).strip()
        url = re.search(r"url\((https://[^)]+\.woff2)\)", body).group(1)
        # Be Vietnam Pro là font tĩnh (mỗi độ đậm một file) nên tên file có cả độ đậm
        name = f"{fam.replace(' ', '')}-{'italic' if style == 'italic' else 'roman'}-{weight.replace(' ', '-')}-{subset}.woff2"
        if not (DEST / name).exists():
            data = get(url)
            (DEST / name).write_bytes(data)
            total += len(data)
        manifest.append({"family": fam, "weight": weight, "style": style, "file": name, "unicode_range": rng, "subset": subset})
    keep = {m["file"] for m in manifest}
    for old in DEST.glob("*.woff2"):   # bỏ file của font cũ không còn dùng
        if old.name not in keep:
            old.unlink()
    (DEST / "fonts.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    size = sum((DEST / m["file"]).stat().st_size for m in manifest)
    print(f"Đã có {len(manifest)} file font ({size // 1024} KB) ở {DEST.relative_to(ROOT)}; mới tải {total // 1024} KB. Ghi fonts.json.")
    print("Chạy tiếp: python -X utf8 scripts/build_docs.py --all")
    return 0


if __name__ == "__main__":
    sys.exit(main())
