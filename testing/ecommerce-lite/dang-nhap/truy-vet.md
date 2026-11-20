# Truy vết — Đăng nhập

*File này do `scripts/truy-vet.py` tự sinh, đừng sửa tay. Muốn đổi thì sửa nguồn rồi chạy lại script.*

| | |
|---|---|
| Lần chạy gần nhất | 2026-11-20 16:56:12 (+07:00) (chốt mốc mới) |
| Requirement | srs/ecommerce-lite/dang-nhap.md (cập nhật 2026-11-20); bảng soát (cập nhật ?), câu trả lời đến TL-02 |
| Test case (đã gồm checklist) | [test-case.md](test-case.md) |
| Mốc đã chốt | 2026-11-20 16:56:12 (+07:00) (khi đó: SRS 2026-11-20, bảng soát ?, TL đến TL-02) |

## 1. Tóm tắt
- Mã requirement: 28 trong SRS, 2 câu trả lời (TL). Test case: 19.
- Trạng thái test case: Còn đúng 19
- Mã requirement đã đổi so với mốc đã chốt: không có; mã mới: không có.
- Mã SRS chưa có test case nào: không có.
- Test case đã bỏ khỏi file: không có.
- Vấn đề khác: không có

## 2. Khi requirement đổi, làm gì
1. Sửa SRS hoặc ghi câu trả lời mới của BA vào bảng soát (như mọi lần).
2. Chạy `python -X utf8 scripts/truy-vet.py kiem ecommerce-lite dang-nhap`. Script liệt kê mã đã đổi và các test case chuyển sang **Cần xem lại**.
3. Mở từng test case đó (bảng 6 dưới đây), sửa test case cho khớp (checklist nằm chung bảng).
4. Chạy `python -X utf8 scripts/truy-vet.py chot ecommerce-lite dang-nhap -m "đã làm gì, vì sao"`. Script ghi một dòng lịch sử và chốt mốc mới.
5. Muốn xem từng chữ đã đổi, dùng lịch sử git (commit sau mỗi lần chốt).

## 3. Bảng tra mã
Mã trong cột Nguồn của checklist và test case bỏ tiền tố `LOGIN-`. `S01-AC02` là story 1, tình huống 2; `R` là quy tắc; `M` là thông báo; `TL` là câu trả lời của BA.

