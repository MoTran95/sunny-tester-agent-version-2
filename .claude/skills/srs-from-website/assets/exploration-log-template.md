# <Feature> — nhật ký khám phá

Ngày: YYYY-MM-DD · Hệ thống: <URL> · Phiên bản (ghi ở chân trang/`/api/health`): <x.y.z>
Khung nhìn: <ví dụ 606×845>. Ảnh: `screenshots/NN-…jpg`. Ảnh nền cũ (nếu có): `<đường dẫn>`.
Quy tắc: không tự gõ mật khẩu (kể cả sai); các ca cần mật khẩu ghi ở mục 2 và chờ người dùng.

## 0. Bảng phủ (điền khi xong khám phá; lần sau dựa vào đây để biết đã đủ chưa)
| Nhóm ca | Trạng thái | Hàng nhật ký / lý do |
|---|---|---|
| Luồng chính thành công | Đã làm | #1–#3 |
| Từng nhánh lỗi | | |
| Từng vai trò (ai thấy gì, ai không có nút) | | |
| Đổi ngôn ngữ | | |
| Tải lại trang, nút Back, hai tab | | |
| Link sâu khi chưa đăng nhập / thiếu quyền; địa chỉ không tồn tại | | |
| Phản hồi mạng (mã trạng thái, `GET /api`) | | |
| Tệp giao diện (chuỗi thông báo) | | |
| Nhóm riêng của loại màn hình (form / đăng nhập-phiên / danh sách / nhiều bước): thêm dòng cho từng ca trong `exploration-checklist.md` mục 3 | | |

- Trạng thái: **Đã làm** (ghi số hàng ở mục 1), **Chưa làm** (ghi lý do thật theo mục 4 của checklist, trùng mục 3 bên dưới; đây là ngoại lệ đã ghi, lần sau không khám phá lại), **Không áp dụng** (ghi vì sao, ví dụ "feature không có form"), **Chưa có trong nhật ký** (chỉ dùng khi dựng bảng cho nhật ký cũ mà không thấy hàng nào; đây mới là chỗ thiếu thật → hỏi người dùng).
- Không để ô trống. Ô trống = chưa kiểm = coi như thiếu.
- Kiểm bằng `python -X utf8 .claude/skills/srs-from-website/scripts/kiem-tra-bang-phu.py <bao-cao.md>` (in vài dòng: ĐỦ / CÒN THIẾU / KHÔNG CÓ).
- Nhật ký cũ chưa có bảng này: dựng từ các hàng sẵn có (không mở trình duyệt).

## 1. Đã thấy (có thao tác thật)
| # | Thao tác | Kết quả quan sát (nguyên văn khi có) | Ảnh |
|---|---|---|---|
| 1 | | | |

- Cột "Ảnh": số ảnh, hoặc `—` kèm cách kiểm lại (ví dụ "F12 → Network") nếu là quan sát bằng công cụ.
- Hàng do **người dùng** thao tác ghi rõ "(người dùng gõ)" và ghi mình xác nhận kết quả bằng cách nào.
- Số hàng **không đổi** sau khi đã dẫn từ SRS (SRS trỏ "Nhật ký, hàng N"); hàng mới thêm vào cuối.

## 2. Cần người dùng làm (vì phải gõ mật khẩu) — kết quả
- A. 

## 3. Chưa thử / không kiểm tra được
Mỗi mục kèm **lý do thật** (xem `references/exploration-checklist.md` mục 4).

## 4. Điểm chưa rõ (ứng viên cho mục câu hỏi của SRS)
1. 

> **Ghi chú an toàn:** (nếu lỡ kích hoạt giới hạn/khóa: thời điểm, số lần, ảnh hưởng, dữ liệu có đổi không.)
