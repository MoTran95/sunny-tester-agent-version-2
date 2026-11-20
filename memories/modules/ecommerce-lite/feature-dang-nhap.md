# Ecommerce Lite — Đăng nhập (mã `LOGIN`)
Đọc khi: làm tiếp tính năng Đăng nhập (test plan, test case, chạy test). Trạng thái 2026-11-20: đã có nhật ký khám phá, SRS nháp (6 story, 18 AC), bảng phân tích requirement, câu hỏi BA (chưa gửi, 4 hỏi ngay / 3 hỏi sau / 1 tự kiểm tra). Chưa có test plan, test case.

## Sự thật đã quan sát (chi tiết ở `srs/ecommerce-lite/dang-nhap.md`)
- Tài khoản test: mã `SHOPPER` trong `.env` (vai trò Customer). Đăng nhập script: `auto_login.py SHOPPER --headless`; nhãn ô `Login email`, nút `Sign in`, API `/api/auth/login`, kiểm phiên `/api/me`.
- Sai thông tin → 401 `INVALID_CREDENTIALS` "Email or password is incorrect." (cùng câu cho email không tồn tại, mật khẩu sai, mật khẩu đổi hoa thường). Email không phân biệt hoa thường, bị cắt khoảng trắng. Trang một màn: địa chỉ bất kỳ trả 200 và hiện form khi chưa đăng nhập.
- Bộ đếm nhập sai của máy này đã dùng **3/3** (người test dặn trần 3, chưa biết ngưỡng khóa thật; `block_minutes` chưa khai). Muốn chạy thêm ca nhập sai phải hỏi người test, rồi `run_tests.py --reset-failure-counter` chỉ khi chắc.
- Tệp giao diện công khai: `/app.js`, `/store.js`, `/styles.css`; app.js không có ngưỡng khóa đăng nhập sai (không dùng để suy ra giới hạn).
- `session_minutes` còn `null` trong `auto-config.json` (chưa đo; chưa tự đặt số).

## Bẫy
- Git Bash đổi `/` thành đường dẫn Windows khi truyền `/` cho script: dùng PowerShell.
- Trang ẩn ô mật khẩu sau đăng nhập (không gỡ khỏi trang): `session.py` chờ `hidden` (đã sửa 2026-11-20). `inspect_page.py` cờ `--account` đã sửa. Trang tổng liệt kê tính năng có SRS dù chưa có test case (`docs_pages.py` đã sửa).
- Tài khoản mẫu và mật khẩu mẫu hiện công khai trên trang đăng nhập; vẫn đưa vào `.env`, không chép vào tài liệu.

## Việc tiếp
Chờ BA trả lời (ghi bằng `phan-tich-requirement/scripts/ghi-tl.py`) → test plan → test case. Làm lại ca nút Back sau đăng xuất (C1, không tốn lần sai).
