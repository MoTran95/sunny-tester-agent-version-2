# SRS — Quên mật khẩu (Ecommerce Lite)

*SRS (tài liệu đặc tả yêu cầu) ghi hệ thống phải làm gì ở tính năng này: mỗi tình huống một dòng có mã cố định và bằng chứng. Test case dựa vào các mã này, nên khi requirement đổi sẽ biết ngay test case nào phải sửa.*

| | |
|---|---|
| Mã feature | `FORGOT` |
| Phiên bản hệ thống đã quan sát | chưa đối chiếu hệ thống |
| Cập nhật lần cuối | 2026-11-20 |
| Tình trạng | nháp (viết từ tài liệu yêu cầu, chưa hỏi BA) |
| Nhật ký khám phá gốc (hoặc tài liệu yêu cầu gốc) | [yeu-cau-quen-mat-khau.md](../../evidence/ecommerce-lite/tai-lieu/yeu-cau-quen-mat-khau.md) |

## 1. Mục đích, phạm vi, vai trò
- **Mục đích:** Người dùng đặt lại mật khẩu đăng nhập khi quên, bằng mã OTP gửi qua email đã đăng ký.
- **Ngoài phạm vi / chưa thấy trên màn hình:** Chưa khám phá hệ thống; toàn bộ nội dung lấy từ tài liệu yêu cầu. Tài liệu không nói về vị trí nút "Quên mật khẩu", thông báo lỗi, gửi lại OTP, số lần nhập sai.
- **Vai trò:** Người dùng đã có tài khoản (tài liệu không nêu vai trò cụ thể).

| Tài khoản | Vai trò hiển thị | Đã thử với feature này |
|---|---|---|
| (chưa có) | chưa đối chiếu hệ thống | chưa thử |

## 2. Điều kiện tiên quyết
- Người dùng đã đăng ký tài khoản và có địa chỉ email đã đăng ký (theo tài liệu).
- Người dùng nhận được email chứa OTP.

## 3. User story và tiêu chí chấp nhận

### `FORGOT-S01` — Yêu cầu đặt lại mật khẩu
**Là** người dùng quên mật khẩu, **tôi muốn** nhập email đã đăng ký để nhận mã OTP **để** bắt đầu đặt lại mật khẩu.

**Luồng:** (1) nhập email đã đăng ký → (2) hệ thống gửi OTP 6 chữ số đến email (→ `FORGOT-S01-AC01`).

**Cách đọc:** mỗi dòng là một tình huống test. *Bối cảnh* = tình trạng trước khi làm; *Người dùng làm* = thao tác cụ thể; *Hệ thống phản hồi* = điều tài liệu yêu cầu. (Giới test gọi là Given – When – Then; mỗi dòng là một "tiêu chí chấp nhận", viết tắt AC.)

