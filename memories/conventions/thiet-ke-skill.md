# Thiết kế / tạo skill mới
Đọc khi: người dùng nhờ thiết kế hoặc tạo skill (dặn 2026-11-20).

- **Tìm hiểu trước khi viết:** xác định chất lượng người dùng yêu cầu (đầu ra thế nào là đạt) và cách nhìn ra lỗi; tham khảo skill cùng loại trong repo (`project/skills.md`) và skill `skill-creator` nếu có. Không viết từ trí nhớ.
- **Tối ưu token:** `SKILL.md` ngắn (nguyên tắc, quy trình, bảng "đọc gì cho việc nào"); chi tiết ở `references/` chỉ đọc khi cần; việc lặp/chắc chắn đưa vào script (chạy 0 token), AI chỉ làm phần phán đoán; script soát chỉ in kết luận ngắn.
- **Dùng chung nhiều dự án:** skill và script không chứa thông tin dự án (tên, tài khoản, nghiệp vụ, con số); dữ liệu dự án nằm ở `memories/modules/<slug>/`, `testing/<slug>/`. Ngưỡng an toàn lấy từ requirement, không tự đặt.
- **Kiểm trước khi xong:** thử trên ít nhất một dự án thật, chạy `kiem-tra-bo-nho.py` (có soát lẫn dự án), cập nhật `project/skills.md`, `MEMORY.md`, `docs/quy-trinh-kiem-thu.md` nếu skill nằm trong quy trình.
- Quy tắc người dùng dặn ghi **một dòng** ở `working-preferences.md` + chi tiết ở skill; ví dụ và lý do ghi ở `decisions/decision-log.md`.
