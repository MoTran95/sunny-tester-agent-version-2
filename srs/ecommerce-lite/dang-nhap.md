# SRS — Đăng nhập (Ecommerce Lite)

*SRS (tài liệu đặc tả yêu cầu) ghi hệ thống phải làm gì ở tính năng này: mỗi tình huống một dòng có mã cố định và bằng chứng. Test case dựa vào các mã này, nên khi requirement đổi sẽ biết ngay test case nào phải sửa.*

| | |
|---|---|
| Mã feature | `LOGIN` |
| Phiên bản hệ thống đã quan sát | Không thấy số bản ở chân trang (chỉ có chữ "Sunny Commerce · Training environment"), staging https://staging-ecommerce-lite.vercel.app/ |
| Cập nhật lần cuối | 2026-11-20 |
| Tình trạng | nháp (viết từ nhật ký khám phá, chưa có tài liệu nghiệp vụ hay BA xác nhận) |
| Nhật ký khám phá gốc | [bao-cao.md](../../evidence/ecommerce-lite/features/dang-nhap/bao-cao.md) |

## 1. Mục đích, phạm vi, vai trò
- **Mục đích:** cho người dùng nhập email và mật khẩu để vào cửa hàng Sunny Store; giữ phiên khi tải lại trang; cho đăng xuất; chặn truy cập khi chưa đăng nhập.
- **Ngoài phạm vi (dự án chưa làm, người dùng chốt 2026-11-20; không hỏi BA, không viết test case kỳ vọng, không báo bug; xem lại khi dự án làm):** kiểm định định dạng email (nhập `abc` không báo lỗi), tác dụng của ô "Remember me on this device", khung tài khoản mẫu trên màn hình đăng nhập, thông báo khi Customer mở địa chỉ quản trị (hiện trang chủ cửa hàng), tab đầu tự thoát khi đăng xuất ở tab khác, giới hạn số lần đăng nhập sai, thời gian sống/hết hạn phiên, yêu cầu thời gian chờ đăng nhập. Xem mục 5.
- **Chưa thấy trên màn hình:** tab "Create account" (thuộc tính năng đăng ký), vai Admin (mục 6.2).
- **Vai trò:**

| Tài khoản | Vai trò hiển thị | Đã thử với feature này |
|---|---|---|
| `SHOPPER` (shopper@sunny.test) | Customer ("Sunny Shopper") | Có |
| Tài khoản quản trị | Admin | Chưa có tài khoản |

## 2. Điều kiện tiên quyết
- Có địa chỉ staging và tài khoản Customer (mật khẩu lưu trong `.env`, không ghi vào tài liệu).
- Trang đăng nhập hiện nút "Use customer" tự điền email và mật khẩu mẫu của tài khoản Customer; dùng nút này khi cần mật khẩu đúng.
- Đăng nhập mất vài giây (nút hiện "Signing in…"): chờ trước khi kết luận.

## 3. User story và tiêu chí chấp nhận

### `LOGIN-S01` — Đăng nhập bằng email và mật khẩu
**Là** khách hàng (Customer), **tôi muốn** đăng nhập bằng email và mật khẩu **để** vào cửa hàng mua hàng.

**Luồng:** (1) mở trang chủ khi chưa đăng nhập → (2) hiện form đăng nhập → (3) nhập email và mật khẩu, bấm Sign in hoặc nhấn Enter → (4) vào cửa hàng; rẽ nhánh: bỏ trống ô (→ `LOGIN-S01-AC02`), nhập sai (→ `LOGIN-S01-AC05`, `LOGIN-S01-AC06`).

**Cách đọc:** mỗi dòng là một tình huống test. *Bối cảnh* = tình trạng trước khi làm; *Người dùng làm* = thao tác cụ thể; *Hệ thống phản hồi* = điều đã nhìn thấy (chữ trong `…` là nguyên văn). (Giới test gọi là Given – When – Then; mỗi dòng là một "tiêu chí chấp nhận", viết tắt AC.)

