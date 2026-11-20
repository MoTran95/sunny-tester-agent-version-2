# SRS — Đăng nhập (Ecommerce Lite)

*SRS (tài liệu đặc tả yêu cầu) ghi hệ thống phải làm gì ở tính năng này: mỗi tình huống một dòng có mã cố định và bằng chứng. Test case dựa vào các mã này, nên khi requirement đổi sẽ biết ngay test case nào phải sửa.*

| | |
|---|---|
| Mã feature | `LOGIN` |
| Phiên bản hệ thống đã quan sát | không thấy số phiên bản trên trang; môi trường staging ngày 2026-11-20 |
| Cập nhật lần cuối | 2026-11-20 |
| Tình trạng | nháp (chưa xác nhận với team) |
| Nhật ký khám phá gốc | [bao-cao.md](../../evidence/ecommerce-lite/features/dang-nhap/bao-cao.md) |

## 1. Mục đích, phạm vi, vai trò
- **Mục đích:** cho người dùng vào khu vực cửa hàng bằng email và mật khẩu, giữ phiên đăng nhập trong lúc dùng, và cho đăng xuất.
- **Ngoài phạm vi / chưa thấy trên màn hình:** đăng ký tài khoản (tab "Create account"), khôi phục mật khẩu (đang tắt ở môi trường thử), các màn hình sau đăng nhập (cửa hàng, đơn hàng, hồ sơ).
- **Vai trò:** trang cho biết đây là môi trường thử có tài khoản khách mẫu; mới thử với một tài khoản.

| Tài khoản | Vai trò hiển thị | Đã thử với feature này |
|---|---|---|
| Tài khoản khách mẫu của môi trường thử (mã `SHOPPER` trong `.env`) | `Customer` (tên hiển thị "Sunny Shopper") | Đăng nhập đúng, sai, đăng xuất |
| Vai trò khác | chưa biết | Chưa thử, xem mục 6.2 |

## 2. Điều kiện tiên quyết
- Mở `https://staging-ecommerce-lite.vercel.app/` khi chưa đăng nhập: trang hiện form đăng nhập.
- Có một tài khoản đã tạo sẵn (email, mật khẩu). Mật khẩu của tài khoản test nằm trong `.env`, không ghi vào tài liệu.

## 3. User story và tiêu chí chấp nhận

**Cách đọc chung:** mỗi dòng là một tình huống test. *Bối cảnh* = tình trạng trước khi làm; *Người dùng làm* = thao tác cụ thể; *Hệ thống phản hồi* = điều đã nhìn thấy (chữ trong `…` là nguyên văn). (Giới test gọi là Given – When – Then; mỗi dòng là một "tiêu chí chấp nhận", viết tắt AC.)

### `LOGIN-S01` — Đăng nhập thành công
**Là** khách hàng, **tôi muốn** đăng nhập bằng email và mật khẩu **để** vào cửa hàng.

**Luồng:** (1) mở trang → (2) nhập email và mật khẩu → (3) bấm "Sign in" hoặc nhấn Enter → (4) vào trang cửa hàng với lời chào; sai thông tin → `LOGIN-S02`; thiếu ô → `LOGIN-S03`.

