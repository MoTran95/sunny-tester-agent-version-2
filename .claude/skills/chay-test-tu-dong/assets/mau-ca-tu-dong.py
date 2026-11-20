"""<Hệ thống> · <Tính năng> · TC-xxx: <tình huống một câu>.

Khuôn script ca. Lưu ở testing/<dự-án>/<tính-năng>/auto/tc-xxx.py. Không chứa mật khẩu:
- dùng phiên đã lưu (khai "accounts"), hoặc ctx.sign_in("<mã tài khoản>") khi chính bước đăng nhập/đăng xuất là một phần của ca;
- nhập sai: ctx.submit_login(<mã>, "<mật khẩu giả>", expect_success=False); mật khẩu đúng đổi hoa/thường: password_of="<mã>", variant="swap_letter_case".
Số bước trong tiêu đề ý kiểm trùng số bước của test case để dễ đối chiếu.
"""
CASE_INFO = {
    "code": "TC-xxx",
    "title": "<tình huống>",
    "accounts": ["<MÃ_TÀI_KHOẢN>"],          # tài khoản dùng phiên đã lưu; [] nếu ca chưa đăng nhập
    # "invalidates_sessions": ["<MÃ_TÀI_KHOẢN>"],   # ca làm mất phiên máy chủ (đăng xuất) → runner xóa file phiên đó
    # "ready_account": "<MÃ_TÀI_KHOẢN>", "wrong_attempts": 1,   # ca có cố ý nhập sai: tối đa bao nhiêu lần (trần do dự án khai trong auto-config.json, cộng dồn)
}


def run(ctx):
    ctx.goto("/")                                  # mở trang (đường dẫn tính từ địa chỉ gốc)
    ctx.wait_text("Danh sách việc")                # chờ chữ hiện, không chờ giây cố định
    body = ctx.page_text()
    ctx.screenshot("man-hinh-chinh")               # ảnh gốc làm evidence

    # Ý chính sai = Không đạt; ý phụ sai = Đạt kèm ý phụ sai.
    # mark_text: chữ trên trang để khoanh (xanh khi đạt, đỏ khi sai); error_note: "Lỗi ở bước N (…): thấy <gì>, đáng ra <gì>."
    ctx.check_main("Bước 4: vào Danh sách việc", "Danh sách việc" in body, mark_text="Danh sách việc")
    ctx.check_minor("Bước 5: không có chữ thừa", "DEFAULT" not in body, mark_text="DEFAULT",
                    error_note="Lỗi ở bước 5 (nhìn thanh điều hướng): hiện chữ DEFAULT, đáng ra không có.")
    # Điều kiện trước chưa đúng (dữ liệu, trạng thái): ctx.precondition("<mô tả>", điều_kiện) → ca ra Không kết luận, không phải Không đạt.
    # Dữ liệu test của dự án: ctx.test_data("khóa") đọc từ testing/<dự-án>/auto-data.json.
