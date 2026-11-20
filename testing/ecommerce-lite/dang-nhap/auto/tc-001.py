"""Ecommerce Lite · Đăng nhập · TC-001: Hiện form đăng nhập khi mở trang chủ lúc chưa đăng nhập.

Ngày viết: 2026-11-20. Bản hệ thống: chưa thấy số bản. Nguồn: testing/ecommerce-lite/dang-nhap/test-case.md.
Không chứa mật khẩu. Khung "Customer training login" hiện mật khẩu mẫu trên trang nên được làm mờ trước khi chụp ảnh.
"""
CASE_INFO = {
    "code": "TC-001",
    "title": "Hiện form đăng nhập khi mở trang chủ lúc chưa đăng nhập",
    "accounts": [],
}

CHE_MAT_KHAU = """() => {
  for (const b of document.querySelectorAll('button')) {
    if (!/^Use customer$/i.test(b.textContent.trim())) continue;
    let e = b.parentElement;
    while (e && !(e.innerText.includes('Customer training login') && !e.innerText.includes('Email address'))) e = e.parentElement;
    if (e) e.style.filter = 'blur(8px)';
  }
}"""


def run(ctx):
    ctx.goto("/")                                           # Bước 1: mở trang khi chưa đăng nhập
    ctx.wait_text("Sign in to your workspace")
    ctx.page.evaluate(CHE_MAT_KHAU)
    body = ctx.page_text()
    ctx.screenshot("form-dang-nhap")                        # Bước 2: nhìn màn hình hiện ra
    ctx.check_main("Bước 2: hiện form đăng nhập có ô email, ô mật khẩu, nút Sign in",
                   all(t in body for t in ("Email address", "Password", "Sign in")), mark_text="Sign in to your workspace")
    ctx.check_main("Bước 2: không vào thẳng cửa hàng", "WELCOME, SUNNY" not in body.upper())
    ctx.check_minor("Bước 2: có hai tab Sign in và Create account, ô Remember me, nút Show, liên kết Forgot password?",
                    all(t in body for t in ("Create account", "Remember me on this device", "Show", "Forgot password?")),
                    mark_text=["Create account", "Forgot password?"])
