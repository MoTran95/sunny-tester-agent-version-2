# Bảng phân tích requirement — Đăng nhập (Ecommerce Lite)

| | |
|---|---|
| Nguồn requirement | [srs/ecommerce-lite/dang-nhap.md](../../../srs/ecommerce-lite/dang-nhap.md) (mã `LOGIN`, tình trạng nháp, ghi lại hành vi quan sát trên môi trường thử ngày 2026-11-20) |
| Ngày lập | 2026-11-20 |
| Cách làm | Tách, Xoay, Lọc (skill `phan-tich-requirement`) |
| Phạm vi | 29 đơn vị (18 tiêu chí chấp nhận, 4 quy tắc, 7 thông báo). Chỉ **functional**. Chưa viết checklist hay test case |
| Câu hỏi gửi BA | [cau-hoi-cho-ba.md](cau-hoi-cho-ba.md) |

## 1. Cách đọc
**Mỗi dòng trả lời ba câu:** (1) người dùng làm gì, (2) requirement cho biết gì hoặc chỗ nào chưa rõ, (3) cần hỏi BA câu gì.

**Lưu ý nguồn:** chưa có tài liệu yêu cầu của BA; nguồn là SRS nháp ghi lại điều đã quan sát. Dòng ✅ nghĩa là **hành vi quan sát đã rõ và đủ để viết test**, chưa phải xác nhận chính thức của BA.

**Cách đọc mã:** `LOGIN` là tên tính năng đăng nhập; `S01` là story số 1; `AC01` là tiêu chí số 1 của story đó; `R` là quy tắc dữ liệu, `M` là thông báo.

**Cột Trạng thái:**
- **✅ Đã rõ:** biết thế nào là đúng, trong phạm vi điều đã quan sát.
- **❓ + loại vấn đề:** Thiếu thông tin, Chưa rõ nghĩa, Hai chỗ nói khác nhau, Số liệu không chính xác, hoặc Trình bày không thống nhất.

**Cách xử lý câu hỏi** (in đậm đầu mỗi câu hỏi):
- **🚨 Hỏi BA ngay:** hiểu sai thì kết quả đúng đổi.
- **📋 Hỏi BA sau (gom lại):** câu chữ, hiển thị, hoặc phần ngoài phần đang test.
- **🔍 Tự kiểm tra trên hệ thống trước:** xem hệ thống đang chạy để tìm câu trả lời. Chỉ cho biết hệ thống đang làm gì, không chứng minh là đúng.

**Cột "Câu hỏi gửi BA":** chỉ ghi số câu, tiêu đề và cách xử lý. Nội dung đầy đủ nằm ở [cau-hoi-cho-ba.md](cau-hoi-cho-ba.md).

**Hai điều không hỏi BA** (suy ra từ mục đích của màn hình đăng nhập là chỉ báo đúng hoặc sai): không kiểm định dạng email, độ dài hay ký tự đặc biệt ở màn hình này (đó là việc của phần đăng ký); mọi lỗi đăng nhập dùng chung một câu để không lộ ô nào sai.

## 2. Giải thích thuật ngữ (theo SRS)
| Thuật ngữ | Nghĩa |
|---|---|
| Phiên | Khoảng thời gian người dùng còn đăng nhập sau khi vào được; trình duyệt giữ bằng cookie `sunny_session` |
| Tài khoản khách mẫu | Tài khoản có sẵn của môi trường thử, vai trò hiển thị "Customer" |
| "Remember me on this device" | Ô đánh dấu trên form đăng nhập |

## 3. Câu trả lời đã nhận
Chưa có câu trả lời nào.

## 4. Tổng kết
| Chỉ số | Số lượng |
|---|---|
| Đơn vị chỉ có phần ✅ | 21 |
| Đơn vị có cả ✅ và ❓ | 5 |
| Đơn vị chỉ có ❓ | 3 |
| Tổng | 29 |
| Câu hỏi: 🚨 / 📋 / 🔍 | 4 / 3 / 1 |

## 5. Bảng soát theo từng story

### Đăng nhập thành công (LOGIN-S01)

