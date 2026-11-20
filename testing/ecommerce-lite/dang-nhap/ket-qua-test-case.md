# Kết quả chạy test case đăng nhập — ecommerce-lite

> File tự sinh từ `testing/ecommerce-lite/run-results/dang-nhap.json` bằng `scripts/build_report.py` — đừng sửa tay, chạy lại là ghi đè. Bản dễ xem: `ket-qua-test-case.html`.

| | |
|---|---|
| Build | **Không có số bản ở chân trang** |
| Lượt | 1 / 1 (lượt mới nhất) |
| Thời điểm | 2026-11-20 12:04:03 |
| Người chạy | Mo Tran |
| Cách chạy | Script Playwright (run_tests.py) |
| Kết luận | **Đạt toàn bộ** |
| Ghi chú | Chạy script trên staging ngày 2026-11-20, không thấy số bản ở chân trang. 19 trên 19 case có kết quả, đều Đạt (5 case smoke chạy ở lượt smoke 4, 14 case còn lại chạy trong cùng ngày). |

## Kết luận và rủi ro

Đạt toàn bộ: 19 trên 19 test case đăng nhập đều Đạt khi chạy bằng script ngày 2026-11-20, mỗi case có ảnh làm bằng chứng. Không có lỗi nào cần báo.

Số liệu lượt này: 19 trên 19 case đã có kết quả (100%): 19 Đạt.

**Đã kiểm và đạt**

- Luồng chính: mở trang chưa đăng nhập hiện form; đăng nhập đúng vào cửa hàng; tải lại vẫn đăng nhập; đăng xuất về form với ô email và mật khẩu trống; /api/me trả đúng Customer "Sunny Shopper".
- Đăng nhập sai: email không tồn tại, mật khẩu sai và mật khẩu thừa một dấu cách cuối đều trả 401 và cùng thông báo "Email or password is incorrect."; ô mật khẩu giữ nội dung.
- Ô bỏ trống: bỏ trống cả hai ô hiện "Enter your email address." và "Enter your password."; bỏ trống mật khẩu hiện "Enter your password."; cả hai trường hợp không gửi yêu cầu đăng nhập.
- Email: viết hoa hoặc có khoảng trắng đầu và cuối vẫn đăng nhập được (trả 200).
- Sau 3 lần sai liên tiếp (3 lần trả 401), đăng nhập đúng vẫn được (trả 200), tài khoản chưa bị khóa.
- Bấm Sign in ba lần liên tiếp rất nhanh chỉ gửi 1 yêu cầu đăng nhập.
- Sau đăng xuất: nút Back, #my-orders và #dashboard đều hiện form; đăng xuất ở tab 2 thì tab 1 hiện form khi chuyển trang.
- Customer gọi /api/dashboard bị 403 với "Operations portal access is required.".
- Show và Hide đổi kiểu ô mật khẩu đúng; Forgot password? hiện "Password recovery is disabled in the training environment." và không chuyển trang.

**Chưa có kết quả và vì sao**

| Case | Trạng thái | Lý do |
|---|---|---|
| Vai Admin, tab Create account, hạn phiên, giới hạn số lần sai, thời gian chờ đăng nhập | Chưa có test case | Dự án chưa làm giới hạn lần sai, hạn phiên (người dùng chốt 2026-11-20); vai Admin thiếu tài khoản; Create account thuộc tính năng đăng ký chưa khám phá. |

**Rủi ro để người kiểm thử đánh giá**

- **Test case chưa được BA xác nhận.** Test case dựa trên SRS nháp viết từ quan sát hệ thống, nên "Đạt" nghĩa là hệ thống khớp hành vi đã quan sát, chưa phải khớp yêu cầu chính thức. Nếu BA có yêu cầu khác (ví dụ báo lỗi định dạng email, Remember me) thì phải bổ sung test case.
- **Tác động của cách chạy script.** Script phải chờ trang kiểm phiên xong rồi mới gõ; gõ sớm hơn làm ô mật khẩu bị xóa. Người dùng thật không gõ nhanh đến vậy nên không coi là lỗi, nhưng nếu hệ thống đổi cách kiểm phiên thì kết quả script có thể đổi.
- **Hệ thống chưa giới hạn số lần sai.** Đã gửi tổng cộng khoảng 9 lần đăng nhập sai bằng script (trần người dùng chốt là 10), không thấy khóa. Nếu sau này dự án làm giới hạn thì test case về lần sai cần viết lại.