| ID | Tình huống | Bối cảnh | Người dùng làm | Hệ thống phản hồi | Nhãn · Bằng chứng · Liên quan |
|---|---|---|---|---|---|
| <a id="login-s01-ac01"></a>`LOGIN-S01-AC01` | Mở trang khi chưa đăng nhập | Chưa đăng nhập | Mở trang chủ `/` | Hiện màn hình đăng nhập: hai tab "Sign in" và "Create account", ô email, ô mật khẩu, "Remember me on this device", nút Sign in, nút "Show", liên kết "Forgot password?". Hệ thống kiểm phiên khi tải trang (`GET /api/me` → 401). Form có `novalidate` (trình duyệt không tự kiểm) | đã thấy · [E01](#e01) · |
| <a id="login-s01-ac02"></a>`LOGIN-S01-AC02` | Bỏ trống cả hai ô | Đang ở form đăng nhập, hai ô trống | Bấm Sign in | Dưới ô email hiện `Enter your email address.`, dưới ô mật khẩu hiện `Enter your password.`, hai ô viền đỏ. Không có yêu cầu `POST /api/auth/login` nào được gửi | đã thấy · [E02](#e02) · `LOGIN-R04`, `LOGIN-M01`, `LOGIN-M02` |
| <a id="login-s01-ac03"></a>`LOGIN-S01-AC03` | Bỏ trống ô mật khẩu | Đang ở form, ô email có `abc`, ô mật khẩu trống | Nhấn Enter | Ô mật khẩu báo `Enter your password.`. Không gửi yêu cầu đăng nhập. (Ô email không báo gì với `abc`: dự án chưa làm kiểm định email, không coi là yêu cầu) | đã thấy · [E03](#e03) · `LOGIN-R04`, `LOGIN-M02` |
| <a id="login-s01-ac04"></a>`LOGIN-S01-AC04` | Đăng nhập thành công | Chưa đăng nhập; bấm "Use customer" để điền email `shopper@sunny.test` và mật khẩu mẫu; không đánh dấu Remember me | Bấm Sign in | Nút đổi thành "Signing in…" vài giây rồi vào cửa hàng Sunny Store (Shop, My orders, Profile, Bag), lời chào "WELCOME, SUNNY". Mạng: `POST /api/auth/login` → 200, `GET /api/store/products` → 200, `GET /api/store/cart` → 200 | đã thấy · [E06](#e06) · [Ảnh 06](../../evidence/ecommerce-lite/features/dang-nhap/screenshots/06-sau-dang-nhap-cua-hang.jpg) |
| <a id="login-s01-ac05"></a>`LOGIN-S01-AC05` | Email không tồn tại | Đã bấm "Use customer", rồi đổi email thành `khongtontai@sunny.test` (mật khẩu giữ nguyên) | Nhấn Enter | `POST /api/auth/login` → 401. Khung đỏ dưới nút: `Email or password is incorrect.`. Ô mật khẩu giữ nguyên nội dung, ô email giữ chữ vừa nhập, vẫn ở form | đã thấy · [E12](#e12) · `LOGIN-R03`, `LOGIN-M03` · [Ảnh 05](../../evidence/ecommerce-lite/features/dang-nhap/screenshots/05-email-khong-ton-tai.jpg) |
| <a id="login-s01-ac06"></a>`LOGIN-S01-AC06` | Mật khẩu sai | Email `shopper@sunny.test`, mật khẩu sai (chuỗi tester tự đặt) | Nhấn Enter | `POST /api/auth/login` → 401. Cùng khung `Email or password is incorrect.` như email không tồn tại (không cho biết email có tồn tại). Mật khẩu giữ nguyên trong ô | đã thấy · [E17](#e17) · `LOGIN-R03`, `LOGIN-M03` · [Ảnh 07](../../evidence/ecommerce-lite/features/dang-nhap/screenshots/07-sai-mat-khau.jpg) |
| <a id="login-s01-ac07"></a>`LOGIN-S01-AC07` | Mật khẩu đúng nhưng thêm khoảng trắng cuối | Đã bấm "Use customer", bấm vào cuối ô mật khẩu và gõ thêm một dấu cách | Nhấn Enter | `POST /api/auth/login` → 401, cùng thông báo `Email or password is incorrect.`: mật khẩu không bị cắt khoảng trắng | đã thấy · [E18](#e18) · `LOGIN-R02`, `LOGIN-M03` |
| <a id="login-s01-ac08"></a>`LOGIN-S01-AC08` | Email viết hoa vẫn đăng nhập được | Chưa đăng nhập; mật khẩu mẫu đã điền | Đổi email thành `SHOPPER@SUNNY.TEST`, nhấn Enter | Đăng nhập thành công (`POST /api/auth/login` → 200): email không phân biệt hoa thường | đã thấy · [E13](#e13), [E16](#e16) · `LOGIN-R01` |
| <a id="login-s01-ac09"></a>`LOGIN-S01-AC09` | Bấm Sign in nhiều lần liên tiếp | Đã bấm "Use customer" | Bấm Sign in 3 lần liên tiếp rất nhanh | Chỉ gửi **1** yêu cầu `POST /api/auth/login` (nút bị vô hiệu hóa sau lần bấm đầu, hiện "Signing in…"); đăng nhập thành công, `/api/me` → 200 | đã thấy · [E20](#e20) · |
| <a id="login-s01-ac10"></a>`LOGIN-S01-AC10` | Đăng nhập đúng sau vài lần sai | Đã đăng nhập sai 3 lần liên tiếp (email không tồn tại, mật khẩu sai, mật khẩu thừa dấu cách) | Bấm "Use customer", bấm Sign in | Đăng nhập thành công (`/api/me` → 200), tài khoản chưa bị khóa. (Dự án chưa làm giới hạn nên không có ngưỡng) | đã thấy · [E19](#e19) · `LOGIN-S01-AC05`–`AC07` |
| <a id="login-s01-ac11"></a>`LOGIN-S01-AC11` | Hệ thống biết ai đang đăng nhập | Vừa đăng nhập thành công bằng `SHOPPER` | Xem `GET /api/me` (F12 → Network) | 200; `user` gồm email, id, name "Sunny Shopper", role "Customer", workspaceId | đã thấy · [E07](#e07) · |

### `LOGIN-S02` — Hỗ trợ khi nhập mật khẩu
**Là** khách hàng, **tôi muốn** xem lại mật khẩu đang gõ và có lối "quên mật khẩu" **để** đăng nhập chính xác.

| ID | Tình huống | Bối cảnh | Người dùng làm | Hệ thống phản hồi | Nhãn · Bằng chứng · Liên quan |
|---|---|---|---|---|---|
| <a id="login-s02-ac01"></a>`LOGIN-S02-AC01` | Hiện và ẩn mật khẩu | Ở form đăng nhập, ô mật khẩu đã có nội dung (do "Use customer") | Bấm "Show", rồi bấm lần nữa | Lần 1: ô mật khẩu hiện chữ nhìn thấy được, nút đổi thành "Hide". Lần 2: ô mật khẩu ẩn lại (kiểm bằng thuộc tính `type`, không chụp ảnh vì lộ mật khẩu) | đã thấy · [E05](#e05) · |
| <a id="login-s02-ac02"></a>`LOGIN-S02-AC02` | Bấm "Forgot password?" | Ở form đăng nhập | Bấm "Forgot password?" | Thông báo nhỏ góc dưới phải: `Password recovery is disabled in the training environment.`, không chuyển trang | đã thấy · [E04](#e04) · `LOGIN-M04` · [Ảnh 04](../../evidence/ecommerce-lite/features/dang-nhap/screenshots/04-quen-mat-khau.jpg) |

### `LOGIN-S03` — Giữ phiên và đăng xuất
**Là** khách hàng, **tôi muốn** vẫn đăng nhập khi tải lại trang và thoát được khi cần **để** dùng thuận tiện mà vẫn kiểm soát tài khoản.

| ID | Tình huống | Bối cảnh | Người dùng làm | Hệ thống phản hồi | Nhãn · Bằng chứng · Liên quan |
|---|---|---|---|---|---|
| <a id="login-s03-ac01"></a>`LOGIN-S03-AC01` | Tải lại trang khi đã đăng nhập | Đã đăng nhập, đang ở cửa hàng | Tải lại trang | Vẫn đăng nhập: không hiện form, hiện "Loading your store…" rồi vào lại cửa hàng | đã thấy · [E08](#e08) · |
| <a id="login-s03-ac02"></a>`LOGIN-S03-AC02` | Đăng xuất | Đã đăng nhập | Bấm Sign out (thanh cửa hàng) | Thông báo `You have been signed out.`, quay về form đăng nhập, ô email và mật khẩu trống. `POST /api/auth/logout` → 200, sau đó `GET /api/me` → 401 | đã thấy · [E11](#e11) · `LOGIN-M05` |
| <a id="login-s03-ac03"></a>`LOGIN-S03-AC03` | Truy cập địa chỉ trong ứng dụng sau khi đăng xuất | Vừa đăng xuất | Bấm nút Back của trình duyệt; rồi mở `#profile`, `#my-orders`, `#dashboard` | Back về địa chỉ `#profile` nhưng vẫn hiện form đăng nhập; cả ba địa chỉ đều hiện form đăng nhập. `GET /api/dashboard` và `GET /api/store/products` → 401 | đã thấy · [E14](#e14) · |
| <a id="login-s03-ac04"></a>`LOGIN-S03-AC04` | Đăng xuất ở tab khác | Tab 1 và tab 2 cùng đăng nhập; đã đăng xuất ở tab 2 | Ở tab 1 chuyển trang (mở `#my-orders`) | Tab 1 hiện form đăng nhập, `GET /api/me` → 401. (Trước khi chuyển trang, tab 1 vẫn hiện cửa hàng: dự án chưa làm tự thoát, không coi là yêu cầu) | đã thấy · [E15](#e15) · |

### `LOGIN-S04` — Quyền của Customer với phần quản trị
**Là** hệ thống, **tôi muốn** không cho Customer dùng chức năng quản trị **để** tách cửa hàng và vận hành.

| ID | Tình huống | Bối cảnh | Người dùng làm | Hệ thống phản hồi | Nhãn · Bằng chứng · Liên quan |
|---|---|---|---|---|---|
| <a id="login-s04-ac01"></a>`LOGIN-S04-AC01` | Customer gọi API quản trị | Đăng nhập bằng `SHOPPER` (Customer) | Gọi `GET /api/dashboard`, `/api/products`, `/api/orders` (F12) | Cả ba trả 403, nội dung `{"error":"FORBIDDEN","message":"Operations portal access is required."}`. `GET /api/auth/login` cũng 403 với cùng nội dung | đã thấy · [E10](#e10) · `LOGIN-M06` |

## 4. Bảng tra cứu
### 4.1 Quy tắc dữ liệu
| ID | Trường | Quy tắc quan sát được | Nhãn | Bằng chứng |
|---|---|---|---|---|
| <a id="login-r01"></a>`LOGIN-R01` | Email | Không phân biệt hoa thường; giao diện cắt khoảng trắng đầu/cuối (`trim`) trước khi gửi | đã thấy | [E13](#e13), [E16](#e16) |
| <a id="login-r02"></a>`LOGIN-R02` | Mật khẩu | Không bị cắt khoảng trắng: thêm dấu cách cuối thì không đăng nhập được; gửi lên máy chủ trong thân `{email, password}` | đã thấy | [E16](#e16), [E18](#e18) |
| <a id="login-r03"></a>`LOGIN-R03` | Email và mật khẩu | Lỗi đăng nhập dùng chung một thông báo cho "email không tồn tại" và "mật khẩu sai", không cho biết ô nào sai | đã thấy | [E12](#e12), [E17](#e17) |
| <a id="login-r04"></a>`LOGIN-R04` | Email và mật khẩu | Cả hai ô đều bắt buộc: bỏ trống thì báo ngay trên trang và không gửi yêu cầu lên máy chủ | đã thấy | [E02](#e02), [E03](#e03) |

### 4.2 Thông báo hệ thống (nguyên văn)
| ID | Khi nào | Tiếng Việt | English | Bằng chứng |
|---|---|---|---|---|
| <a id="login-m01"></a>`LOGIN-M01` | Bỏ trống ô email | (chưa có bản tiếng Việt, giao diện chỉ có tiếng Anh) | `Enter your email address.` | [E02](#e02) |
| <a id="login-m02"></a>`LOGIN-M02` | Bỏ trống ô mật khẩu | — | `Enter your password.` | [E02](#e02), [E03](#e03) |
| <a id="login-m03"></a>`LOGIN-M03` | Email hoặc mật khẩu sai | — | `Email or password is incorrect.` | [E12](#e12), [E17](#e17), [E18](#e18) |
| <a id="login-m04"></a>`LOGIN-M04` | Bấm "Forgot password?" | — | `Password recovery is disabled in the training environment.` | [E04](#e04) |
| <a id="login-m05"></a>`LOGIN-M05` | Đăng xuất | — | `You have been signed out.` | [E11](#e11) |
| <a id="login-m06"></a>`LOGIN-M06` | Customer gọi API quản trị (nội dung lỗi trả về) | — | `Operations portal access is required.` | [E10](#e10) |

## 5. Điểm chưa rõ và câu hỏi cho team
Người dùng chốt 2026-11-20: dự án chưa làm các điểm dưới đây nên **không hỏi BA, không viết test case kỳ vọng, không báo bug**; xem lại khi người dùng nói dự án đã làm.

| ID | Đã thấy | Vì sao chưa rõ | Câu hỏi | Liên quan | Trạng thái |
|---|---|---|---|---|---|
| <a id="login-q01"></a>`LOGIN-Q01` | Nhập `abc` ở ô email không báo lỗi định dạng ([E03](#e03)) | Chưa có yêu cầu về định dạng email | Có cần báo lỗi định dạng email không? | `LOGIN-S01-AC03` | bỏ qua, dự án chưa làm |
| <a id="login-q02"></a>`LOGIN-Q02` | "Remember me on this device" không có tác dụng thấy được; mã giao diện không dùng ([E16](#e16)) | Không rõ là thiết kế hay chưa làm | Remember me có tác dụng gì? | `LOGIN-S01-AC04` | bỏ qua, dự án chưa làm |
| <a id="login-q03"></a>`LOGIN-Q03` | Khung "Customer training login" hiện sẵn email và mật khẩu mẫu ([E01](#e01)) | Không rõ có giữ ở môi trường thật | Khung tài khoản mẫu có giữ không? | `LOGIN-S01-AC01` | bỏ qua, dự án chưa làm |
| <a id="login-q04"></a>`LOGIN-Q04` | Customer mở `#dashboard`, `#products`, `#api-lab` thì hiện trang chủ cửa hàng, không báo thiếu quyền ([E09](#e09)) | Không rõ có đúng ý | Có cần báo "không đủ quyền" không? | `LOGIN-S04-AC01` | bỏ qua, dự án chưa làm |
| <a id="login-q05"></a>`LOGIN-Q05` | Đăng xuất ở tab khác, tab đầu chỉ biết khi chuyển trang ([E15](#e15)) | Không rõ có cần tự thoát ngay | Có cần tự thoát ngay ở mọi tab không? | `LOGIN-S03-AC04` | bỏ qua, dự án chưa làm |
| <a id="login-q06"></a>`LOGIN-Q06` | Đã gửi 3 lần sai, chưa thấy khóa ([E19](#e19)); phiên đăng nhập mất vài giây ([E06](#e06)) | Chưa có số lần sai tối đa, thời gian sống phiên, thời gian chờ | Giới hạn lần sai, hạn phiên, thời gian phản hồi là bao nhiêu? | `LOGIN-S01-AC10` | bỏ qua, dự án chưa làm |

## 6. Bằng chứng và chưa khám phá
### 6.1 Bằng chứng
Mỗi bằng chứng là một hàng của [nhật ký khám phá](../../evidence/ecommerce-lite/features/dang-nhap/bao-cao.md) (mục 1, cột "#"). Tài khoản `SHOPPER`, ngày 2026-11-20, khung nhìn 1280×800. "Quan sát công cụ" = F12, không có ảnh.

| ID | Loại | Ngày · phiên bản · tài khoản | Thao tác đã làm | Tệp | Cách kiểm lại |
|---|---|---|---|---|---|
| <a id="e01"></a>`LOGIN-E01` | ảnh | 2026-11-20 · không rõ số bản · chưa đăng nhập | Mở `/` khi chưa đăng nhập | [Ảnh 01](../../evidence/ecommerce-lite/features/dang-nhap/screenshots/01-man-hinh-dang-nhap.jpg), nhật ký hàng 1 | Mở `/` ở cửa sổ ẩn danh; F12 → Network → `/api/me` |
| <a id="e02"></a>`LOGIN-E02` | ảnh | cùng | Bỏ trống hai ô, bấm Sign in | [Ảnh 02](../../evidence/ecommerce-lite/features/dang-nhap/screenshots/02-bo-trong-hai-o.jpg), hàng 2 | Làm lại; F12 → Network không có `login` |
| <a id="e03"></a>`LOGIN-E03` | ảnh | cùng | Email `abc`, bỏ trống mật khẩu, Enter | [Ảnh 03](../../evidence/ecommerce-lite/features/dang-nhap/screenshots/03-email-abc-bo-trong-mat-khau.jpg), hàng 3 | Làm lại |
| <a id="e04"></a>`LOGIN-E04` | ảnh | cùng | Bấm "Forgot password?" | [Ảnh 04](../../evidence/ecommerce-lite/features/dang-nhap/screenshots/04-quen-mat-khau.jpg), hàng 4 | Làm lại |
| <a id="e05"></a>`LOGIN-E05` | quan sát công cụ nhà phát triển | cùng | "Use customer", rồi "Show" / "Hide" | [Nhật ký hàng 5](../../evidence/ecommerce-lite/features/dang-nhap/bao-cao.md) (không có ảnh vì lộ mật khẩu) | F12 → Elements, thuộc tính `type` của ô mật khẩu |
| <a id="e06"></a>`LOGIN-E06` | ảnh | cùng | Đăng nhập bằng tài khoản mẫu | [Ảnh 06](../../evidence/ecommerce-lite/features/dang-nhap/screenshots/06-sau-dang-nhap-cua-hang.jpg), hàng 6 | Làm lại; F12 → Network |
| <a id="e07"></a>`LOGIN-E07` | quan sát công cụ nhà phát triển | cùng | Đọc `GET /api/me` sau đăng nhập | [Nhật ký hàng 7](../../evidence/ecommerce-lite/features/dang-nhap/bao-cao.md) | F12 → Network → `/api/me` |
| <a id="e08"></a>`LOGIN-E08` | quan sát | cùng | Tải lại trang khi đã đăng nhập | [Nhật ký hàng 8](../../evidence/ecommerce-lite/features/dang-nhap/bao-cao.md) | Làm lại |
| <a id="e09"></a>`LOGIN-E09` | quan sát | cùng | Đổi địa chỉ thành `#dashboard`, `#products`, `#api-lab`, `#khong-ton-tai`, `#profile` | [Nhật ký hàng 9](../../evidence/ecommerce-lite/features/dang-nhap/bao-cao.md) | Làm lại |
| <a id="e10"></a>`LOGIN-E10` | quan sát công cụ nhà phát triển | cùng | Gọi API quản trị khi là Customer | [Nhật ký hàng 10](../../evidence/ecommerce-lite/features/dang-nhap/bao-cao.md) | F12 → Network / Console gọi `fetch('/api/dashboard')` |
| <a id="e11"></a>`LOGIN-E11` | quan sát | cùng | Bấm Sign out | [Nhật ký hàng 11](../../evidence/ecommerce-lite/features/dang-nhap/bao-cao.md) | Làm lại; F12 → Network → `logout` |
| <a id="e12"></a>`LOGIN-E12` | ảnh | cùng | "Use customer", đổi email thành `khongtontai@sunny.test`, Enter | [Ảnh 05](../../evidence/ecommerce-lite/features/dang-nhap/screenshots/05-email-khong-ton-tai.jpg), hàng 12 | Làm lại; F12 → Network |
| <a id="e13"></a>`LOGIN-E13` | quan sát | cùng | Email `SHOPPER@SUNNY.TEST` + mật khẩu mẫu, Enter | [Nhật ký hàng 13](../../evidence/ecommerce-lite/features/dang-nhap/bao-cao.md) | Làm lại |
| <a id="e14"></a>`LOGIN-E14` | quan sát | cùng | Sau đăng xuất: Back, mở `#profile`, `#my-orders`, `#dashboard` | [Nhật ký hàng 14](../../evidence/ecommerce-lite/features/dang-nhap/bao-cao.md) | Làm lại |
| <a id="e15"></a>`LOGIN-E15` | quan sát | cùng | Hai tab, đăng xuất ở tab 2, chuyển trang ở tab 1 | [Nhật ký hàng 15](../../evidence/ecommerce-lite/features/dang-nhap/bao-cao.md) | Làm lại với hai tab cùng trình duyệt |
| <a id="e16"></a>`LOGIN-E16` | tệp giao diện | cùng | Đọc `/app.js` (chỉ đọc) | [Nhật ký hàng 16](../../evidence/ecommerce-lite/features/dang-nhap/bao-cao.md) | Mở `/app.js`, tìm hàm gửi form đăng nhập |
| <a id="e17"></a>`LOGIN-E17` | ảnh | cùng | Email đúng, mật khẩu sai, Enter | [Ảnh 07](../../evidence/ecommerce-lite/features/dang-nhap/screenshots/07-sai-mat-khau.jpg), hàng 17 | Làm lại |
| <a id="e18"></a>`LOGIN-E18` | quan sát công cụ nhà phát triển | cùng | Mật khẩu mẫu thêm dấu cách cuối, Enter | [Nhật ký hàng 18](../../evidence/ecommerce-lite/features/dang-nhap/bao-cao.md) | F12 → Network |
| <a id="e19"></a>`LOGIN-E19` | quan sát | cùng | Sau 3 lần sai, đăng nhập đúng | [Nhật ký hàng 19](../../evidence/ecommerce-lite/features/dang-nhap/bao-cao.md) | Làm lại |
| <a id="e20"></a>`LOGIN-E20` | quan sát công cụ nhà phát triển | cùng | Bấm Sign in 3 lần nhanh | [Nhật ký hàng 20](../../evidence/ecommerce-lite/features/dang-nhap/bao-cao.md) | F12 → Network, đếm `login` |

### 6.2 Chưa khám phá
- **Giới hạn số lần đăng nhập sai, hết hạn phiên:** dự án chưa làm (người dùng chốt 2026-11-20); đã gửi 3 lần sai, không thấy khóa.
- **Email/mật khẩu rất dài, ký tự đặc biệt:** gửi lên máy chủ tính là lần sai; không thử thêm khi chưa có ngưỡng.
- **Vai Admin (cổng quản trị):** thiếu tài khoản.
- **Tab "Create account":** thuộc tính năng đăng ký, cần tạo dữ liệu thật.
- **Cookie phiên có đổi theo "Remember me":** cookie không đọc được từ trang.

## 7. Lịch sử thay đổi
| Ngày | Phiên bản hệ thống | Thay đổi | Lý do |
|---|---|---|---|
| 2026-11-20 | không rõ số bản | Tạo mới từ nhật ký khám phá: 4 story, 18 tiêu chí chấp nhận (AC), 4 quy tắc, 6 thông báo, 6 câu hỏi (đều bỏ qua), 20 bằng chứng | Có mã cố định để phân tích requirement và viết test case |
