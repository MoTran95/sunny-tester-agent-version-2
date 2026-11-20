# Sở thích làm việc của người dùng (LUÔN ĐỌC)
Chi tiết viết tài liệu: `document-preferences.md`. Quy tắc đã có ở `CLAUDE.md` (dự án hiện tại, MarkItDown, trả một link trang tổng, memory chỉ cho AI) không chép lại ở đây.

- Tiếng Việt. Người dùng là **tester**, nói bằng giọng nói nên có từ lệch → hỏi lại nghĩa, không đoán.
- **Từng bước nhỏ rồi ghép**; chưa rõ thì **hỏi, không suy diễn, không bịa**. Chỉ test **functional**.
- **Hỏi người dùng:** câu đủ ngữ cảnh (không cần lật chat cũ), đưa lựa chọn theo logic kèm hệ quả và một đề xuất, dùng hộp chọn khi có; **Không hỏi lại điều đã có câu trả lời** trong chat, `memories/`, skill, tài liệu dự án.
- **Mật khẩu và chạy tự động (chốt 2026-11-19, mọi dự án):** **Không gõ mật khẩu** (kể cả sai), không đọc ra, không ghi; chỉ script (`auto_login.py`, runner) đọc `.env`, và chỉ trên địa chỉ người dùng nêu có nhãn môi trường thử. Được chạy ca đăng nhập/nhập sai bằng runner; **bỏ qua cho người dùng tự làm** mọi ca mà chính bước làm có thể chặn hệ thống. Tên hàm/biến/khóa JSON tiếng Anh; thông báo, tài liệu tiếng Việt. Chi tiết `project/tu-dong-hoa-test.md`.
- **An toàn hệ thống đang test:** không khóa, không đổi dữ liệu người khác, không kích hoạt giới hạn. **Ngưỡng (số lần sai, thời gian chặn…): không tự đặt con số**, lấy từ requirement hoặc hỏi người test; runner đếm cộng dồn, từ chối vượt trần đã khai; lỡ kích hoạt thì báo ngay (`pitfalls/dont-trigger-lockouts.md`).
- **Đã khám phá rồi thì không khám phá lại**, trừ khi người dùng nói rõ phần nào đổi (`project/srs-process.md`).
- **Thứ tự quy trình (chốt 2026-11-19):** phân tích requirement → **test plan** → test case → smoke, regression (xong thì "Cập nhật test plan") → chạy → bug → re-test → báo cáo tổng kết. Hướng dẫn cho người dùng chỉ viết ở `docs/bat-dau.md` (có "Lời chào trong chat": tự xưng **trợ lý Sunny Testing**); đổi cách dùng repo thì sửa trang đó cùng lượt.
- **Cách gọi:** "phân tích requirement", "bảng phân tích requirement" (không "soát"); nhắc SRS với người mới thì nói rõ là gì, vì sao cần.
- **Bug (chốt 2026-11-19):** chạy test ra **Không đạt** thật → tạo bug luôn kèm ảnh + video (skill `tao-bug-report`, tra bug trùng trước); **Jira chỉ khi người dùng nhờ**. Bug lọt production chưa có case chặn → viết case mới vào regression (skill `de-xuat-regression`).
- **Truy vết:** mọi mã requirement/TC trong tài liệu phải là link bấm được; chữ không link là lỗi.
- **Commit/push chỉ khi người dùng nhờ.** Kết quả dài lưu file, chat chỉ tóm tắt + link.
- Tài liệu **đọc là hiểu**: tiếng Việt thường, câu đủ ý; không Given/When/Then, FR/BR hay mã nội bộ làm nhãn/nội dung chính.
- Connector/plugin mặc định tắt, **hỏi trước khi bật** (`connectors-and-plugins.md`).
