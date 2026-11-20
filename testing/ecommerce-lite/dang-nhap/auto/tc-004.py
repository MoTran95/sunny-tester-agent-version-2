"""Ecommerce Lite · Đăng nhập · TC-004: Hiện "Email or password is incorrect." khi email đúng nhưng mật khẩu sai.

Ngày viết: 2026-11-20. Bản hệ thống: chưa thấy số bản. Nguồn: testing/ecommerce-lite/dang-nhap/test-case.md.
Cố ý nhập sai ĐÚNG 1 lần bằng chuỗi giả; thư viện đếm vào bộ đếm sai. Không chứa mật khẩu thật.
"""
CASE_INFO = {
    "code": "TC-004",
    "title": "Hiện thông báo lỗi khi email đúng nhưng mật khẩu sai",
    "accounts": [],
    "ready_account": "SHOPPER",
    "wrong_attempts": 1,
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
    ctx.goto("/")                                           # Bước 1
    ctx.wait_text("Sign in to your workspace")
    # Trang kiểm phiên (GET /api/me) rồi vẽ lại form: nhập trước lúc đó thì ô mật khẩu bị xóa (đo 2026-11-20), nên chờ xong rồi mới nhập
    ctx.page.wait_for_load_state("networkidle")
    ctx.page.wait_for_timeout(1500)
    # Bước 2 đến 4: nhập email đúng, mật khẩu sai (chuỗi giả), nhấn Enter; thư viện gửi đúng một lần
    status = ctx.submit_login("shopper@sunny.test", "Sai@Matkhau1", expect_success=False, via="enter_in_password")
    ctx.poll_until(lambda: "Email or password is incorrect." in ctx.page_text(), seconds=10)
    body = ctx.page_text()
    mau = []
    for _ in range(4):                                      # đo độ dài ô mật khẩu theo thời gian (không in nội dung)
        mau.append(len(ctx.page.locator("input[type=password]").first.input_value()))
        ctx.page.wait_for_timeout(1000)
    ctx.page.evaluate(CHE_MAT_KHAU)                         # che khung mật khẩu mẫu ngay trước khi chụp
    ctx.screenshot("sai-mat-khau")                          # Bước 5
    ctx.check_main("Bước 5: POST /api/auth/login trả 401", status == 401, note=f"Mã trả về: {status}")
    ctx.check_main("Bước 5: hiện Email or password is incorrect.", "Email or password is incorrect." in body,
                   mark_text="Email or password is incorrect.",
                   error_note="Lỗi ở bước 5 (nhấn Enter): không thấy thông báo Email or password is incorrect.")
    ctx.check_main("Bước 5: vẫn ở form đăng nhập", "Sign in to your workspace" in body)
    ctx.check_minor("Bước 5: ô mật khẩu giữ nguyên nội dung", mau[-1] > 0,
                    note=f"Độ dài ô mật khẩu sau 0, 1, 2, 3 giây: {mau}")
