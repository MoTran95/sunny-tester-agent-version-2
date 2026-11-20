#!/usr/bin/env python3
"""Đổi Word, PowerPoint, Excel, PDF chữ, HTML sang Markdown bằng MarkItDown (để đọc ít token hơn). Chạy được ở máy nào.

    python -X utf8 scripts/doi-sang-markdown.py <file hoặc URL đã biết nguồn> -o <thư-mục-tạm>/<tên>.md

Tự tìm Python có MarkItDown: `.venv` trong repo (cài bằng scripts/cai-dat-may-moi.py), rồi `~/.venvs/markitdown` và
`~/.venvs/playwright` (cách cũ). Ghi ra file `-o` rồi đọc file đó (in thẳng ra màn hình Windows làm tiếng Việt thành `?`).
Không dùng cho .txt/.md, Excel lớn, PDF scan; chỉ đưa file/URL đã biết nguồn.
"""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOME_VENVS = Path.home() / ".venvs"


def candidates():
    for base in (ROOT / ".venv", HOME_VENVS / "markitdown", HOME_VENVS / "playwright"):
        for rel in ("Scripts/python.exe", "bin/python"):
            if (base / rel).exists():
                yield base / rel


def has_markitdown(python):
    return subprocess.run([str(python), "-c", "import markitdown"], capture_output=True).returncode == 0


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return 2
    for python in candidates():
        if has_markitdown(python):
            env = dict(os.environ, PYTHONUTF8="1")
            return subprocess.call([str(python), "-m", "markitdown", *sys.argv[1:]], env=env)
    print("Chưa cài MarkItDown. Chạy một lần: python scripts/cai-dat-may-moi.py (Mac: python3)", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
