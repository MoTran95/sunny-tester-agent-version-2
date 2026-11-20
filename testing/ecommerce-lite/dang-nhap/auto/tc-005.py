"""Ecommerce Lite · Đăng nhập · TC-005: Báo lỗi ở cả hai ô và không gửi yêu cầu khi bỏ trống email và mật khẩu.

Ngày viết: 2026-11-20. Nguồn: testing/ecommerce-lite/dang-nhap/test-case.md. Không gửi yêu cầu nên không tính vào bộ đếm sai.
"""
from login_common import che, mo_form, theo_doi_dang_nhap

CASE_INFO = {"code": "TC-005", "title": "Báo lỗi ở cả hai ô và không gửi yêu cầu khi bỏ trống email và mật khẩu", "accounts": []}


def run(ctx):
    mo_form(ctx)                                            # Bước 1
    ds = theo_doi_dang_nhap(ctx.page)
    ctx.page.locator("#sign-in-button").click()             # Bước 2 và 3: để trống hai ô, bấm Sign in
    ctx.wait_text("Enter your email address.", timeout_ms=8000)
    ctx.page.wait_for_timeout(1500)
    body = ctx.page_text()
    che(ctx)
    ctx.screenshot("bo-trong-hai-o")                        # Bước 4
    ctx.check_main("Bước 3: hiện Enter your email address. dưới ô email", "Enter your email address." in body,
                   mark_text="Enter your email address.",
                   error_note="Lỗi ở bước 3 (bấm Sign in): không thấy Enter your email address.")
    ctx.check_main("Bước 3: hiện Enter your password. dưới ô mật khẩu", "Enter your password." in body, mark_text="Enter your password.",
                   error_note="Lỗi ở bước 3 (bấm Sign in): không thấy Enter your password.")
    ctx.check_main("Bước 4: Network không có yêu cầu POST /api/auth/login", ds == [], note=f"Các mã trả về: {ds}")