| Mã | Tên ngắn | Nguyên văn (rút gọn) | Mở ở đâu |
|---|---|---|---|
| M01 | Bỏ trống ô email | (chưa có bản tiếng Việt, giao diện chỉ có tiếng Anh) | [dang-nhap.md dòng 89](../../../srs/ecommerce-lite/dang-nhap.md#L89) |
| M02 | Bỏ trống ô mật khẩu | — | [dang-nhap.md dòng 90](../../../srs/ecommerce-lite/dang-nhap.md#L90) |
| M03 | Email hoặc mật khẩu sai | — | [dang-nhap.md dòng 91](../../../srs/ecommerce-lite/dang-nhap.md#L91) |
| M04 | Bấm "Forgot password?" | — | [dang-nhap.md dòng 92](../../../srs/ecommerce-lite/dang-nhap.md#L92) |
| M05 | Đăng xuất | — | [dang-nhap.md dòng 93](../../../srs/ecommerce-lite/dang-nhap.md#L93) |
| M06 | Customer gọi API quản trị (nội dung lỗi… | — | [dang-nhap.md dòng 94](../../../srs/ecommerce-lite/dang-nhap.md#L94) |
| R01 | Email | Không phân biệt hoa thường; giao diện cắt khoảng trắng đầu/cuối (`trim`) trước khi gửi | [dang-nhap.md dòng 81](../../../srs/ecommerce-lite/dang-nhap.md#L81) |
| R02 | Mật khẩu | Không bị cắt khoảng trắng: thêm dấu cách cuối thì không đăng nhập được; gửi lên máy chủ trong thân `{email, password}` | [dang-nhap.md dòng 82](../../../srs/ecommerce-lite/dang-nhap.md#L82) |
| R03 | Email và mật khẩu | Lỗi đăng nhập dùng chung một thông báo cho "email không tồn tại" và "mật khẩu sai", không cho biết ô nào sai | [dang-nhap.md dòng 83](../../../srs/ecommerce-lite/dang-nhap.md#L83) |
| R04 | Email và mật khẩu | Cả hai ô đều bắt buộc: bỏ trống thì báo ngay trên trang và không gửi yêu cầu lên máy chủ | [dang-nhap.md dòng 84](../../../srs/ecommerce-lite/dang-nhap.md#L84) |
| S01-AC01 | Mở trang khi chưa đăng nhập | Hiện màn hình đăng nhập: hai tab "Sign in" và "Create account", ô email, ô mật khẩu, "Remember me on this device", nút Sign in, nút "Show", liên kết… | [dang-nhap.md dòng 40](../../../srs/ecommerce-lite/dang-nhap.md#L40) |
| S01-AC02 | Bỏ trống cả hai ô | Dưới ô email hiện `Enter your email address.`, dưới ô mật khẩu hiện `Enter your password.`, hai ô viền đỏ. Không có yêu cầu `POST /api/auth/login` nà… | [dang-nhap.md dòng 41](../../../srs/ecommerce-lite/dang-nhap.md#L41) |
| S01-AC03 | Bỏ trống ô mật khẩu | Ô mật khẩu báo `Enter your password.`. Không gửi yêu cầu đăng nhập. (Ô email không báo gì với `abc`: dự án chưa làm kiểm định email, không coi là yêu… | [dang-nhap.md dòng 42](../../../srs/ecommerce-lite/dang-nhap.md#L42) |
| S01-AC04 | Đăng nhập thành công | Nút đổi thành "Signing in…" vài giây rồi vào cửa hàng Sunny Store (Shop, My orders, Profile, Bag), lời chào "WELCOME, SUNNY". Mạng: `POST /api/auth/l… | [dang-nhap.md dòng 43](../../../srs/ecommerce-lite/dang-nhap.md#L43) |
| S01-AC05 | Email không tồn tại | `POST /api/auth/login` → 401. Khung đỏ dưới nút: `Email or password is incorrect.`. Ô mật khẩu giữ nguyên nội dung, ô email giữ chữ vừa nhập, vẫn ở f… | [dang-nhap.md dòng 44](../../../srs/ecommerce-lite/dang-nhap.md#L44) |
| S01-AC06 | Mật khẩu sai | `POST /api/auth/login` → 401. Cùng khung `Email or password is incorrect.` như email không tồn tại (không cho biết email có tồn tại). Mật khẩu giữ ng… | [dang-nhap.md dòng 45](../../../srs/ecommerce-lite/dang-nhap.md#L45) |
| S01-AC07 | Mật khẩu đúng nhưng thêm khoảng trắng c… | `POST /api/auth/login` → 401, cùng thông báo `Email or password is incorrect.`: mật khẩu không bị cắt khoảng trắng | [dang-nhap.md dòng 46](../../../srs/ecommerce-lite/dang-nhap.md#L46) |
| S01-AC08 | Email viết hoa vẫn đăng nhập được | Đăng nhập thành công (`POST /api/auth/login` → 200): email không phân biệt hoa thường | [dang-nhap.md dòng 47](../../../srs/ecommerce-lite/dang-nhap.md#L47) |
| S01-AC09 | Bấm Sign in nhiều lần liên tiếp | Chỉ gửi **1** yêu cầu `POST /api/auth/login` (nút bị vô hiệu hóa sau lần bấm đầu, hiện "Signing in…"); đăng nhập thành công, `/api/me` → 200 | [dang-nhap.md dòng 48](../../../srs/ecommerce-lite/dang-nhap.md#L48) |
| S01-AC10 | Đăng nhập đúng sau vài lần sai | Đăng nhập thành công (`/api/me` → 200), tài khoản chưa bị khóa. (Dự án chưa làm giới hạn nên không có ngưỡng) | [dang-nhap.md dòng 49](../../../srs/ecommerce-lite/dang-nhap.md#L49) |
| S01-AC11 | Hệ thống biết ai đang đăng nhập | 200; `user` gồm email, id, name "Sunny Shopper", role "Customer", workspaceId | [dang-nhap.md dòng 50](../../../srs/ecommerce-lite/dang-nhap.md#L50) |
| S02-AC01 | Hiện và ẩn mật khẩu | Lần 1: ô mật khẩu hiện chữ nhìn thấy được, nút đổi thành "Hide". Lần 2: ô mật khẩu ẩn lại (kiểm bằng thuộc tính `type`, không chụp ảnh vì lộ mật khẩu) | [dang-nhap.md dòng 57](../../../srs/ecommerce-lite/dang-nhap.md#L57) |
| S02-AC02 | Bấm "Forgot password?" | Thông báo nhỏ góc dưới phải: `Password recovery is disabled in the training environment.`, không chuyển trang | [dang-nhap.md dòng 58](../../../srs/ecommerce-lite/dang-nhap.md#L58) |
| S03-AC01 | Tải lại trang khi đã đăng nhập | Vẫn đăng nhập: không hiện form, hiện "Loading your store…" rồi vào lại cửa hàng | [dang-nhap.md dòng 65](../../../srs/ecommerce-lite/dang-nhap.md#L65) |
| S03-AC02 | Đăng xuất | Thông báo `You have been signed out.`, quay về form đăng nhập, ô email và mật khẩu trống. `POST /api/auth/logout` → 200, sau đó `GET /api/me` → 401 | [dang-nhap.md dòng 66](../../../srs/ecommerce-lite/dang-nhap.md#L66) |
| S03-AC03 | Truy cập địa chỉ trong ứng dụng sau khi… | Back về địa chỉ `#profile` nhưng vẫn hiện form đăng nhập; cả ba địa chỉ đều hiện form đăng nhập. `GET /api/dashboard` và `GET /api/store/products` →… | [dang-nhap.md dòng 67](../../../srs/ecommerce-lite/dang-nhap.md#L67) |
| S03-AC04 | Đăng xuất ở tab khác | Tab 1 hiện form đăng nhập, `GET /api/me` → 401. (Trước khi chuyển trang, tab 1 vẫn hiện cửa hàng: dự án chưa làm tự thoát, không coi là yêu cầu) | [dang-nhap.md dòng 68](../../../srs/ecommerce-lite/dang-nhap.md#L68) |
| S04-AC01 | Customer gọi API quản trị | Cả ba trả 403, nội dung `{"error":"FORBIDDEN","message":"Operations portal access is required."}`. `GET /api/auth/login` cũng 403 với cùng nội dung | [dang-nhap.md dòng 75](../../../srs/ecommerce-lite/dang-nhap.md#L75) |
| TL-01 | Dự án chưa làm kiểm định định dạng emai… | Dự án chưa làm kiểm định định dạng email, tác dụng của Remember me, khung tài khoản mẫu, thông báo khi Customer mở địa chỉ quản trị, tab đầu tự thoát… | [bang-soat-requirement.md dòng 34](bang-soat-requirement.md#L34) |
| TL-02 | Dự án chưa làm giới hạn số lần đăng nhậ… | Dự án chưa làm giới hạn số lần đăng nhập sai, thời gian sống/hết hạn phiên, yêu cầu thời gian chờ đăng nhập: không hỏi, không test, không báo bug | [bang-soat-requirement.md dòng 35](bang-soat-requirement.md#L35) |

## 4. Yêu cầu theo BA của từng mã SRS
Gom từ bảng soát (mục 5, 6) để mỗi mã SRS có chỗ ghi điều BA trả lời, kể cả khi SRS (bản quan sát hệ thống 1.3.0) ghi khác. Test case viết theo cột "Theo BA"; chỗ có ⚠️ là nghi lỗi của hệ thống, chưa phải lỗi đã xác nhận. SRS không bị sửa.

| Mã | Tên ngắn | Theo BA (hoặc suy ra) | Hệ thống 1.3.0 hiện tại | Còn mở |
|---|---|---|---|---|
| [M01](../../../srs/ecommerce-lite/dang-nhap.md#L89) | Bỏ trống ô email | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [M02](../../../srs/ecommerce-lite/dang-nhap.md#L90) | Bỏ trống ô mật khẩu | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [M03](../../../srs/ecommerce-lite/dang-nhap.md#L91) | Email hoặc mật khẩu sai | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [M04](../../../srs/ecommerce-lite/dang-nhap.md#L92) | Bấm "Forgot password?" | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [M05](../../../srs/ecommerce-lite/dang-nhap.md#L93) | Đăng xuất | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [M06](../../../srs/ecommerce-lite/dang-nhap.md#L94) | Customer gọi API quản trị (nội dung lỗi… | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [R01](../../../srs/ecommerce-lite/dang-nhap.md#L81) | Email | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [R02](../../../srs/ecommerce-lite/dang-nhap.md#L82) | Mật khẩu | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [R03](../../../srs/ecommerce-lite/dang-nhap.md#L83) | Email và mật khẩu | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [R04](../../../srs/ecommerce-lite/dang-nhap.md#L84) | Email và mật khẩu | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [S01-AC01](../../../srs/ecommerce-lite/dang-nhap.md#L40) | Mở trang khi chưa đăng nhập | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [S01-AC02](../../../srs/ecommerce-lite/dang-nhap.md#L41) | Bỏ trống cả hai ô | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [S01-AC03](../../../srs/ecommerce-lite/dang-nhap.md#L42) | Bỏ trống ô mật khẩu | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [S01-AC04](../../../srs/ecommerce-lite/dang-nhap.md#L43) | Đăng nhập thành công | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [S01-AC05](../../../srs/ecommerce-lite/dang-nhap.md#L44) | Email không tồn tại | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [S01-AC06](../../../srs/ecommerce-lite/dang-nhap.md#L45) | Mật khẩu sai | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [S01-AC07](../../../srs/ecommerce-lite/dang-nhap.md#L46) | Mật khẩu đúng nhưng thêm khoảng trắng c… | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [S01-AC08](../../../srs/ecommerce-lite/dang-nhap.md#L47) | Email viết hoa vẫn đăng nhập được | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [S01-AC09](../../../srs/ecommerce-lite/dang-nhap.md#L48) | Bấm Sign in nhiều lần liên tiếp | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [S01-AC10](../../../srs/ecommerce-lite/dang-nhap.md#L49) | Đăng nhập đúng sau vài lần sai | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [S01-AC11](../../../srs/ecommerce-lite/dang-nhap.md#L50) | Hệ thống biết ai đang đăng nhập | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [S02-AC01](../../../srs/ecommerce-lite/dang-nhap.md#L57) | Hiện và ẩn mật khẩu | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [S02-AC02](../../../srs/ecommerce-lite/dang-nhap.md#L58) | Bấm "Forgot password?" | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [S03-AC01](../../../srs/ecommerce-lite/dang-nhap.md#L65) | Tải lại trang khi đã đăng nhập | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [S03-AC02](../../../srs/ecommerce-lite/dang-nhap.md#L66) | Đăng xuất | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [S03-AC03](../../../srs/ecommerce-lite/dang-nhap.md#L67) | Truy cập địa chỉ trong ứng dụng sau khi… | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [S03-AC04](../../../srs/ecommerce-lite/dang-nhap.md#L68) | Đăng xuất ở tab khác | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [S04-AC01](../../../srs/ecommerce-lite/dang-nhap.md#L75) | Customer gọi API quản trị | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |

## 5. Từ requirement tới test case
| Mã | Tên ngắn | Trạng thái requirement | Test case |
|---|---|---|---|
| [M01](../../../srs/ecommerce-lite/dang-nhap.md#L89) | Bỏ trống ô email | Không đổi | 1: [TC-005](test-case.md#tc-005) |
| [M02](../../../srs/ecommerce-lite/dang-nhap.md#L90) | Bỏ trống ô mật khẩu | Không đổi | 2: [TC-005](test-case.md#tc-005), [TC-006](test-case.md#tc-006) |
| [M03](../../../srs/ecommerce-lite/dang-nhap.md#L91) | Email hoặc mật khẩu sai | Không đổi | 4: [TC-003](test-case.md#tc-003), [TC-004](test-case.md#tc-004), [TC-011](test-case.md#tc-011), [TC-015](test-case.md#tc-015) |
| [M04](../../../srs/ecommerce-lite/dang-nhap.md#L92) | Bấm "Forgot password?" | Không đổi | 1: [TC-019](test-case.md#tc-019) |
| [M05](../../../srs/ecommerce-lite/dang-nhap.md#L93) | Đăng xuất | Không đổi | 1: [TC-008](test-case.md#tc-008) |
| [M06](../../../srs/ecommerce-lite/dang-nhap.md#L94) | Customer gọi API quản trị (nội dung lỗi… | Không đổi | 1: [TC-010](test-case.md#tc-010) |
| [R01](../../../srs/ecommerce-lite/dang-nhap.md#L81) | Email | Không đổi | 2: [TC-012](test-case.md#tc-012), [TC-013](test-case.md#tc-013) |
| [R02](../../../srs/ecommerce-lite/dang-nhap.md#L82) | Mật khẩu | Không đổi | 1: [TC-011](test-case.md#tc-011) |
| [R03](../../../srs/ecommerce-lite/dang-nhap.md#L83) | Email và mật khẩu | Không đổi | 2: [TC-003](test-case.md#tc-003), [TC-004](test-case.md#tc-004) |
| [R04](../../../srs/ecommerce-lite/dang-nhap.md#L84) | Email và mật khẩu | Không đổi | 2: [TC-005](test-case.md#tc-005), [TC-006](test-case.md#tc-006) |
| [S01-AC01](../../../srs/ecommerce-lite/dang-nhap.md#L40) | Mở trang khi chưa đăng nhập | Không đổi | 1: [TC-001](test-case.md#tc-001) |
| [S01-AC02](../../../srs/ecommerce-lite/dang-nhap.md#L41) | Bỏ trống cả hai ô | Không đổi | 1: [TC-005](test-case.md#tc-005) |
| [S01-AC03](../../../srs/ecommerce-lite/dang-nhap.md#L42) | Bỏ trống ô mật khẩu | Không đổi | 1: [TC-006](test-case.md#tc-006) |
| [S01-AC04](../../../srs/ecommerce-lite/dang-nhap.md#L43) | Đăng nhập thành công | Không đổi | 1: [TC-002](test-case.md#tc-002) |
| [S01-AC05](../../../srs/ecommerce-lite/dang-nhap.md#L44) | Email không tồn tại | Không đổi | 1: [TC-003](test-case.md#tc-003) |
| [S01-AC06](../../../srs/ecommerce-lite/dang-nhap.md#L45) | Mật khẩu sai | Không đổi | 1: [TC-004](test-case.md#tc-004) |
| [S01-AC07](../../../srs/ecommerce-lite/dang-nhap.md#L46) | Mật khẩu đúng nhưng thêm khoảng trắng c… | Không đổi | 1: [TC-011](test-case.md#tc-011) |
| [S01-AC08](../../../srs/ecommerce-lite/dang-nhap.md#L47) | Email viết hoa vẫn đăng nhập được | Không đổi | 1: [TC-012](test-case.md#tc-012) |
| [S01-AC09](../../../srs/ecommerce-lite/dang-nhap.md#L48) | Bấm Sign in nhiều lần liên tiếp | Không đổi | 1: [TC-014](test-case.md#tc-014) |
| [S01-AC10](../../../srs/ecommerce-lite/dang-nhap.md#L49) | Đăng nhập đúng sau vài lần sai | Không đổi | 1: [TC-015](test-case.md#tc-015) |
| [S01-AC11](../../../srs/ecommerce-lite/dang-nhap.md#L50) | Hệ thống biết ai đang đăng nhập | Không đổi | 1: [TC-016](test-case.md#tc-016) |
| [S02-AC01](../../../srs/ecommerce-lite/dang-nhap.md#L57) | Hiện và ẩn mật khẩu | Không đổi | 1: [TC-018](test-case.md#tc-018) |
| [S02-AC02](../../../srs/ecommerce-lite/dang-nhap.md#L58) | Bấm "Forgot password?" | Không đổi | 1: [TC-019](test-case.md#tc-019) |
| [S03-AC01](../../../srs/ecommerce-lite/dang-nhap.md#L65) | Tải lại trang khi đã đăng nhập | Không đổi | 1: [TC-007](test-case.md#tc-007) |
| [S03-AC02](../../../srs/ecommerce-lite/dang-nhap.md#L66) | Đăng xuất | Không đổi | 1: [TC-008](test-case.md#tc-008) |
| [S03-AC03](../../../srs/ecommerce-lite/dang-nhap.md#L67) | Truy cập địa chỉ trong ứng dụng sau khi… | Không đổi | 1: [TC-009](test-case.md#tc-009) |
| [S03-AC04](../../../srs/ecommerce-lite/dang-nhap.md#L68) | Đăng xuất ở tab khác | Không đổi | 1: [TC-017](test-case.md#tc-017) |
| [S04-AC01](../../../srs/ecommerce-lite/dang-nhap.md#L75) | Customer gọi API quản trị | Không đổi | 1: [TC-010](test-case.md#tc-010) |
| [TL-01](bang-soat-requirement.md#L34) | Dự án chưa làm kiểm định định dạng emai… | Không đổi | — |
| [TL-02](bang-soat-requirement.md#L35) | Dự án chưa làm giới hạn số lần đăng nhậ… | Không đổi | — |

## 6. Từ test case tới requirement
| Mã | Tình huống | Ưu tiên | Mã requirement dùng | Trạng thái | Tạo | Sửa lần cuối | Tự động hóa |
|---|---|---|---|---|---|---|---|
| [TC-001](test-case.md#tc-001) | Hiện form đăng nhập khi mở trang chủ lúc chưa đăng nhập | Cao | [S01-AC01](../../../srs/ecommerce-lite/dang-nhap.md#L40) (Mở trang khi chưa đăng nhập) | Còn đúng | 2026-11-20 | 2026-11-20 | Có: testing/ecommerce-lite/dang-nhap/auto/tc-001.py |
| [TC-002](test-case.md#tc-002) | Đăng nhập thành công và vào cửa hàng khi nhập đúng email và mật khẩu | Cao | [S01-AC04](../../../srs/ecommerce-lite/dang-nhap.md#L43) (Đăng nhập thành công) | Còn đúng | 2026-11-20 | 2026-11-20 | Có: testing/ecommerce-lite/dang-nhap/auto/tc-002.py |
| [TC-003](test-case.md#tc-003) | Hiện `Email or password is incorrect.` khi nhập email không tồn tại | Cao | [M03](../../../srs/ecommerce-lite/dang-nhap.md#L91) (Email hoặc mật khẩu sai), [R03](../../../srs/ecommerce-lite/dang-nhap.md#L83) (Email và mật khẩu), [S01-AC05](../../../srs/ecommerce-lite/dang-nhap.md#L44) (Email không tồn tại) | Còn đúng | 2026-11-20 | 2026-11-20 | Có: testing/ecommerce-lite/dang-nhap/auto/tc-003.py |
| [TC-004](test-case.md#tc-004) | Hiện `Email or password is incorrect.` khi email đúng nhưng mật khẩu sai | Cao | [M03](../../../srs/ecommerce-lite/dang-nhap.md#L91) (Email hoặc mật khẩu sai), [R03](../../../srs/ecommerce-lite/dang-nhap.md#L83) (Email và mật khẩu), [S01-AC06](../../../srs/ecommerce-lite/dang-nhap.md#L45) (Mật khẩu sai) | Còn đúng | 2026-11-20 | 2026-11-20 | Có: testing/ecommerce-lite/dang-nhap/auto/tc-004.py |
| [TC-005](test-case.md#tc-005) | Báo lỗi ở cả hai ô và không gửi yêu cầu đăng nhập khi bỏ trống email và mật khẩu | Cao | [M01](../../../srs/ecommerce-lite/dang-nhap.md#L89) (Bỏ trống ô email), [M02](../../../srs/ecommerce-lite/dang-nhap.md#L90) (Bỏ trống ô mật khẩu), [R04](../../../srs/ecommerce-lite/dang-nhap.md#L84) (Email và mật khẩu), [S01-AC02](../../../srs/ecommerce-lite/dang-nhap.md#L41) (Bỏ trống cả hai ô) | Còn đúng | 2026-11-20 | 2026-11-20 | Có: testing/ecommerce-lite/dang-nhap/auto/tc-005.py |
| [TC-006](test-case.md#tc-006) | Báo lỗi ở ô mật khẩu và không gửi yêu cầu đăng nhập khi bỏ trống mật khẩu | Cao | [M02](../../../srs/ecommerce-lite/dang-nhap.md#L90) (Bỏ trống ô mật khẩu), [R04](../../../srs/ecommerce-lite/dang-nhap.md#L84) (Email và mật khẩu), [S01-AC03](../../../srs/ecommerce-lite/dang-nhap.md#L42) (Bỏ trống ô mật khẩu) | Còn đúng | 2026-11-20 | 2026-11-20 | Có: testing/ecommerce-lite/dang-nhap/auto/tc-006.py |
| [TC-007](test-case.md#tc-007) | Vẫn đăng nhập và vào lại cửa hàng khi tải lại trang sau khi đã đăng nhập | Cao | [S03-AC01](../../../srs/ecommerce-lite/dang-nhap.md#L65) (Tải lại trang khi đã đăng nhập) | Còn đúng | 2026-11-20 | 2026-11-20 | Có: testing/ecommerce-lite/dang-nhap/auto/tc-007.py |
| [TC-008](test-case.md#tc-008) | Về form đăng nhập và báo đã đăng xuất khi bấm Sign out | Cao | [M05](../../../srs/ecommerce-lite/dang-nhap.md#L93) (Đăng xuất), [S03-AC02](../../../srs/ecommerce-lite/dang-nhap.md#L66) (Đăng xuất) | Còn đúng | 2026-11-20 | 2026-11-20 | Có: testing/ecommerce-lite/dang-nhap/auto/tc-008.py |
| [TC-009](test-case.md#tc-009) | Hiện form đăng nhập khi bấm Back hoặc mở lại địa chỉ trong ứng dụng sau khi đăng xuất | Cao | [S03-AC03](../../../srs/ecommerce-lite/dang-nhap.md#L67) (Truy cập địa chỉ trong ứng dụng sau khi…) | Còn đúng | 2026-11-20 | 2026-11-20 | Có: testing/ecommerce-lite/dang-nhap/auto/tc-009.py |
| [TC-010](test-case.md#tc-010) | Trả lỗi 403 khi Customer gọi API quản trị `/api/dashboard` | Cao | [M06](../../../srs/ecommerce-lite/dang-nhap.md#L94) (Customer gọi API quản trị (nội dung lỗi…), [S04-AC01](../../../srs/ecommerce-lite/dang-nhap.md#L75) (Customer gọi API quản trị) | Còn đúng | 2026-11-20 | 2026-11-20 | Có: testing/ecommerce-lite/dang-nhap/auto/tc-010.py |
| [TC-011](test-case.md#tc-011) | Không đăng nhập được khi mật khẩu đúng nhưng thêm một khoảng trắng ở cuối | Trung bình | [M03](../../../srs/ecommerce-lite/dang-nhap.md#L91) (Email hoặc mật khẩu sai), [R02](../../../srs/ecommerce-lite/dang-nhap.md#L82) (Mật khẩu), [S01-AC07](../../../srs/ecommerce-lite/dang-nhap.md#L46) (Mật khẩu đúng nhưng thêm khoảng trắng c…) | Còn đúng | 2026-11-20 | 2026-11-20 | Có: testing/ecommerce-lite/dang-nhap/auto/tc-011.py |
| [TC-012](test-case.md#tc-012) | Đăng nhập thành công khi nhập email viết hoa | Trung bình | [R01](../../../srs/ecommerce-lite/dang-nhap.md#L81) (Email), [S01-AC08](../../../srs/ecommerce-lite/dang-nhap.md#L47) (Email viết hoa vẫn đăng nhập được) | Còn đúng | 2026-11-20 | 2026-11-20 | Có: testing/ecommerce-lite/dang-nhap/auto/tc-012.py |
| [TC-013](test-case.md#tc-013) | Đăng nhập thành công khi email có khoảng trắng ở đầu và cuối | Trung bình | [R01](../../../srs/ecommerce-lite/dang-nhap.md#L81) (Email) | Còn đúng | 2026-11-20 | 2026-11-20 | Có: testing/ecommerce-lite/dang-nhap/auto/tc-013.py |
| [TC-014](test-case.md#tc-014) | Chỉ gửi một yêu cầu đăng nhập khi bấm Sign in nhiều lần liên tiếp rất nhanh | Trung bình | [S01-AC09](../../../srs/ecommerce-lite/dang-nhap.md#L48) (Bấm Sign in nhiều lần liên tiếp) | Còn đúng | 2026-11-20 | 2026-11-20 | Có: testing/ecommerce-lite/dang-nhap/auto/tc-014.py |
| [TC-015](test-case.md#tc-015) | Đăng nhập thành công khi nhập đúng sau 3 lần đăng nhập sai liên tiếp | Trung bình | [M03](../../../srs/ecommerce-lite/dang-nhap.md#L91) (Email hoặc mật khẩu sai), [S01-AC10](../../../srs/ecommerce-lite/dang-nhap.md#L49) (Đăng nhập đúng sau vài lần sai) | Còn đúng | 2026-11-20 | 2026-11-20 | Có: testing/ecommerce-lite/dang-nhap/auto/tc-015.py |
| [TC-016](test-case.md#tc-016) | Hệ thống trả đúng thông tin người đang đăng nhập khi xem `/api/me` sau đăng nhập | Trung bình | [S01-AC11](../../../srs/ecommerce-lite/dang-nhap.md#L50) (Hệ thống biết ai đang đăng nhập) | Còn đúng | 2026-11-20 | 2026-11-20 | Có: testing/ecommerce-lite/dang-nhap/auto/tc-016.py |
| [TC-017](test-case.md#tc-017) | Hiện form đăng nhập ở tab 1 khi chuyển trang sau khi đã đăng xuất ở tab 2 | Trung bình | [S03-AC04](../../../srs/ecommerce-lite/dang-nhap.md#L68) (Đăng xuất ở tab khác) | Còn đúng | 2026-11-20 | 2026-11-20 | Có: testing/ecommerce-lite/dang-nhap/auto/tc-017.py |
| [TC-018](test-case.md#tc-018) | Hiện mật khẩu thành chữ khi bấm Show và ẩn lại khi bấm Hide | Trung bình | [S02-AC01](../../../srs/ecommerce-lite/dang-nhap.md#L57) (Hiện và ẩn mật khẩu) | Còn đúng | 2026-11-20 | 2026-11-20 | Có: testing/ecommerce-lite/dang-nhap/auto/tc-018.py |
| [TC-019](test-case.md#tc-019) | Hiện thông báo khôi phục mật khẩu bị tắt khi bấm Forgot password? | Thấp | [M04](../../../srs/ecommerce-lite/dang-nhap.md#L92) (Bấm "Forgot password?"), [S02-AC02](../../../srs/ecommerce-lite/dang-nhap.md#L58) (Bấm "Forgot password?") | Còn đúng | 2026-11-20 | 2026-11-20 | Có: testing/ecommerce-lite/dang-nhap/auto/tc-019.py |

## 7. Lịch sử thay đổi
Ghi mỗi lần chạy `chot`. **Thời điểm chốt** là giờ máy lúc bấm chốt (kèm múi giờ), không phải giờ BA trả lời hay giờ requirement đổi; mốc cũ chỉ có ngày thì ghi "không rõ giờ". **Commit gốc** là commit đang đứng lúc chốt ("+ sửa chưa commit" nghĩa là còn thay đổi chưa commit); muốn xem từng chữ đã đổi, dùng git. **Ngày BA trả lời** chỉ ghi khi biết.

| Thời điểm chốt (giờ máy) | Commit gốc | Ngày BA trả lời | Đối tượng | Nội dung | Dựa trên | Mã requirement đổi | Test case mới / sửa / bỏ |
|---|---|---|---|---|---|---|---|
| 2026-11-20 11:28:37 (+07:00) | `29192bc` + sửa chưa commit | — | checklist, test-case | Lập test case đầu tiên từ SRS LOGIN (19 TC) | SRS 2026-11-20; bảng soát ?; TL đến TL-02 | M01 (mới), M02 (mới), M03 (mới), M04 (mới), M05 (mới), M06 (mới), R01 (mới), R02 (mới), R03 (mới), R04 (mới), S01-AC01 (mới), S01-AC02 (mới), S01-AC03 (mới), S01-AC04 (mới), S01-AC05 (mới), S01-AC06 (mới), S01-AC07 (mới), S01-AC08 (mới), S01-AC09 (mới), S01-AC10 (mới), S01-AC11 (mới), S02-AC01 (mới), S02-AC02 (mới), S03-AC01 (mới), S03-AC02 (mới), S03-AC03 (mới), S03-AC04 (mới), S04-AC01 (mới), TL-01 (mới), TL-02 (mới) | mới 19; sửa 0; bỏ 0 |
| 2026-11-20 11:51:05 (+07:00) | `29192bc` + sửa chưa commit | — | checklist, test-case | Ghi kết quả chạy script lượt smoke 2 và cột Tự động hóa | SRS 2026-11-20; bảng soát ?; TL đến TL-02 | — | mới 0; sửa 0; bỏ 0 |
| 2026-11-20 11:58:01 (+07:00) | `29192bc` + sửa chưa commit | — | checklist, test-case | Ghi kết quả lượt smoke 4 | SRS 2026-11-20; bảng soát ?; TL đến TL-02 | — | mới 0; sửa 0; bỏ 0 |
| 2026-11-20 12:04:48 (+07:00) | `29192bc` + sửa chưa commit | — | checklist, test-case | Ghi kết quả test sâu 14 case | SRS 2026-11-20; bảng soát ?; TL đến TL-02 | — | mới 0; sửa 0; bỏ 0 |
| 2026-11-20 16:56:12 (+07:00) | `29192bc` + sửa chưa commit | — | checklist, test-case | TC-013: bỏ cờ chưa thử vì đã xác nhận trên hệ thống | SRS 2026-11-20; bảng soát ?; TL đến TL-02 | — | mới 0; sửa TC-013; bỏ 0 |
