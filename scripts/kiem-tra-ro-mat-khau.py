#!/usr/bin/env python3
"""Dò mật khẩu trong `.env` có lọt vào file văn bản nào của repo không (md, html, json, py, txt…).

    python -X utf8 scripts/kiem-tra-ro-mat-khau.py

Chỉ báo TÊN KHÓA và đường dẫn file, KHÔNG BAO GIỜ in giá trị. Không đọc ảnh (ảnh nhạy cảm vẫn phải tự kiểm bằng mắt).
Bỏ qua: .env, .git, .venv, .phien-dang-nhap, video. Không có .env thì bỏ qua (thoát mã 0). Có chỗ rò thì thoát mã 1.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXT_EXT = (".md", ".html", ".json", ".py", ".txt", ".csv", ".js", ".css", ".svg", ".sh", ".ps1", ".yml", ".yaml")
SKIP_DIRS = {".git", ".venv", ".phien-dang-nhap", "__pycache__", "node_modules", "video", "video-tmp"}
MIN_LENGTH = 6   # mật khẩu ngắn hơn dễ trùng chữ thường: không dò


def read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except (OSError, UnicodeDecodeError):
        return ""


def passwords():
    path = os.path.join(ROOT, ".env")
    found = {}
    if not os.path.exists(path):
        return found
    for line in read(path).splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip().strip('"').strip("'")
        if key.strip().upper().endswith("PASSWORD") and len(value) >= MIN_LENGTH:
            found[key.strip()] = value
    return found


def main():
    secrets = passwords()
    if not secrets:
        print("Không có .env hoặc chưa có mật khẩu nào để dò: bỏ qua.")
        return 0
    leaks = []
    scanned = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if name == ".env" or not name.lower().endswith(TEXT_EXT):
                continue
            path = os.path.join(dirpath, name)
            text = read(path)
            scanned += 1
            for key, value in secrets.items():
                if value in text:
                    leaks.append((os.path.relpath(path, ROOT).replace(os.sep, "/"), key))
    if leaks:
        print(f"{len(leaks)} chỗ chứa mật khẩu của .env (chỉ in tên khóa, không in giá trị):")
        for f, key in leaks[:30]:
            print(f"  - {f}  (khóa {key})")
        print("Xóa mật khẩu khỏi file ngay; nếu đã commit hoặc gửi đi thì đổi mật khẩu.")
        return 1
    print(f"Không thấy mật khẩu của .env trong {scanned} file văn bản ({len(secrets)} khóa mật khẩu được dò).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
