# Đăng nhập — nhật ký khám phá

Ngày: 2026-11-20 · Hệ thống: https://staging-ecommerce-lite.vercel.app/ · Phiên bản: không thấy số bản ở chân trang (chỉ có chữ "Sunny Commerce · Training environment")
Khung nhìn: 1280×800. Ảnh: `screenshots/NN-…jpg` (mật khẩu mẫu hiện trên trang đã được che).
Tài khoản dùng: `SHOPPER` (vai Customer, người dùng cung cấp). Quy tắc: mình không gõ mật khẩu; mật khẩu điền bằng nút "Use customer" của chính trang (trang tự điền mật khẩu mẫu). Mọi ca cần gõ mật khẩu khác ghi ở mục 2.

## 0. Bảng phủ
| Nhóm ca | Trạng thái | Hàng nhật ký / lý do |
|---|---|---|
| Luồng chính thành công | Đã làm | #6–#8 |
| Từng nhánh lỗi | Đã làm | #1, #2, #12, #17, #18 |
| Từng vai trò (ai thấy gì, ai không có nút) | Đã làm | #9–#10 (chỉ có tài khoản Customer; vai Admin xem mục 3) |
| Đổi ngôn ngữ | Không áp dụng | Giao diện chỉ có tiếng Anh, không thấy nút đổi ngôn ngữ |
| Tải lại trang, nút Back, hai tab | Đã làm | #8, #14, #15 |
| Link sâu khi chưa đăng nhập / thiếu quyền; địa chỉ không tồn tại | Đã làm | #9, #14 |
| Phản hồi mạng (mã trạng thái, `GET /api`) | Đã làm | #1, #6, #10, #12 |
| Tệp giao diện (chuỗi thông báo) | Đã làm | #16 |
| Ô nhập: để trống từng ô và cả hai | Đã làm | #1, #2 |
| Ô nhập: sai định dạng email | Đã làm | #3 |
| Ô nhập: khoảng trắng đầu/cuối, chữ hoa thường | Đã làm | #13, #16, #18 |
| Ô nhập: nhấn Enter | Đã làm | #3, #12 |
| Ô nhập: rất dài, ký tự đặc biệt | Chưa làm | Gửi lên máy chủ tính là lần đăng nhập sai; dự án chưa làm giới hạn nên không thử thêm |
| Ô nhập: bấm hai lần liên tiếp | Đã làm | #20 |
| Nút hiện/ẩn mật khẩu, Quên mật khẩu, Remember me | Đã làm | #4, #5, #16 |
| Đăng xuất, Back sau đăng xuất, đăng xuất ở tab khác | Đã làm | #11, #14, #15 |
| Hết hạn phiên | Chưa làm | Dự án chưa làm phần này (người dùng chốt 2026-11-20) |
| Giới hạn đăng nhập sai | Chưa làm | Dự án chưa làm giới hạn này (người dùng chốt 2026-11-20); đã gửi 3 lần sai, chưa thấy khóa (#19) |

## 1. Đã thấy (có thao tác thật)
| # | Thao tác | Kết quả quan sát (nguyên văn khi có) | Ảnh |
|---|---|---|---|
| 1 | Mở trang chủ khi chưa đăng nhập (`/`) | Hiện màn hình đăng nhập, hai tab "Sign in" và "Create account", khung "Customer training login" (có sẵn email và mật khẩu mẫu của tài khoản Customer, nút "Use customer"). Mạng: `GET /api/me` → 401 (hệ thống kiểm phiên khi tải trang). Form có `novalidate` (trình duyệt không tự kiểm), ô email `type=email`, ô mật khẩu `type=password` | 1 |
| 2 | Bỏ trống cả hai ô, bấm Sign in | Dưới ô email: "Enter your email address." Dưới ô mật khẩu: "Enter your password." Hai ô viền đỏ. **Không có** yêu cầu `POST /api/auth/login` nào được gửi (kiểm bằng Network) | 2 |
| 3 | Nhập `abc` vào ô email, bỏ trống mật khẩu, nhấn Enter | Chỉ ô mật khẩu báo "Enter your password."; ô email **không báo gì** dù `abc` không phải email. Không gửi yêu cầu đăng nhập | 3 |
| 4 | Bấm "Forgot password?" | Thông báo nhỏ góc dưới phải: "Password recovery is disabled in the training environment." (không chuyển trang) | 4 |
| 5 | Bấm "Use customer", rồi bấm "Show" | "Use customer" điền email `shopper@sunny.test` và mật khẩu mẫu (11 ký tự). "Show" đổi ô mật khẩu thành chữ nhìn thấy được, nút đổi thành "Hide"; bấm lần nữa trở lại ẩn (kiểm bằng thuộc tính `type`, không chụp ảnh vì lộ mật khẩu) | — (kiểm lại: F12 → Elements, thuộc tính `type` của ô mật khẩu) |
| 6 | Bấm Sign in với tài khoản mẫu (không tick Remember me) | Nút đổi thành "Signing in…" khoảng vài giây rồi vào **cửa hàng** (Sunny Store: Shop, My orders, Profile, Bag). Mạng: `POST /api/auth/login` → 200, sau đó `GET /api/store/products` → 200, `GET /api/store/cart` → 200. Lời chào "WELCOME, SUNNY" | 6 |
| 7 | Đọc `GET /api/me` sau đăng nhập | 200, `user` gồm email, id, name "Sunny Shopper", role "Customer", workspaceId | — (kiểm lại: F12 → Network → `/api/me`) |
| 8 | Tải lại trang khi đã đăng nhập | Vẫn đăng nhập (không hiện form), hiện "Loading your store…" rồi vào cửa hàng | — |
| 9 | Khi đã đăng nhập Customer, đổi địa chỉ thành `#dashboard`, `#products`, `#api-lab`, `#khong-ton-tai` | Cả bốn đều hiện lại trang chủ cửa hàng (không hiện trang quản trị, không báo lỗi). `#profile` hiện trang "My profile" | — |
| 10 | Đọc API quản trị khi là Customer: `GET /api/dashboard`, `/api/products`, `/api/orders` | Đều 403, nội dung `{"error":"FORBIDDEN","message":"Operations portal access is required."}`. `GET /api/auth/login` cũng 403 (chính message đó) | — (kiểm lại: F12 → Network) |
| 11 | Bấm Sign out (thanh cửa hàng) | Thông báo "You have been signed out." Quay về form đăng nhập, ô email và mật khẩu trống. `GET /api/me` → 401. Mạng: `POST /api/auth/logout` → 200 | — |
| 12 | Bấm "Use customer", đổi email thành `khongtontai@sunny.test`, nhấn Enter | Mạng: `POST /api/auth/login` → 401. Khung đỏ dưới nút: "Email or password is incorrect." Ô mật khẩu **giữ nguyên** nội dung, ô email giữ chữ vừa nhập | 5 |
| 13 | Email viết hoa `SHOPPER@SUNNY.TEST` (mật khẩu mẫu), nhấn Enter | **Đăng nhập thành công** (`POST /api/auth/login` → 200): email không phân biệt hoa thường | — |
| 14 | Sau đăng xuất: nút Back, rồi mở `#profile`, `#my-orders`, `#dashboard` | Back về địa chỉ `#profile` nhưng vẫn hiện form đăng nhập; cả ba địa chỉ đều hiện form đăng nhập. `GET /api/dashboard` và `GET /api/store/products` → 401 | — |
| 15 | Hai tab: đăng nhập ở tab 1, mở tab 2 (vẫn đăng nhập), đăng xuất ở tab 2 | Tab 1 không đổi ngay (vẫn hiện cửa hàng); khi tab 1 chuyển trang (`#my-orders`) thì hiện form đăng nhập, `GET /api/me` → 401 | — |
| 16 | Đọc tệp giao diện `/app.js` (chỉ đọc) | Form: email được cắt khoảng trắng đầu/cuối (`trim`) trước khi gửi; mật khẩu không cắt. Gửi `POST /api/auth/login` thân `{email, password}` (không có trường "remember"). Ô "Remember me on this device" **không được dùng** trong mã. Thông báo lỗi lấy từ phản hồi máy chủ. Khi gặp 401 ở trang khác, hệ thống đưa về form đăng nhập | — (kiểm lại: mở `/app.js`) |
| 17 | (Người dùng nhờ mình gõ) Email đúng `shopper@sunny.test`, mật khẩu sai do mình đặt, nhấn Enter | `POST /api/auth/login` → 401; "Email or password is incorrect." (**cùng thông báo** như email không tồn tại, không lộ email có tồn tại); mật khẩu giữ nguyên trong trường | 7 |
| 18 | Mật khẩu mẫu thêm một khoảng trắng ở cuối (bấm "Use customer", End, gõ dấu cách), Enter | `POST /api/auth/login` → 401, cùng thông báo: mật khẩu **không** bị cắt khoảng trắng | — (kiểm lại: F12 → Network) |
| 19 | Sau 3 lần sai (#12, #17, #18), đăng nhập đúng lại | Đăng nhập thành công (`/api/me` 200), tài khoản chưa bị khóa; dự án chưa làm giới hạn nên không có ngưỡng | — |
| 20 | Bấm Use customer, rồi bấm Sign in 3 lần liên tiếp rất nhanh | Chỉ **1** yêu cầu `POST /api/auth/login` được gửi (nút bị vô hiệu hóa sau lần bấm đầu, hiện "Signing in…"); đăng nhập thành công, `/api/me` 200 | — (kiểm lại: F12 → Network) |

## 2. Cần người dùng làm (vì phải gõ mật khẩu) — kết quả
- Không còn. Người dùng đã nhờ mình gõ mật khẩu sai (#17, #18).

## 3. Chưa thử / không kiểm tra được
- **Giới hạn số lần đăng nhập sai / khóa tạm:** dự án chưa làm (người dùng chốt 2026-11-20, không có số lần tối đa); ngưỡng cần requirement hoặc người test chốt. Đã gửi **3** lần đăng nhập sai (#12, #17, #18), không thấy khóa; không gửi thêm khi chưa có ngưỡng.
- **Rất dài, ký tự đặc biệt (gửi lên máy chủ):** cùng lý do (có thể tăng bộ đếm sai).
- **Hết hạn phiên:** dự án chưa làm (người dùng chốt 2026-11-20).
- **Vai Admin (cổng quản trị: Dashboard, Products, Orders, Customers, API Lab, Challenges):** thiếu tài khoản (người dùng mới đưa tài khoản Customer). Trang tự hiện sẵn khung đăng nhập mẫu cho Customer; mã nguồn giao diện còn có thông tin tài khoản quản trị khác trong màn API Lab nhưng người dùng chưa cung cấp nên không dùng.
- **Tác động của "Remember me on this device":** mã không dùng ô này (#16); chưa kiểm xem cookie phiên có đổi theo ô này không (cookie không đọc được từ trang).
- **Tab "Create account":** thuộc tính năng đăng ký, chưa khám phá (cần tạo dữ liệu thật, hỏi người dùng trước).

## 4. Điểm chưa rõ (ứng viên cho mục câu hỏi của SRS)
**Quyết định của người dùng (2026-11-20): các điểm 1–5 dưới đây, dự án chưa làm; không hỏi BA, không viết test case kỳ vọng, không báo bug; xem lại khi dự án làm.** Điểm 6 (giới hạn lần sai, thời gian sống phiên) và 7 (thời gian chờ đăng nhập) cũng được chốt là dự án chưa làm (2026-11-20).
1. Ô email nhập `abc` (không phải email) không báo lỗi định dạng ở trình duyệt (#3); chưa kiểm xem máy chủ trả gì khi gửi email sai định dạng kèm mật khẩu.
2. Ô "Remember me on this device" không có tác dụng thấy được (#16). Đây là thiết kế hay chưa làm?
3. Khung "Customer training login" hiện sẵn email và mật khẩu mẫu ngay trên màn hình đăng nhập: có giữ ở môi trường thật không?
4. Tài khoản Customer đăng nhập vào cửa hàng, địa chỉ quản trị (`#dashboard`…) chỉ đưa về trang chủ cửa hàng (#9), không báo "không đủ quyền". Có đúng ý không?
5. Đăng xuất ở tab khác: tab đầu chỉ biết sau khi bấm chuyển trang (#15). Có cần tự thoát ngay không?
6. Giới hạn số lần đăng nhập sai và thời gian sống của phiên là bao nhiêu?
7. Thời gian chờ đăng nhập thành công khoảng vài giây ("Signing in…"): có yêu cầu thời gian phản hồi không?

> **Ghi chú an toàn:** đã gửi 3 lần đăng nhập sai (#12, #17, #18) và 3 lần đăng nhập đúng (#6, #13, #19); không thấy dấu hiệu khóa. Không đổi dữ liệu người khác.
