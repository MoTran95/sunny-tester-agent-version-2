# Thang mức độ nghiêm trọng và mức độ ưu tiên

Mặc định, team đổi được (người dùng chốt 2026-11-19: mỗi team tự chọn thang). **Bug đầu tiên của một dự án:** nếu chưa có `testing/<slug>/thang-muc-do-bug.json` và bộ nhớ dự án chưa ghi "dùng thang mặc định", hỏi người dùng một câu: team có thang mức độ riêng không (đưa thang dưới làm lựa chọn đề xuất). Có thì ghi vào `testing/<slug>/thang-muc-do-bug.json` dạng `{"severity": ["…"], "priority": ["…"]}` (tên mức tiếng Việt; `kiem-tra-bug.py` đọc file này); dùng mặc định thì ghi một dòng vào `memories/modules/<slug>/overview.md` để không hỏi lại. **Ghi bằng tiếng Việt** trong file bug (ví dụ `**Rất nhỏ.**`), không ghi Severity/Priority/Critical/Major/Minor/Trivial.

| Mức độ nghiêm trọng | Khi nào |
|---|---|
| Nghiêm trọng | Luồng chính không thực hiện được hoặc làm sai/mất dữ liệu, số tiền; không có cách đi vòng |
| Lớn (cũng gọi Nặng) | Chức năng quan trọng sai kết quả nghiệp vụ, hoặc không dùng được nhưng còn cách đi vòng |
| Nhỏ | Chức năng phụ hoặc tình huống hiếm sai; có cách đi vòng; kết quả nghiệp vụ chính vẫn đúng |
| Rất nhỏ | Chữ, chính tả, căn lề, thông báo thiếu rõ nhưng không ảnh hưởng thao tác |

(Cách gọi `Nặng` coi là cùng mức với `Lớn`.)

- **Lý do** viết 1 đến 2 câu nối với **ảnh hưởng cụ thể của bug này**, không chép định nghĩa. Thiếu dữ kiện để chấm (ví dụ không biết có cách đi vòng không) thì dữ kiện đó là `[Giả định: …]`.
- **Mức độ ưu tiên**: `Cao` (chặn việc test hoặc vận hành tiếp theo, hoặc cần sửa ngay), `Trung bình`, `Thấp`, kèm một câu lý do; luôn ghi là **đề xuất, team hoặc PO sẽ chốt**.
- Hai mức khác nhau: một bug Nhỏ vẫn có thể ưu tiên Cao nếu chặn luồng test khác.
