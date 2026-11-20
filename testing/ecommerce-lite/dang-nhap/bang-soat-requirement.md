# Bảng phân tích requirement — Đăng nhập (Ecommerce Lite)

| | |
|---|---|
| Nguồn requirement | [dang-nhap.md](../../../srs/ecommerce-lite/dang-nhap.md) (mã `LOGIN`, tình trạng nháp viết từ nhật ký khám phá, chưa có tài liệu nghiệp vụ) |
| Ngày lập | 2026-11-20 |
| Cách làm | Tách, Xoay, Lọc (skill `phan-tich-requirement`) |
| Phạm vi | 28 đơn vị (18 tiêu chí chấp nhận, 4 quy tắc, 6 thông báo). Chỉ **functional**. Chưa viết checklist hay test case |
| Câu hỏi gửi BA | [cau-hoi-cho-ba.md](cau-hoi-cho-ba.md) |

## 1. Cách đọc
**Mỗi dòng trả lời ba câu:** (1) người dùng làm gì, (2) requirement cho biết gì hoặc chỗ nào chưa rõ, (3) cần hỏi BA câu gì.

**Cách đọc mã:** `LOGIN` là tên tính năng đăng nhập; `S01` là story số 1; `AC01` là tiêu chí số 1 của story đó; `R01` là quy tắc dữ liệu; `M01` là thông báo của hệ thống.

**Cột Trạng thái:**
- **✅ Đã rõ:** requirement trả lời đủ để biết thế nào là đúng. **Lưu ý:** SRS này viết từ việc quan sát hệ thống (chưa có tài liệu nghiệp vụ hay BA xác nhận), nên "đã rõ" nghĩa là rõ trong phạm vi hành vi đã quan sát, chưa phải xác nhận chính thức. Người dùng đã chốt (2026-11-20) hành vi đã quan sát là cơ sở để viết test case.
- **❓ + loại vấn đề:** Thiếu thông tin, Chưa rõ nghĩa, Hai chỗ nói khác nhau, Số liệu không chính xác, hoặc Trình bày không thống nhất.

**Cách xử lý câu hỏi:** có ba nhóm (🚨 Hỏi BA ngay, 📋 Hỏi BA sau, 🔍 Tự kiểm tra trên hệ thống trước). Lần phân tích này **không có câu hỏi nào** (xem mục 7).

## 2. Giải thích thuật ngữ (theo requirement)
| Thuật ngữ | Nghĩa |
|---|---|
| Customer | Vai khách hàng của cửa hàng; tài khoản `SHOPPER` là Customer |
| Use customer | Nút trên màn hình đăng nhập tự điền email và mật khẩu mẫu của tài khoản Customer |
| Sign in / Sign out | Đăng nhập / đăng xuất |
| `/api/me` | Địa chỉ hệ thống trả về người đang đăng nhập; 401 nghĩa là chưa đăng nhập |
| Cổng quản trị | Phần Dashboard, Products, Orders… dành cho Admin, Customer không được dùng |

## 3. Câu trả lời đã nhận
| Mã | Nội dung trả lời | Nguồn | Áp dụng cho | Còn lại |
|---|---|---|---|---|
| TL-01 | Dự án chưa làm kiểm định định dạng email, tác dụng của Remember me, khung tài khoản mẫu, thông báo khi Customer mở địa chỉ quản trị, tab đầu tự thoát khi đăng xuất ở tab khác: không hỏi BA, không viết test case kỳ vọng, không báo bug | Người dùng (tester) chốt, 2026-11-20, trong chat; chưa có xác nhận của BA | LOGIN-Q01 đến LOGIN-Q05 | Xem lại khi người dùng nói dự án đã làm |
| TL-02 | Dự án chưa làm giới hạn số lần đăng nhập sai, thời gian sống/hết hạn phiên, yêu cầu thời gian chờ đăng nhập: không hỏi, không test, không báo bug | Người dùng (tester) chốt, 2026-11-20, trong chat; chưa có xác nhận của BA | LOGIN-Q06 | Chưa có ngưỡng nào; không tự đặt con số |

