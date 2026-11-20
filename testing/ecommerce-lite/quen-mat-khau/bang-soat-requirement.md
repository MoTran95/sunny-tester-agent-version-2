# Bảng phân tích requirement — Quên mật khẩu (Ecommerce Lite)

| | |
|---|---|
| Nguồn requirement | [quen-mat-khau.md](../../../srs/ecommerce-lite/quen-mat-khau.md) (mã `FORGOT`, tình trạng nháp, viết từ [requirement người dùng dán](../../../evidence/ecommerce-lite/tai-lieu/yeu-cau-quen-mat-khau.md), chưa đối chiếu hệ thống) |
| Ngày lập | 2026-11-20 |
| Cách làm | Tách, Xoay, Lọc (skill `phan-tich-requirement`) |
| Phạm vi | 13 đơn vị (8 tiêu chí chấp nhận, 5 quy tắc, 0 thông báo). Chỉ **functional**. Chưa viết checklist hay test case |
| Câu hỏi gửi BA | [cau-hoi-cho-ba.md](cau-hoi-cho-ba.md) |

## 1. Cách đọc
**Mỗi dòng trả lời ba câu:** (1) người dùng làm gì, (2) requirement cho biết gì hoặc chỗ nào chưa rõ, (3) cần hỏi BA câu gì.

**Cách đọc mã:** `FORGOT` là tên tính năng quên mật khẩu; `S01` là story số 1; `AC01` là tiêu chí số 1 của story đó; `R01` là quy tắc dữ liệu.

**Cột Trạng thái:**
- **✅ Đã rõ:** requirement trả lời đủ để biết thế nào là đúng. Đây là requirement dạng văn bản, chưa có xác nhận của BA.
- **❓ + loại vấn đề:** Thiếu thông tin, Chưa rõ nghĩa, Hai chỗ nói khác nhau, Số liệu không chính xác, hoặc Trình bày không thống nhất.

**Cách xử lý câu hỏi** (in đậm đầu mỗi câu hỏi):
- **🚨 Hỏi BA ngay:** hiểu sai thì kết quả đúng đổi.
- **📋 Hỏi BA sau (gom lại):** câu chữ, hiển thị, hoặc phần ngoài phần đang test.
- **🔍 Tự kiểm tra trên hệ thống trước:** xem hệ thống đang chạy để tìm câu trả lời. Chỉ cho biết hệ thống đang làm gì, không chứng minh là đúng.

**Cột "Câu hỏi gửi BA":** ghi số câu và tiêu đề câu hỏi cùng cách xử lý. Nội dung đầy đủ chỉ nằm ở [cau-hoi-cho-ba.md](cau-hoi-cho-ba.md).

**Tính lại số liệu:** requirement chỉ có các số 6 (chữ số OTP), 5 (phút), 8 và 16 (độ dài), 5 (mật khẩu gần nhất), không có công thức hay ví dụ tính. Không có chỗ lệch.

## 2. Giải thích thuật ngữ (theo requirement)
| Thuật ngữ | Nghĩa |
|---|---|
| OTP | Mã gồm 6 chữ số gửi đến email đã đăng ký, có hiệu lực 5 phút |
| 5 mật khẩu gần nhất | Mật khẩu mới không được trùng với 5 mật khẩu này |

## 3. Câu trả lời đã nhận
Chưa có câu trả lời nào.

## 4. Tổng kết
| Chỉ số | Số lượng |
|---|---|
| Đơn vị chỉ có phần ✅ | 3 |
| Đơn vị có cả ✅ và ❓ | 10 |
| Đơn vị chỉ có ❓ | 0 |
| Tổng | 13 |
| Câu hỏi: 🚨 / 📋 / 🔍 | 6 / 3 / 1 |

## 5. Bảng phân tích theo từng story

### Yêu cầu đặt lại mật khẩu (FORGOT-S01)