**Đề xuất (người kiểm thử hoặc PO quyết định)**

Đề xuất coi tính năng Đăng nhập đạt ở mức hành vi đã quan sát; bước tiếp theo là regression hoặc khám phá các tính năng khác (cửa hàng, giỏ, đơn). Quyết định nhận hay trả build là của người test hoặc PO.

## Kết quả lượt mới nhất

| ID | Test case | Các bước | Kết quả mong đợi | Status | Evidence | Bug | Số lần chạy |
|---|---|---|---|---|---|---|---|
| TC-001 | Hiện form đăng nhập khi mở trang chủ lúc chưa đăng nhập (Ưu tiên Cao) | 1. Mở https://staging-ecommerce-lite.vercel.app/ trong cửa sổ ẩn danh.<br>2. Nhìn màn hình hiện ra. | Bước 2: hiện màn hình đăng nhập có hai tab Sign in và Create account, ô email, ô mật khẩu, ô Remember me on this device, nút Sign in, nút Show, liên kết Forgot password?; không vào thẳng cửa hàng. | Đạt | [dang-nhap-tc-001-form-dang-nhap-20261120-115706.png](../../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-001-form-dang-nhap-20261120-115706.png)<br>[dang-nhap-tc-001-kiem-20261120-115706.png](../../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-001-kiem-20261120-115706.png) | — | 1 |
| TC-002 | Đăng nhập thành công và vào cửa hàng khi nhập đúng email và mật khẩu (Ưu tiên Cao) | 1. Mở https://staging-ecommerce-lite.vercel.app/ và mở F12, tab Network.<br>2. Bấm nút Use customer (trang tự điền email và mật khẩu).<br>3. Bấm nút Sign in.<br>4. Chờ vài giây, nhìn màn hình và tab Network. | Bước 3: nút đổi thành Signing in….<br>Bước 4: vào cửa hàng Sunny Store có Shop, My orders, Profile, Bag, lời chào WELCOME, SUNNY; Network có POST /api/auth/login trả 200. | Đạt | [dang-nhap-tc-002-cua-hang-sau-dang-nhap-20261120-115722.png](../../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-002-cua-hang-sau-dang-nhap-20261120-115722.png)<br>[dang-nhap-tc-002-kiem-20261120-115722.png](../../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-002-kiem-20261120-115722.png) | — | 1 |
| TC-003 | Hiện `Email or password is incorrect.` khi nhập email không tồn tại (Ưu tiên Cao) | 1. Mở https://staging-ecommerce-lite.vercel.app/ và mở F12, tab Network.<br>2. Bấm nút Use customer.<br>3. Xóa email đã điền, nhập khongtontai@sunny.test (giữ nguyên mật khẩu đã điền).<br>4. Nhấn Enter.<br>5. Nhìn màn hình và tab Network. | Bước 5: Network có POST /api/auth/login trả 401; khung đỏ dưới nút hiện Email or password is incorrect.; vẫn ở form đăng nhập; ô email giữ chữ vừa nhập, ô mật khẩu vẫn còn nội dung. | Đạt | [dang-nhap-tc-003-email-khong-ton-tai-20261120-120315.png](../../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-003-email-khong-ton-tai-20261120-120315.png)<br>[dang-nhap-tc-003-kiem-20261120-120315.png](../../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-003-kiem-20261120-120315.png) | — | 1 |
| TC-004 | Hiện `Email or password is incorrect.` khi email đúng nhưng mật khẩu sai (Ưu tiên Cao) | 1. Mở https://staging-ecommerce-lite.vercel.app/ và mở F12, tab Network.<br>2. Ở ô email nhập shopper@sunny.test.<br>3. Ở ô mật khẩu nhập Sai@Matkhau1.<br>4. Nhấn Enter.<br>5. Nhìn màn hình và tab Network. | Bước 5: Network có POST /api/auth/login trả 401; khung đỏ hiện Email or password is incorrect. (cùng chữ như khi email không tồn tại); vẫn ở form; ô mật khẩu giữ nguyên nội dung. | Đạt | [dang-nhap-tc-004-sai-mat-khau-20261120-115717.png](../../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-004-sai-mat-khau-20261120-115717.png)<br>[dang-nhap-tc-004-kiem-20261120-115717.png](../../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-004-kiem-20261120-115717.png) | — | 1 |
| TC-005 | Báo lỗi ở cả hai ô và không gửi yêu cầu đăng nhập khi bỏ trống email và mật khẩu (Ưu tiên Cao) | 1. Mở https://staging-ecommerce-lite.vercel.app/ và mở F12, tab Network.<br>2. Để trống cả hai ô.<br>3. Bấm nút Sign in.<br>4. Nhìn màn hình và tab Network. | Bước 3: dưới ô email hiện Enter your email address., dưới ô mật khẩu hiện Enter your password., hai ô viền đỏ.<br>Bước 4: Network không có yêu cầu POST /api/auth/login. | Đạt | [dang-nhap-tc-005-bo-trong-hai-o-20261120-120140.png](../../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-005-bo-trong-hai-o-20261120-120140.png)<br>[dang-nhap-tc-005-kiem-20261120-120140.png](../../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-005-kiem-20261120-120140.png) | — | 1 |
| TC-006 | Báo lỗi ở ô mật khẩu và không gửi yêu cầu đăng nhập khi bỏ trống mật khẩu (Ưu tiên Cao) | 1. Mở https://staging-ecommerce-lite.vercel.app/ và mở F12, tab Network.<br>2. Ở ô email nhập abc.<br>3. Để trống ô mật khẩu.<br>4. Nhấn Enter.<br>5. Nhìn màn hình và tab Network. | Bước 5: dưới ô mật khẩu hiện Enter your password.; Network không có yêu cầu POST /api/auth/login. | Đạt | [dang-nhap-tc-006-bo-trong-mat-khau-20261120-120145.png](../../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-006-bo-trong-mat-khau-20261120-120145.png)<br>[dang-nhap-tc-006-kiem-20261120-120145.png](../../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-006-kiem-20261120-120145.png) | — | 1 |
| TC-007 | Vẫn đăng nhập và vào lại cửa hàng khi tải lại trang sau khi đã đăng nhập (Ưu tiên Cao) | 1. Mở https://staging-ecommerce-lite.vercel.app/, bấm Use customer, bấm Sign in, chờ vào cửa hàng.<br>2. Tải lại trang (F5).<br>3. Nhìn màn hình. | Bước 3: không hiện form đăng nhập; hiện Loading your store… rồi vào lại cửa hàng. | Đạt | [dang-nhap-tc-007-cua-hang-sau-tai-lai-20261120-115728.png](../../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-007-cua-hang-sau-tai-lai-20261120-115728.png) | — | 1 |
| TC-008 | Về form đăng nhập và báo đã đăng xuất khi bấm Sign out (Ưu tiên Cao) | 1. Mở https://staging-ecommerce-lite.vercel.app/ và mở F12, tab Network.<br>2. Bấm Use customer, bấm Sign in, chờ vào cửa hàng.<br>3. Bấm Sign out trên thanh cửa hàng.<br>4. Nhìn màn hình và tab Network. | Bước 3: hiện thông báo You have been signed out..<br>Bước 4: quay về form đăng nhập, ô email và ô mật khẩu trống; Network có POST /api/auth/logout trả 200. | Đạt | [dang-nhap-tc-008-sau-dang-xuat-20261120-115736.png](../../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-008-sau-dang-xuat-20261120-115736.png)<br>[dang-nhap-tc-008-kiem-20261120-115736.png](../../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-008-kiem-20261120-115736.png) | — | 1 |
| TC-009 | Hiện form đăng nhập khi bấm Back hoặc mở lại địa chỉ trong ứng dụng sau khi đăng xuất (Ưu tiên Cao) | 1. Mở https://staging-ecommerce-lite.vercel.app/, bấm Use customer, bấm Sign in, chờ vào cửa hàng.<br>2. Mở #profile (bấm Profile).<br>3. Bấm Sign out.<br>4. Bấm nút Back của trình duyệt, nhìn màn hình.<br>5. Sửa địa chỉ thành https://staging-ecommerce-lite.vercel.app/#my-orders, nhìn màn hình.<br>6. Sửa địa chỉ thành https://staging-ecommerce-lite.vercel.app/#dashboard, nhìn màn hình. | Bước 4: địa chỉ về #profile nhưng vẫn hiện form đăng nhập.<br>Bước 5: hiện form đăng nhập.<br>Bước 6: hiện form đăng nhập. | Đạt | [dang-nhap-tc-009-sau-back-20261120-120241.png](../../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-009-sau-back-20261120-120241.png)<br>[dang-nhap-tc-009-mo-dashboard-sau-dang-xuat-20261120-120244.png](../../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-009-mo-dashboard-sau-dang-xuat-20261120-120244.png)<br>[dang-nhap-tc-009-kiem-20261120-120244.png](../../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-009-kiem-20261120-120244.png) | — | 1 |
| TC-010 | Trả lỗi 403 khi Customer gọi API quản trị `/api/dashboard` (Ưu tiên Cao) | 1. Mở https://staging-ecommerce-lite.vercel.app/, bấm Use customer, bấm Sign in, chờ vào cửa hàng.<br>2. Mở F12, tab Console.<br>3. Gõ fetch('/api/dashboard').then(async r => [r.status, await r.text()]) rồi nhấn Enter.<br>4. Đọc kết quả. | Bước 4: mã trạng thái 403, nội dung {"error":"FORBIDDEN","message":"Operations portal access is required."}. | Đạt | [dang-nhap-tc-010-cua-hang-truoc-khi-goi-api-20261120-120153.png](../../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-010-cua-hang-truoc-khi-goi-api-20261120-120153.png) | — | 1 |
| TC-011 | Không đăng nhập được khi mật khẩu đúng nhưng thêm một khoảng trắng ở cuối (Ưu tiên Trung bình) | 1. Mở https://staging-ecommerce-lite.vercel.app/ và mở F12, tab Network.<br>2. Bấm Use customer.<br>3. Bấm vào ô mật khẩu, nhấn phím End, gõ một dấu cách.<br>4. Nhấn Enter.<br>5. Nhìn màn hình và tab Network. | Bước 5: Network có POST /api/auth/login trả 401; hiện Email or password is incorrect.; vẫn ở form. | Đạt | [dang-nhap-tc-011-mat-khau-them-dau-cach-20261120-120321.png](../../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-011-mat-khau-them-dau-cach-20261120-120321.png)<br>[dang-nhap-tc-011-kiem-20261120-120321.png](../../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-011-kiem-20261120-120321.png) | — | 1 |
| TC-012 | Đăng nhập thành công khi nhập email viết hoa (Ưu tiên Trung bình) | 1. Mở https://staging-ecommerce-lite.vercel.app/ và mở F12, tab Network.<br>2. Bấm Use customer.<br>3. Xóa email đã điền, nhập SHOPPER@SUNNY.TEST.<br>4. Nhấn Enter.<br>5. Chờ vài giây, nhìn màn hình và tab Network. | Bước 5: Network có POST /api/auth/login trả 200; vào cửa hàng. | Đạt | [dang-nhap-tc-012-dang-nhap-email-viet-hoa-20261120-120227.png](../../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-012-dang-nhap-email-viet-hoa-20261120-120227.png) | — | 1 |
| TC-013 | Đăng nhập thành công khi email có khoảng trắng ở đầu và cuối (Ưu tiên Trung bình) | 1. Mở https://staging-ecommerce-lite.vercel.app/ và mở F12, tab Network.<br>2. Bấm Use customer.<br>3. Xóa email đã điền, nhập một dấu cách, shopper@sunny.test, rồi một dấu cách nữa.<br>4. Nhấn Enter.<br>5. Chờ vài giây, nhìn màn hình và tab Network. | Bước 5: Network có POST /api/auth/login trả 200; vào cửa hàng. | Đạt | [dang-nhap-tc-013-email-co-khoang-trang-20261120-120254.png](../../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-013-email-co-khoang-trang-20261120-120254.png) | — | 1 |
| TC-014 | Chỉ gửi một yêu cầu đăng nhập khi bấm Sign in nhiều lần liên tiếp rất nhanh (Ưu tiên Trung bình) | 1. Mở https://staging-ecommerce-lite.vercel.app/ và mở F12, tab Network.<br>2. Bấm Use customer.<br>3. Bấm nút Sign in 3 lần liên tiếp rất nhanh (nhấp ba lần).<br>4. Chờ vài giây, đếm số yêu cầu login trong tab Network. | Bước 3: nút bị vô hiệu hóa sau lần bấm đầu và hiện Signing in….<br>Bước 4: chỉ có 1 yêu cầu POST /api/auth/login; đăng nhập thành công, vào cửa hàng. | Đạt | [dang-nhap-tc-014-sau-khi-bam-nhieu-lan-20261120-120221.png](../../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-014-sau-khi-bam-nhieu-lan-20261120-120221.png) | — | 1 |
| TC-015 | Đăng nhập thành công khi nhập đúng sau 3 lần đăng nhập sai liên tiếp (Ưu tiên Trung bình) | 1. Mở https://staging-ecommerce-lite.vercel.app/.<br>2. Lần sai thứ 1: bấm Use customer, đổi email thành khongtontai@sunny.test, nhấn Enter, nhìn thông báo.<br>3. Lần sai thứ 2: tải lại trang, nhập email shopper@sunny.test, mật khẩu Sai@Matkhau1, nhấn Enter, nhìn thông báo.<br>4. Lần sai thứ 3: bấm Use customer, gõ thêm một dấu cách cuối mật khẩu, nhấn Enter, nhìn thông báo.<br>5. Bấm Use customer (trả về email và mật khẩu đúng), bấm Sign in.<br>6. Chờ vài giây, nhìn màn hình. | Bước 2, 3, 4: mỗi lần hiện Email or password is incorrect..<br>Bước 6: đăng nhập thành công, vào cửa hàng; tài khoản không bị khóa. | Đạt | [dang-nhap-tc-015-lan-sai-thu-3-20261120-120345.png](../../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-015-lan-sai-thu-3-20261120-120345.png)<br>[dang-nhap-tc-015-dang-nhap-dung-sau-3-lan-sai-20261120-120403.png](../../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-015-dang-nhap-dung-sau-3-lan-sai-20261120-120403.png) | — | 1 |
| TC-016 | Hệ thống trả đúng thông tin người đang đăng nhập khi xem `/api/me` sau đăng nhập (Ưu tiên Trung bình) | 1. Mở https://staging-ecommerce-lite.vercel.app/, bấm Use customer, bấm Sign in, chờ vào cửa hàng.<br>2. Mở F12, tab Console.<br>3. Gõ fetch('/api/me').then(async r => [r.status, await r.text()]) rồi nhấn Enter.<br>4. Đọc kết quả. | Bước 4: mã trạng thái 200; user có email shopper@sunny.test, name Sunny Shopper, role Customer, cùng id và workspaceId. | Đạt | [dang-nhap-tc-016-cua-hang-truoc-khi-goi-api-20261120-120203.png](../../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-016-cua-hang-truoc-khi-goi-api-20261120-120203.png) | — | 1 |
| TC-017 | Hiện form đăng nhập ở tab 1 khi chuyển trang sau khi đã đăng xuất ở tab 2 (Ưu tiên Trung bình) | 1. Ở tab 1 mở https://staging-ecommerce-lite.vercel.app/, bấm Use customer, bấm Sign in, chờ vào cửa hàng.<br>2. Mở tab 2 cùng địa chỉ (vẫn đăng nhập).<br>3. Ở tab 2 bấm Sign out.<br>4. Quay lại tab 1, sửa địa chỉ thành https://staging-ecommerce-lite.vercel.app/#my-orders.<br>5. Nhìn màn hình tab 1. | Bước 5: tab 1 hiện form đăng nhập. | Đạt | [dang-nhap-tc-017-tab-1-sau-khi-chuyen-trang-20261120-120306.png](../../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-017-tab-1-sau-khi-chuyen-trang-20261120-120306.png)<br>[dang-nhap-tc-017-kiem-20261120-120306.png](../../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-017-kiem-20261120-120306.png) | — | 1 |
| TC-018 | Hiện mật khẩu thành chữ khi bấm Show và ẩn lại khi bấm Hide (Ưu tiên Trung bình) | 1. Mở https://staging-ecommerce-lite.vercel.app/.<br>2. Bấm Use customer.<br>3. Bấm nút Show, nhìn ô mật khẩu và nút.<br>4. Bấm nút Hide, nhìn ô mật khẩu và nút. | Bước 3: ô mật khẩu hiện chữ nhìn thấy được, nút đổi thành Hide.<br>Bước 4: ô mật khẩu ẩn lại, nút trở về Show. | Đạt | [dang-nhap-tc-018-mat-khau-da-an-lai-20261120-120208.png](../../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-018-mat-khau-da-an-lai-20261120-120208.png) | — | 1 |
| TC-019 | Hiện thông báo khôi phục mật khẩu bị tắt khi bấm Forgot password? (Ưu tiên Thấp) | 1. Mở https://staging-ecommerce-lite.vercel.app/.<br>2. Bấm liên kết Forgot password?.<br>3. Nhìn góc dưới bên phải và địa chỉ trang. | Bước 3: góc dưới bên phải hiện thông báo Password recovery is disabled in the training environment.; không chuyển trang. | Đạt | [dang-nhap-tc-019-quen-mat-khau-20261120-120212.png](../../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-019-quen-mat-khau-20261120-120212.png)<br>[dang-nhap-tc-019-kiem-20261120-120212.png](../../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-019-kiem-20261120-120212.png) | — | 1 |

