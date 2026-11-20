"""Ecommerce Lite · Đăng nhập · TC-018: Hiện mật khẩu thành chữ khi bấm Show và ẩn lại khi bấm Hide.

Ngày viết: 2026-11-20. Nguồn: testing/ecommerce-lite/dang-nhap/test-case.md. Mật khẩu do nút Use customer điền.
KHÔNG chụp ảnh lúc mật khẩu đang hiện (lộ mật khẩu); kiểm bằng thuộc tính type, ảnh chỉ chụp sau khi đã ẩn lại.
"""
import re

from login_common import bam_use_customer, che, mo_form

CASE_INFO = {"code": "TC-018", "title": "Hiện mật khẩu thành chữ khi bấm Show và ẩn lại khi bấm Hide", "accounts": []}


def run(ctx):
    mo_form(ctx)                                            # Bước 1
    bam_use_customer(ctx)                                   # Bước 2
    ctx.precondition("ô mật khẩu đang ẩn và có nội dung", ctx.page.locator("#password").get_attribute("type") == "password"
                     and len(ctx.page.locator("#password").input_value()) > 0)
    nut = ctx.page.get_by_role("button", name=re.compile("(Show|Hide)", re.I)).filter(has_not_text="Sign").first
    nut.click()                                             # Bước 3: bấm Show
    ctx.page.wait_for_timeout(500)
    kieu_hien = ctx.page.locator("#password").get_attribute("type")
    ten_hien = (nut.inner_text() or "").strip()
    nut.click()                                             # Bước 4: bấm Hide
    ctx.page.wait_for_timeout(500)
    kieu_an = ctx.page.locator("#password").get_attribute("type")
    ten_an = (nut.inner_text() or "").strip()
    che(ctx)
    ctx.screenshot("mat-khau-da-an-lai")
    ctx.check_main("Bước 3: ô mật khẩu hiện chữ nhìn thấy được", kieu_hien == "text", note=f"type = {kieu_hien}",
                   error_note="Lỗi ở bước 3 (bấm Show): ô mật khẩu vẫn ẩn.")
    ctx.check_main("Bước 4: ô mật khẩu ẩn lại", kieu_an == "password", note=f"type = {kieu_an}")
    ctx.check_minor("Bước 3: nút đổi thành Hide", ten_hien == "Hide", note=f"Chữ trên nút: {ten_hien}")
    ctx.check_minor("Bước 4: nút trở về Show", ten_an == "Show", note=f"Chữ trên nút: {ten_an}")