| Mã | Tình huống (người dùng làm gì) | Requirement cho biết gì, hoặc chỗ chưa rõ | Trạng thái | Câu hỏi gửi BA | Trích nguyên văn |
|---|---|---|---|---|---|
| FORGOT-S01-AC01 | Nhập email đã đăng ký tài khoản để yêu cầu đặt lại mật khẩu. | Hệ thống gửi OTP 6 chữ số đến email đó, OTP có hiệu lực 5 phút. | ✅ Đã rõ | — | “Gửi mã OTP gồm 6 chữ số đến email đã đăng ký. OTP có hiệu lực trong 5 phút” |
| FORGOT-S01-AC01 | **Phần còn chưa rõ** của dòng trên (email chưa đăng ký) | Requirement chỉ nói email đã đăng ký, không nói khi email chưa có tài khoản. | ❓ Thiếu thông tin | **A1. Nhập email chưa đăng ký thì hệ thống làm gì?** (🚨 Hỏi BA ngay) | — |
| FORGOT-S01-AC01 | **Phần còn chưa rõ** của dòng trên (email để trống hoặc sai dạng) | Requirement không nói khi để trống hoặc nhập sai dạng email. | ❓ Thiếu thông tin | **B1. Để trống hoặc nhập email sai dạng thì hiện gì?** (📋 Hỏi BA sau (gom lại)) | — |
| FORGOT-S01-AC01 | **Phần còn chưa rõ** của dòng trên (hệ thống hiện tại) | Lượt khám phá đăng nhập thấy bấm "Forgot password?" chỉ hiện thông báo "Password recovery is disabled in the training environment.", chưa chạy được chức năng này. | ❓ Hai chỗ nói khác nhau | **C1. Hệ thống Ecommerce Lite có chạy được chức năng Quên mật khẩu không?** (🔍 Tự kiểm tra trên hệ thống trước) | — |

### Xác thực OTP (FORGOT-S02)

| Mã | Tình huống (người dùng làm gì) | Requirement cho biết gì, hoặc chỗ chưa rõ | Trạng thái | Câu hỏi gửi BA | Trích nguyên văn |
|---|---|---|---|---|---|
| FORGOT-S02-AC01 | Nhập đúng OTP trong vòng 5 phút. | Chuyển đến màn hình tạo mật khẩu mới. | ✅ Đã rõ | — | “Chuyển đến màn hình tạo mật khẩu mới” |
| FORGOT-S02-AC01 | **Phần còn chưa rõ** của dòng trên (nhập sai OTP) | Requirement không nói thông báo và số lần được nhập sai. | ❓ Thiếu thông tin | **A2. Nhập sai OTP thì hệ thống làm gì, được sai mấy lần?** (🚨 Hỏi BA ngay) | — |
| FORGOT-S02-AC01 | **Phần còn chưa rõ** của dòng trên (OTP quá 5 phút) | Requirement không nói thông báo khi OTP hết hạn, có gửi lại được không. | ❓ Thiếu thông tin | **A3. OTP quá 5 phút thì hiện gì, có gửi lại OTP được không?** (🚨 Hỏi BA ngay) | — |
| FORGOT-S02-AC01 | **Phần còn chưa rõ** của dòng trên (xin OTP mới, dùng lại OTP) | Requirement không nói OTP cũ có còn dùng được không, OTP đã dùng có dùng lại được không. | ❓ Thiếu thông tin | **A4. Xin OTP mới thì OTP cũ còn dùng được không, OTP dùng rồi có dùng lại được không?** (🚨 Hỏi BA ngay) | — |

### Tạo mật khẩu mới (FORGOT-S03)