## Lịch sử các lượt

| Lượt | Build | Thời điểm | Người chạy | Kết quả | Kết luận |
|---|---|---|---|---|---|
| 1 | Không có số bản ở chân trang | 2026-11-20 12:04:03 | Mo Tran | 19 Đạt | Đạt toàn bộ |

## Từng case qua các lượt (tối đa 8 lượt gần nhất)

| ID | Lượt 1 (Không có số bản ở chân trang) |
|---|---|
| TC-001 | Đạt |
| TC-002 | Đạt |
| TC-003 | Đạt |
| TC-004 | Đạt |
| TC-005 | Đạt |
| TC-006 | Đạt |
| TC-007 | Đạt |
| TC-008 | Đạt |
| TC-009 | Đạt |
| TC-010 | Đạt |
| TC-011 | Đạt |
| TC-012 | Đạt |
| TC-013 | Đạt |
| TC-014 | Đạt |
| TC-015 | Đạt |
| TC-016 | Đạt |
| TC-017 | Đạt |
| TC-018 | Đạt |
| TC-019 | Đạt |

Các bước và Kết quả mong đợi lấy từ test case gốc. Bị chặn: chưa test được vì bug khác (xem cột Bug). Số lần chạy: số lượt có kết luận Đạt, Đạt kèm lỗi đã biết, Đạt kèm ý phụ sai hoặc Không đạt; lượt Không kết luận và Chưa chạy không tính.