| Mã | Tình huống (người dùng làm gì) | Requirement cho biết gì, hoặc chỗ nào chưa rõ | Trạng thái | Câu hỏi gửi BA | Trích nguyên văn |
|---|---|---|---|---|---|
| LOGIN-S01-AC01 | Nhập email và mật khẩu đúng của tài khoản khách, bấm "Sign in". | Vào cửa hàng, hiện lời chào và các mục menu. | ✅ Đã rõ | — | “Thanh trên có "Shop", "My orders", "Profile", "Bag 0", nút "Sign out"; lời chào "Welcome, Sunny".” |
| LOGIN-S01-AC01 | Mình chưa biết vai trò nào khác có thể đăng nhập cùng form này. | **Phần còn chưa rõ** của dòng trên: chưa có tài khoản vai trò khác để thử. | ❓ Thiếu thông tin | **A4. Có tài khoản vai trò khác ngoài khách không?** (🚨 Hỏi BA ngay) | — |
| LOGIN-S01-AC02 | Nhập email viết hoa hết và mật khẩu đúng, nhấn Enter ở ô mật khẩu. | Nhấn Enter cũng đăng nhập được như bấm nút. | ✅ Đã rõ | — | “nhấn Enter khi đang ở ô mật khẩu” |
| LOGIN-S01-AC02 | Email viết hoa hết vẫn vào được. | **Phần còn chưa rõ** của dòng trên: chưa biết email có được coi là không phân biệt chữ hoa, thường theo yêu cầu không. | ❓ Chưa rõ nghĩa | **B1. Email viết hoa có tính là cùng một email không?** (📋 Hỏi BA sau (gom lại)) | “Thông tin người dùng trả về có email chữ thường.” |
| LOGIN-S01-AC03 | Nhập email có dấu cách đầu và cuối cùng mật khẩu đúng, bấm "Sign in". | Đăng nhập thành công; khoảng trắng đầu cuối của email không cản trở. | ✅ Đã rõ | — | “Nhập email có hai dấu cách đầu và cuối cùng mật khẩu đúng, bấm "Sign in"” |
| LOGIN-S01-AC04 | Đăng nhập một lần có tích và một lần không tích "Remember me on this device". | Cả hai lần giống hệt nhau; không biết ô này phải làm gì. | ❓ Thiếu thông tin | **A3. Ô "Remember me on this device" để làm gì?** (🚨 Hỏi BA ngay) | “Cả hai lần đăng nhập thành công, cùng một cookie phiên, thời hạn cookie hai lần giống nhau; không thấy hộp này làm khác đi điều gì.” |

### Đăng nhập không thành công (LOGIN-S02)