| Mã | Tình huống (người dùng làm gì) | Requirement cho biết gì, hoặc chỗ chưa rõ | Trạng thái | Câu hỏi gửi BA | Trích nguyên văn |
|---|---|---|---|---|---|
| FORGOT-S03-AC01 | Nhập mật khẩu mới thỏa mọi quy tắc (8–16 ký tự, đủ bốn loại ký tự, không trùng 5 mật khẩu gần nhất). | Mật khẩu mới được chấp nhận. Suy ra từ FORGOT-R03–R05: thỏa mọi quy tắc thì được đổi. | ✅ Đã rõ | — | “Nhập mật khẩu 8–16 ký tự có đủ chữ hoa, chữ thường, số, ký tự đặc biệt và không trùng 5 mật khẩu gần nhất” |
| FORGOT-S03-AC01 | **Phần còn chưa rõ** của dòng trên (ký tự đặc biệt) | Requirement không liệt kê ký tự đặc biệt hợp lệ. | ❓ Thiếu thông tin | **A5. Ký tự đặc biệt hợp lệ gồm những ký tự nào?** (🚨 Hỏi BA ngay) | — |
| FORGOT-S03-AC01 | **Phần còn chưa rõ** của dòng trên (mật khẩu đang dùng) | Requirement không nói mật khẩu đang dùng có tính trong 5 mật khẩu gần nhất không. | ❓ Chưa rõ nghĩa | **A6. Mật khẩu đang dùng có nằm trong 5 mật khẩu gần nhất không?** (🚨 Hỏi BA ngay) | — |
| FORGOT-S03-AC02 | Nhập mật khẩu mới ngắn hơn 8 hoặc dài hơn 16 ký tự. | Không được chấp nhận. Suy ra từ "phải có từ 8 đến 16 ký tự"; đúng 8 và đúng 16 là hợp lệ. | ✅ Đã rõ | — | “Nhập mật khẩu có độ dài ngoài khoảng 8 đến 16 ký tự” |
| FORGOT-S03-AC02 | **Phần còn chưa rõ** của dòng trên (thông báo) | Requirement không nói thông báo lỗi, không nói có ô nhập lại mật khẩu. | ❓ Thiếu thông tin | **B2. Mật khẩu mới không hợp lệ thì hiện thông báo gì, có ô nhập lại mật khẩu không?** (📋 Hỏi BA sau (gom lại)) | — |
| FORGOT-S03-AC03 | Nhập mật khẩu mới 8–16 ký tự nhưng thiếu một loại: chữ hoa, hoặc chữ thường, hoặc số, hoặc ký tự đặc biệt. | Không được chấp nhận. Suy ra từ "bao gồm chữ hoa, chữ thường, số và ký tự đặc biệt": thiếu một loại là không hợp lệ. | ✅ Đã rõ | — | “Nhập mật khẩu 8–16 ký tự nhưng thiếu chữ hoa, hoặc chữ thường, hoặc số, hoặc ký tự đặc biệt” |
| FORGOT-S03-AC03 | **Phần còn chưa rõ** của dòng trên (thông báo) | Requirement không nói thông báo lỗi cho từng loại thiếu. | ❓ Thiếu thông tin | **B2. Mật khẩu mới không hợp lệ thì hiện thông báo gì, có ô nhập lại mật khẩu không?** (📋 Hỏi BA sau (gom lại)) | — |
| FORGOT-S03-AC04 | Nhập mật khẩu mới trùng một trong 5 mật khẩu gần nhất. | Không được chấp nhận. Suy ra từ "không được trùng". | ✅ Đã rõ | — | “Nhập mật khẩu trùng một trong 5 mật khẩu gần nhất” |
| FORGOT-S03-AC04 | **Phần còn chưa rõ** của dòng trên (thông báo) | Requirement không nói thông báo khi trùng. | ❓ Thiếu thông tin | **B2. Mật khẩu mới không hợp lệ thì hiện thông báo gì, có ô nhập lại mật khẩu không?** (📋 Hỏi BA sau (gom lại)) | — |

### Kết thúc đặt lại mật khẩu (FORGOT-S04)

| Mã | Tình huống (người dùng làm gì) | Requirement cho biết gì, hoặc chỗ chưa rõ | Trạng thái | Câu hỏi gửi BA | Trích nguyên văn |
|---|---|---|---|---|---|
| FORGOT-S04-AC01 | Đổi mật khẩu thành công. | Hệ thống hiển thị thông báo thành công. | ✅ Đã rõ | — | “Hiển thị thông báo thành công” |
| FORGOT-S04-AC01 | **Phần còn chưa rõ** của dòng trên (nguyên văn thông báo) | Requirement không ghi nguyên văn thông báo. | ❓ Thiếu thông tin | **B3. Đổi mật khẩu xong hiện thông báo gì, chuyển đến đâu, mật khẩu cũ còn đăng nhập được không?** (📋 Hỏi BA sau (gom lại)) | — |
| FORGOT-S04-AC02 | Đổi mật khẩu thành công, không làm gì thêm. | Hệ thống yêu cầu người dùng đăng nhập lại. | ✅ Đã rõ | — | “Yêu cầu người dùng đăng nhập lại” |
| FORGOT-S04-AC02 | **Phần còn chưa rõ** của dòng trên (trang chuyển đến, mật khẩu cũ) | Requirement không nói chuyển đến trang nào, mật khẩu cũ còn dùng được không. | ❓ Thiếu thông tin | **B3. Đổi mật khẩu xong hiện thông báo gì, chuyển đến đâu, mật khẩu cũ còn đăng nhập được không?** (📋 Hỏi BA sau (gom lại)) | — |

