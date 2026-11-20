# Ecommerce Lite — tính năng Quên mật khẩu (SRS + phân tích 2026-11-20)
Đọc khi: viết test case, hỏi BA, chạy test cho Quên mật khẩu (mã `FORGOT`).

## Trạng thái
- Requirement do người dùng dán trong chat (bản gốc `evidence/ecommerce-lite/tai-lieu/yeu-cau-quen-mat-khau.md`) → SRS `srs/ecommerce-lite/quen-mat-khau.md` (4 story, 8 AC, 5 R, 0 M, 8 Q). Nhãn `theo tài liệu`, chưa đối chiếu hệ thống.
- Đã phân tích: `testing/ecommerce-lite/quen-mat-khau/` (bảng soát 13 đơn vị, 6 câu A + 3 câu B + 1 mục C). **Chưa gửi BA, chưa có TL.** Người dùng chọn "phân tích trước, chờ BA rồi viết test case" (2026-11-20). Đã viết test case `testing/ecommerce-lite/quen-mat-khau/test-case.md` (14 TC, chỉ phần ✅, chưa chạy; người dùng duyệt danh sách 2026-11-20). Phần ❓ (A1–A6, B1–B3) chưa có TC, chờ BA.

## Bẫy
- Hệ thống staging: bấm "Forgot password?" chỉ hiện toast "Password recovery is disabled in the training environment." (từ lượt khám phá đăng nhập) → chức năng chưa chạy được ở đây, test case chưa chạy được; câu C1 hỏi khi nào có.
- Không tự đặt số lần nhập sai OTP, thời gian chờ gửi lại; chờ BA (A2, A3).
- Ca nhập sai OTP nhiều lần: chỉ chạy khi biết giới hạn và người dùng đồng ý.
- Ca đổi mật khẩu thành công làm đổi mật khẩu thật của tài khoản test: không dùng `SHOPPER` khi chưa cập nhật `.env`; mỗi ca dùng mật khẩu mới khác nhau (tránh trùng 5 gần nhất).
- Tên ô/nút của tính năng chưa khám phá nên bước viết bằng việc cần làm; sửa khi hệ thống có tính năng.
