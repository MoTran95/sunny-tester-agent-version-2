"""Ecommerce Lite · Đăng nhập · TC-014: Chỉ gửi một yêu cầu đăng nhập khi bấm Sign in nhiều lần liên tiếp rất nhanh.

Ngày viết: 2026-11-20. Nguồn: testing/ecommerce-lite/dang-nhap/test-case.md. Mật khẩu do nút Use customer của trang điền. Không chứa mật khẩu.
"""
from login_common import bam_use_customer, mo_form, theo_doi_dang_nhap

CASE_INFO = {"code": "TC-014", "title": "Chỉ gửi một yêu cầu đăng nhập khi bấm Sign in nhiều lần liên tiếp rất nhanh", "accounts": []}


def run(ctx):
    mo_form(ctx)                                            # Bước 1
    ds = theo_doi_dang_nhap(ctx.page)
    bam_use_customer(ctx)                                   # Bước 2
    nut = ctx.page.locator("#sign-in-button")
    nut.click(click_count=3, delay=20)                      # Bước 3: ba lần bấm liên tiếp rất nhanh
    ctx.page.wait_for_timeout(300)
    vo_hieu = nut.is_disabled()
    ctx.wait_text("WELCOME, SUNNY")
    ctx.page.wait_for_timeout(1500)
    ctx.screenshot("sau-khi-bam-nhieu-lan")                 # Bước 4
    ctx.check_main("Bước 4: chỉ có 1 yêu cầu POST /api/auth/login", len(ds) == 1, note=f"Các mã trả về: {ds}",
                   error_note="Lỗi ở bước 4: gửi nhiều hơn một yêu cầu đăng nhập khi bấm nhiều lần.")
    ctx.check_main("Bước 4: đăng nhập thành công, vào cửa hàng", "WELCOME, SUNNY" in ctx.page_text().upper(), mark_text="WELCOME")
    ctx.check_minor("Bước 3: nút bị vô hiệu hóa ngay sau lần bấm đầu", vo_hieu)
