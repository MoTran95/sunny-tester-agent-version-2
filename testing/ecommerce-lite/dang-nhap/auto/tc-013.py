"""Ecommerce Lite · Đăng nhập · TC-013: Đăng nhập thành công khi email có khoảng trắng ở đầu và cuối.

Ngày viết: 2026-11-20. Nguồn: testing/ecommerce-lite/dang-nhap/test-case.md. Kết quả mong đợi mới thấy trong tệp giao diện (chưa thử trên hệ thống).
Mật khẩu do thư viện đọc từ .env. Không chứa mật khẩu.
"""
from login_common import EMAIL, bam_use_customer, mo_form, theo_doi_dang_nhap

CASE_INFO = {"code": "TC-013", "title": "Đăng nhập thành công khi email có khoảng trắng ở đầu và cuối", "accounts": []}


def run(ctx):
    mo_form(ctx)                                            # Bước 1
    ds = theo_doi_dang_nhap(ctx.page)
    bam_use_customer(ctx)                                   # Bước 2
    # Bước 3 và 4: email có một dấu cách đầu và một dấu cách cuối, nhấn Enter
    ctx.submit_login(" " + EMAIL + " ", password_of="SHOPPER", expect_success=True, via="enter_in_password")
    ctx.page.wait_for_timeout(5000)
    body = ctx.page_text()
    vao = "WELCOME, SUNNY" in body.upper()
    ctx.screenshot("email-co-khoang-trang")                 # Bước 5
    ctx.check_main("Bước 5: POST /api/auth/login trả 200", ds == [200], note=f"Các mã trả về: {ds}")
    ctx.check_main("Bước 5: vào cửa hàng", vao, mark_text="WELCOME",
                   error_note="Lỗi ở bước 5: email thừa khoảng trắng đầu/cuối không đăng nhập được, đáng ra được cắt.")
