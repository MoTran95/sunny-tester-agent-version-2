"""Ecommerce Lite · Đăng nhập · TC-016: Hệ thống trả đúng thông tin người đang đăng nhập khi xem /api/me sau đăng nhập.

Ngày viết: 2026-11-20. Nguồn: testing/ecommerce-lite/dang-nhap/test-case.md. Chỉ đọc (GET).
"""
import json

from login_common import EMAIL, vao_cua_hang

CASE_INFO = {"code": "TC-016", "title": "Hệ thống trả đúng thông tin người đang đăng nhập khi xem /api/me sau đăng nhập", "accounts": []}


def run(ctx):
    vao_cua_hang(ctx)                                       # Bước 1
    kq = ctx.page.evaluate("fetch('/api/me').then(async r => [r.status, await r.text()])")   # Bước 2 và 3
    ctx.screenshot("cua-hang-truoc-khi-goi-api")
    try:
        user = json.loads(kq[1]).get("user", {})
    except ValueError:
        user = {}
    ctx.check_main("Bước 4: mã trạng thái 200", kq[0] == 200, note=f"Mã trả về: {kq[0]}")
    ctx.check_main("Bước 4: user có email shopper@sunny.test, name Sunny Shopper, role Customer",
                   user.get("email", "").lower() == EMAIL and user.get("name") == "Sunny Shopper" and user.get("role") == "Customer",
                   note=f"email={user.get('email')}, name={user.get('name')}, role={user.get('role')}")
    ctx.check_minor("Bước 4: user có id và workspaceId", bool(user.get("id")) and bool(user.get("workspaceId")))