| ID | Tình huống | Bối cảnh | Người dùng làm | Hệ thống phản hồi | Nhãn · Bằng chứng · Liên quan |
|---|---|---|---|---|---|
| <a id="forgot-s01-ac01"></a>`FORGOT-S01-AC01` | Nhận OTP khi nhập email đã đăng ký | Có tài khoản đã đăng ký với một email | Nhập địa chỉ email đã đăng ký tài khoản để yêu cầu đặt lại mật khẩu | Gửi mã OTP gồm 6 chữ số đến email đã đăng ký. OTP có hiệu lực trong 5 phút | theo tài liệu · [E01](#e01) · `FORGOT-R01`, `FORGOT-R02` |

### `FORGOT-S02` — Xác thực OTP
**Là** người dùng quên mật khẩu, **tôi muốn** nhập OTP nhận được **để** được phép tạo mật khẩu mới.

**Luồng:** (1) nhập OTP → (2) nếu đúng và còn hiệu lực, chuyển đến màn hình tạo mật khẩu mới (→ `FORGOT-S02-AC01`).

| ID | Tình huống | Bối cảnh | Người dùng làm | Hệ thống phản hồi | Nhãn · Bằng chứng · Liên quan |
|---|---|---|---|---|---|
| <a id="forgot-s02-ac01"></a>`FORGOT-S02-AC01` | Chuyển đến màn hình tạo mật khẩu mới khi nhập đúng OTP còn hiệu lực | Đã nhận OTP, chưa quá 5 phút | Nhập đúng OTP | Chuyển đến màn hình tạo mật khẩu mới | theo tài liệu · [E01](#e01) · `FORGOT-R02` |

### `FORGOT-S03` — Tạo mật khẩu mới
**Là** người dùng đã xác thực OTP, **tôi muốn** đặt mật khẩu mới hợp lệ **để** đăng nhập lại.

**Luồng:** (1) nhập mật khẩu mới → (2) mật khẩu thỏa quy tắc thì được chấp nhận (→ `FORGOT-S03-AC01`); không thỏa thì không được chấp nhận (→ `FORGOT-S03-AC02`–`AC04`).

| ID | Tình huống | Bối cảnh | Người dùng làm | Hệ thống phản hồi | Nhãn · Bằng chứng · Liên quan |
|---|---|---|---|---|---|
| <a id="forgot-s03-ac01"></a>`FORGOT-S03-AC01` | Chấp nhận mật khẩu mới khi thỏa mọi quy tắc | Đang ở màn hình tạo mật khẩu mới | Nhập mật khẩu 8–16 ký tự có đủ chữ hoa, chữ thường, số, ký tự đặc biệt và không trùng 5 mật khẩu gần nhất | Mật khẩu mới được chấp nhận (kết quả sau đó: `FORGOT-S04-AC01`) | theo tài liệu · [E01](#e01) · `FORGOT-R03`, `FORGOT-R04`, `FORGOT-R05` |
| <a id="forgot-s03-ac02"></a>`FORGOT-S03-AC02` | Không chấp nhận mật khẩu mới ngắn hơn 8 hoặc dài hơn 16 ký tự | Đang ở màn hình tạo mật khẩu mới | Nhập mật khẩu có độ dài ngoài khoảng 8 đến 16 ký tự | Mật khẩu không được chấp nhận. Tài liệu không nêu thông báo (→ `FORGOT-Q06`) | theo tài liệu · [E01](#e01) · `FORGOT-R03` |
| <a id="forgot-s03-ac03"></a>`FORGOT-S03-AC03` | Không chấp nhận mật khẩu mới thiếu một trong bốn loại ký tự bắt buộc | Đang ở màn hình tạo mật khẩu mới | Nhập mật khẩu 8–16 ký tự nhưng thiếu chữ hoa, hoặc chữ thường, hoặc số, hoặc ký tự đặc biệt | Mật khẩu không được chấp nhận. Tài liệu không nêu thông báo (→ `FORGOT-Q06`) | theo tài liệu · [E01](#e01) · `FORGOT-R04` |
| <a id="forgot-s03-ac04"></a>`FORGOT-S03-AC04` | Không chấp nhận mật khẩu mới trùng một trong 5 mật khẩu gần nhất | Tài khoản đã từng có ít nhất một mật khẩu cũ | Nhập mật khẩu trùng một trong 5 mật khẩu gần nhất | Mật khẩu không được chấp nhận. Tài liệu không nêu thông báo (→ `FORGOT-Q06`, `FORGOT-Q07`) | theo tài liệu · [E01](#e01) · `FORGOT-R05` |

### `FORGOT-S04` — Kết thúc đặt lại mật khẩu
**Là** người dùng vừa đổi mật khẩu, **tôi muốn** biết việc đổi đã thành công **để** đăng nhập lại bằng mật khẩu mới.

**Luồng:** (1) đổi mật khẩu thành công → (2) hiển thị thông báo thành công (→ `FORGOT-S04-AC01`) → (3) yêu cầu đăng nhập lại (→ `FORGOT-S04-AC02`).

| ID | Tình huống | Bối cảnh | Người dùng làm | Hệ thống phản hồi | Nhãn · Bằng chứng · Liên quan |
|---|---|---|---|---|---|
| <a id="forgot-s04-ac01"></a>`FORGOT-S04-AC01` | Hiển thị thông báo thành công sau khi đổi mật khẩu | Vừa nhập mật khẩu mới hợp lệ (`FORGOT-S03-AC01`) | Xác nhận đổi mật khẩu | Hiển thị thông báo thành công (nguyên văn chưa rõ, → `FORGOT-Q08`) | theo tài liệu · [E01](#e01) |
| <a id="forgot-s04-ac02"></a>`FORGOT-S04-AC02` | Yêu cầu đăng nhập lại sau khi đổi mật khẩu | Vừa đổi mật khẩu thành công | Không làm thêm gì | Yêu cầu người dùng đăng nhập lại (cách thể hiện chưa rõ, → `FORGOT-Q08`) | theo tài liệu · [E01](#e01) |

## 4. Bảng tra cứu
### 4.1 Quy tắc dữ liệu
| ID | Trường | Quy tắc quan sát được | Nhãn | Bằng chứng |
|---|---|---|---|---|
| <a id="forgot-r01"></a>`FORGOT-R01` | Mã OTP | Gồm 6 chữ số | theo tài liệu | [E01](#e01) |
| <a id="forgot-r02"></a>`FORGOT-R02` | Mã OTP | Có hiệu lực trong 5 phút | theo tài liệu | [E01](#e01) |
| <a id="forgot-r03"></a>`FORGOT-R03` | Mật khẩu mới | Từ 8 đến 16 ký tự | theo tài liệu | [E01](#e01) |
| <a id="forgot-r04"></a>`FORGOT-R04` | Mật khẩu mới | Bao gồm chữ hoa, chữ thường, số và ký tự đặc biệt | theo tài liệu | [E01](#e01) |
| <a id="forgot-r05"></a>`FORGOT-R05` | Mật khẩu mới | Không được trùng với 5 mật khẩu gần nhất | theo tài liệu | [E01](#e01) |

### 4.2 Thông báo hệ thống (nguyên văn)
Tài liệu không ghi nguyên văn thông báo nào. Chưa có dòng `FORGOT-M`; sau khi BA trả lời hoặc khám phá hệ thống thì thêm.

| ID | Khi nào | Tiếng Việt | English | Bằng chứng |
|---|---|---|---|---|
| (chưa có) | | | | |

## 5. Điểm chưa rõ và câu hỏi cho team
| ID | Đã thấy | Vì sao chưa rõ | Câu hỏi | Liên quan | Trạng thái |
|---|---|---|---|---|---|
| <a id="forgot-q01"></a>`FORGOT-Q01` | Tài liệu chỉ nói về email đã đăng ký | Không nói khi email chưa đăng ký | Nhập email chưa đăng ký thì hệ thống làm gì và hiển thị gì (có gửi OTP không)? | `FORGOT-S01-AC01` | chờ trả lời |
| <a id="forgot-q02"></a>`FORGOT-Q02` | Không có | Không nói khi để trống hoặc nhập sai định dạng email | Để trống hoặc nhập sai định dạng email thì hệ thống phản hồi thế nào? | `FORGOT-S01-AC01` | chờ trả lời |
| <a id="forgot-q03"></a>`FORGOT-Q03` | Chỉ nói nhập đúng OTP còn hiệu lực | Không nói khi nhập sai OTP | Nhập sai OTP thì hiển thị thông báo gì? Được nhập sai tối đa bao nhiêu lần, quá số lần thì sao? | `FORGOT-S02-AC01` | chờ trả lời |
| <a id="forgot-q04"></a>`FORGOT-Q04` | OTP có hiệu lực 5 phút | Không nói khi OTP đã quá 5 phút | Nhập OTP đã hết hạn thì hiển thị thông báo gì? Có cho gửi lại OTP không, chờ bao lâu giữa hai lần gửi? | `FORGOT-R02` | chờ trả lời |
| <a id="forgot-q05"></a>`FORGOT-Q05` | Không có | Không nói khi yêu cầu OTP lần thứ hai | Xin OTP mới khi OTP cũ còn hạn thì OTP cũ còn dùng được không? OTP đã dùng xong có dùng lại được không? | `FORGOT-R02` | chờ trả lời |
| <a id="forgot-q06"></a>`FORGOT-Q06` | Mật khẩu mới phải thỏa các quy tắc | Không nói thông báo lỗi và không nói ký tự đặc biệt nào hợp lệ | Thông báo khi mật khẩu không hợp lệ là gì? Ký tự đặc biệt hợp lệ gồm những ký tự nào? Có ô nhập lại mật khẩu để xác nhận không? | `FORGOT-R03`, `FORGOT-R04` | chờ trả lời |
| <a id="forgot-q07"></a>`FORGOT-Q07` | "Không trùng 5 mật khẩu gần nhất" | Không nói mật khẩu đang dùng có tính trong 5 mật khẩu đó không, và thông báo khi trùng | Mật khẩu hiện tại có nằm trong 5 mật khẩu gần nhất không? Thông báo khi trùng là gì? | `FORGOT-R05` | chờ trả lời |
| <a id="forgot-q08"></a>`FORGOT-Q08` | Hiển thị thông báo thành công và yêu cầu đăng nhập lại | Không có nguyên văn và không nói chuyển đến trang nào | Nguyên văn thông báo thành công là gì? Sau đó chuyển đến trang nào? Mật khẩu cũ có còn đăng nhập được không? | `FORGOT-S04-AC01`, `FORGOT-S04-AC02` | chờ trả lời |

## 6. Bằng chứng và chưa khám phá
### 6.1 Bằng chứng
| ID | Loại | Ngày · phiên bản · tài khoản | Thao tác đã làm | Tệp | Cách kiểm lại |
|---|---|---|---|---|---|
| <a id="e01"></a>`FORGOT-E01` | tài liệu yêu cầu | 2026-11-20 · chưa đối chiếu hệ thống · không có | Người dùng dán requirement vào chat; lưu nguyên văn | [yeu-cau-quen-mat-khau.md](../../evidence/ecommerce-lite/tai-lieu/yeu-cau-quen-mat-khau.md) | Mở tệp, đối chiếu các gạch đầu dòng theo thứ tự từ trên xuống |

### 6.2 Chưa khám phá
- Toàn bộ hành vi trên hệ thống thật: chưa khám phá vì mới chuyển từ tài liệu yêu cầu, người dùng chưa nhờ khám phá.

## 7. Lịch sử thay đổi
| Ngày | Phiên bản hệ thống | Thay đổi | Lý do |
|---|---|---|---|
| 2026-11-20 | chưa đối chiếu hệ thống | Tạo SRS: 4 story, 8 AC, 5 quy tắc, 0 thông báo, 8 câu hỏi, 1 bằng chứng | Chuyển requirement Quên mật khẩu thành SRS có mã |
