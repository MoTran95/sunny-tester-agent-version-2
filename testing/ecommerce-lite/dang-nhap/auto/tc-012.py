"""Ecommerce Lite · Đăng nhập · TC-012: Đăng nhập thành công khi nhập email viết hoa.

Ngày viết: 2026-11-20. Nguồn: testing/ecommerce-lite/dang-nhap/test-case.md. Mật khẩu do thư viện đọc từ .env. Không chứa mật khẩu.
"""
from login_common import bam_use_customer, mo_form, theo_doi_dang_nhap

CASE_INFO = {"code": "TC-012", "title": "Đăng nhập thành công khi nhập email viết hoa", "accounts": []}


def run(ctx):
    mo_form(ctx)                                            # Bước 1
    ds = theo_doi_dang_nhap(ctx.page)
    bam_use_customer(ctx)                                   # Bước 2
    # Bước 3 và 4: đổi email thành chữ hoa, nhấn Enter (đúng mật khẩu, không đếm vào bộ đếm sai)
    ctx.submit_login("SHOPPER@SUNNY.TEST", password_of="SHOPPER", expect_success=True, via="enter_in_password")
    ctx.wait_text("WELCOME, SUNNY")                         # Bước 5
    ctx.screenshot("dang-nhap-email-viet-hoa")
    ctx.check_main("Bước 5: POST /api/auth/login trả 200", ds == [200], note=f"Các mã trả về: {ds}")
    ctx.check_main("Bước 5: vào cửa hàng", "WELCOME, SUNNY" in ctx.page_text().upper(), mark_text="WELCOME",
                   error_note="Lỗi ở bước 5: email viết hoa không đăng nhập được.")