| Mã | Tình huống (người dùng làm gì) | Requirement cho biết gì, hoặc chỗ nào chưa rõ | Trạng thái | Câu hỏi gửi BA | Trích nguyên văn |
|---|---|---|---|---|---|
| LOGIN-S02-AC01 | Nhập email đúng và một mật khẩu sai, bấm "Sign in". | Hiện câu lỗi chung, ở lại form, giữ email, xóa mật khẩu. | ✅ Đã rõ | — | “Ở lại form; email còn nguyên trong ô, ô mật khẩu bị xóa trống. Không vào được cửa hàng.” |
| LOGIN-S02-AC02 | Nhập email không có thật và mật khẩu bất kỳ. | Cùng câu lỗi với mật khẩu sai. Suy ra từ [LOGIN-R04](../../../srs/ecommerce-lite/dang-nhap.md#login-r04): màn hình chỉ báo đúng hoặc sai, không lộ ô nào sai. | ✅ Đã rõ | — | “không cho biết email sai hay mật khẩu sai” |
| LOGIN-S02-AC03 | Nhập email đúng, mật khẩu đúng nhưng đổi hoa/thường một chữ. | Không đăng nhập được, cùng câu lỗi chung. | ✅ Đã rõ | — | “mật khẩu phân biệt chữ hoa, thường” |
| LOGIN-S02-AC04 | Đăng nhập sai nhiều lần liên tiếp. | Mới thử đúng 3 lần, chưa thấy bị chặn; chưa biết có giới hạn không, bao nhiêu lần, chặn bao lâu. | ❓ Thiếu thông tin | **A1. Đăng nhập sai bao nhiêu lần thì bị chặn?** (🚨 Hỏi BA ngay) | “không thấy bị chặn hay thông báo khóa; đăng nhập đúng sau đó vẫn thành công. Chưa thử quá 3 lần.” |

### Báo thiếu thông tin trước khi gửi (LOGIN-S03)

| Mã | Tình huống (người dùng làm gì) | Requirement cho biết gì, hoặc chỗ nào chưa rõ | Trạng thái | Câu hỏi gửi BA | Trích nguyên văn |
|---|---|---|---|---|---|
| LOGIN-S03-AC01 | Để trống cả hai ô, bấm "Sign in". | Báo lỗi dưới từng ô trống, không gửi lên máy chủ. | ✅ Đã rõ | — | “Không có lệnh gọi đăng nhập nào gửi đi.” |
| LOGIN-S03-AC02 | Nhập `abc` vào ô email, để trống mật khẩu, bấm "Sign in". | Không báo lỗi định dạng email. Suy ra là đúng: màn hình đăng nhập chỉ báo đúng hoặc sai, không kiểm định dạng (kiểm định dạng là việc của phần đăng ký). | ✅ Đã rõ | — | “ô email không báo lỗi định dạng.” |

### Phiên đăng nhập và đăng xuất (LOGIN-S04)

| Mã | Tình huống (người dùng làm gì) | Requirement cho biết gì, hoặc chỗ nào chưa rõ | Trạng thái | Câu hỏi gửi BA | Trích nguyên văn |
|---|---|---|---|---|---|
| LOGIN-S04-AC01 | Tải lại trang khi đã đăng nhập. | Vẫn đăng nhập. | ✅ Đã rõ | — | “Vẫn đăng nhập: thấy "Sign out", không thấy ô mật khẩu.” |
| LOGIN-S04-AC02 | Mở tab thứ hai trong cùng trình duyệt. | Tab thứ hai cũng đã đăng nhập. | ✅ Đã rõ | — | “Tab thứ hai cũng đã đăng nhập.” |
| LOGIN-S04-AC03 | Bấm "Sign out". | Về form đăng nhập; phiên máy chủ mất. Phần nút Back chưa có kết quả có nghĩa, mình tự kiểm tra. | ✅ Đã rõ | **C1. Bấm Back sau khi đăng xuất thì thấy gì?** (🔍 Tự kiểm tra trên hệ thống trước) | “quay lại form đăng nhập; gọi `GET /api/me` trả 401.” |
| LOGIN-S04-AC04 | Đăng xuất ở tab này rồi xem tab kia. | Tab kia mất phiên, tải lại thì hiện form. Suy ra từ [LOGIN-R03](../../../srs/ecommerce-lite/dang-nhap.md#login-r03): các tab dùng chung một phiên. | ✅ Đã rõ | — | “tải lại thì tab 2 hiện form đăng nhập.” |

### Truy cập khi chưa đăng nhập (LOGIN-S05)

| Mã | Tình huống (người dùng làm gì) | Requirement cho biết gì, hoặc chỗ nào chưa rõ | Trạng thái | Câu hỏi gửi BA | Trích nguyên văn |
|---|---|---|---|---|---|
| LOGIN-S05-AC01 | Chưa đăng nhập, mở thẳng `/#profile`. | Thấy form đăng nhập, không thấy trang hồ sơ. | ✅ Đã rõ | — | “Địa chỉ giữ nguyên `/#profile` nhưng nội dung là form đăng nhập; không thấy trang hồ sơ.” |
| LOGIN-S05-AC02 | Chưa đăng nhập, mở địa chỉ không tồn tại. | Hiện luôn trang đăng nhập với mã 200, không có trang "không tìm thấy"; chưa biết có đúng yêu cầu không. | ❓ Chưa rõ nghĩa | **B2. Mở địa chỉ không tồn tại thì nên hiện gì?** (📋 Hỏi BA sau (gom lại)) | “không có trang "không tìm thấy".” |
| LOGIN-S05-AC03 | Chưa đăng nhập, trình duyệt kiểm phiên. | Kiểm phiên trả 401. | ✅ Đã rõ | — | “Gọi `GET /api/me` (trình duyệt tự gọi khi mở trang)” |

### Quên mật khẩu (LOGIN-S06)

| Mã | Tình huống (người dùng làm gì) | Requirement cho biết gì, hoặc chỗ nào chưa rõ | Trạng thái | Câu hỏi gửi BA | Trích nguyên văn |
|---|---|---|---|---|---|
| LOGIN-S06-AC01 | Bấm "Forgot password?". | Hiện thông báo tạm, trang không đổi. | ✅ Đã rõ | — | “trang không đổi.” |
| LOGIN-S06-AC01 | Bản thật xử lý quên mật khẩu thế nào. | **Phần còn chưa rõ** của dòng trên: môi trường thử đang tắt tính năng này. | ❓ Thiếu thông tin | **B3. "Forgot password?" ở bản thật làm gì?** (📋 Hỏi BA sau (gom lại)) | — |

## 6. Phụ lục: quy tắc và thông báo

| Mã | Tình huống | Requirement cho biết gì, hoặc chỗ nào chưa rõ | Trạng thái | Câu hỏi gửi BA | Trích nguyên văn |
|---|---|---|---|---|---|
| LOGIN-R01 | Nhập ô email. | Bắt buộc; không kiểm định dạng ở màn hình đăng nhập; khoảng trắng đầu cuối bị cắt. | ✅ Đã rõ | — | “Bắt buộc (trình duyệt chỉ kiểm không để trống, không kiểm định dạng)” |
| LOGIN-R01 | Email viết hoa, thường. | **Phần còn chưa rõ** của dòng trên: chưa có yêu cầu nói email có phân biệt chữ hoa, thường không. | ❓ Chưa rõ nghĩa | **B1. Email viết hoa có tính là cùng một email không?** (📋 Hỏi BA sau (gom lại)) | — |
| LOGIN-R02 | Nhập ô mật khẩu. | Bắt buộc; phân biệt chữ hoa, thường; gửi nguyên văn. Độ dài, ký tự cho phép thuộc phần đăng ký, không hỏi ở đây. | ✅ Đã rõ | — | “phân biệt chữ hoa, thường; gửi nguyên văn, không cắt khoảng trắng.” |
| LOGIN-R03 | Đăng nhập xong. | Phiên giữ bằng cookie có `HttpOnly`, `Secure`, `SameSite=Lax`. | ✅ Đã rõ | — | “Cookie `sunny_session` có `HttpOnly`, `Secure`, `SameSite=Lax`” |
| LOGIN-R03 | Phiên hết hạn. | **Phần còn chưa rõ** của dòng trên: chưa biết phiên giữ bao lâu và hết hạn thì thấy gì. | ❓ Thiếu thông tin | **A2. Đăng nhập xong thì giữ được bao lâu?** (🚨 Hỏi BA ngay) | — |
| LOGIN-R04 | Đăng nhập sai (email hay mật khẩu). | Cùng một câu lỗi và cùng mã lỗi `INVALID_CREDENTIALS`. | ✅ Đã rõ | — | “Email không tồn tại và mật khẩu sai cho cùng một câu lỗi và cùng mã lỗi `INVALID_CREDENTIALS`.” |
| LOGIN-M01 | Để trống ô email. | Thông báo nguyên văn, chỉ có tiếng Anh. | ✅ Đã rõ | — | “`Enter your email address.`” |
| LOGIN-M02 | Để trống ô mật khẩu. | Thông báo nguyên văn. | ✅ Đã rõ | — | “`Enter your password.`” |
| LOGIN-M03 | Email hoặc mật khẩu không đúng. | Thông báo nguyên văn do máy chủ trả về. | ✅ Đã rõ | — | “`Email or password is incorrect.`” |
| LOGIN-M04 | Đăng nhập thành công. | Thông báo chào bằng tên đầu của người dùng. | ✅ Đã rõ | — | “`Welcome back, Sunny!`” |
| LOGIN-M05 | Đăng xuất. | Thông báo nguyên văn. | ✅ Đã rõ | — | “`You have been signed out.`” |
| LOGIN-M06 | Bấm "Forgot password?". | Thông báo nguyên văn của môi trường thử. | ✅ Đã rõ | — | “`Password recovery is disabled in the training environment.`” |
| LOGIN-M07 | Đang gửi đăng nhập. | Chữ trên nút đổi trong lúc chờ; chỉ thấy trong tệp giao diện. Hành vi trên màn hình đã rõ nên không hỏi. | ✅ Đã rõ | — | “Chữ trên nút đổi thành `Signing in…`” |

## 7. Nhóm 🚨 Hỏi BA ngay
Nội dung đầy đủ ở Phần A của [cau-hoi-cho-ba.md](cau-hoi-cho-ba.md). Danh sách và mã liên quan:
- **A1. Đăng nhập sai bao nhiêu lần thì bị chặn?** (liên quan LOGIN-S02-AC04)
- **A2. Đăng nhập xong thì giữ được bao lâu?** (liên quan LOGIN-R03)
- **A3. Ô "Remember me on this device" để làm gì?** (liên quan LOGIN-S01-AC04)
- **A4. Có tài khoản vai trò khác ngoài khách không?** (liên quan LOGIN-S01-AC01)

## 8. Tự kiểm
- Đủ 29 đơn vị: mọi mã xuất hiện ít nhất một dòng.
- Mọi câu hỏi xuất hiện ít nhất một lần.
- Trích dẫn đã so từng chuỗi với requirement bằng `kiem-tra.py`.

## 9. Lịch sử thay đổi
| Ngày | Thay đổi |
|---|---|
| 2026-11-20 | Tạo mới: 29 đơn vị, 8 câu hỏi (4 hỏi ngay, 3 hỏi sau, 1 tự kiểm tra) |
