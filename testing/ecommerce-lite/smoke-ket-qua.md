# Kết quả chạy smoke test — ecommerce-lite

> File tự sinh từ `testing/ecommerce-lite/run-results/smoke.json` bằng `scripts/build_report.py` — đừng sửa tay, chạy lại là ghi đè. Bản dễ xem: `smoke-ket-qua.html`.

| | |
|---|---|
| Build | **Không có số bản ở chân trang** |
| Lượt | 4 / 4 (lượt mới nhất) |
| Thời điểm | 2026-11-20 11:57:37 |
| Người chạy | Mo Tran |
| Cách chạy | Tự động (Playwright) |
| Kết luận | **Nhận build** |
| Ghi chú | — |

## Kết luận và rủi ro

Nhận build: cả 5 case smoke đăng nhập đều Đạt khi chạy bằng script ngày 2026-11-20, mỗi case có ảnh làm bằng chứng. Smoke chỉ bảo đảm đăng nhập dùng được.

Số liệu lượt này: 5 trên 5 case đã có kết quả (100%): 5 Đạt.

**Đã kiểm và đạt**

- Mở trang khi chưa đăng nhập: hiện form đăng nhập có ô email, ô mật khẩu và nút Sign in, không vào thẳng cửa hàng.
- Mật khẩu sai (một lần): máy chủ trả 401, hiện "Email or password is incorrect.", vẫn ở form, ô mật khẩu giữ nội dung.
- Đăng nhập đúng bằng tài khoản SHOPPER: vào cửa hàng, có lời chào WELCOME, SUNNY và các mục Shop, My orders, Profile, Bag.
- Tải lại trang khi đã đăng nhập: không hiện form, vào lại cửa hàng; /api/me trả 200.
- Đăng xuất: hiện "You have been signed out.", quay về form với ô email và mật khẩu trống, logout trả 200, /api/me trả 401.

**Chưa có kết quả và vì sao**

| Case | Trạng thái | Lý do |
|---|---|---|
| Các hành trình ngoài đăng nhập: duyệt cửa hàng, giỏ và đặt hàng, xem đơn, hồ sơ, cổng quản trị | Chưa có test case | Mới khám phá và viết test case cho tính năng Đăng nhập; các hành trình này chưa khám phá nên smoke không kiểm được. |
| 14 test case đăng nhập ngoài smoke (TC-003, 005, 006, 009 đến 019) | Chưa chạy | Không thuộc smoke, để test sâu sau khi nhận build. |

**Rủi ro để người kiểm thử đánh giá**

- **Phạm vi smoke hẹp.** Smoke Đạt chỉ cho biết người dùng đăng nhập, giữ phiên và đăng xuất được. Nếu mua hàng hoặc xem đơn hỏng thì lượt này không phát hiện; chưa kiểm.
- **Test case chưa được BA xác nhận.** Test case đăng nhập dựa trên SRS nháp viết từ quan sát hệ thống, nên kết quả mong đợi là hành vi hiện tại, chưa phải yêu cầu chính thức.
- **Gõ quá sớm làm ô mật khẩu bị xóa (chỉ ảnh hưởng cách chạy script).** Lượt 2 và 3 thấy ô mật khẩu trống sau lần sai vì script gõ ngay khi trang vừa hiện, trước lúc trang kiểm phiên xong (GET /api/me) và vẽ lại form. Đo riêng: chờ kiểm phiên xong rồi mới gõ thì ô giữ nguyên 12 ký tự; kiểm tay cũng giữ nguyên. Người dùng thật không gõ nhanh đến mức đó. Lượt 4 chạy lại với script đã chờ.
- **Ảnh bằng chứng che khung tài khoản mẫu.** Trang đăng nhập hiện mật khẩu mẫu, nên script làm mờ khung đó trước khi chụp. Video không quay cho case Đạt, bằng chứng của case Đạt là ảnh.

**Đề xuất (người kiểm thử hoặc PO quyết định)**

Đề xuất nhận build để test sâu đăng nhập. Quyết định nhận hay trả build là của người test hoặc PO.

## Kết quả lượt mới nhất

