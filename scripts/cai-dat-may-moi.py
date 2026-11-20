#!/usr/bin/env python3
"""Cài môi trường chạy test tự động và đọc Office/PDF cho MÁY MỚI (làm một lần). Chạy được trên Windows, macOS và Linux.

Chạy từ thư mục repo:
    Windows:      python scripts/cai-dat-may-moi.py
    macOS/Linux:  python3 scripts/cai-dat-may-moi.py

Việc làm:
- tạo venv `.venv` trong repo (không commit, không đụng Python hệ thống);
- cài thư viện trong scripts/requirements-tu-dong.txt (Playwright, MarkItDown, Pillow, fonttools, brotli; cần mạng, vài phút);
- bật hook git sinh lại trang HTML (`core.hooksPath .githooks`) và `core.longpaths` cho repo này, đặt quyền chạy cho hook.
KHÔNG tải ffmpeg hay trình duyệt, KHÔNG sửa cấu hình git toàn máy. Chạy lại nhiều lần được (không làm hỏng gì).
"""
import os
import platform
import shutil
import stat
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IS_WINDOWS = platform.system() == "Windows"
PYTHON_CMD = "python" if IS_WINDOWS else "python3"


def venv_python():
    return ROOT / ".venv" / ("Scripts/python.exe" if IS_WINDOWS else "bin/python")


def run(args, **kwargs):
    print("  $", " ".join(str(a) for a in args))
    return subprocess.run([str(a) for a in args], cwd=ROOT, **kwargs)


def chrome_or_edge_found():
    candidates = []
    if IS_WINDOWS:
        for base in (os.environ.get("ProgramFiles"), os.environ.get("ProgramFiles(x86)"), os.environ.get("LOCALAPPDATA")):
            if base:
                candidates += [Path(base, "Google/Chrome/Application/chrome.exe"), Path(base, "Microsoft/Edge/Application/msedge.exe")]
    elif platform.system() == "Darwin":
        candidates += [Path("/Applications/Google Chrome.app"), Path("/Applications/Microsoft Edge.app"),
                       Path.home() / "Applications/Google Chrome.app"]
    return any(c.exists() for c in candidates) or any(shutil.which(n) for n in ("google-chrome", "google-chrome-stable", "chromium", "microsoft-edge"))


def main():
    if any(a in ("-h", "--help") for a in sys.argv[1:]):
        print(__doc__)
        return 0
    if sys.version_info < (3, 10):
        print(f"Python hiện tại là {sys.version.split()[0]}, cần 3.10 trở lên. Cài bản mới hơn (python.org) rồi chạy lại.")
        return 1
    print(f"1. Tạo venv .venv ({platform.system()}, Python {sys.version.split()[0]})")
    if not venv_python().exists():
        if run([sys.executable, "-m", "venv", ".venv"]).returncode != 0:
            print("Không tạo được venv. Linux có thể cần: sudo apt install python3-venv")
            return 1
    print("2. Cài thư viện (cần mạng, vài phút)")
    for args in ([venv_python(), "-m", "pip", "install", "--upgrade", "pip"],
                 [venv_python(), "-m", "pip", "install", "-r", "scripts/requirements-tu-dong.txt"]):
        if run(args).returncode != 0:
            print("Cài thư viện lỗi (thường do mất mạng). Chạy lại lệnh này khi có mạng.")
            return 1
    print("3. Cấu hình git cho repo này")
    if (ROOT / ".git").exists() and shutil.which("git"):
        run(["git", "config", "core.hooksPath", ".githooks"])
        run(["git", "config", "core.longpaths", "true"])
        hook = ROOT / ".githooks" / "pre-commit"
        if hook.exists() and not IS_WINDOWS:
            hook.chmod(hook.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)   # macOS/Linux cần quyền chạy mới kích hoạt hook
    else:
        print("  (không thấy thư mục .git hoặc lệnh git: bỏ qua)")
    print()
    print("Xong. Kiểm tra máy: " + PYTHON_CMD + " -X utf8 scripts/kiem-tra-may-moi.py")
    if not chrome_or_edge_found():
        print("LƯU Ý: không thấy Chrome hoặc Edge. Cài Chrome, hoặc (~150 MB, hỏi người dùng trước): "
              + str(venv_python().relative_to(ROOT)).replace(os.sep, "/") + " -m playwright install chromium")
    print("Video ca lỗi (tùy chọn, ~1,6 MiB, cần mạng): " + str(venv_python().relative_to(ROOT)).replace(os.sep, "/") + " -m playwright install ffmpeg")
    return 0


if __name__ == "__main__":
    sys.exit(main())