## 4. Tổng kết
| Chỉ số | Số lượng |
|---|---|
| Đơn vị chỉ có phần ✅ | 28 |
| Đơn vị có cả ✅ và ❓ | 0 |
| Đơn vị chỉ có ❓ | 0 |
| Tổng | 28 |
| Câu hỏi: 🚨 / 📋 / 🔍 | 0 / 0 / 0 |

## 5. Bảng soát theo từng story

### Đăng nhập bằng email và mật khẩu (LOGIN-S01)

| Mã | Tình huống (người dùng làm gì) | Requirement cho biết gì, hoặc chỗ chưa rõ | Trạng thái | Câu hỏi gửi BA | Trích nguyên văn |
|---|---|---|---|---|---|
| LOGIN-S01-AC01 | Chưa đăng nhập. Mở trang chủ `/`. | Hiện màn hình đăng nhập: hai tab "Sign in" và "Create account", ô email, ô mật khẩu, "Remember me on this device", nút Sign in, nút "Show", liên kết "Forgot password?". Hệ thống kiểm phiên khi tải trang (`GET /api/me` → 401). Form có `novalidate` (trình duyệt không tự kiểm) | ✅ Đã rõ (theo quan sát) | — | “Hiện màn hình đăng nhập: hai tab "Sign in" và "Create account", ô email, ô mật khẩu, "Remember me on this device", nút Sign in, nút "Show", liên kết "Forgot password?".” |
| LOGIN-S01-AC02 | Đang ở form đăng nhập, hai ô trống. Bấm Sign in. | Dưới ô email hiện `Enter your email address.`, dưới ô mật khẩu hiện `Enter your password.`, hai ô viền đỏ. Không có yêu cầu `POST /api/auth/login` nào được gửi | ✅ Đã rõ (theo quan sát) | — | “Dưới ô email hiện `Enter your email address.`, dưới ô mật khẩu hiện `Enter your password.`, hai ô viền đỏ.” |
| LOGIN-S01-AC03 | Đang ở form, ô email có `abc`, ô mật khẩu trống. Nhấn Enter. | Ô mật khẩu báo `Enter your password.`. Không gửi yêu cầu đăng nhập. (Ô email không báo gì với `abc`: dự án chưa làm kiểm định email, không coi là yêu cầu) | ✅ Đã rõ (theo quan sát) | — | “Ô mật khẩu báo `Enter your password.`.” |
| LOGIN-S01-AC04 | Chưa đăng nhập; bấm "Use customer" để điền email `shopper@sunny.test` và mật khẩu mẫu; không đánh dấu Remember me. Bấm Sign in. | Nút đổi thành "Signing in…" vài giây rồi vào cửa hàng Sunny Store (Shop, My orders, Profile, Bag), lời chào "WELCOME, SUNNY". Mạng: `POST /api/auth/login` → 200, `GET /api/store/products` → 200, `GET /api/store/cart` → 200 | ✅ Đã rõ (theo quan sát) | — | “Nút đổi thành "Signing in…" vài giây rồi vào cửa hàng Sunny Store (Shop, My orders, Profile, Bag), lời chào "WELCOME, SUNNY".” |
| LOGIN-S01-AC05 | Đã bấm "Use customer", rồi đổi email thành `khongtontai@sunny.test` (mật khẩu giữ nguyên). Nhấn Enter. | `POST /api/auth/login` → 401. Khung đỏ dưới nút: `Email or password is incorrect.`. Ô mật khẩu giữ nguyên nội dung, ô email giữ chữ vừa nhập, vẫn ở form | ✅ Đã rõ (theo quan sát) | — | “`POST /api/auth/login` → 401.” |
| LOGIN-S01-AC06 | Email `shopper@sunny.test`, mật khẩu sai (chuỗi tester tự đặt). Nhấn Enter. | `POST /api/auth/login` → 401. Cùng khung `Email or password is incorrect.` như email không tồn tại (không cho biết email có tồn tại). Mật khẩu giữ nguyên trong ô | ✅ Đã rõ (theo quan sát) | — | “`POST /api/auth/login` → 401.” |
| LOGIN-S01-AC07 | Đã bấm "Use customer", bấm vào cuối ô mật khẩu và gõ thêm một dấu cách. Nhấn Enter. | `POST /api/auth/login` → 401, cùng thông báo `Email or password is incorrect.`: mật khẩu không bị cắt khoảng trắng | ✅ Đã rõ (theo quan sát) | — | “`POST /api/auth/login` → 401, cùng thông báo `Email or password is incorrect.`: mật khẩu không bị cắt khoảng trắng” |
| LOGIN-S01-AC08 | Chưa đăng nhập; mật khẩu mẫu đã điền. Đổi email thành `SHOPPER@SUNNY.TEST`, nhấn Enter. | Đăng nhập thành công (`POST /api/auth/login` → 200): email không phân biệt hoa thường | ✅ Đã rõ (theo quan sát) | — | “Đăng nhập thành công (`POST /api/auth/login` → 200): email không phân biệt hoa thường” |
| LOGIN-S01-AC09 | Đã bấm "Use customer". Bấm Sign in 3 lần liên tiếp rất nhanh. | Chỉ gửi **1** yêu cầu `POST /api/auth/login` (nút bị vô hiệu hóa sau lần bấm đầu, hiện "Signing in…"); đăng nhập thành công, `/api/me` → 200 | ✅ Đã rõ (theo quan sát) | — | “Chỉ gửi **1** yêu cầu `POST /api/auth/login` (nút bị vô hiệu hóa sau lần bấm đầu, hiện "Signing in…"); đăng nhập thành công, `/api/me` → 200” |
| LOGIN-S01-AC10 | Đã đăng nhập sai 3 lần liên tiếp (email không tồn tại, mật khẩu sai, mật khẩu thừa dấu cách). Bấm "Use customer", bấm Sign in. | Đăng nhập thành công (`/api/me` → 200), tài khoản chưa bị khóa. (Dự án chưa làm giới hạn nên không có ngưỡng) | ✅ Đã rõ (theo quan sát) | — | “Đăng nhập thành công (`/api/me` → 200), tài khoản chưa bị khóa.” |
| LOGIN-S01-AC11 | Vừa đăng nhập thành công bằng `SHOPPER`. Xem `GET /api/me` (F12 → Network). | 200; `user` gồm email, id, name "Sunny Shopper", role "Customer", workspaceId | ✅ Đã rõ (theo quan sát) | — | “200; `user` gồm email, id, name "Sunny Shopper", role "Customer", workspaceId” |

