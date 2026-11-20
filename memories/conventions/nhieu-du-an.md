# Nhiều dự án: chọn, tạo mới, không lẫn kiến thức
Cách bắt lẫn (2026-11-19): `scripts/kiem-tra-lan-du-an.py` (chạy trong `kiem-tra-bo-nho.py`) dò dấu hiệu từng dự án trong skill dùng chung và trong thư mục của dự án khác; skill không được chứa tên dự án, tài khoản, địa chỉ hay con số của dự án nào. Từ ngữ BA riêng: `modules/<slug>/tu-ngu-cau-hoi-ba.md` (tạo sẵn rỗng khi tạo dự án).
Đọc khi: máy mới, đổi dự án, tạo dự án. Người dùng chọn (2026-11-18): hỏi **một lần mỗi máy**; thư mục **theo cấu trúc hiện có**.

## Dự án hiện tại
- File `.du-an-hien-tai` ở gốc repo: một dòng slug (không commit, mỗi máy một file).
- Chưa có file → **hỏi riêng câu này trước mọi việc**: liệt kê bảng dự án ở `project/overview.md` + lựa chọn "dự án mới"; không gộp câu hỏi khác, không đưa feature/tài liệu của dự án nào làm lựa chọn khi chưa chọn dự án. Trả lời xong ghi slug.
- Có file → dùng luôn. Người dùng nhắc dự án khác → hỏi xác nhận đổi rồi ghi lại.

## Dự án mới
1. Hỏi tên, URL (nếu có), slug (kebab-case, tiếng Anh không dấu); không tự đặt.
2. `python -X utf8 scripts/tao-du-an.py <slug> "<Tên>" [<URL>]` → tạo `memories/modules/<slug>/overview.md`, `srs/ testing/ evidence/<slug>/` (`.gitkeep`), thêm dòng bảng dự án, ghi `.du-an-hien-tai`.
3. Thêm mục dự án vào `memories/MEMORY.md`. Không tự commit; báo file đã tạo.
4. Tài khoản test: người dùng tự thêm vào `.env` tiền tố `<SLUG_HOA>_` theo `.env.example`.

## Không lẫn kiến thức
- **Phần dùng chung = bộ lõi đem đi** (`scripts/xuat-bo-loi.py`, chốt 2026-11-20): mọi file ngoài thư mục dự án (skill, script, `docs/`, khuôn, memory chung trừ `modules/`) phải viết trung tính. Bài học mới rút ra từ một dự án: ghi quy tắc chung bằng ví dụ trung tính (`CART`, `cua-hang-mau`, `NV01`, "dự án đầu"), còn số liệu/mã/trạng thái của dự án ghi ở `modules/<slug>/`. `kiem-tra-lan-du-an.py` soát toàn bộ phần chung; file cố ý liệt kê dự án và file không xuất khai ở `scripts/bo-loi.json`.
- Chỉ đọc memory/SRS/bảng soát/bằng chứng của dự án hiện tại; không mở thư mục dự án khác, kể cả "xem mẫu".
- Khuôn chung (`srs/_template.md`, `srs/id-and-source-rules.md`, `assets/` của skill) dùng được; ví dụ trong đó (mã tính năng như `CART`, tên trường…) chỉ minh họa cách làm, không phải luật nghiệp vụ.
- Không mang sang: quy tắc nghiệp vụ, tài khoản, dữ liệu test, tên màn hình, thông báo, từ đã chốt với BA (`modules/<slug>/tu-ngu-cau-hoi-ba.md`), giới hạn khóa/chặn đã đo. Được mang: `memories/user/`, `memories/conventions/`, quy trình/bài học trong skill.
- Chưa biết gì về dự án mới thì ghi chưa biết và hỏi.
