#!/usr/bin/env python3
"""Đăng nhập tự động bằng Playwright rồi lưu phiên (dùng cho mọi dự án có `auto-config.json`).

Người dùng TỰ CHẠY script này trên máy mình. Mật khẩu chỉ đọc từ `.env` ở gốc repo
trong tiến trình Python; Claude không thấy mật khẩu khi dùng script này.

Ví dụ (một hoặc nhiều tài khoản):
    python -X utf8 scripts/auto_login.py NV01            # mở cửa sổ đã đăng nhập sẵn
    python -X utf8 scripts/auto_login.py NV01 NV02 NV03 --headless   # chạy ẩn, lưu 3 phiên
    python -X utf8 scripts/auto_login.py NV01 --project <dự-án> --reuse

Mỗi tài khoản chỉ đăng nhập TỐI ĐA 1 lần, sai/bị chặn thì dừng, không tự thử lại
(memories/pitfalls/dont-trigger-lockouts.md). Phiên lưu ở `.phien-dang-nhap/<dự-án>/<mã>.json`.
Cài đặt: docs/chay-test-tu-dong.md.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _venv  # noqa: E402

_venv.ensure_playwright()  # chưa có Playwright thì tự chạy lại bằng venv của repo
from test_automation import config, session  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="Đăng nhập tự động (Playwright) và lưu phiên")
    ap.add_argument("accounts", nargs="+", help="mã tài khoản có trong .env, ví dụ NV01")
    ap.add_argument("--project", help="slug dự án (mặc định đọc .du-an-hien-tai)")
    ap.add_argument("--headless", action="store_true", help="chạy ẩn, lưu phiên rồi thoát")
    ap.add_argument("--reuse", action="store_true", help="dùng lại phiên đã lưu nếu còn hạn")
    ap.add_argument("--manual", action="store_true", help="tự đăng nhập tay trong cửa sổ trình duyệt (SSO, mã xác nhận, captcha), script chỉ chờ rồi lưu phiên; không đọc mật khẩu")
    ap.add_argument("--wait-minutes", type=int, default=5, help="với --manual: chờ tối đa bấy nhiêu phút (chỉ là thời gian chờ, không phải ngưỡng an toàn)")
    args = ap.parse_args()

    try:
        cfg = config.load(args.project)
        print(cfg.banner())
        available = cfg.available_accounts()
        account_codes = [m.strip().upper() for m in args.accounts]
        args.manual = args.manual or cfg.login_mode == "manual"
        missing = [] if args.manual else [m for m in account_codes if m not in available]
        if missing:
            print(f"Không có tài khoản {', '.join(missing)} trong .env. Hiện có: {', '.join(available) or '(chưa có)'}")
            return 2
    except config.ConfigError as error:
        print(error)
        return 2

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Chưa cài Playwright. Xem docs/chay-test-tu-dong.md, mục Cài một lần.")
        return 2

    keep_open = (not args.headless) and len(account_codes) == 1
    if not args.headless and len(account_codes) > 1:
        print("Nhiều tài khoản: tự chuyển sang chạy ẩn (--headless).")
        args.headless = True

    pairs = 0
    with sync_playwright() as p:
        if args.manual:
            for account in account_codes:
                if session.manual_login(p, cfg, account, wait_minutes=args.wait_minutes) != 0:
                    return 1
            return 0
        for account in account_codes:
            exit_code, browser, context = session.login(p, cfg, account, headless=args.headless, reuse=args.reuse, keep_open=keep_open)
            if exit_code != 0:
                pairs = 1
                break  # một tài khoản lỗi thì dừng hẳn, không thử tiếp (tránh kích hoạt chặn)
            if keep_open and browser is not None:
                print("Trình duyệt đang mở và đã đăng nhập. Đóng cửa sổ hoặc nhấn Ctrl+C để kết thúc.")
                try:
                    context.wait_for_event("close", timeout=0)
                except (KeyboardInterrupt, Exception):  # noqa: BLE001
                    pass
                try:
                    browser.close()
                except Exception:  # noqa: BLE001
                    pass
    return pairs


if __name__ == "__main__":
    sys.exit(main())