| ID | Tình huống | Bối cảnh | Người dùng làm | Hệ thống phản hồi | Nhãn · Bằng chứng · Liên quan |
|---|---|---|---|---|---|
| <a id="login-s01-ac01"></a>`LOGIN-S01-AC01` | Đăng nhập đúng bằng nút | Chưa đăng nhập, đang ở form đăng nhập | Nhập email và mật khẩu đúng của tài khoản khách, bấm "Sign in" | Vào trang cửa hàng. Hiện [LOGIN-M04](#login-m04). Thanh trên có "Shop", "My orders", "Profile", "Bag 0", nút "Sign out"; lời chào "Welcome, Sunny". Phiên được lưu bằng cookie ([LOGIN-R03](#login-r03)). Trong lúc chờ, theo tệp giao diện nút đổi chữ thành [LOGIN-M07](#login-m07) (chưa thấy trên màn hình). | đã thấy · [E05](#e05), [E13](#e13) · `LOGIN-R03`, `LOGIN-M04`, `LOGIN-M07` |
| <a id="login-s01-ac02"></a>`LOGIN-S01-AC02` | Email viết hoa chữ, nhấn Enter | Chưa đăng nhập | Nhập email `SHOPPER@SUNNY.TEST` (viết hoa hết) và mật khẩu đúng, nhấn Enter khi đang ở ô mật khẩu | Đăng nhập thành công như `LOGIN-S01-AC01`; hiện [LOGIN-M04](#login-m04). Thông tin người dùng trả về có email chữ thường. | đã thấy · [E04](#e04) · `LOGIN-R01`, `LOGIN-M04` |
| <a id="login-s01-ac03"></a>`LOGIN-S01-AC03` | Email có khoảng trắng đầu và cuối | Chưa đăng nhập | Nhập email có hai dấu cách đầu và cuối cùng mật khẩu đúng, bấm "Sign in" | Đăng nhập thành công; hiện [LOGIN-M04](#login-m04). | đã thấy · [E13](#e13), [E12](#e12) · `LOGIN-R01`, `LOGIN-M04` |
| <a id="login-s01-ac04"></a>`LOGIN-S01-AC04` | Tích "Remember me on this device" | Chưa đăng nhập | Đăng nhập đúng một lần có tích và một lần không tích | Cả hai lần đăng nhập thành công, cùng một cookie phiên, thời hạn cookie hai lần giống nhau; không thấy hộp này làm khác đi điều gì. | chưa rõ · [E13](#e13) · `LOGIN-Q02` |

### `LOGIN-S02` — Đăng nhập không thành công
**Là** khách hàng, **tôi muốn** biết khi thông tin đăng nhập không đúng **để** nhập lại.

**Luồng:** (1) nhập email, mật khẩu → (2) bấm "Sign in" → (3) khung lỗi đỏ dưới nút; ở lại form.

| ID | Tình huống | Bối cảnh | Người dùng làm | Hệ thống phản hồi | Nhãn · Bằng chứng · Liên quan |
|---|---|---|---|---|---|
| <a id="login-s02-ac01"></a>`LOGIN-S02-AC01` | Email đúng, mật khẩu sai | Chưa đăng nhập | Nhập `shopper@sunny.test` và một mật khẩu sai, bấm "Sign in" | Hiện [LOGIN-M03](#login-m03) trong khung đỏ dưới nút. Ở lại form; email còn nguyên trong ô, ô mật khẩu bị xóa trống. Không vào được cửa hàng. | đã thấy · [E01](#e01) · `LOGIN-R04`, `LOGIN-M03` |
| <a id="login-s02-ac02"></a>`LOGIN-S02-AC02` | Email không tồn tại | Chưa đăng nhập | Nhập `nobody.xyz@sunny.test` và một mật khẩu bất kỳ, bấm "Sign in" | Máy chủ trả 401 với mã lỗi `INVALID_CREDENTIALS`; hiện cùng câu [LOGIN-M03](#login-m03) như `LOGIN-S02-AC01` (không cho biết email sai hay mật khẩu sai). Email giữ nguyên, mật khẩu xóa. | đã thấy · [E02](#e02), [E13](#e13) · `LOGIN-R04`, `LOGIN-M03` |
| <a id="login-s02-ac03"></a>`LOGIN-S02-AC03` | Mật khẩu đúng nhưng đổi hoa/thường một chữ | Chưa đăng nhập | Nhập email đúng, mật khẩu đúng nhưng một chữ cái đổi hoa thành thường (hoặc ngược lại), bấm "Sign in" | Không đăng nhập được; hiện [LOGIN-M03](#login-m03) (mật khẩu phân biệt chữ hoa, thường). | đã thấy · [E03](#e03), [E13](#e13) · `LOGIN-R02`, `LOGIN-M03` |
| <a id="login-s02-ac04"></a>`LOGIN-S02-AC04` | Ba lần sai liên tiếp | Chưa đăng nhập | Đăng nhập sai ba lần liên tiếp (một lần mỗi tình huống `LOGIN-S02-AC01`, `AC02`, `AC03`), rồi đăng nhập đúng | Cả ba lần đều chỉ báo [LOGIN-M03](#login-m03); không thấy bị chặn hay thông báo khóa; đăng nhập đúng sau đó vẫn thành công. Chưa thử quá 3 lần. | chưa rõ · [E15](#e15) · `LOGIN-Q01` |

### `LOGIN-S03` — Báo thiếu thông tin trước khi gửi
**Là** khách hàng, **tôi muốn** được báo ngay khi quên nhập ô nào **để** khỏi gửi form thiếu.

**Luồng:** (1) bấm "Sign in" khi còn ô trống → (2) lỗi ngay dưới từng ô trống, không gửi lên máy chủ.

| ID | Tình huống | Bối cảnh | Người dùng làm | Hệ thống phản hồi | Nhãn · Bằng chứng · Liên quan |
|---|---|---|---|---|---|
| <a id="login-s03-ac01"></a>`LOGIN-S03-AC01` | Để trống cả hai ô | Chưa đăng nhập, hai ô trống | Bấm "Sign in" | Hiện [LOGIN-M01](#login-m01) dưới ô email và [LOGIN-M02](#login-m02) dưới ô mật khẩu; hai ô viền đỏ. Không có lệnh gọi đăng nhập nào gửi đi. | đã thấy · [E10](#e10) · `LOGIN-R01`, `LOGIN-R02`, `LOGIN-M01`, `LOGIN-M02` |
| <a id="login-s03-ac02"></a>`LOGIN-S03-AC02` | Email sai định dạng, mật khẩu trống | Chưa đăng nhập | Nhập `abc` vào ô email, để trống mật khẩu, bấm "Sign in" | Chỉ hiện [LOGIN-M02](#login-m02); ô email không báo lỗi định dạng. | đã thấy · [E10](#e10) · `LOGIN-R01`, `LOGIN-M02`, `LOGIN-Q04` |

### `LOGIN-S04` — Phiên đăng nhập và đăng xuất
**Là** khách hàng, **tôi muốn** vẫn đăng nhập khi tải lại trang và đăng xuất khi xong **để** dùng tiện và an toàn.

**Luồng:** (1) đăng nhập → (2) tải lại hoặc mở thêm tab, vẫn đăng nhập → (3) bấm "Sign out" → (4) về form đăng nhập.

| ID | Tình huống | Bối cảnh | Người dùng làm | Hệ thống phản hồi | Nhãn · Bằng chứng · Liên quan |
|---|---|---|---|---|---|
| <a id="login-s04-ac01"></a>`LOGIN-S04-AC01` | Tải lại trang khi đã đăng nhập | Đã đăng nhập | Tải lại trang | Vẫn đăng nhập: thấy "Sign out", không thấy ô mật khẩu. | đã thấy · [E06](#e06) · `LOGIN-R03` |
| <a id="login-s04-ac02"></a>`LOGIN-S04-AC02` | Mở tab thứ hai cùng phiên | Đã đăng nhập ở tab 1 | Mở tab mới, vào địa chỉ gốc | Tab thứ hai cũng đã đăng nhập. | đã thấy · [E13](#e13) · `LOGIN-R03` |
| <a id="login-s04-ac03"></a>`LOGIN-S04-AC03` | Đăng xuất | Đã đăng nhập | Bấm nút "Sign out" | Hiện [LOGIN-M05](#login-m05); quay lại form đăng nhập; gọi `GET /api/me` trả 401. | đã thấy · [E07](#e07), [E13](#e13) · `LOGIN-M05` |
| <a id="login-s04-ac04"></a>`LOGIN-S04-AC04` | Đăng xuất ở tab này, tab kia | Đã đăng nhập ở hai tab cùng phiên | Đăng xuất ở tab 1, rồi gọi `GET /api/me` ở tab 2 và tải lại tab 2 | `GET /api/me` ở tab 2 trả 401; tải lại thì tab 2 hiện form đăng nhập. | đã thấy · [E13](#e13) · `LOGIN-R03` |

### `LOGIN-S05` — Truy cập khi chưa đăng nhập
**Là** người chưa đăng nhập, **tôi muốn** bị đưa về form đăng nhập **để** không xem được nội dung dành cho người đã đăng nhập.

| ID | Tình huống | Bối cảnh | Người dùng làm | Hệ thống phản hồi | Nhãn · Bằng chứng · Liên quan |
|---|---|---|---|---|---|
| <a id="login-s05-ac01"></a>`LOGIN-S05-AC01` | Mở thẳng một trang bên trong | Chưa đăng nhập | Mở `…/#profile` | Địa chỉ giữ nguyên `/#profile` nhưng nội dung là form đăng nhập; không thấy trang hồ sơ. | đã thấy · [E08](#e08) |
| <a id="login-s05-ac02"></a>`LOGIN-S05-AC02` | Mở địa chỉ không tồn tại | Chưa đăng nhập | Mở `…/khong-ton-tai` | Máy chủ trả 200 và hiện luôn trang đăng nhập; không có trang "không tìm thấy". | chưa rõ · [E09](#e09) · `LOGIN-Q05` |
| <a id="login-s05-ac03"></a>`LOGIN-S05-AC03` | Kiểm phiên khi chưa đăng nhập | Chưa đăng nhập | Gọi `GET /api/me` (trình duyệt tự gọi khi mở trang) | Trả 401. | đã thấy · [E10](#e10), [E13](#e13) · `LOGIN-R03` |

### `LOGIN-S06` — Quên mật khẩu
**Là** khách hàng, **tôi muốn** biết cách lấy lại mật khẩu **để** vào lại tài khoản.

| ID | Tình huống | Bối cảnh | Người dùng làm | Hệ thống phản hồi | Nhãn · Bằng chứng · Liên quan |
|---|---|---|---|---|---|
| <a id="login-s06-ac01"></a>`LOGIN-S06-AC01` | Bấm "Forgot password?" | Chưa đăng nhập | Bấm "Forgot password?" | Hiện [LOGIN-M06](#login-m06) trong thông báo tạm; trang không đổi. | chưa rõ · [E14](#e14) · `LOGIN-M06`, `LOGIN-Q06` |

## 4. Bảng tra cứu
### 4.1 Quy tắc dữ liệu
| ID | Trường | Quy tắc quan sát được | Nhãn | Bằng chứng |
|---|---|---|---|---|
| <a id="login-r01"></a>`LOGIN-R01` | Email | Bắt buộc (trình duyệt chỉ kiểm không để trống, không kiểm định dạng); ô kiểu email, không giới hạn độ dài; khoảng trắng đầu cuối bị cắt trước khi gửi; chữ hoa thường không ảnh hưởng (mới thử một email viết hoa toàn bộ). | đã thấy | [E10](#e10), [E11](#e11), [E12](#e12), [E04](#e04) |
| <a id="login-r02"></a>`LOGIN-R02` | Mật khẩu | Bắt buộc; không giới hạn độ dài ở ô nhập; phân biệt chữ hoa, thường; gửi nguyên văn, không cắt khoảng trắng. | đã thấy | [E10](#e10), [E11](#e11), [E12](#e12), [E03](#e03) |
| <a id="login-r03"></a>`LOGIN-R03` | Phiên | Cookie `sunny_session` có `HttpOnly`, `Secure`, `SameSite=Lax`; không lưu gì trong `localStorage` hay `sessionStorage`; các tab cùng trình duyệt dùng chung phiên. | đã thấy | [E13](#e13) |
| <a id="login-r04"></a>`LOGIN-R04` | Thông tin đăng nhập sai | Email không tồn tại và mật khẩu sai cho cùng một câu lỗi và cùng mã lỗi `INVALID_CREDENTIALS`. | đã thấy | [E01](#e01), [E02](#e02), [E13](#e13) |

### 4.2 Thông báo hệ thống (nguyên văn)
| ID | Khi nào | Tiếng Việt | English | Bằng chứng |
|---|---|---|---|---|
| <a id="login-m01"></a>`LOGIN-M01` | Để trống ô email | (hệ thống chỉ có tiếng Anh) | `Enter your email address.` | [E10](#e10), [E12](#e12) |
| <a id="login-m02"></a>`LOGIN-M02` | Để trống ô mật khẩu | (hệ thống chỉ có tiếng Anh) | `Enter your password.` | [E10](#e10), [E12](#e12) |
| <a id="login-m03"></a>`LOGIN-M03` | Email hoặc mật khẩu không đúng | (hệ thống chỉ có tiếng Anh) | `Email or password is incorrect.` (chữ do máy chủ trả về) | [E01](#e01), [E02](#e02), [E03](#e03) |
| <a id="login-m04"></a>`LOGIN-M04` | Đăng nhập thành công | (hệ thống chỉ có tiếng Anh) | `Welcome back, Sunny!` (tên đầu của người dùng) | [E04](#e04), [E05](#e05) |
| <a id="login-m05"></a>`LOGIN-M05` | Đăng xuất | (hệ thống chỉ có tiếng Anh) | `You have been signed out.` | [E07](#e07) |
| <a id="login-m06"></a>`LOGIN-M06` | Bấm "Forgot password?" | (hệ thống chỉ có tiếng Anh) | `Password recovery is disabled in the training environment.` | [E14](#e14), [E12](#e12) |
| <a id="login-m07"></a>`LOGIN-M07` | Đang gửi đăng nhập | (hệ thống chỉ có tiếng Anh) | Chữ trên nút đổi thành `Signing in…`, nút bị khóa trong lúc chờ (chỉ thấy trong tệp giao diện, chưa thấy trên màn hình) | [E12](#e12) |

## 5. Điểm chưa rõ và câu hỏi cho team
| ID | Đã thấy | Vì sao chưa rõ | Câu hỏi | Liên quan | Trạng thái |
|---|---|---|---|---|---|
| <a id="login-q01"></a>`LOGIN-Q01` | Ba lần sai liên tiếp vẫn không bị chặn | Dừng ở 3 lần theo dặn của người test để khỏi khóa hệ thống | Có giới hạn đăng nhập sai không? Bao nhiêu lần, chặn bao lâu, tính theo tài khoản hay theo địa chỉ? | `LOGIN-S02-AC04` | mở |
| <a id="login-q02"></a>`LOGIN-Q02` | Tích "Remember me" cho cookie giống hệt không tích | Không thấy khác biệt | Hộp này phải làm gì (ví dụ kéo dài phiên)? | `LOGIN-S01-AC04` | mở |
| <a id="login-q03"></a>`LOGIN-Q03` | Cookie phiên có thời hạn | Chưa đo giá trị chính xác, chưa chờ hết hạn | Phiên sống bao lâu và hết hạn thì hệ thống làm gì? | `LOGIN-R03` | mở |
| <a id="login-q04"></a>`LOGIN-Q04` | Email `abc` không bị trình duyệt chặn | Chưa gửi lên máy chủ (mỗi lần gửi sai là một lần đếm) | Email sai định dạng có cần báo lỗi riêng không? | `LOGIN-S03-AC02`, `LOGIN-R01` | mở |
| <a id="login-q05"></a>`LOGIN-Q05` | Địa chỉ không tồn tại trả 200 và hiện trang đăng nhập | Không biết do thiết kế (trang một màn) hay thiếu trang 404 | Có yêu cầu trang "không tìm thấy" không? | `LOGIN-S05-AC02` | mở |
| <a id="login-q06"></a>`LOGIN-Q06` | "Forgot password?" chỉ báo đang tắt | Môi trường thử | Bản thật xử lý quên mật khẩu thế nào? | `LOGIN-S06-AC01` | mở |
| <a id="login-q07"></a>`LOGIN-Q07` | Chỉ thấy vai trò "Customer" | Chưa có tài khoản khác | Có vai trò khác (ví dụ quản trị) không, và nhìn thấy gì khác? | `LOGIN-S01-AC01` | mở |
| <a id="login-q08"></a>`LOGIN-Q08` | Email viết hoa vẫn đăng nhập được | Mới thử một ví dụ | Email có được coi là không phân biệt chữ hoa thường theo yêu cầu không? | `LOGIN-R01`, `LOGIN-S01-AC02` | mở |

## 6. Bằng chứng và chưa khám phá
### 6.1 Bằng chứng
Cột "Ngày · phiên bản · tài khoản": tất cả ngày 2026-11-20, staging, không thấy số phiên bản; tài khoản khách mẫu khi có đăng nhập.

| ID | Loại | Ngày · phiên bản · tài khoản | Thao tác đã làm | Tệp | Cách kiểm lại |
|---|---|---|---|---|---|
| <a id="e01"></a>`LOGIN-E01` | ảnh | 2026-11-20 · khách mẫu | Email đúng + mật khẩu sai | [01-sai-mat-khau.png](../../evidence/ecommerce-lite/features/dang-nhap/screenshots/01-sai-mat-khau.png) | Mở trang, nhập email của tài khoản mẫu và một mật khẩu sai, bấm Sign in |
| <a id="e02"></a>`LOGIN-E02` | ảnh | 2026-11-20 · không có tài khoản | Email không tồn tại | [02-email-khong-ton-tai.png](../../evidence/ecommerce-lite/features/dang-nhap/screenshots/02-email-khong-ton-tai.png) | Nhập email không có thật và mật khẩu bất kỳ |
| <a id="e03"></a>`LOGIN-E03` | ảnh | 2026-11-20 · khách mẫu | Mật khẩu đúng đổi hoa/thường một chữ | [03-mat-khau-doi-hoa-thuong.png](../../evidence/ecommerce-lite/features/dang-nhap/screenshots/03-mat-khau-doi-hoa-thuong.png) | Nhập mật khẩu đúng nhưng đổi một chữ cái từ hoa sang thường |
| <a id="e04"></a>`LOGIN-E04` | ảnh | 2026-11-20 · khách mẫu | Email viết hoa, nhấn Enter | [04-email-viet-hoa-enter.png](../../evidence/ecommerce-lite/features/dang-nhap/screenshots/04-email-viet-hoa-enter.png) | Nhập email viết hoa toàn bộ và mật khẩu đúng, nhấn Enter |
| <a id="e05"></a>`LOGIN-E05` | ảnh | 2026-11-20 · khách mẫu | Đăng nhập đúng | [05-dang-nhap-dung.png](../../evidence/ecommerce-lite/features/dang-nhap/screenshots/05-dang-nhap-dung.png) | Đăng nhập đúng bằng tài khoản mẫu |
| <a id="e06"></a>`LOGIN-E06` | ảnh | 2026-11-20 · khách mẫu | Tải lại trang | [06-sau-tai-lai.png](../../evidence/ecommerce-lite/features/dang-nhap/screenshots/06-sau-tai-lai.png) | Đăng nhập rồi bấm F5 |
| <a id="e07"></a>`LOGIN-E07` | ảnh | 2026-11-20 · khách mẫu | Đăng xuất | [07-sau-dang-xuat.png](../../evidence/ecommerce-lite/features/dang-nhap/screenshots/07-sau-dang-xuat.png) | Đăng nhập rồi bấm Sign out |
| <a id="e08"></a>`LOGIN-E08` | ảnh | 2026-11-20 · chưa đăng nhập | Mở `/#profile` | [08-lien-ket-sau-chua-dang-nhap.png](../../evidence/ecommerce-lite/features/dang-nhap/screenshots/08-lien-ket-sau-chua-dang-nhap.png) | Cửa sổ ẩn danh, mở địa chỉ gốc + `#profile` |
| <a id="e09"></a>`LOGIN-E09` | ảnh | 2026-11-20 · chưa đăng nhập | Mở `/khong-ton-tai` | [09-dia-chi-khong-ton-tai.png](../../evidence/ecommerce-lite/features/dang-nhap/screenshots/09-dia-chi-khong-ton-tai.png) | Cửa sổ ẩn danh, mở địa chỉ gốc + `khong-ton-tai` |
| <a id="e10"></a>`LOGIN-E10` | quan sát công cụ nhà phát triển | 2026-11-20 · chưa đăng nhập | Bấm Sign in khi để trống; email `abc` + mật khẩu trống; xem lệnh gọi mạng | không có ảnh; [nhật ký hàng 1–3](../../evidence/ecommerce-lite/features/dang-nhap/bao-cao.md) | F12 → Network, bấm Sign in khi để trống: không thấy `/api/auth/login`, chỉ `GET /api/me` → 401 |
| <a id="e11"></a>`LOGIN-E11` | quan sát công cụ nhà phát triển | 2026-11-20 · chưa đăng nhập | Đọc thuộc tính ô nhập | không có ảnh; [nhật ký hàng 4](../../evidence/ecommerce-lite/features/dang-nhap/bao-cao.md) | F12 → Elements, chọn `#email`, `#password`, `#login-form` |
| <a id="e12"></a>`LOGIN-E12` | tệp giao diện | 2026-11-20 | Đọc `/app.js` công khai | không có ảnh; [nhật ký hàng 24](../../evidence/ecommerce-lite/features/dang-nhap/bao-cao.md) | F12 → Sources → `app.js`, tìm `login-form`; tên tệp và nội dung có thể đổi theo bản |
| <a id="e13"></a>`LOGIN-E13` | quan sát công cụ nhà phát triển (script) | 2026-11-20 · khách mẫu | Script đọc mã trạng thái, tên cookie, hai tab, đăng xuất | [kham-pha-dang-nhap.py](../../evidence/ecommerce-lite/features/dang-nhap/kham-pha-dang-nhap.py); [nhật ký hàng 7–17](../../evidence/ecommerce-lite/features/dang-nhap/bao-cao.md) | F12 → Network và Application → Cookies khi làm lại từng thao tác; script cần `.env` và đã dùng hết 3 lần sai |
| <a id="e14"></a>`LOGIN-E14` | quan sát công cụ nhà phát triển | 2026-11-20 · chưa đăng nhập | Bấm "Forgot password?" | không có ảnh; [nhật ký hàng 5](../../evidence/ecommerce-lite/features/dang-nhap/bao-cao.md) | Bấm "Forgot password?", đọc thông báo tạm ở góc dưới phải (biến mất sau vài giây) |
| <a id="e15"></a>`LOGIN-E15` | ảnh | 2026-11-20 · khách mẫu | Ba lần sai liên tiếp rồi đăng nhập đúng | [01](../../evidence/ecommerce-lite/features/dang-nhap/screenshots/01-sai-mat-khau.png), [02](../../evidence/ecommerce-lite/features/dang-nhap/screenshots/02-email-khong-ton-tai.png), [03](../../evidence/ecommerce-lite/features/dang-nhap/screenshots/03-mat-khau-doi-hoa-thuong.png), [04](../../evidence/ecommerce-lite/features/dang-nhap/screenshots/04-email-viet-hoa-enter.png) | Làm lại ba tình huống sai rồi đăng nhập đúng (chỉ khi người test cho phép, vì chưa biết ngưỡng khóa) |

### 6.2 Chưa khám phá
- **Đăng nhập sai quá 3 lần, thời gian chặn:** có thể khóa hệ thống; người test dặn tối đa 3 lần. Cần câu trả lời cho `LOGIN-Q01`.
- **Hết hạn phiên:** cần chờ dài; chưa đo thời hạn cookie.
- **Vai trò khác ngoài khách:** chưa có tài khoản.
- **Nút Back sau đăng xuất:** lần thử đầu cho kết quả không có nghĩa (mở từ trang trắng).
- **Ô email rất dài, ký tự đặc biệt, email sai định dạng gửi lên máy chủ:** mỗi ca là một lần sai, đã dùng hết 3 lần.
- **Nút "Show" (hiện mật khẩu), bấm "Sign in" hai lần liên tiếp:** chưa bấm thử.
- **Đăng ký tài khoản (tab "Create account"):** ngoài phạm vi feature này.

## 7. Lịch sử thay đổi
| Ngày | Phiên bản hệ thống | Thay đổi | Lý do |
|---|---|---|---|
| 2026-11-20 | không thấy số phiên bản | Tạo SRS lần đầu: 6 story, 18 AC (S01: 4, S02: 4, S03: 2, S04: 4, S05: 3, S06: 1), 4 quy tắc, 7 thông báo, 8 câu hỏi, 15 bằng chứng | Khám phá đăng nhập lần đầu |
