"""Ecommerce Lite · Đăng nhập · TC-008: Về form đăng nhập và báo đã đăng xuất khi bấm Sign out.

Ngày viết: 2026-11-20. Bản hệ thống: chưa thấy số bản. Nguồn: testing/ecommerce-lite/dang-nhap/test-case.md.
Dùng phiên đã lưu của SHOPPER; đăng xuất làm mất phiên máy chủ nên runner xóa phiên đã lưu sau ca. Không chứa mật khẩu.
"""
CASE_INFO = {
    "code": "TC-008",
    "title": "Về form đăng nhập và báo đã đăng xuất khi bấm Sign out",
    "accounts": ["SHOPPER"],
    "invalidates_sessions": ["SHOPPER"],
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
    page = ctx.page
    ctx.goto("/")                                           # Bước 1: đã đăng nhập sẵn bằng phiên đã lưu
    ctx.wait_text("WELCOME, SUNNY")
    nut = [b for b in page.get_by_role("button", name="Sign out").all() if b.is_visible()]
    ctx.precondition("có nút Sign out đang hiện", len(nut) > 0)
    # Bước 3: bấm Sign out, ghi mã trả về của yêu cầu đăng xuất
    with page.expect_response(lambda r: r.request.method == "POST" and r.url.rstrip("/").endswith("/api/auth/logout"), timeout=10_000) as info:
        nut[0].click()
    logout_status = info.value.status
    try:
        ctx.wait_text("You have been signed out.", timeout_ms=10_000)
        toast_hien = True
    except Exception:  # noqa: BLE001
        toast_hien = False
    ctx.wait_text("Sign in to your workspace")
    page.evaluate(CHE_MAT_KHAU)
    body = ctx.page_text()
    ctx.screenshot("sau-dang-xuat")                         # Bước 4
    email = page.get_by_label("Login email").first.input_value()
    mat_khau = page.locator("input[type=password]").first.input_value()
    me = page.evaluate("fetch('/api/me').then(r => r.status)")
    ctx.check_main("Bước 4: quay về form đăng nhập, ô email và mật khẩu trống",
                   "Sign in to your workspace" in body and email == "" and mat_khau == "", mark_text="Sign in to your workspace",
                   error_note="Lỗi ở bước 4: không về form đăng nhập hoặc ô còn nội dung.")
    ctx.check_main("Bước 4: POST /api/auth/logout trả 200", logout_status == 200, note=f"Mã trả về: {logout_status}")
    ctx.check_minor("Bước 4: sau đăng xuất /api/me trả 401", me == 401, note=f"Mã trả về: {me}")
    ctx.check_minor("Bước 3: hiện thông báo You have been signed out.", toast_hien, mark_text="You have been signed out.")
