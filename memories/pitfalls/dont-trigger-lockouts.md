# Bẫy: tự kích hoạt khóa/giới hạn khi test
Đọc khi: trước thao tác lặp có thể gây khóa/chặn.

- Đã xảy ra (dự án đầu, tính năng đăng nhập, 2026-11-17): người dùng dặn không làm việc có thể khóa; mình vẫn gửi liên tiếp nhiều lần đăng nhập sai (nhiều biến thể mã đăng nhập) → bị **chặn tạm** (429).
- Sai ở đâu: nghĩ "mã không tồn tại thì không đụng tài khoản thật" (bỏ qua giới hạn theo nguồn/toàn hệ thống; không có bằng chứng hệ thống không giới hạn); không đặt ngưỡng dừng, chạy theo lô 4 lần; không hỏi dù đã được cảnh báo.
- Làm đúng: số lần nhập sai cho phép do requirement hoặc người test chốt (không tự đặt số); làm tay từng lần rồi dừng hỏi; runner tự động đếm từng lần, từ chối vượt trần đã khai và dừng hỏi; lỡ kích hoạt báo ngay (quy tắc ở `user/working-preferences.md`). Muốn biết có giới hạn không mà không kích hoạt: đọc tệp giao diện công khai (tìm `auth.locked`) hoặc hỏi team. Nếu có giới hạn: chờ hết hạn rồi thử lại **một** lần để biết có tự hết không.
- Lần hai (2026-11-19, staging, runner tự động): mình viết bộ đếm theo giả định "đăng nhập đúng đưa số lần sai về 0" (câu trả lời của BA) nên chạy nhiều ca nhập sai xen đăng nhập đúng; hệ thống không reset, tài khoản bị chặn tạm. Làm đúng: bộ đếm cộng dồn, chỉ reset khi chặn hết hạn hoặc người dùng đặt tay; chạy từng đợt nhỏ và chỉ tin điều đã quan sát. Ảnh hưởng: chặn tạm, đã báo người dùng.
- Con số trần/thời gian chặn của từng dự án ở `modules/<slug>/` và `testing/<slug>/auto-config.json`, không mang sang dự án khác.
