# Bộ smoke test — Ecommerce Lite (bản: không thấy số bản ở chân trang)

| | |
|---|---|
| Ngày lập | 2026-11-20 |
| Cập nhật lần cuối | 2026-11-20 11:41:09 (+07:00) (cập nhật: Chốt thời gian mục tiêu 10 phút; ghi lượt smoke 1) |
| Người lập | Mo Tran |
| Hệ thống | Ecommerce Lite, staging https://staging-ecommerce-lite.vercel.app/ |
| Thời gian mục tiêu (tham khảo, không cứng) | **khoảng 10 phút** (người dùng chốt theo đề xuất, 2026-11-20) |
| Nguồn case | Chỉ chọn từ test case đã có: [Đăng nhập](dang-nhap/test-case.md) (19 case). Mã TC có thể trùng giữa module nên cột Mã case gốc ghi kèm tên module |
| Case mới đề xuất | Không có |
| Release note | **Chưa có**, nên chưa có dòng nào thuộc phần Theo build |
| Truy vết | Cột Mã case gốc link tới đúng dòng test case gốc; mục "Truy vết" và "Lịch sử tạo và cập nhật" ở cuối file. Chỉ một file này, mốc nằm trong file |
| Tình trạng | Mọi case gốc đang ở trạng thái "Chưa chạy" (đã chạy thật 0); thời gian là **ước lượng**. Test case Đăng nhập dựa trên SRS nháp viết từ quan sát, chưa BA xác nhận: lượt chạy đầu là lượt hiệu chuẩn, case Không đạt thì kiểm lại test case trước khi kết luận trả build |

**Mục đích.** Smoke test trả lời một câu: build này đủ ổn để bắt đầu test sâu chưa? Một case được chọn khi nó hỏng thì việc test khác vô nghĩa hoặc bị chặn, không phải vì nó nhanh hay dễ. Thời gian chỉ là mục tiêu để giữ smoke nông và gọn; nếu một case cần cho mục đích mà làm vượt mục tiêu thì giữ case, chấp nhận vượt và ghi lý do.

**Cách đọc.** Chạy đúng thứ tự bảng để dùng lại phiên: hai case đầu bắt đầu ở trạng thái chưa đăng nhập (dùng cửa sổ ẩn danh), case 3 đăng nhập, case 4 dùng lại phiên vừa đăng nhập, case 5 đăng xuất ở cuối. Mật khẩu đúng điền bằng nút `Use customer` của trang, mật khẩu sai là chuỗi giả; không gõ mật khẩu thật vào tài liệu hay chat.

