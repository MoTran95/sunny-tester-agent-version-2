"""Ecommerce Lite · Đăng nhập · TC-017: Hiện form đăng nhập ở tab 1 khi chuyển trang sau khi đã đăng xuất ở tab 2.

Ngày viết: 2026-11-20. Nguồn: testing/ecommerce-lite/dang-nhap/test-case.md. Hai tab cùng một phiên trình duyệt (cùng cookie).
"""
from login_common import che, doi_form, nut_sign_out, vao_cua_hang

CASE_INFO = {"code": "TC-017", "title": "Hiện form đăng nhập ở tab 1 khi chuyển trang sau khi đã đăng xuất ở tab 2",
             "accounts": [], "invalidates_sessions": ["SHOPPER"]}


def run(ctx):
    tab1 = ctx.page
    vao_cua_hang(ctx)                                       # Bước 1: tab 1 đã đăng nhập
    tab2 = tab1.context.new_page()                          # Bước 2: mở tab 2 cùng địa chỉ, vẫn đăng nhập
    try:
        tab2.goto(ctx.cfg.url + "/", wait_until="domcontentloaded")
        tab2.get_by_text("WELCOME, SUNNY").first.wait_for(state="visible", timeout=20_000)
        nut = nut_sign_out(tab2)
        ctx.precondition("tab 2 có nút Sign out đang hiện", len(nut) > 0)
        nut[0].click()                                      # Bước 3: đăng xuất ở tab 2
        ctx.precondition("tab 2 đã về form đăng nhập", doi_form(ctx, tab2))
    finally:
        tab2.close()
    tab1.bring_to_front()                                   # Bước 4: về tab 1, chuyển trang
    tab1.evaluate("location.hash = '#my-orders'")
    hien_form = doi_form(ctx, tab1)                         # Bước 5
    che(ctx, tab1)
    ctx.screenshot("tab-1-sau-khi-chuyen-trang")
    ctx.check_main("Bước 5: tab 1 hiện form đăng nhập", hien_form, mark_text="Sign in to your workspace",
                   error_note="Lỗi ở bước 5 (chuyển trang ở tab 1): vẫn hiện cửa hàng dù đã đăng xuất ở tab 2.")
