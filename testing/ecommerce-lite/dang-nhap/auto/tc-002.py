"""Ecommerce Lite · Đăng nhập · TC-002: Đăng nhập thành công và vào cửa hàng khi nhập đúng email và mật khẩu.

Ngày viết: 2026-11-20. Bản hệ thống: chưa thấy số bản. Nguồn: testing/ecommerce-lite/dang-nhap/test-case.md.
Không chứa mật khẩu: thư viện đọc mật khẩu của SHOPPER trong .env và bấm Sign in đúng một lần.
"""
CASE_INFO = {
    "code": "TC-002",
    "title": "Đăng nhập thành công và vào cửa hàng khi nhập đúng email và mật khẩu",
    "accounts": [],
    "invalidates_sessions": [],
}


def run(ctx):
    ctx.goto("/")                                           # Bước 1
    ctx.wait_text("Sign in to your workspace")
    ctx.sign_in("SHOPPER")                                  # Bước 2 đến 3: điền email, mật khẩu đúng, bấm Sign in một lần
    ctx.wait_text("WELCOME, SUNNY")                         # Bước 4: chờ vào cửa hàng
    body = ctx.page_text()
    ctx.screenshot("cua-hang-sau-dang-nhap")
    ctx.check_main("Bước 4: đăng nhập thành công (POST /api/auth/login trả 200) và vào cửa hàng",
                   "WELCOME, SUNNY" in body.upper(), mark_text="WELCOME",
                   error_note="Lỗi ở bước 4 (chờ vài giây): không vào được cửa hàng sau khi bấm Sign in.")
    ctx.check_minor("Bước 4: có các mục Shop, My orders, Profile, Bag",
                    all(t in body for t in ("Shop", "My orders", "Profile", "Bag")), mark_text=["My orders", "Profile"])
