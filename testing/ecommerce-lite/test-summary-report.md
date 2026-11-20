# Báo cáo tổng kết kiểm thử

> File tự sinh bằng `scripts/build_docs.py` từ các lượt chạy, bug và truy vết; đừng sửa tay. Quyết định của người test và người duyệt nằm ở `testing/ecommerce-lite/duyet-build.json` (điền trên trang HTML rồi tải file về). Bản dễ xem và có nút in PDF: `test-summary-report.html`.

## 1. Thông tin chung

| Mục | Nội dung |
|---|---|
| Dự án | ecommerce-lite |
| Build | Không có số bản ở chân trang |
| Môi trường | https://staging-ecommerce-lite.vercel.app |
| Thời gian test | 2026-11-20 11:49:41 đến 2026-11-20 12:04:03 |
| Người viết báo cáo | Mo Tran |
| Người test | Mo Tran: Tự động (Playwright), Script Playwright (run_tests.py) (Smoke test (lượt 4); Test case Đăng nhập (lượt 1)) |
| Phạm vi | Smoke, regression và test case theo từng tính năng: Đăng nhập, Quên mật khẩu |

## 2. Kết luận

**Tình trạng theo số liệu.** Tổng 33 test case của 2 tính năng: 19 đã có kết luận (58%), trong đó 19 Đạt, 0 Đạt kèm lỗi, 0 Không đạt; 0 bị chặn hoặc chưa kết luận được, 0 bỏ qua, 14 chưa chạy. 0 bug được ghi nhận trong các lượt của build này (tổng 0 bug đã ghi).

- Smoke test: Nhận build: cả 5 case smoke đăng nhập đều Đạt khi chạy bằng script ngày 2026-11-20, mỗi case có ảnh làm bằng chứng. Smoke chỉ bảo đảm đăng nhập dùng được.
- Test case Đăng nhập: Đạt toàn bộ: 19 trên 19 test case đăng nhập đều Đạt khi chạy bằng script ngày 2026-11-20, mỗi case có ảnh làm bằng chứng. Không có lỗi nào cần báo.

**Đề xuất của người test** (nhận build / không nhận / nhận có điều kiện):

| Mục | Nội dung |
|---|---|
| Đề xuất | (chưa điền) |
| Lý do | (chưa điền) |
| Ngày | (chưa điền) |

## 3. Kết quả theo tính năng

Mỗi test case lấy kết quả mới nhất trong các lượt của build này (smoke, regression, test case tính năng). Tỉ lệ đạt tính trên số đã có kết luận.

| Tính năng | Tổng | Đạt | Đạt kèm lỗi | Không đạt | Bị chặn / Không kết luận | Bỏ qua | Chưa chạy | Đã chạy | Tỉ lệ đạt |
|---|---|---|---|---|---|---|---|---|---|
| Đăng nhập | 19 | 19 | 0 | 0 | 0 | 0 | 0 | 100% | 100% |
| Quên mật khẩu | 14 | 0 | 0 | 0 | 0 | 0 | 14 | 0% | — |

## 4. Kết quả theo bộ test

| Bộ test | Lượt | Thời điểm | Kết quả | Kết luận | Trang kết quả |
|---|---|---|---|---|---|
| Smoke test | 4 | 2026-11-20 11:57:37 | 5 Đạt | Nhận build | [mở](smoke-ket-qua.html) |
| Test case Đăng nhập | 1 | 2026-11-20 12:04:03 | 19 Đạt | Đạt toàn bộ | [mở](dang-nhap/ket-qua-test-case.html) |

## 5. Bug

Chưa có bug nào được ghi.

Trạng thái bug đọc từ mục Trạng thái trong file bug, do người test chốt sau khi re-test (skill lap-ke-hoach-retest). Bug ghi "Chưa ghi" là chưa ai chốt trong kho; trạng thái chính thức nằm ở công cụ của team.

## 6. Độ phủ requirement

| Tính năng | Mã requirement | Mã chưa có test case | Trạng thái test case | Truy vết |
|---|---|---|---|---|
| Đăng nhập | 28 trong SRS, 2 câu trả lời (TL). Test case: 19 | không có | Còn đúng 19 | [mở](dang-nhap/truy-vet.html) |
| Quên mật khẩu | 13 trong SRS, 0 câu trả lời (TL). Test case: 14 | không có | Còn đúng 14 | [mở](quen-mat-khau/truy-vet.html) |

## 7. Rủi ro còn lại

**Chưa có kết quả và vì sao**

