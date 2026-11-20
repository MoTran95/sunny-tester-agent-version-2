"""Ecommerce Lite · Đăng nhập · TC-003: Hiện "Email or password is incorrect." khi nhập email không tồn tại.

Ngày viết: 2026-11-20. Nguồn: testing/ecommerce-lite/dang-nhap/test-case.md. Cố ý sai 1 lần (email không có thật, mật khẩu mẫu
do thư viện đọc từ .env). Không chứa mật khẩu.
"""
from login_common import bam_use_customer, che, mo_form, theo_doi_dang_nhap

CASE_INFO = {"code": "TC-003", "title": "Hiện thông báo lỗi khi nhập email không tồn tại",
             "accounts": [], "ready_account": "SHOPPER", "wrong_attempts": 1}


def run(ctx):
    mo_form(ctx)                                            # Bước 1
    ds = theo_doi_dang_nhap(ctx.page)
    bam_use_customer(ctx)                                   # Bước 2
    # Bước 3 và 4: đổi email thành email không tồn tại (mật khẩu giữ nguyên), nhấn Enter
    ctx.submit_login("khongtontai@sunny.test", password_of="SHOPPER", expect_success=False, via="enter_in_password")
    ctx.poll_until(lambda: "Email or password is incorrect." in ctx.page_text(), seconds=10)
    ctx.page.wait_for_timeout(2000)
    body = ctx.page_text()
    email = ctx.page.locator("#email").input_value()
    mau = len(ctx.page.locator("#password").input_value())
    che(ctx)
    ctx.screenshot("email-khong-ton-tai")                   # Bước 5
    ctx.check_main("Bước 5: POST /api/auth/login trả 401", ds == [401], note=f"Các mã trả về: {ds}")
    ctx.check_main("Bước 5: hiện Email or password is incorrect.", "Email or password is incorrect." in body,
                   mark_text="Email or password is incorrect.",
                   error_note="Lỗi ở bước 5 (nhấn Enter): không thấy thông báo Email or password is incorrect.")
    ctx.check_main("Bước 5: vẫn ở form đăng nhập", "Sign in to your workspace" in body)
    ctx.check_minor("Bước 5: ô email giữ chữ vừa nhập", email == "khongtontai@sunny.test")
    ctx.check_minor("Bước 5: ô mật khẩu vẫn còn nội dung", mau > 0, note=f"Độ dài: {mau}")
