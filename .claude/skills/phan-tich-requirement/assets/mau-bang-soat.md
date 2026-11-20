# Bảng phân tích requirement — <tên feature> (<hệ thống>)

| | |
|---|---|
| Nguồn requirement | [<đường dẫn file>](<liên kết tương đối>) (mã `<MÃ>`, tình trạng <nháp / chính thức>, <phiên bản hệ thống nếu có>) |
| Ngày lập | <YYYY-MM-DD> |
| Cách làm | Tách, Xoay, Lọc (skill `phan-tich-requirement`) |
| Phạm vi | <số> đơn vị (AC, quy tắc, thông báo), cộng phụ lục cho chủ đề chung. Chỉ **functional**. Chưa viết checklist hay test case |
| Câu hỏi gửi BA | [cau-hoi-cho-ba.md](cau-hoi-cho-ba.md) |

## 1. Cách đọc
**Mỗi dòng trả lời ba câu:** (1) người dùng làm gì, (2) requirement cho biết gì hoặc chỗ nào chưa rõ, (3) cần hỏi BA câu gì.

**Cách đọc mã:** <giải thích cấu trúc mã của tài liệu, ví dụ `CART` là tên feature, `S01` là story số 1, `AC01` là tiêu chí số 1>.

**Cột Trạng thái:**
- **✅ Đã rõ:** requirement trả lời đủ để biết thế nào là đúng. <Nếu tài liệu là bản nháp: nói rõ chưa phải xác nhận chính thức.>
- **❓ + loại vấn đề:** Thiếu thông tin, Chưa rõ nghĩa, Hai chỗ nói khác nhau, Số liệu không chính xác, hoặc Trình bày không thống nhất.

**Cách xử lý câu hỏi** (in đậm đầu mỗi câu hỏi):
- **🚨 Hỏi BA ngay:** hiểu sai thì kết quả đúng đổi.
- **📋 Hỏi BA sau (gom lại):** câu chữ, hiển thị, hoặc phần ngoài phần đang test.
- **🔍 Tự kiểm tra trên hệ thống trước:** xem hệ thống đang chạy để tìm câu trả lời. Chỉ cho biết hệ thống đang làm gì, không chứng minh là đúng.

**Cột "Câu hỏi gửi BA":** ghi số câu và tiêu đề câu hỏi (A1, B3, C5…) cùng cách xử lý, và câu BA đã trả lời nếu có (dòng "BA trả lời", kèm mã TL ở mục 3). Nội dung đầy đủ của câu hỏi (tình huống, hỏi gì, mình đang hiểu thế nào, vì sao hỏi) chỉ nằm ở [cau-hoi-cho-ba.md](cau-hoi-cho-ba.md), không chép lại ở đây.

## 2. Giải thích thuật ngữ (theo requirement)
| Thuật ngữ | Nghĩa |
|---|---|
| <thuật ngữ> | <nghĩa, lấy theo lời của tài liệu> |

## 3. Câu trả lời đã nhận
| Mã | Nội dung trả lời | Nguồn | Áp dụng cho | Còn lại |
|---|---|---|---|---|
| TL-01 | <đúng ý người trả lời> | <ai nói, ngày, ở đâu; nếu là tester tự chốt thì ghi "chưa có xác nhận của BA"> | <mã câu hỏi, mã requirement> | <chỗ chưa trả lời, người cần xác nhận, hệ quả> |

(Chưa có câu trả lời nào thì ghi một dòng: "Chưa có câu trả lời nào.")

## 4. Tổng kết
| Chỉ số | Số lượng |
|---|---|
| Đơn vị chỉ có phần ✅ | <n> |
| Đơn vị có cả ✅ và ❓ | <n> |
| Đơn vị chỉ có ❓ | <n> |
| Tổng | <n> |
| Câu hỏi: 🚨 / 📋 / 🔍 | <a> / <b> / <c> |

## 5. Bảng soát theo từng story (hoặc theo nhóm requirement)

### <Tên nhóm 1> (<mã nhóm>)

| Mã | Tình huống (người dùng làm gì) | Requirement cho biết gì, hoặc chỗ chưa rõ | Trạng thái | Câu hỏi gửi BA | Trích nguyên văn |
|---|---|---|---|---|---|
| <MÃ-S01-AC01> | Ở đơn hàng nền 1.000.000 đ, nhập mã giảm 10%. | Dòng Giảm giá ghi 100.000 đ. Dòng Tổng thanh toán ghi 900.000 đ. | ✅ Đã rõ | — | “<đoạn chép đúng nguyên văn từ requirement>” |
| <MÃ-S01-AC02> | Ở đơn hàng nền 333.400 đ, nhập mã giảm 15%. | Requirement ghi "giảm đúng 50.000 đ", nhưng tính lại ra 50.010 đ. | ❓ Số liệu không chính xác | **A1. <Tiêu đề, đúng chữ như ở file câu hỏi>** (🚨 Hỏi BA ngay) | “<đoạn chép đúng nguyên văn>” |

Quy tắc cột câu hỏi: khuôn `**<số câu>. <tiêu đề>** (<nhóm>)`; nhóm là `🚨 Hỏi BA ngay` (phần A), `📋 Hỏi BA sau (gom lại)` (phần B) hoặc `🔍 Tự kiểm tra trên hệ thống trước` (phần C). Nhiều câu thì nối bằng `<br>`. **Không** chép lại Hỏi, Mình đang hiểu, Cần xem: script báo lỗi. Khi đã có câu trả lời, thêm ngay sau tiêu đề: `<br>**BA trả lời:** <nguyên văn> (TL-xx)`. Ghi chú riêng của dòng (nếu cần) để sau cùng. Đơn vị rõ một nửa thì có một dòng ✅ và các dòng ❓ cùng mã.

## 6. Phụ lục: chủ đề chung, quy tắc và thông báo không gắn với một tiêu chí
| Mã | Tình huống | Requirement cho biết gì, hoặc chỗ chưa rõ | Trạng thái | Câu hỏi gửi BA | Trích nguyên văn |
|---|---|---|---|---|---|

## 7. Nhóm 🚨 Hỏi BA ngay
Nội dung đầy đủ ở Phần A của [cau-hoi-cho-ba.md](cau-hoi-cho-ba.md). Danh sách và mã liên quan:
- **A1. <Tiêu đề>** (liên quan <mã>)

## 8. Tự kiểm
- Đủ <n> đơn vị: mọi mã xuất hiện ít nhất một dòng.
- Mọi câu hỏi xuất hiện ít nhất một lần.
- Trích dẫn đã so từng chuỗi với requirement bằng `kiem-tra.py` (lỗi: 0).

## 9. Lịch sử thay đổi
| Ngày | Thay đổi |
|---|---|
| <YYYY-MM-DD> | Tạo mới |