| # | Smoke case | Mã case gốc | Phần | Vì sao chọn | Thời gian ước tính | Nên tự động hoá? |
|---|---|---|---|---|---|---|
| 1 | Hiện form đăng nhập khi mở trang chủ lúc chưa đăng nhập | [Đăng nhập · TC-001](dang-nhap/test-case.md#tc-001) | Cố định | Hỏng thì không có cửa vào hệ thống, mọi việc test khác bị chặn | 0,5 phút | Nên: chỉ mở trang và kiểm các thành phần |
| 2 | Hiện `Email or password is incorrect.` khi email đúng nhưng mật khẩu sai | [Đăng nhập · TC-004](dang-nhap/test-case.md#tc-004) | Cố định | Hỏng thì mật khẩu sai vẫn vào được (hoặc không báo gì), nên các ca phân quyền sau đó vô nghĩa; chỉ sai một lần | 1,5 phút | Nên: mật khẩu sai là chuỗi giả, không cần `.env` |
| 3 | Đăng nhập thành công và vào cửa hàng khi nhập đúng email và mật khẩu | [Đăng nhập · TC-002](dang-nhap/test-case.md#tc-002) | Cố định | Hỏng thì không ai vào được cửa hàng, mọi việc test cần đăng nhập đều bị chặn | 1 phút | Nên: mật khẩu lấy từ biến môi trường `.env`, không ghi vào script |
| 4 | Vẫn đăng nhập và vào lại cửa hàng khi tải lại trang sau khi đã đăng nhập | [Đăng nhập · TC-007](dang-nhap/test-case.md#tc-007) | Cố định | Hỏng thì phiên mất mỗi lần tải lại, mọi lần test sau phải đăng nhập lại | 1 phút | Nên |
| 5 | Về form đăng nhập và báo đã đăng xuất khi bấm Sign out | [Đăng nhập · TC-008](dang-nhap/test-case.md#tc-008) | Cố định | Hỏng thì không kết thúc được phiên, không đổi được tài khoản để test vai khác | 1 phút | Nên |

**Theo build:** chưa có dòng nào vì chưa có release note. `truy-vet.py kiem` báo cả 19 case ở trạng thái "Mới, chưa chốt" nên chưa có gợi ý chỗ đổi.

**Phạm vi chưa phủ:** chỉ có tính năng Đăng nhập có test case. Các hành trình khác của hệ thống chưa có test case và chưa khám phá: duyệt cửa hàng (Shop), giỏ (Bag) và đặt hàng, xem đơn (My orders), hồ sơ (Profile), cổng quản trị (Dashboard, Products, Orders, Customers). Vai Admin và tab `Create account` cũng chưa có. **Smoke Đạt chỉ bảo đảm đăng nhập dùng được, không bảo đảm các hành trình này.** Đã loại khỏi smoke (để test sâu): bỏ trống ô, email hoa thường, khoảng trắng, bấm nhiều lần, 3 lần sai, `/api/me`, hai tab, Show/Hide, Forgot password, quyền API quản trị.

## Thời gian ước tính (tham khảo)

| Khoản | Phút (ước lượng) |
|---|---|
| 5 smoke case (0,5 + 1,5 + 1 + 1 + 1) | 5 |
| Chuẩn bị chung, không phải case: mở cửa sổ ẩn danh và F12 tab Network, làm một lần | 1 |
| **Tổng** | **6, thấp hơn mục tiêu khoảng 10** |

Ước lượng theo số bước (mỗi bước khoảng 15–20 giây, trang tải 3–5 giây, đăng nhập mất vài giây), chưa đo bằng chạy thật. Không dùng con số này để cắt case.

## Tiêu chí trả build

Chạy theo thứ tự bảng. **Case nào Không đạt thì dừng ngay, trả build, không chạy tiếp.** "Đạt" chỉ xét **ý chính** (theo số bước của case gốc); ý phụ chỉ ghi vào Kết quả thực tế, không dừng. *Phần tách ý chính/ý phụ đã được người dùng duyệt ngày 2026-11-20.*

| Case | Đạt khi (ý chính; ý phụ ghi trong ngoặc) | Không đạt thì dừng vì |
|---|---|---|
| 1. Hiện form đăng nhập | Bước 2: hiện màn hình đăng nhập có ô email, ô mật khẩu, nút `Sign in`; không vào thẳng cửa hàng. (Ý phụ: hai tab, `Remember me`, nút `Show`, liên kết `Forgot password?`) | Không có form thì không đăng nhập được |
| 2. Sai mật khẩu bị từ chối | Bước 5: `POST /api/auth/login` trả 401, hiện `Email or password is incorrect.`, vẫn ở form. (Ý phụ: ô mật khẩu giữ nội dung) | Mật khẩu sai không bị từ chối thì kiểm soát truy cập hỏng |
| 3. Đăng nhập thành công | Bước 4: `POST /api/auth/login` trả 200 và vào cửa hàng Sunny Store. (Ý phụ: nút `Signing in…` ở bước 3, lời chào `WELCOME, SUNNY`, các mục `Shop`, `My orders`, `Profile`, `Bag`) | Không vào được cửa hàng thì không test được gì |
| 4. Tải lại vẫn đăng nhập | Bước 3: không hiện form đăng nhập, vào lại cửa hàng. (Ý phụ: chữ `Loading your store…`) | Mất phiên mỗi lần tải lại làm mọi ca sau gián đoạn |
| 5. Đăng xuất | Bước 4: quay về form đăng nhập, ô email và mật khẩu trống, `POST /api/auth/logout` trả 200. (Ý phụ: thông báo `You have been signed out.` ở bước 3) | Không đăng xuất được thì không đổi tài khoản để test vai khác |

Đạt cả 5 thì nhận build để test sâu.

## Lượt chạy

Mỗi lần chạy smoke cho một build ghi một dòng: `python -X utf8 scripts/truy-vet-smoke.py ghi-luot <dự-án> --build "<số bản ở chân trang>" --status "1=Đạt,2=Không đạt" [--note "…"]` (số là cột # của bảng; case không nêu coi là Chưa chạy; script tự tính nhận hay trả build). Cách chạy: skill `tao-smoke-test`, mục "Chạy smoke".

<!-- LUOT-CHAY:BAT-DAU (tự sinh bởi scripts/truy-vet-smoke.py ghi-luot, không sửa tay) -->
<!-- LUOT-CHAY:KET-THUC -->

## Truy vết về test case và requirement

Bảng tự sinh khi chốt (đừng sửa tay). Chỉ mã có điểm nhảy trong tài liệu nguồn mới có link.

<!-- TRUY-VET:BAT-DAU (tự sinh bởi scripts/truy-vet-smoke.py, không sửa tay) -->
| # | Test case gốc | Requirement mà test case dựa vào |
|---|---|---|
| 1 | [Đăng nhập · TC-001](dang-nhap/test-case.md#tc-001) | [S01-AC01](../../srs/ecommerce-lite/dang-nhap.md#login-s01-ac01) Mở trang khi chưa đăng nhập |
| 2 | [Đăng nhập · TC-004](dang-nhap/test-case.md#tc-004) | [M03](../../srs/ecommerce-lite/dang-nhap.md#login-m03) Email hoặc mật khẩu sai<br>[R03](../../srs/ecommerce-lite/dang-nhap.md#login-r03) Email và mật khẩu<br>[S01-AC06](../../srs/ecommerce-lite/dang-nhap.md#login-s01-ac06) Mật khẩu sai |
| 3 | [Đăng nhập · TC-002](dang-nhap/test-case.md#tc-002) | [S01-AC04](../../srs/ecommerce-lite/dang-nhap.md#login-s01-ac04) Đăng nhập thành công |
| 4 | [Đăng nhập · TC-007](dang-nhap/test-case.md#tc-007) | [S03-AC01](../../srs/ecommerce-lite/dang-nhap.md#login-s03-ac01) Tải lại trang khi đã đăng nhập |
| 5 | [Đăng nhập · TC-008](dang-nhap/test-case.md#tc-008) | [M05](../../srs/ecommerce-lite/dang-nhap.md#login-m05) Đăng xuất<br>[S03-AC02](../../srs/ecommerce-lite/dang-nhap.md#login-s03-ac02) Đăng xuất |
<!-- TRUY-VET:KET-THUC -->

## Khi requirement hoặc test case đổi

Chạy `python -X utf8 scripts/truy-vet-smoke.py kiem <dự-án>` (chỉ đọc, in vài dòng). Case báo "Cần xem lại" hoặc "Test case đã sửa": đọc lại test case gốc rồi giữ, đổi hoặc bỏ; sửa thẳng bảng trong file này, rồi `python -X utf8 scripts/truy-vet-smoke.py chot <dự-án> -m "đã làm gì"`. Case mới chưa có test case gốc thì viết test case gốc trước rồi link.

## Lịch sử tạo và cập nhật

<!-- LICH-SU:BAT-DAU (tự sinh bởi scripts/truy-vet-smoke.py, không sửa tay) -->
| Thời điểm | Việc | Người | Nội dung | Số case · tổng phút (ước lượng) | Commit |
|---|---|---|---|---|---|
| 2026-11-20 11:41:09 (+07:00) | Cập nhật | Mo Tran | Chốt thời gian mục tiêu 10 phút; ghi lượt smoke 1 | 5 case · 5 phút | `29192bc` + sửa chưa commit |
| 2026-11-20 11:38:13 (+07:00) | Cập nhật | Mo Tran | Người dùng duyệt tách ý chính/ý phụ trong tiêu chí trả build | 5 case · 5 phút | `29192bc` + sửa chưa commit |
| 2026-11-20 11:36:33 (+07:00) | Tạo | Mo Tran | Lập bộ smoke đầu tiên: 5 case đăng nhập | 5 case · 5 phút | `29192bc` + sửa chưa commit |
<!-- LICH-SU:KET-THUC -->
<!-- SMOKE-MOC: {"case":{"dang-nhap/TC-001":{"r":"6debb30799af","ma":{"S01-AC01":["14c806262ad3","da39a3ee5e6b"]}},"dang-nhap/TC-004":{"r":"7dbe2b5b2b4d","ma":{"M03":["b9aaf5dad995","da39a3ee5e6b"],"R03":["3b61d9f0648d","da39a3ee5e6b"],"S01-AC06":["c0bb56f4ae60","da39a3ee5e6b"]}},"dang-nhap/TC-002":{"r":"549bc203a2e9","ma":{"S01-AC04":["f1635a27e1a1","da39a3ee5e6b"]}},"dang-nhap/TC-007":{"r":"f9fcea9147c7","ma":{"S03-AC01":["cfa4a6bd9d13","da39a3ee5e6b"]}},"dang-nhap/TC-008":{"r":"8316f1ad6acd","ma":{"M05":["8d288d6d92b4","da39a3ee5e6b"],"S03-AC02":["64da7bcae8cf","da39a3ee5e6b"]}}}} -->
