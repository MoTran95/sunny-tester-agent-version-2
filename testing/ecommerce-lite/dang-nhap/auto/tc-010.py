"""Ecommerce Lite · Đăng nhập · TC-010: Trả lỗi 403 khi Customer gọi API quản trị /api/dashboard.

Ngày viết: 2026-11-20. Nguồn: testing/ecommerce-lite/dang-nhap/test-case.md. Chỉ đọc (GET), không đổi dữ liệu.
"""
from login_common import vao_cua_hang

CASE_INFO = {"code": "TC-010", "title": "Trả lỗi 403 khi Customer gọi API quản trị /api/dashboard", "accounts": []}


def run(ctx):
    vao_cua_hang(ctx)                                       # Bước 1
    # Bước 2 và 3: gọi API ngay trong trang (tương đương gõ vào Console)
    kq = ctx.page.evaluate("fetch('/api/dashboard').then(async r => [r.status, await r.text()])")
    ctx.screenshot("cua-hang-truoc-khi-goi-api")
    ctx.check_main("Bước 4: mã trạng thái 403", kq[0] == 403, note=f"Mã trả về: {kq[0]}")
    ctx.check_main("Bước 4: nội dung có error FORBIDDEN và message Operations portal access is required.",
                   "FORBIDDEN" in kq[1] and "Operations portal access is required." in kq[1], note=kq[1][:200])
