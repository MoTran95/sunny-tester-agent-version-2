"""Khuôn script re-test một bug "chữ không được xuất hiện" (ví dụ chữ thừa, câu báo sai) trên thanh/khung của màn hình.

Cách dùng: sao chép thành `testing/<dự-án>/<tính-năng>/auto/retest-bug-<số>.py` (tên KHÔNG bắt đầu bằng `tc-`,
để `--feature` không chạy kèm), rồi chỉ sửa phần "ĐIỀN" bên dưới. Phần `run` giữ nguyên.
Bug thuộc loại khác (nhập dữ liệu, bấm nút, luồng nhiều bước) thì viết lại `run` theo khuôn `chay-test-tu-dong/assets/mau-ca-tu-dong.py`.

Ý chính (check_main) = từng chỗ trong "Phạm vi ảnh hưởng" của bug → điều kiện đóng bug.
Ý phụ (check_minor, trong BIEN_THE) = biến thể → ghi nhận, không tính vào điều kiện đóng; lỗi script ở biến thể được ghi
"chưa kiểm được", không im lặng. Không có mật khẩu trong script: dùng phiên đã lưu (`auto_login.py <tài khoản…> --headless` ngay trước khi chạy).

Chạy: python -X utf8 scripts/run_tests.py --case-id <tính-năng>/retest-bug-<số> --bug-build <số build lúc tạo bug>
Sau đó: python -X utf8 .claude/skills/lap-ke-hoach-retest/scripts/ghi-lich-su-retest.py <file bug> --ket-qua <result-*.json> --phien-ban <số> [--ghi]
"""
import re

# ===== ĐIỀN =====
CASE_INFO = {
    "code": "RT-BUG-<số>",
    "title": "Re-test BUG-<số>: <mô tả ngắn lỗi đã sửa>",
    "accounts": ["<tài khoản 1>", "<tài khoản 2>"],  # đủ MỌI chỗ trong Phạm vi ảnh hưởng của bug
}
OPEN_PATH = "/"                       # đường dẫn mở sau khi có phiên (như bước tái hiện của bug)
WAIT_TEXT = "<chữ báo trang đã tải xong>"
AREA = "header"                       # vùng cần kiểm (selector CSS), ví dụ thanh điều hướng
FORBIDDEN = "<chữ không được còn>"    # ví dụ chữ thừa; so khớp nguyên từ
ERROR_NOTE = "Lỗi ở bước <N> (<việc làm>): vẫn thấy <FORBIDDEN>, đáng ra không có."
# Mỗi chỗ trong phạm vi: (tài khoản, [chữ BẮT BUỘC có])
SCOPE = [
    ("<tài khoản 1>", ["<chữ phải có, ví dụ mã và vai trò>"]),
    ("<tài khoản 2>", ["<chữ phải có>"]),
]
# Biến thể (tối đa 3). Mỗi mục: (tên biến thể, hàm(ctx, trang) → (đạt: bool, ghi chú: str))
BIEN_THE = []


# ===== GIỮ NGUYÊN =====
FORBIDDEN_RE = re.compile(rf"\b{re.escape(FORBIDDEN)}\b")


def _area_text(ctx, account):
    page = ctx.page_for(account)
    area = page.locator(AREA)
    return area.first.inner_text() if area.count() else ctx.page_text(account)[:400]


def _line(text):
    return "nội dung: " + " | ".join(s.strip() for s in text.splitlines() if s.strip())


def run(ctx):
    for account, must_have in SCOPE:
        ctx.goto(OPEN_PATH, account=account)
        ctx.wait_text(WAIT_TEXT, account=account)
        ctx.page_for(account).wait_for_timeout(1000)  # trang hay ở "Đang tải…" vài giây
        text = _area_text(ctx, account)
        ctx.screenshot(f"{account.lower()}-man-hinh", account=account)
        ctx.check_main(f"{account}: có đủ {', '.join(must_have)}", all(w in text for w in must_have), _line(text), account=account)
        ctx.check_main(f"{account}: không còn chữ {FORBIDDEN}", FORBIDDEN_RE.search(text) is None, _line(text),
                       mark_text=FORBIDDEN, account=account, error_note=ERROR_NOTE)

    first = SCOPE[0][0]
    ctx.goto(OPEN_PATH, account=first)
    ctx.wait_text(WAIT_TEXT, account=first)
    for name, fn in BIEN_THE[:3]:
        try:
            passed, note = fn(ctx, ctx.page_for(first))
            ctx.check_minor(name, passed, note, account=first)
        except Exception as error:  # noqa: BLE001
            first_line = (str(error).splitlines() or [""])[0]
            ctx.check_minor(name, False, f"Chưa kiểm được biến thể này (lỗi script {type(error).__name__}: {first_line}); làm tay")
