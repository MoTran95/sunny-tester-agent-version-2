# Đăng nhập — nhật ký khám phá

Ngày: 2026-11-20 · Hệ thống: https://staging-ecommerce-lite.vercel.app/ (môi trường staging, chân trang ghi "Sunny Commerce training environment"; không thấy số phiên bản)
Khung nhìn: 1024×768. Ảnh: `screenshots/NN-….png`. Người làm: Mo Tran (người test), mình (trợ lý) khám phá.
Cách làm: phần không cần mật khẩu mình tự thao tác trong trình duyệt; phần cần mật khẩu chạy bằng script [kham-pha-dang-nhap.py](kham-pha-dang-nhap.py) (mật khẩu đọc từ `.env`, không in ra, không có trong file). Số lần đăng nhập sai tối đa 3 theo người test dặn (chưa biết ngưỡng khóa của hệ thống); đã dùng đúng 3 lần.

## 0. Bảng phủ
| Nhóm ca | Trạng thái | Hàng nhật ký / lý do |
|---|---|---|
| Luồng chính thành công | Đã làm | #12, #10, #11, #15 |
| Từng nhánh lỗi | Đã làm | #2, #3, #7, #8, #9 |
| Từng vai trò (ai thấy gì, ai không có nút) | Chưa làm | Mới có một tài khoản khách (Customer); chưa có tài khoản vai trò khác (xem mục 3) |
| Đổi ngôn ngữ | Không áp dụng | Màn hình đăng nhập không có nút đổi ngôn ngữ; mọi chữ là tiếng Anh |
| Tải lại trang, nút Back, hai tab | Đã làm | Tải lại #13, hai tab #14 và #17; nút Back chưa ra kết quả có nghĩa (xem mục 3) |
| Link sâu khi chưa đăng nhập / thiếu quyền; địa chỉ không tồn tại | Đã làm | #19, #20 (thiếu quyền: chỉ có một vai trò, xem mục 3) |
| Phản hồi mạng (mã trạng thái, `GET /api`) | Đã làm | #1, #7–#12, #16, #21 |
| Tệp giao diện (chuỗi thông báo) | Đã làm | #24 |
| Kiểm tra ô nhập (để trống, sai định dạng, khoảng trắng, chữ hoa, Enter, thuộc tính HTML) | Đã làm | #2, #3, #4, #10, #11; độ dài rất dài và ký tự đặc biệt chưa làm (mục 3) |
| Đăng nhập sai nhiều lần (giới hạn) | Chưa làm | Có thể khóa hệ thống: đã dừng sau 3 lần sai theo người test dặn, không thấy bị chặn (#23) |
| Hết hạn phiên | Chưa làm | Cần chờ thời gian dài (xem mục 3) |

## 1. Đã thấy (có thao tác thật)
| # | Thao tác | Kết quả quan sát (nguyên văn khi có) | Ảnh |
|---|---|---|---|
| 1 | Mở `/` khi chưa đăng nhập | Trang một màn: hai tab "Sign in" và "Create account"; khung "Customer training login" (email và mật khẩu mẫu của môi trường thử, nút "Use customer" tự điền); ô "Email address", "Password" (nút "Show"), "Forgot password?", hộp "Remember me on this device", nút "Sign in". Trình duyệt tự gọi `GET /api/me` → 401. | Ảnh 01 (nửa dưới ảnh); mạng: F12 → Network |
| 2 | Để trống cả hai ô, bấm "Sign in" | Hiện "Enter your email address." dưới ô email và "Enter your password." dưới ô mật khẩu, hai ô viền đỏ. Không có lệnh gọi `/api/auth/login` nào (danh sách mạng chỉ có `GET /api/me` → 401). | — (không có ảnh lưu; F12 → Network, bấm Sign in khi để trống) |
| 3 | Gõ `abc` vào ô email, để trống mật khẩu, bấm "Sign in" | Chỉ hiện "Enter your password."; ô email không báo lỗi định dạng dù `abc` không phải email. | — (như #2) |
| 4 | Đọc thuộc tính ô nhập bằng công cụ nhà phát triển | Form đăng nhập `id=login-form` có `novalidate`; email `type=email`, `required`, `autocomplete=username`; mật khẩu `type=password`, `required`, `autocomplete=current-password`; cả hai không có `maxlength`. | — (F12 → Elements) |
| 5 | Bấm "Forgot password?" | Hiện thông báo tạm: "Password recovery is disabled in the training environment." Trang không đổi. | — (thông báo tạm biến mất sau vài giây) |
| 6 | Nút "Show" | Chưa bấm thử; chỉ biết từ tệp giao diện: đổi kiểu ô mật khẩu giữa ẩn và hiện (xem #24). | — |
| 7 | Email `shopper@sunny.test` + một mật khẩu sai, bấm "Sign in" | Máy chủ trả lỗi; hiện "Email or password is incorrect." ở khung đỏ dưới nút. Email còn nguyên trong ô, ô mật khẩu bị xóa trống. Mã lỗi trả về `INVALID_CREDENTIALS` (script đọc phản hồi; bộ đếm sai tính đây là lần sai, mã 400 hoặc 401). | Ảnh 01 |
| 8 | Email không tồn tại `nobody.xyz@sunny.test` + một mật khẩu bất kỳ | `POST /api/auth/login` → 401, mã `INVALID_CREDENTIALS`, cùng câu "Email or password is incorrect." như #7. Email giữ nguyên, mật khẩu xóa. | Ảnh 02 |
| 9 | Email đúng + mật khẩu đúng nhưng đổi hoa/thường một chữ cái | 401, cùng câu "Email or password is incorrect." → mật khẩu phân biệt chữ hoa, thường. | Ảnh 03 |
| 10 | Email viết hoa toàn bộ (`SHOPPER@SUNNY.TEST`) + mật khẩu đúng, nhấn Enter trong ô mật khẩu | 200; hiện "Welcome back, Sunny!"; vào được trang cửa hàng. Phản hồi trả email `shopper@sunny.test` (chữ thường). | Ảnh 04 |
| 11 | Email có hai dấu cách đầu và cuối + mật khẩu đúng, bấm "Sign in" | 200; "Welcome back, Sunny!". Mã nguồn giao diện cắt khoảng trắng của email trước khi gửi (xem #24). | — (script; ảnh không lưu) |
| 12 | Email và mật khẩu đúng của tài khoản test, bấm "Sign in" | 200. Phản hồi: tên "Sunny Shopper", vai trò "Customer". Thông báo "Welcome back, Sunny!". Cookie `sunny_session`: `HttpOnly`, `Secure`, `SameSite=Lax`. `localStorage` và `sessionStorage` đều trống. Màn hình sau đăng nhập có "Shop", "My orders", "Profile", giỏ "Bag 0", nút "Sign out", lời chào "Welcome, Sunny". | Ảnh 05 |
| 13 | Tải lại trang sau khi đăng nhập | Vẫn đăng nhập, thấy nút "Sign out", không thấy ô mật khẩu. | Ảnh 06 |
| 14 | Mở tab thứ hai trong cùng phiên, vào `/` | Tab thứ hai cũng đã đăng nhập (thấy "Sign out"). | — (script) |
| 15 | Đăng nhập đúng có tích "Remember me on this device" so với không tích | Cả hai lần đều 200 và cùng một cookie `sunny_session`; thời điểm hết hạn của hai cookie cách nhau 16 giây, đúng bằng khoảng cách giữa hai lần đăng nhập → thời hạn cookie giống nhau, không thấy "Remember me" đổi gì. | — (script) |
| 16 | Bấm "Sign out" | `POST /api/auth/logout` → 200; hiện "You have been signed out."; quay lại form đăng nhập; `GET /api/me` → 401. | Ảnh 07 |
| 17 | Sau khi tab 1 đăng xuất, kiểm tab 2 (cùng phiên) | `GET /api/me` ở tab 2 → 401; tải lại tab 2 thì hiện form đăng nhập. | — (script) |
| 18 | Nút Back sau đăng xuất | Chưa có kết quả có nghĩa: tab thử mở từ trang trắng nên Back quay về trang trắng. Chưa kiểm được. | — |
| 19 | Chưa đăng nhập, mở thẳng `/#profile` | Địa chỉ giữ nguyên `/#profile` nhưng nội dung là form đăng nhập; không thấy trang hồ sơ. | Ảnh 08 |
| 20 | Chưa đăng nhập, mở `/khong-ton-tai` | HTTP 200 và hiện luôn trang đăng nhập (không có trang 404). | Ảnh 09 |
| 21 | Chưa đăng nhập, gọi `GET /api/me` | 401. | — (script, F12 → Network) |
| 22 | Vai trò hiển thị | Chỉ có một tài khoản khách: vai trò "Customer". Khung trên trang chỉ nhắc "Customer training login". | Ảnh 05 |
| 23 | Ba lần đăng nhập sai liên tiếp (#7, #8, #9) | Cả ba đều là lỗi thông thường; không thấy mã 429, không thấy thông báo bị chặn; đăng nhập đúng ngay sau đó vẫn được (#10). Đã dừng ở 3 lần theo người test dặn, nên chưa biết ngưỡng thật. | Ảnh 01–04 |
| 24 | Đọc tệp giao diện `/app.js` (công khai) | Các chuỗi: "Enter your email address.", "Enter your password.", "Password recovery is disabled in the training environment.", "Signing in…" (chữ trên nút khi đang gửi, nút bị khóa trong lúc chờ), "Welcome back, <tên>!". Email được cắt khoảng trắng trước khi gửi; mật khẩu gửi nguyên. Lỗi từ máy chủ hiện nguyên chữ máy chủ trả về. Nút "Show" đổi kiểu ô mật khẩu. | — (F12 → Sources → app.js, tìm `login-form`) |

## 2. Cần người dùng làm (vì phải gõ mật khẩu) — kết quả
Không có. Người test chọn cách để script đọc tài khoản test trong `.env`; script đã chạy các ca nhập mật khẩu.

## 3. Chưa thử / không kiểm tra được
- **Đăng nhập sai quá 3 lần, ngưỡng khóa, thời gian chặn:** có thể khóa hệ thống của cả môi trường thử; người test dặn tối đa 3 lần và chưa biết ngưỡng. Cần BA hoặc dev cho biết (Q01).
- **Hết hạn phiên:** cần chờ dài (cookie có thời hạn, giá trị chưa đo chính xác), chưa chờ.
- **Vai trò khác ngoài khách:** chưa có tài khoản nào khác; tài khoản có sẵn trên trang chỉ là khách.
- **Nút Back sau đăng xuất:** lần thử đầu mở từ trang trắng nên không ra kết quả có nghĩa; cần thử lại bằng cách vào trang rồi đăng nhập, đăng xuất, bấm Back (không tốn lần nhập sai).
- **Ô email rất dài, ký tự đặc biệt, gửi email sai định dạng lên máy chủ:** mỗi ca là một lần đăng nhập sai, đã hết 3 lần cho phép.
- **Nút "Show", bấm hai lần liên tiếp nút "Sign in", tab "Create account":** chưa bấm thử; "Create account" là tính năng đăng ký, ngoài phạm vi đăng nhập.

## 4. Điểm chưa rõ
1. Hệ thống có giới hạn số lần đăng nhập sai không, bao nhiêu lần, chặn bao lâu? (#23)
2. "Remember me on this device" có tác dụng gì? Cookie không đổi (#15).
3. Phiên sống bao lâu? Cookie có hạn nhưng chưa đo.
4. Email sai định dạng (`abc`) không bị chặn ở trình duyệt (#3); máy chủ phản hồi thế nào chưa thử (tốn lần sai).
5. Địa chỉ không tồn tại trả 200 và hiện trang đăng nhập (#20): có chủ ý không?
6. "Forgot password?" tắt trong môi trường thử (#5): bản thật hoạt động thế nào?
7. Có tài khoản vai trò khác (quản trị, nhân viên) không? Trang sau đăng nhập còn mục nào theo vai trò?
8. Email không phân biệt chữ hoa thường (#10) có phải yêu cầu không.

> **Ghi chú an toàn:** đã gửi đúng 3 lần đăng nhập sai (#7, #8, #9), không thấy bị chặn. Các lần đăng nhập đúng sau đó không bị ảnh hưởng. Không đổi dữ liệu của ai. Đăng xuất đã làm mất phiên máy chủ của phiên script (không phải phiên của người dùng).
