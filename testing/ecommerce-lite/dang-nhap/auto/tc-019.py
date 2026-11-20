"""Ecommerce Lite · Đăng nhập · TC-019: Hiện thông báo khôi phục mật khẩu bị tắt khi bấm Forgot password?.

Ngày viết: 2026-11-20. Nguồn: testing/ecommerce-lite/dang-nhap/test-case.md.
"""
from login_common import che, mo_form

CASE_INFO = {"code": "TC-019", "title": "Hiện thông báo khôi phục mật khẩu bị tắt khi bấm Forgot password?", "accounts": []}


def run(ctx):
    mo_form(ctx)                                            # Bước 1
    truoc = ctx.page.url
    ctx.page.locator("#forgot-password").click()            # Bước 2
    ctx.wait_text("Password recovery is disabled in the training environment.", timeout_ms=8000)   # Bước 3
    che(ctx)
    body = ctx.page_text()
    ctx.screenshot("quen-mat-khau")
    ctx.check_main("Bước 3: hiện thông báo Password recovery is disabled in the training environment.",
                   "Password recovery is disabled in the training environment." in body,
                   mark_text="Password recovery is disabled in the training environment.",
                   error_note="Lỗi ở bước 3 (bấm Forgot password?): không thấy thông báo khôi phục bị tắt.")
    ctx.check_main("Bước 3: không chuyển trang", ctx.page.url == truoc and "Sign in to your workspace" in body,
                   note=f"Địa chỉ trước: {truoc}, sau: {ctx.page.url}")