| Bộ test | Case | Trạng thái | Lý do |
|---|---|---|---|
| Smoke test | Các hành trình ngoài đăng nhập: duyệt cửa hàng, giỏ và đặt hàng, xem đơn, hồ sơ, cổng quản trị | Chưa có test case | Mới khám phá và viết test case cho tính năng Đăng nhập; các hành trình này chưa khám phá nên smoke không kiểm được. |
| Smoke test | 14 test case đăng nhập ngoài smoke (TC-003, 005, 006, 009 đến 019) | Chưa chạy | Không thuộc smoke, để test sâu sau khi nhận build. |
| Test case Đăng nhập | Vai Admin, tab Create account, hạn phiên, giới hạn số lần sai, thời gian chờ đăng nhập | Chưa có test case | Dự án chưa làm giới hạn lần sai, hạn phiên (người dùng chốt 2026-11-20); vai Admin thiếu tài khoản; Create account thuộc tính năng đăng ký chưa khám phá. |

- **Phạm vi smoke hẹp** (Smoke test). Smoke Đạt chỉ cho biết người dùng đăng nhập, giữ phiên và đăng xuất được. Nếu mua hàng hoặc xem đơn hỏng thì lượt này không phát hiện; chưa kiểm.
- **Test case chưa được BA xác nhận** (Smoke test). Test case đăng nhập dựa trên SRS nháp viết từ quan sát hệ thống, nên kết quả mong đợi là hành vi hiện tại, chưa phải yêu cầu chính thức.
- **Gõ quá sớm làm ô mật khẩu bị xóa (chỉ ảnh hưởng cách chạy script)** (Smoke test). Lượt 2 và 3 thấy ô mật khẩu trống sau lần sai vì script gõ ngay khi trang vừa hiện, trước lúc trang kiểm phiên xong (GET /api/me) và vẽ lại form. Đo riêng: chờ kiểm phiên xong rồi mới gõ thì ô giữ nguyên 12 ký tự; kiểm tay cũng giữ nguyên. Người dùng thật không gõ nhanh đến mức đó. Lượt 4 chạy lại với script đã chờ.
- **Ảnh bằng chứng che khung tài khoản mẫu** (Smoke test). Trang đăng nhập hiện mật khẩu mẫu, nên script làm mờ khung đó trước khi chụp. Video không quay cho case Đạt, bằng chứng của case Đạt là ảnh.
- **Test case chưa được BA xác nhận** (Test case Đăng nhập). Test case dựa trên SRS nháp viết từ quan sát hệ thống, nên "Đạt" nghĩa là hệ thống khớp hành vi đã quan sát, chưa phải khớp yêu cầu chính thức. Nếu BA có yêu cầu khác (ví dụ báo lỗi định dạng email, Remember me) thì phải bổ sung test case.
- **Tác động của cách chạy script** (Test case Đăng nhập). Script phải chờ trang kiểm phiên xong rồi mới gõ; gõ sớm hơn làm ô mật khẩu bị xóa. Người dùng thật không gõ nhanh đến vậy nên không coi là lỗi, nhưng nếu hệ thống đổi cách kiểm phiên thì kết quả script có thể đổi.
- **Hệ thống chưa giới hạn số lần sai** (Test case Đăng nhập). Đã gửi tổng cộng khoảng 9 lần đăng nhập sai bằng script (trần người dùng chốt là 10), không thấy khóa. Nếu sau này dự án làm giới hạn thì test case về lần sai cần viết lại.

## 8. Đề xuất bước tiếp theo

- Smoke test: Đề xuất nhận build để test sâu đăng nhập. Quyết định nhận hay trả build là của người test hoặc PO.
- Test case Đăng nhập: Đề xuất coi tính năng Đăng nhập đạt ở mức hành vi đã quan sát; bước tiếp theo là regression hoặc khám phá các tính năng khác (cửa hàng, giỏ, đơn). Quyết định nhận hay trả build là của người test hoặc PO.

## 9. Duyệt build

Người duyệt điền trên trang HTML (mục 9), tải file `duyet-build.json`, đặt vào `testing/ecommerce-lite/` rồi chạy lại `python -X utf8 scripts/build_docs.py`.

| Mục | Nội dung |
|---|---|
| Người duyệt | (chưa điền) |
| Chức danh | (chưa điền) |
| Quyết định | (chưa điền) |
| Điều kiện kèm theo | (chưa điền) |
| Ghi chú | (chưa điền) |
| Ngày duyệt | (chưa điền) |

## Phụ lục: trang kết quả từng lượt

- [Smoke test](smoke-ket-qua.html)
- [Test case Đăng nhập](dang-nhap/ket-qua-test-case.html)