### Hỗ trợ khi nhập mật khẩu (LOGIN-S02)

| Mã | Tình huống (người dùng làm gì) | Requirement cho biết gì, hoặc chỗ chưa rõ | Trạng thái | Câu hỏi gửi BA | Trích nguyên văn |
|---|---|---|---|---|---|
| LOGIN-S02-AC01 | Ở form đăng nhập, ô mật khẩu đã có nội dung (do "Use customer"). Bấm "Show", rồi bấm lần nữa. | Lần 1: ô mật khẩu hiện chữ nhìn thấy được, nút đổi thành "Hide". Lần 2: ô mật khẩu ẩn lại (kiểm bằng thuộc tính `type`, không chụp ảnh vì lộ mật khẩu) | ✅ Đã rõ (theo quan sát) | — | “Lần 1: ô mật khẩu hiện chữ nhìn thấy được, nút đổi thành "Hide".” |
| LOGIN-S02-AC02 | Ở form đăng nhập. Bấm "Forgot password?". | Thông báo nhỏ góc dưới phải: `Password recovery is disabled in the training environment.`, không chuyển trang | ✅ Đã rõ (theo quan sát) | — | “Thông báo nhỏ góc dưới phải: `Password recovery is disabled in the training environment.`, không chuyển trang” |

### Giữ phiên và đăng xuất (LOGIN-S03)

