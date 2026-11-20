"""Hàm dùng chung cho các ca tự động của tính năng Đăng nhập (Ecommerce Lite). Không chứa mật khẩu.

Bẫy đã đo (2026-11-20): trang kiểm phiên (GET /api/me) rồi vẽ lại form; gõ trước lúc đó thì ô mật khẩu bị xóa.
Nên luôn mở form bằng mo_form() (chờ trang tải xong) trước khi nhập.
"""
import re

CHE_MAT_KHAU = """() => {
  for (const b of document.querySelectorAll('button')) {
    if (!/^Use customer$/i.test(b.textContent.trim())) continue;
    let e = b.parentElement;
    while (e && !(e.innerText.includes('Customer training login') && !e.innerText.includes('Email address'))) e = e.parentElement;
    if (e) e.style.filter = 'blur(8px)';
  }
}"""
EMAIL = "shopper@sunny.test"
TIEU_DE_FORM = "Sign in to your workspace"


def mo_form(ctx):
    """Mở trang chủ khi chưa đăng nhập và chờ form sẵn sàng (đã kiểm phiên xong)."""
    ctx.goto("/")
    ctx.wait_text(TIEU_DE_FORM)
    ctx.page.wait_for_load_state("networkidle")
    ctx.page.wait_for_timeout(1500)


def che(ctx, page=None):
    """Làm mờ khung tài khoản mẫu (hiện mật khẩu mẫu) ngay trước khi chụp ảnh."""
    (page or ctx.page).evaluate(CHE_MAT_KHAU)


def theo_doi_dang_nhap(page):
    """Ghi lại mã trả về của mọi yêu cầu POST /api/auth/login (trả về danh sách, tự cập nhật)."""
    ds = []
    page.on("response", lambda r: ds.append(r.status) if r.request.method == "POST" and r.url.rstrip("/").endswith("/api/auth/login") else None)
    return ds


def bam_use_customer(ctx):
    ctx.page.get_by_role("button", name=re.compile("^Use customer$", re.I)).first.click()


def nut_sign_out(page):
    return [b for b in page.get_by_role("button", name="Sign out").all() if b.is_visible()]


def form_dang_hien(ctx, page=None):
    return (page or ctx.page).get_by_text(TIEU_DE_FORM).first.is_visible()


def doi_form(ctx, page=None, giay=8):
    """Chờ form đăng nhập hiện lại (sau đăng xuất hoặc khi bị đưa về form); trả True/False."""
    pg = page or ctx.page
    for _ in range(int(giay * 2)):
        if form_dang_hien(ctx, pg):
            return True
        pg.wait_for_timeout(500)
    return False


def vao_cua_hang(ctx):
    """Đăng nhập đúng bằng SHOPPER (mật khẩu do thư viện đọc từ .env) và chờ vào cửa hàng."""
    mo_form(ctx)
    ctx.sign_in("SHOPPER")
    ctx.wait_text("WELCOME, SUNNY")
