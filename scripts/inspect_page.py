#!/usr/bin/env python3
"""In cấu trúc một trang (cây trợ năng: vai trò + tên) để viết selector cho script test case.

Dùng phiên đã lưu bởi scripts/auto_login.py, KHÔNG đọc mật khẩu, chỉ mở trang (GET).

    python -X utf8 scripts/inspect_page.py /orders/<id> --account NV01
    python -X utf8 scripts/inspect_page.py / --no-login          # trang công khai (form đăng nhập)
    ... --wait-text "Lương hằng tháng"   # chờ chữ này hiện trước khi in (trang hay 'Đang tải…')
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
    ap = argparse.ArgumentParser(description="In cấu trúc trang để viết selector")
    ap.add_argument("path", help="đường dẫn trong hệ thống, ví dụ /applications/<id>/financials")
    ap.add_argument("--account", help="mã tài khoản đã lưu phiên")
    ap.add_argument("--no-login", action="store_true")
    ap.add_argument("--project")
    ap.add_argument("--wait-text", help="chờ chữ này hiện trước khi in")
    args = ap.parse_args()
    if not args.accounts and not args.no_login:
        print("Cần --account <mã> hoặc --no-login")
        return 2
    try:
        cfg = config.load(args.project)
    except config.ConfigError as error:
        print(error)
        return 2
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = session.launch_browser(p, headless=True)
        options = {"viewport": {"width": 1366, "height": 800}}
        if args.accounts:
            f = session.session_file(cfg, args.accounts)
            if not f.exists():
                print(f"Chưa có phiên đã lưu của {args.accounts}. Chạy scripts/auto_login.py {args.accounts} --headless")
                return 3
            options["storage_state"] = str(f)
        context = browser.new_context(**options)
        if args.accounts and not session.is_session_valid(cfg, context):
            print("Phiên đã hết hạn. Đăng nhập lại rồi chạy tiếp.")
            return 3
        page = context.new_page()
        page.goto(cfg.url + args.path, wait_until="domcontentloaded")
        if args.wait_text:
            page.get_by_text(args.wait_text).first.wait_for(state="visible", timeout=20000)
        else:
            page.wait_for_timeout(6000)
        print(f"# {page.url}")
        print(page.locator("body").aria_snapshot())
        browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