| Mã | Tình huống (người dùng làm gì) | Requirement cho biết gì, hoặc chỗ chưa rõ | Trạng thái | Câu hỏi gửi BA | Trích nguyên văn |
|---|---|---|---|---|---|
| LOGIN-S03-AC01 | Đã đăng nhập, đang ở cửa hàng. Tải lại trang. | Vẫn đăng nhập: không hiện form, hiện "Loading your store…" rồi vào lại cửa hàng | ✅ Đã rõ (theo quan sát) | — | “Vẫn đăng nhập: không hiện form, hiện "Loading your store…" rồi vào lại cửa hàng” |
| LOGIN-S03-AC02 | Đã đăng nhập. Bấm Sign out (thanh cửa hàng). | Thông báo `You have been signed out.`, quay về form đăng nhập, ô email và mật khẩu trống. `POST /api/auth/logout` → 200, sau đó `GET /api/me` → 401 | ✅ Đã rõ (theo quan sát) | — | “Thông báo `You have been signed out.`, quay về form đăng nhập, ô email và mật khẩu trống. `POST /api/auth/logout` → 200, sau đó `GET /api/me` → 401” |
| LOGIN-S03-AC03 | Vừa đăng xuất. Bấm nút Back của trình duyệt; rồi mở `#profile`, `#my-orders`, `#dashboard`. | Back về địa chỉ `#profile` nhưng vẫn hiện form đăng nhập; cả ba địa chỉ đều hiện form đăng nhập. `GET /api/dashboard` và `GET /api/store/products` → 401 | ✅ Đã rõ (theo quan sát) | — | “Back về địa chỉ `#profile` nhưng vẫn hiện form đăng nhập; cả ba địa chỉ đều hiện form đăng nhập. `GET /api/dashboard` và `GET /api/store/products` → 401” |
| LOGIN-S03-AC04 | Tab 1 và tab 2 cùng đăng nhập; đã đăng xuất ở tab 2. Ở tab 1 chuyển trang (mở `#my-orders`). | Tab 1 hiện form đăng nhập, `GET /api/me` → 401. (Trước khi chuyển trang, tab 1 vẫn hiện cửa hàng: dự án chưa làm tự thoát, không coi là yêu cầu) | ✅ Đã rõ (theo quan sát) | — | “Tab 1 hiện form đăng nhập, `GET /api/me` → 401.” |

### Quyền của Customer với phần quản trị (LOGIN-S04)

| Mã | Tình huống (người dùng làm gì) | Requirement cho biết gì, hoặc chỗ chưa rõ | Trạng thái | Câu hỏi gửi BA | Trích nguyên văn |
|---|---|---|---|---|---|
| LOGIN-S04-AC01 | Đăng nhập bằng `SHOPPER` (Customer). Gọi `GET /api/dashboard`, `/api/products`, `/api/orders` (F12). | Cả ba trả 403, nội dung `{"error":"FORBIDDEN","message":"Operations portal access is required."}`. `GET /api/auth/login` cũng 403 với cùng nội dung | ✅ Đã rõ (theo quan sát) | — | “Cả ba trả 403, nội dung `{"error":"FORBIDDEN","message":"Operations portal access is required."}`. `GET /api/auth/login` cũng 403 với cùng nội dung” |

