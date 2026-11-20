"""Ecommerce Lite · Đăng nhập · TC-007: Vẫn đăng nhập và vào lại cửa hàng khi tải lại trang sau khi đã đăng nhập.

Ngày viết: 2026-11-20. Bản hệ thống: chưa thấy số bản. Nguồn: testing/ecommerce-lite/dang-nhap/test-case.md.
Dùng phiên đã lưu của SHOPPER (auto_login.py). Không chứa mật khẩu.
"""
CASE_INFO = {
    "code": "TC-007",
    "title": "Vẫn đăng nhập và vào lại cửa hàng khi tải lại trang sau khi đã đăng nhập",
    "accounts": ["SHOPPER"],
}


def run(ctx):
    ctx.goto("/")                                           # Bước 1: đã đăng nhập sẵn bằng phiên đã lưu
    ctx.wait_text("WELCOME, SUNNY")
    ctx.page.reload(wait_until="domcontentloaded")          # Bước 2: tải lại trang
    ctx.wait_text("WELCOME, SUNNY")                         # Bước 3: chờ cửa hàng hiện lại
    body = ctx.page_text()
    ctx.screenshot("cua-hang-sau-tai-lai")
    form_hien = ctx.page.get_by_label("Login email").first.is_visible()
    me = ctx.page.evaluate("fetch('/api/me').then(r => r.status)")
    ctx.check_main("Bước 3: không hiện form đăng nhập, vào lại cửa hàng sau khi tải lại",
                   (not form_hien) and "WELCOME, SUNNY" in body.upper(), mark_text="WELCOME",
                   error_note="Lỗi ở bước 3 (tải lại trang): hiện lại form đăng nhập, đáng ra vẫn đăng nhập.")
    ctx.check_minor("Bước 3: /api/me trả 200", me == 200, note=f"Mã trả về: {me}")