## 6. Phụ lục: quy tắc dữ liệu

| Mã | Tình huống (người dùng làm gì) | Requirement cho biết gì, hoặc chỗ chưa rõ | Trạng thái | Câu hỏi gửi BA | Trích nguyên văn |
|---|---|---|---|---|---|
| FORGOT-R01 | OTP nhận được. | OTP gồm 6 chữ số. | ✅ Đã rõ | — | “Gồm 6 chữ số” |
| FORGOT-R02 | OTP đã gửi. | OTP có hiệu lực 5 phút. | ✅ Đã rõ | — | “Có hiệu lực trong 5 phút” |
| FORGOT-R03 | Mật khẩu mới. | Từ 8 đến 16 ký tự. "Từ … đến …" gồm cả 8 và 16. | ✅ Đã rõ | — | “Từ 8 đến 16 ký tự” |
| FORGOT-R04 | Mật khẩu mới. | Phải có chữ hoa, chữ thường, số và ký tự đặc biệt. | ✅ Đã rõ | — | “Bao gồm chữ hoa, chữ thường, số và ký tự đặc biệt” |
| FORGOT-R04 | **Phần còn chưa rõ** của dòng trên (ký tự đặc biệt) | Không liệt kê ký tự đặc biệt hợp lệ. | ❓ Thiếu thông tin | **A5. Ký tự đặc biệt hợp lệ gồm những ký tự nào?** (🚨 Hỏi BA ngay) | — |
| FORGOT-R05 | Mật khẩu mới. | Không được trùng với 5 mật khẩu gần nhất. | ✅ Đã rõ | — | “Không được trùng với 5 mật khẩu gần nhất” |
| FORGOT-R05 | **Phần còn chưa rõ** của dòng trên (mật khẩu đang dùng) | Không nói mật khẩu đang dùng có tính không. | ❓ Chưa rõ nghĩa | **A6. Mật khẩu đang dùng có nằm trong 5 mật khẩu gần nhất không?** (🚨 Hỏi BA ngay) | — |

## 7. Nhóm 🚨 Hỏi BA ngay
Nội dung đầy đủ ở Phần A của [cau-hoi-cho-ba.md](cau-hoi-cho-ba.md). Danh sách và mã liên quan:
- **A1. Nhập email chưa đăng ký thì hệ thống làm gì?** (liên quan FORGOT-S01-AC01)
- **A2. Nhập sai OTP thì hệ thống làm gì, được sai mấy lần?** (liên quan FORGOT-S02-AC01)
- **A3. OTP quá 5 phút thì hiện gì, có gửi lại OTP được không?** (liên quan FORGOT-S02-AC01)
- **A4. Xin OTP mới thì OTP cũ còn dùng được không, OTP dùng rồi có dùng lại được không?** (liên quan FORGOT-S02-AC01)
- **A5. Ký tự đặc biệt hợp lệ gồm những ký tự nào?** (liên quan FORGOT-R04)
- **A6. Mật khẩu đang dùng có nằm trong 5 mật khẩu gần nhất không?** (liên quan FORGOT-R05)

## 8. Tự kiểm
- Đủ 13 đơn vị: mọi mã xuất hiện ít nhất một dòng.
- Mọi câu hỏi xuất hiện ít nhất một lần.
- Trích dẫn đã so từng chuỗi với requirement bằng `kiem-tra.py`.

## 9. Lịch sử thay đổi
| Ngày | Thay đổi |
|---|---|
| 2026-11-20 | Tạo mới |