## 6. Phụ lục: quy tắc và thông báo không gắn với một tiêu chí
| Mã | Tình huống (người dùng làm gì) | Requirement cho biết gì, hoặc chỗ chưa rõ | Trạng thái | Câu hỏi gửi BA | Trích nguyên văn |
|---|---|---|---|---|---|
| LOGIN-R01 | Quy tắc cho trường Email. | Không phân biệt hoa thường; giao diện cắt khoảng trắng đầu/cuối (`trim`) trước khi gửi | ✅ Đã rõ (theo quan sát) | — | “Không phân biệt hoa thường; giao diện cắt khoảng trắng đầu/cuối (`trim`) trước khi gửi” |
| LOGIN-R02 | Quy tắc cho trường Mật khẩu. | Không bị cắt khoảng trắng: thêm dấu cách cuối thì không đăng nhập được; gửi lên máy chủ trong thân `{email, password}` | ✅ Đã rõ (theo quan sát) | — | “Không bị cắt khoảng trắng: thêm dấu cách cuối thì không đăng nhập được; gửi lên máy chủ trong thân `{email, password}`” |
| LOGIN-R03 | Quy tắc cho trường Email và mật khẩu. | Lỗi đăng nhập dùng chung một thông báo cho "email không tồn tại" và "mật khẩu sai", không cho biết ô nào sai | ✅ Đã rõ (theo quan sát) | — | “Lỗi đăng nhập dùng chung một thông báo cho "email không tồn tại" và "mật khẩu sai", không cho biết ô nào sai” |
| LOGIN-R04 | Quy tắc cho trường Email và mật khẩu. | Cả hai ô đều bắt buộc: bỏ trống thì báo ngay trên trang và không gửi yêu cầu lên máy chủ | ✅ Đã rõ (theo quan sát) | — | “Cả hai ô đều bắt buộc: bỏ trống thì báo ngay trên trang và không gửi yêu cầu lên máy chủ” |
| LOGIN-M01 | Bỏ trống ô email. | Thông báo hiện đúng chữ `Enter your email address.` | ✅ Đã rõ (theo quan sát) | — | “`Enter your email address.`” |
| LOGIN-M02 | Bỏ trống ô mật khẩu. | Thông báo hiện đúng chữ `Enter your password.` | ✅ Đã rõ (theo quan sát) | — | “`Enter your password.`” |
| LOGIN-M03 | Email hoặc mật khẩu sai. | Thông báo hiện đúng chữ `Email or password is incorrect.` | ✅ Đã rõ (theo quan sát) | — | “`Email or password is incorrect.`” |
| LOGIN-M04 | Bấm "Forgot password?". | Thông báo hiện đúng chữ `Password recovery is disabled in the training environment.` | ✅ Đã rõ (theo quan sát) | — | “`Password recovery is disabled in the training environment.`” |
| LOGIN-M05 | Đăng xuất. | Thông báo hiện đúng chữ `You have been signed out.` | ✅ Đã rõ (theo quan sát) | — | “`You have been signed out.`” |
| LOGIN-M06 | Customer gọi API quản trị (nội dung lỗi trả về). | Thông báo hiện đúng chữ `Operations portal access is required.` | ✅ Đã rõ (theo quan sát) | — | “`Operations portal access is required.`” |

## 7. Nhóm 🚨 Hỏi BA ngay
Không có câu nào. Lý do:
- Mọi tiêu chí đều có bằng chứng quan sát và hành vi rõ; không có con số nào để tính lại (không có số liệu, công thức trong requirement).
- Sáu điểm chưa rõ trong SRS ([LOGIN-Q01 đến Q06](../../../srs/ecommerce-lite/dang-nhap.md#5-điểm-chưa-rõ-và-câu-hỏi-cho-team)) đều là phần dự án chưa làm theo quyết định của người dùng (TL-01, TL-02): không hỏi BA.
- Lý do "chỉ báo đúng hoặc sai" của màn hình đăng nhập đủ để suy ra không cần test độ dài, ký tự đặc biệt của mật khẩu ở đây (thuộc phần đăng ký).
- Hệ thống cho biết email không phân biệt hoa thường và mật khẩu không bị cắt khoảng trắng: SRS ghi rõ (quy tắc R01, R02), không phải điểm mơ hồ.

## 8. Tự kiểm
- Đủ 28 đơn vị: mọi mã xuất hiện ít nhất một dòng.
- Không có câu hỏi nào.
- Trích dẫn đã so từng chuỗi với requirement bằng `kiem-tra.py` (lỗi: 0).

## 9. Lịch sử thay đổi
| Ngày | Thay đổi |
|---|---|
| 2026-11-20 | Tạo mới |
