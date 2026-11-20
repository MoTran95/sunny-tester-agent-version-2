"""Ecommerce Lite · Đăng nhập · TC-011: Không đăng nhập được khi mật khẩu đúng nhưng thêm một khoảng trắng ở cuối.

Ngày viết: 2026-11-20. Nguồn: testing/ecommerce-lite/dang-nhap/test-case.md. Cố ý sai 1 lần; mật khẩu do thư viện đọc từ .env. Không chứa mật khẩu.
"""
from login_common import EMAIL, bam_use_customer, che, mo_form, theo_doi_dang_nhap

CASE_INFO = {"code": "TC-011", "title": "Không đăng nhập được khi mật khẩu đúng nhưng thêm một khoảng trắng ở cuối",
             "accounts": [], "ready_account": "SHOPPER", "wrong_attempts": 1}


def run(ctx):
    mo_form(ctx)                                            # Bước 1
    ds = theo_doi_dang_nhap(ctx.page)
    bam_use_customer(ctx)                                   # Bước 2
    # Bước 3 và 4: thêm một dấu cách cuối mật khẩu, nhấn Enter
    ctx.submit_login(EMAIL, password_of="SHOPPER", variant="trailing_space", expect_success=False, via="enter_in_password")
    ctx.poll_until(lambda: "Email or password is incorrect." in ctx.page_text(), seconds=10)
    body = ctx.page_text()
    che(ctx)
    ctx.screenshot("mat-khau-them-dau-cach")                # Bước 5
    ctx.check_main("Bước 5: POST /api/auth/login trả 401", ds == [401], note=f"Các mã trả về: {ds}")
    ctx.check_main("Bước 5: hiện Email or password is incorrect.", "Email or password is incorrect." in body,
                   mark_text="Email or password is incorrect.",
                   error_note="Lỗi ở bước 5 (nhấn Enter): mật khẩu thừa dấu cách mà không báo lỗi.")
    ctx.check_main("Bước 5: vẫn ở form đăng nhập", "Sign in to your workspace" in body)
