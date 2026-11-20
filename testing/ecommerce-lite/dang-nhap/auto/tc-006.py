"""Ecommerce Lite · Đăng nhập · TC-006: Báo lỗi ở ô mật khẩu và không gửi yêu cầu khi bỏ trống mật khẩu.

Ngày viết: 2026-11-20. Nguồn: testing/ecommerce-lite/dang-nhap/test-case.md. Email `abc` chỉ để có chữ trong ô; ca không kiểm gì về ô email.
"""
from login_common import che, mo_form, theo_doi_dang_nhap

CASE_INFO = {"code": "TC-006", "title": "Báo lỗi ở ô mật khẩu và không gửi yêu cầu khi bỏ trống mật khẩu", "accounts": []}


def run(ctx):
    mo_form(ctx)                                            # Bước 1
    ds = theo_doi_dang_nhap(ctx.page)
    ctx.page.locator("#email").click()
    ctx.page.locator("#email").press_sequentially("abc")    # Bước 2
    ctx.page.locator("#password").click()                   # Bước 3: để trống mật khẩu
    ctx.page.locator("#password").press("Enter")            # Bước 4
    ctx.wait_text("Enter your password.", timeout_ms=8000)
    ctx.page.wait_for_timeout(1500)
    body = ctx.page_text()
    che(ctx)
    ctx.screenshot("bo-trong-mat-khau")                     # Bước 5
    ctx.check_main("Bước 5: hiện Enter your password. dưới ô mật khẩu", "Enter your password." in body, mark_text="Enter your password.",
                   error_note="Lỗi ở bước 5 (nhấn Enter): không thấy Enter your password.")
    ctx.check_main("Bước 5: Network không có yêu cầu POST /api/auth/login", ds == [], note=f"Các mã trả về: {ds}")