| ID | Smoke case | Các bước | Kết quả mong đợi | Status | Evidence | Bug | Số lần chạy |
|---|---|---|---|---|---|---|---|
| SM-01 | Hiện form đăng nhập khi mở trang chủ lúc chưa đăng nhập (Đăng nhập · TC-001) | 1. Mở https://staging-ecommerce-lite.vercel.app/ trong cửa sổ ẩn danh.<br>2. Nhìn màn hình hiện ra. | Bước 2: hiện màn hình đăng nhập có hai tab Sign in và Create account, ô email, ô mật khẩu, ô Remember me on this device, nút Sign in, nút Show, liên kết Forgot password?; không vào thẳng cửa hàng. | Đạt | [dang-nhap-tc-001-form-dang-nhap-20261120-115706.png](../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-001-form-dang-nhap-20261120-115706.png)<br>[dang-nhap-tc-001-kiem-20261120-115706.png](../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-001-kiem-20261120-115706.png) | — | 4 |
| SM-02 | Hiện `Email or password is incorrect.` khi email đúng nhưng mật khẩu sai (Đăng nhập · TC-004) | 1. Mở https://staging-ecommerce-lite.vercel.app/ và mở F12, tab Network.<br>2. Ở ô email nhập shopper@sunny.test.<br>3. Ở ô mật khẩu nhập Sai@Matkhau1.<br>4. Nhấn Enter.<br>5. Nhìn màn hình và tab Network. | Bước 5: Network có POST /api/auth/login trả 401; khung đỏ hiện Email or password is incorrect. (cùng chữ như khi email không tồn tại); vẫn ở form; ô mật khẩu giữ nguyên nội dung. | Đạt | [dang-nhap-tc-004-sai-mat-khau-20261120-115717.png](../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-004-sai-mat-khau-20261120-115717.png)<br>[dang-nhap-tc-004-kiem-20261120-115717.png](../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-004-kiem-20261120-115717.png) | — | 4 |
| SM-03 | Đăng nhập thành công và vào cửa hàng khi nhập đúng email và mật khẩu (Đăng nhập · TC-002) | 1. Mở https://staging-ecommerce-lite.vercel.app/ và mở F12, tab Network.<br>2. Bấm nút Use customer (trang tự điền email và mật khẩu).<br>3. Bấm nút Sign in.<br>4. Chờ vài giây, nhìn màn hình và tab Network. | Bước 3: nút đổi thành Signing in….<br>Bước 4: vào cửa hàng Sunny Store có Shop, My orders, Profile, Bag, lời chào WELCOME, SUNNY; Network có POST /api/auth/login trả 200. | Đạt | [dang-nhap-tc-002-cua-hang-sau-dang-nhap-20261120-115722.png](../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-002-cua-hang-sau-dang-nhap-20261120-115722.png)<br>[dang-nhap-tc-002-kiem-20261120-115722.png](../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-002-kiem-20261120-115722.png) | — | 4 |
| SM-04 | Vẫn đăng nhập và vào lại cửa hàng khi tải lại trang sau khi đã đăng nhập (Đăng nhập · TC-007) | 1. Mở https://staging-ecommerce-lite.vercel.app/, bấm Use customer, bấm Sign in, chờ vào cửa hàng.<br>2. Tải lại trang (F5).<br>3. Nhìn màn hình. | Bước 3: không hiện form đăng nhập; hiện Loading your store… rồi vào lại cửa hàng. | Đạt | [dang-nhap-tc-007-cua-hang-sau-tai-lai-20261120-115728.png](../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-007-cua-hang-sau-tai-lai-20261120-115728.png) | — | 4 |
| SM-05 | Về form đăng nhập và báo đã đăng xuất khi bấm Sign out (Đăng nhập · TC-008) | 1. Mở https://staging-ecommerce-lite.vercel.app/ và mở F12, tab Network.<br>2. Bấm Use customer, bấm Sign in, chờ vào cửa hàng.<br>3. Bấm Sign out trên thanh cửa hàng.<br>4. Nhìn màn hình và tab Network. | Bước 3: hiện thông báo You have been signed out..<br>Bước 4: quay về form đăng nhập, ô email và ô mật khẩu trống; Network có POST /api/auth/logout trả 200. | Đạt | [dang-nhap-tc-008-sau-dang-xuat-20261120-115736.png](../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-008-sau-dang-xuat-20261120-115736.png)<br>[dang-nhap-tc-008-kiem-20261120-115736.png](../../evidence/ecommerce-lite/chay-test/dang-nhap-tc-008-kiem-20261120-115736.png) | — | 4 |

## Lịch sử các lượt

| Lượt | Build | Thời điểm | Người chạy | Kết quả | Kết luận |
|---|---|---|---|---|---|
| 4 | Không có số bản ở chân trang | 2026-11-20 11:57:37 | Mo Tran | 5 Đạt | Nhận build |
| 3 | Không có số bản ở chân trang | 2026-11-20 11:54:05 | Mo Tran | 4 Đạt, 1 Đạt kèm ý phụ sai | Nhận build |
| 2 | Không có số bản ở chân trang | 2026-11-20 11:49:41 | Mo Tran | 4 Đạt, 1 Đạt kèm ý phụ sai | Nhận build |
| 1 | Không có số bản ở chân trang | 2026-11-20 12:00:00 | Mo Tran | 5 Đạt | Nhận build |

## Từng case qua các lượt (tối đa 8 lượt gần nhất)

| ID | Lượt 1 (Không có số bản ở chân trang) | Lượt 2 (Không có số bản ở chân trang) | Lượt 3 (Không có số bản ở chân trang) | Lượt 4 (Không có số bản ở chân trang) |
|---|---|---|---|---|
| SM-01 | Đạt | Đạt | Đạt | Đạt |
| SM-02 | Đạt | Đạt kèm ý phụ sai | Đạt kèm ý phụ sai | Đạt |
| SM-03 | Đạt | Đạt | Đạt | Đạt |
| SM-04 | Đạt | Đạt | Đạt | Đạt |
| SM-05 | Đạt | Đạt | Đạt | Đạt |

Các bước và Kết quả mong đợi lấy từ test case gốc. Bị chặn: chưa test được vì bug khác (xem cột Bug). Số lần chạy: số lượt có kết luận Đạt, Đạt kèm lỗi đã biết, Đạt kèm ý phụ sai hoặc Không đạt; lượt Không kết luận và Chưa chạy không tính.
