"""Ecommerce Lite · Đăng nhập · TC-015: Đăng nhập thành công khi nhập đúng sau 3 lần đăng nhập sai liên tiếp.

Ngày viết: 2026-11-20. Nguồn: testing/ecommerce-lite/dang-nhap/test-case.md. Cố ý sai đúng 3 lần (trần của dự án là 10, cộng dồn;
người dùng chốt 2026-11-20 vì hệ thống chưa làm giới hạn). Mật khẩu do thư viện đọc từ .env. Không chứa mật khẩu.
"""
from login_common import EMAIL, bam_use_customer, che, mo_form, theo_doi_dang_nhap

CASE_INFO = {"code": "TC-015", "title": "Đăng nhập thành công khi nhập đúng sau 3 lần đăng nhập sai liên tiếp",
             "accounts": [], "ready_account": "SHOPPER", "wrong_attempts": 3}

LOI = "Email or password is incorrect."


def run(ctx):
    mo_form(ctx)                                            # Bước 1
    ds = theo_doi_dang_nhap(ctx.page)
    bam_use_customer(ctx)                                   # Bước 2: lần sai thứ 1, email không tồn tại
    ctx.submit_login("khongtontai@sunny.test", password_of="SHOPPER", expect_success=False, via="enter_in_password")
    ctx.poll_until(lambda: LOI in ctx.page_text(), seconds=10)
    sai1 = LOI in ctx.page_text()
    mo_form(ctx)                                            # Bước 3: lần sai thứ 2, mật khẩu sai
    ctx.submit_login(EMAIL, "Sai@Matkhau1", expect_success=False, via="enter_in_password")
    ctx.poll_until(lambda: LOI in ctx.page_text(), seconds=10)
    sai2 = LOI in ctx.page_text()
    mo_form(ctx)                                            # Bước 4: lần sai thứ 3, mật khẩu đúng thêm dấu cách cuối
    bam_use_customer(ctx)
    ctx.submit_login(EMAIL, password_of="SHOPPER", variant="trailing_space", expect_success=False, via="enter_in_password")
    ctx.poll_until(lambda: LOI in ctx.page_text(), seconds=10)
    sai3 = LOI in ctx.page_text()
    che(ctx)
    ctx.screenshot("lan-sai-thu-3")
    mo_form(ctx)                                            # Bước 5: đăng nhập đúng
    ctx.submit_login(EMAIL, password_of="SHOPPER", expect_success=True, via="button")
    ctx.wait_text("WELCOME, SUNNY")                         # Bước 6
    ctx.screenshot("dang-nhap-dung-sau-3-lan-sai")
    ctx.check_main("Bước 2: lần sai thứ 1 hiện Email or password is incorrect.", sai1, mark_text=None)
    ctx.check_main("Bước 3: lần sai thứ 2 hiện Email or password is incorrect.", sai2)
    ctx.check_main("Bước 4: lần sai thứ 3 hiện Email or password is incorrect.", sai3)
    ctx.check_main("Bước 6: đăng nhập thành công, vào cửa hàng, không bị khóa", "WELCOME, SUNNY" in ctx.page_text().upper(),
                   mark_text="WELCOME", note=f"Các mã trả về: {ds}",
                   error_note="Lỗi ở bước 6: đăng nhập đúng sau 3 lần sai nhưng không vào được cửa hàng.")
