#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Xuất test plan ra PDF bằng Edge hoặc Chrome có sẵn trên máy (không cần cài thêm thư viện Python).

  python -X utf8 .claude/skills/tao-test-plan/scripts/xuat-pdf.py <dự-án> [--file test-plan.html] [--ra <đường-dẫn.pdf>]

Mặc định ghi `testing/<dự-án>/test-plan.pdf` (không commit nếu không cần: PDF sinh lại bất kỳ lúc nào từ HTML).
Trình duyệt tìm theo thứ tự: biến môi trường BROWSER_PATH, Edge/Chrome trên Windows, Chrome/Edge trên Mac, chrome/chromium trên Linux.
Link tương đối giữa các tài liệu trong PDF không bấm được ở máy khác (chữ vẫn đọc được).
"""
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
CANDIDATES = [   # Chrome trước: trên máy thử, Edge chạy ẩn không ghi ra PDF
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]


def find_browsers():
    found = []
    env = os.environ.get("BROWSER_PATH")
    if env and Path(env).exists():
        found.append(env)
    found += [c for c in CANDIDATES if Path(c).exists()]
    for name in ("google-chrome", "chromium", "chromium-browser", "chrome", "msedge"):
        p = shutil.which(name)
        if p and p not in found:
            found.append(p)
    return found


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project")
    ap.add_argument("--file", default="test-plan.html")
    ap.add_argument("--ra")
    a = ap.parse_args()
    src = ROOT / "testing" / a.project / a.file
    if not src.exists():
        sys.exit(f"Không thấy {src}: chạy `python -X utf8 scripts/build_docs.py --all` trước")
    out = (Path(a.ra) if a.ra else src.with_suffix(".pdf")).resolve()
    browsers = find_browsers()
    if not browsers:
        sys.exit("Không tìm thấy Edge/Chrome. Đặt biến BROWSER_PATH trỏ tới trình duyệt, hoặc mở trang HTML và bấm nút In / Lưu PDF.")
    tmp_profile = ROOT / ".phien-dang-nhap" / "pdf-profile"
    tmp_profile.mkdir(parents=True, exist_ok=True)
    err = ""
    for browser in browsers:
        if out.exists():
            out.unlink()
        cmd = [browser, "--headless=new", "--disable-gpu", f"--user-data-dir={tmp_profile}", "--no-pdf-header-footer",
               f"--print-to-pdf={out}", src.resolve().as_uri()]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
            err = r.stderr[-300:]
        except subprocess.TimeoutExpired:
            err = f"{browser}: quá 90 giây"
        if out.exists():
            break
    if not out.exists():
        sys.exit(f"Không tạo được PDF bằng trình duyệt nào trong: {browsers}\n{err}\nMở trang HTML và bấm nút In / Lưu PDF.")
    print(f"Đã ghi {out} ({out.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
