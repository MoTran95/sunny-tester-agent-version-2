"""Ecommerce Lite · Đăng nhập · TC-009: Hiện form đăng nhập khi bấm Back hoặc mở lại địa chỉ trong ứng dụng sau khi đăng xuất.

Ngày viết: 2026-11-20. Nguồn: testing/ecommerce-lite/dang-nhap/test-case.md. Đăng nhập rồi đăng xuất nên khai invalidates_sessions.
"""
from login_common import che, doi_form, nut_sign_out, vao_cua_hang

CASE_INFO = {"code": "TC-009", "title": "Hiện form đăng nhập khi bấm Back hoặc mở lại địa chỉ trong ứng dụng sau khi đăng xuất",
             "accounts": [], "invalidates_sessions": ["SHOPPER"]}


def run(ctx):
    page = ctx.page
    vao_cua_hang(ctx)                                       # Bước 1
    page.evaluate("location.hash = '#profile'")             # Bước 2: mở Profile
    ctx.wait_text("My profile")
    nut = nut_sign_out(page)
    ctx.precondition("có nút Sign out đang hiện", len(nut) > 0)
    nut[0].click()                                          # Bước 3
    ctx.precondition("đã về form sau khi đăng xuất", doi_form(ctx))
    page.go_back()                                          # Bước 4: nút Back
    page.wait_for_timeout(1500)
    sau_back = doi_form(ctx, giay=3)
    hash_sau_back = page.evaluate("location.hash")
    che(ctx)
    ctx.screenshot("sau-back")
    page.evaluate("location.hash = '#my-orders'")           # Bước 5
    page.wait_for_timeout(1500)
    orders = doi_form(ctx, giay=3)
    page.evaluate("location.hash = '#dashboard'")           # Bước 6
    page.wait_for_timeout(1500)
    dashboard = doi_form(ctx, giay=3)
    che(ctx)
    ctx.screenshot("mo-dashboard-sau-dang-xuat")
    ctx.check_main("Bước 4: sau Back vẫn hiện form đăng nhập", sau_back, mark_text="Sign in to your workspace",
                   error_note="Lỗi ở bước 4 (nút Back): không hiện form đăng nhập sau khi đăng xuất.")
    ctx.check_main("Bước 5: mở #my-orders hiện form đăng nhập", orders)
    ctx.check_main("Bước 6: mở #dashboard hiện form đăng nhập", dashboard, mark_text="Sign in to your workspace",
                   error_note="Lỗi ở bước 6 (mở #dashboard): không hiện form đăng nhập.")
    ctx.check_minor("Bước 4: địa chỉ sau Back là #profile", hash_sau_back == "#profile", note=f"Địa chỉ: {hash_sau_back}")
