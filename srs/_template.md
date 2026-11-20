<!--
KHUÔN SRS v2 — Story + AC (nháp, 2026-11-17). Quy tắc ID và ghi nguồn: srs/id-and-source-rules.md (đọc trước).
- Mỗi feature một file: srs/<hệ-thống>/<ten-feature>.md. Feature đổi → SỬA TẠI CHỖ + thêm dòng ở mục 7, giữ ID.
- Chỉ ghi điều ĐÃ THẤY (nhãn "đã thấy"), hoặc điều tài liệu yêu cầu ghi rõ (nhãn "theo tài liệu", khi SRS viết từ tài liệu, xem id-and-source-rules.md mục 2e). Chưa chắc → nhãn "chưa rõ" + câu hỏi ở mục 5. Không ghi "đúng/lỗi" khi chưa có tài liệu nghiệp vụ.
- AC = MỘT tình huống kiểm chứng được. Viết bằng tiếng Việt thường, câu đầy đủ, 3 phần: Bối cảnh (trước khi làm) → Người dùng làm → Hệ thống phản hồi (điều đã thấy). KHÔNG dùng thuật ngữ "Given/When/Then/Cho trước/Khi/Thì" làm tên cột; chỉ nhắc một lần ở đoạn "Cách đọc". Chép nguyên văn thông báo ngay trong cột phản hồi để người đọc không phải tra chéo. Có bằng chứng (ID E ở mục 6.1).
- Ô ID đầu mỗi dòng AC, quy tắc (R), thông báo (M), câu hỏi (Q) có thẻ neo `<a id="<mã chữ thường>"></a>` để test case link tới đúng dòng. Quên thì `check-srs.py --them-neo` tự chèn.
- Thông báo của hệ thống chép NGUYÊN VĂN trong `…` (bảng 4.2), AC chỉ trỏ tới ID thông báo.
Xóa khối chú thích này trong file thật.
-->

# SRS — <Tên feature> (<Hệ thống>)

*SRS (tài liệu đặc tả yêu cầu) ghi hệ thống phải làm gì ở tính năng này: mỗi tình huống một dòng có mã cố định và bằng chứng. Test case dựa vào các mã này, nên khi requirement đổi sẽ biết ngay test case nào phải sửa.*

| | |
|---|---|
| Mã feature | `<MÃ>` |
| Phiên bản hệ thống đã quan sát | <số phiên bản, hoặc "chưa đối chiếu hệ thống" nếu viết từ tài liệu> |
| Cập nhật lần cuối | YYYY-MM-DD |
| Tình trạng | nháp / đã review / đã xác nhận với team |
| Nhật ký khám phá gốc (hoặc tài liệu yêu cầu gốc) | [bao-cao.md](../../evidence/<hệ-thống>/features/<feature>/bao-cao.md) |

## 1. Mục đích, phạm vi, vai trò
- **Mục đích:** (1–3 câu theo điều đã thấy).
- **Ngoài phạm vi / chưa thấy trên màn hình:**
- **Vai trò:**

| Tài khoản | Vai trò hiển thị | Đã thử với feature này |
|---|---|---|

## 2. Điều kiện tiên quyết
Dữ liệu/trạng thái cần có trước khi dùng feature.

## 3. User story và tiêu chí chấp nhận

### `<MÃ>-S01` — <Tên story>
**Là** <vai trò>, **tôi muốn** <làm gì> **để** <lợi ích>.

**Luồng:** (1) … → (2) … → (3) …; rẽ nhánh: … (→ `<MÃ>-S01-AC03`).

**Cách đọc:** mỗi dòng là một tình huống test. *Bối cảnh* = tình trạng trước khi làm; *Người dùng làm* = thao tác cụ thể; *Hệ thống phản hồi* = điều đã nhìn thấy (chữ trong `…` là nguyên văn). (Giới test gọi là Given – When – Then; mỗi dòng là một "tiêu chí chấp nhận", viết tắt AC.)

| ID | Tình huống | Bối cảnh | Người dùng làm | Hệ thống phản hồi | Nhãn · Bằng chứng · Liên quan |
|---|---|---|---|---|---|
| <a id="<mã>-s01-ac01"></a>`<MÃ>-S01-AC01` | (tên ngắn) | | | | đã thấy · [E01](#e01) · `<MÃ>-R01`, `<MÃ>-M01` |

## 4. Bảng tra cứu
### 4.1 Quy tắc dữ liệu
| ID | Trường | Quy tắc quan sát được | Nhãn | Bằng chứng |
|---|---|---|---|---|

### 4.2 Thông báo hệ thống (nguyên văn)
| ID | Khi nào | Tiếng Việt | English | Bằng chứng |
|---|---|---|---|---|

## 5. Điểm chưa rõ và câu hỏi cho team
| ID | Đã thấy | Vì sao chưa rõ | Câu hỏi | Liên quan | Trạng thái |
|---|---|---|---|---|---|

## 6. Bằng chứng và chưa khám phá
### 6.1 Bằng chứng
| ID | Loại | Ngày · phiên bản · tài khoản | Thao tác đã làm | Tệp | Cách kiểm lại |
|---|---|---|---|---|---|

### 6.2 Chưa khám phá
- 

## 7. Lịch sử thay đổi
| Ngày | Phiên bản hệ thống | Thay đổi | Lý do |
|---|---|---|---|
