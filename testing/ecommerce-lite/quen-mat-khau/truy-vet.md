# Truy vết — Quên mật khẩu

*File này do `scripts/truy-vet.py` tự sinh, đừng sửa tay. Muốn đổi thì sửa nguồn rồi chạy lại script.*

| | |
|---|---|
| Lần chạy gần nhất | 2026-11-20 17:27:06 (+07:00) (chốt mốc mới) |
| Requirement | srs/ecommerce-lite/quen-mat-khau.md (cập nhật 2026-11-20); bảng soát (cập nhật ?), câu trả lời đến ? |
| Test case (đã gồm checklist) | [test-case.md](test-case.md) |
| Mốc đã chốt | 2026-11-20 17:27:06 (+07:00) (khi đó: SRS 2026-11-20, bảng soát ?, TL đến ?) |

## 1. Tóm tắt
- Mã requirement: 13 trong SRS, 0 câu trả lời (TL). Test case: 14.
- Trạng thái test case: Còn đúng 14
- Mã requirement đã đổi so với mốc đã chốt: không có; mã mới: không có.
- Mã SRS chưa có test case nào: không có.
- Test case đã bỏ khỏi file: không có.
- Vấn đề khác: không có

## 2. Khi requirement đổi, làm gì
1. Sửa SRS hoặc ghi câu trả lời mới của BA vào bảng soát (như mọi lần).
2. Chạy `python -X utf8 scripts/truy-vet.py kiem ecommerce-lite quen-mat-khau`. Script liệt kê mã đã đổi và các test case chuyển sang **Cần xem lại**.
3. Mở từng test case đó (bảng 6 dưới đây), sửa test case cho khớp (checklist nằm chung bảng).
4. Chạy `python -X utf8 scripts/truy-vet.py chot ecommerce-lite quen-mat-khau -m "đã làm gì, vì sao"`. Script ghi một dòng lịch sử và chốt mốc mới.
5. Muốn xem từng chữ đã đổi, dùng lịch sử git (commit sau mỗi lần chốt).

## 3. Bảng tra mã
Mã trong cột Nguồn của checklist và test case bỏ tiền tố `FORGOT-`. `S01-AC02` là story 1, tình huống 2; `R` là quy tắc; `M` là thông báo; `TL` là câu trả lời của BA.

| Mã | Tên ngắn | Nguyên văn (rút gọn) | Mở ở đâu |
|---|---|---|---|
| R01 | Mã OTP | Gồm 6 chữ số | [quen-mat-khau.md dòng 74](../../../srs/ecommerce-lite/quen-mat-khau.md#L74) |
| R02 | Mã OTP | Có hiệu lực trong 5 phút | [quen-mat-khau.md dòng 75](../../../srs/ecommerce-lite/quen-mat-khau.md#L75) |
| R03 | Mật khẩu mới | Từ 8 đến 16 ký tự | [quen-mat-khau.md dòng 76](../../../srs/ecommerce-lite/quen-mat-khau.md#L76) |
| R04 | Mật khẩu mới | Bao gồm chữ hoa, chữ thường, số và ký tự đặc biệt | [quen-mat-khau.md dòng 77](../../../srs/ecommerce-lite/quen-mat-khau.md#L77) |
| R05 | Mật khẩu mới | Không được trùng với 5 mật khẩu gần nhất | [quen-mat-khau.md dòng 78](../../../srs/ecommerce-lite/quen-mat-khau.md#L78) |
| S01-AC01 | Nhận OTP khi nhập email đã đăng ký | Gửi mã OTP gồm 6 chữ số đến email đã đăng ký. OTP có hiệu lực trong 5 phút | [quen-mat-khau.md dòng 37](../../../srs/ecommerce-lite/quen-mat-khau.md#L37) |
| S02-AC01 | Chuyển đến màn hình tạo mật khẩu mới kh… | Chuyển đến màn hình tạo mật khẩu mới | [quen-mat-khau.md dòng 46](../../../srs/ecommerce-lite/quen-mat-khau.md#L46) |
| S03-AC01 | Chấp nhận mật khẩu mới khi thỏa mọi quy… | Mật khẩu mới được chấp nhận (kết quả sau đó: `FORGOT-S04-AC01`) | [quen-mat-khau.md dòng 55](../../../srs/ecommerce-lite/quen-mat-khau.md#L55) |
| S03-AC02 | Không chấp nhận mật khẩu mới ngắn hơn 8… | Mật khẩu không được chấp nhận. Tài liệu không nêu thông báo (→ `FORGOT-Q06`) | [quen-mat-khau.md dòng 56](../../../srs/ecommerce-lite/quen-mat-khau.md#L56) |
| S03-AC03 | Không chấp nhận mật khẩu mới thiếu một… | Mật khẩu không được chấp nhận. Tài liệu không nêu thông báo (→ `FORGOT-Q06`) | [quen-mat-khau.md dòng 57](../../../srs/ecommerce-lite/quen-mat-khau.md#L57) |
| S03-AC04 | Không chấp nhận mật khẩu mới trùng một… | Mật khẩu không được chấp nhận. Tài liệu không nêu thông báo (→ `FORGOT-Q06`, `FORGOT-Q07`) | [quen-mat-khau.md dòng 58](../../../srs/ecommerce-lite/quen-mat-khau.md#L58) |
| S04-AC01 | Hiển thị thông báo thành công sau khi đ… | Hiển thị thông báo thành công (nguyên văn chưa rõ, → `FORGOT-Q08`) | [quen-mat-khau.md dòng 67](../../../srs/ecommerce-lite/quen-mat-khau.md#L67) |
| S04-AC02 | Yêu cầu đăng nhập lại sau khi đổi mật k… | Yêu cầu người dùng đăng nhập lại (cách thể hiện chưa rõ, → `FORGOT-Q08`) | [quen-mat-khau.md dòng 68](../../../srs/ecommerce-lite/quen-mat-khau.md#L68) |

## 4. Yêu cầu theo BA của từng mã SRS
Gom từ bảng soát (mục 5, 6) để mỗi mã SRS có chỗ ghi điều BA trả lời, kể cả khi SRS (bản quan sát hệ thống 1.3.0) ghi khác. Test case viết theo cột "Theo BA"; chỗ có ⚠️ là nghi lỗi của hệ thống, chưa phải lỗi đã xác nhận. SRS không bị sửa.

| Mã | Tên ngắn | Theo BA (hoặc suy ra) | Hệ thống 1.3.0 hiện tại | Còn mở |
|---|---|---|---|---|
| [R01](../../../srs/ecommerce-lite/quen-mat-khau.md#L74) | Mã OTP | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [R02](../../../srs/ecommerce-lite/quen-mat-khau.md#L75) | Mã OTP | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [R03](../../../srs/ecommerce-lite/quen-mat-khau.md#L76) | Mật khẩu mới | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [R04](../../../srs/ecommerce-lite/quen-mat-khau.md#L77) | Mật khẩu mới | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [R05](../../../srs/ecommerce-lite/quen-mat-khau.md#L78) | Mật khẩu mới | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [S01-AC01](../../../srs/ecommerce-lite/quen-mat-khau.md#L37) | Nhận OTP khi nhập email đã đăng ký | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [S02-AC01](../../../srs/ecommerce-lite/quen-mat-khau.md#L46) | Chuyển đến màn hình tạo mật khẩu mới kh… | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [S03-AC01](../../../srs/ecommerce-lite/quen-mat-khau.md#L55) | Chấp nhận mật khẩu mới khi thỏa mọi quy… | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [S03-AC02](../../../srs/ecommerce-lite/quen-mat-khau.md#L56) | Không chấp nhận mật khẩu mới ngắn hơn 8… | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [S03-AC03](../../../srs/ecommerce-lite/quen-mat-khau.md#L57) | Không chấp nhận mật khẩu mới thiếu một… | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [S03-AC04](../../../srs/ecommerce-lite/quen-mat-khau.md#L58) | Không chấp nhận mật khẩu mới trùng một… | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [S04-AC01](../../../srs/ecommerce-lite/quen-mat-khau.md#L67) | Hiển thị thông báo thành công sau khi đ… | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |
| [S04-AC02](../../../srs/ecommerce-lite/quen-mat-khau.md#L68) | Yêu cầu đăng nhập lại sau khi đổi mật k… | Chưa có câu trả lời riêng của BA; theo SRS | Không có điểm khác đã biết | — |

## 5. Từ requirement tới test case
| Mã | Tên ngắn | Trạng thái requirement | Test case |
|---|---|---|---|
| [R01](../../../srs/ecommerce-lite/quen-mat-khau.md#L74) | Mã OTP | Không đổi | 1: [TC-001](test-case.md#tc-001) |
| [R02](../../../srs/ecommerce-lite/quen-mat-khau.md#L75) | Mã OTP | Không đổi | 2: [TC-001](test-case.md#tc-001), [TC-002](test-case.md#tc-002) |
| [R03](../../../srs/ecommerce-lite/quen-mat-khau.md#L76) | Mật khẩu mới | Không đổi | 5: [TC-003](test-case.md#tc-003), [TC-006](test-case.md#tc-006), [TC-007](test-case.md#tc-007), [TC-013](test-case.md#tc-013), [TC-014](test-case.md#tc-014) |
| [R04](../../../srs/ecommerce-lite/quen-mat-khau.md#L77) | Mật khẩu mới | Không đổi | 5: [TC-003](test-case.md#tc-003), [TC-008](test-case.md#tc-008), [TC-009](test-case.md#tc-009), [TC-010](test-case.md#tc-010), [TC-011](test-case.md#tc-011) |
| [R05](../../../srs/ecommerce-lite/quen-mat-khau.md#L78) | Mật khẩu mới | Không đổi | 2: [TC-003](test-case.md#tc-003), [TC-012](test-case.md#tc-012) |
| [S01-AC01](../../../srs/ecommerce-lite/quen-mat-khau.md#L37) | Nhận OTP khi nhập email đã đăng ký | Không đổi | 1: [TC-001](test-case.md#tc-001) |
| [S02-AC01](../../../srs/ecommerce-lite/quen-mat-khau.md#L46) | Chuyển đến màn hình tạo mật khẩu mới kh… | Không đổi | 1: [TC-002](test-case.md#tc-002) |
| [S03-AC01](../../../srs/ecommerce-lite/quen-mat-khau.md#L55) | Chấp nhận mật khẩu mới khi thỏa mọi quy… | Không đổi | 3: [TC-003](test-case.md#tc-003), [TC-013](test-case.md#tc-013), [TC-014](test-case.md#tc-014) |
| [S03-AC02](../../../srs/ecommerce-lite/quen-mat-khau.md#L56) | Không chấp nhận mật khẩu mới ngắn hơn 8… | Không đổi | 2: [TC-006](test-case.md#tc-006), [TC-007](test-case.md#tc-007) |
| [S03-AC03](../../../srs/ecommerce-lite/quen-mat-khau.md#L57) | Không chấp nhận mật khẩu mới thiếu một… | Không đổi | 4: [TC-008](test-case.md#tc-008), [TC-009](test-case.md#tc-009), [TC-010](test-case.md#tc-010), [TC-011](test-case.md#tc-011) |
| [S03-AC04](../../../srs/ecommerce-lite/quen-mat-khau.md#L58) | Không chấp nhận mật khẩu mới trùng một… | Không đổi | 1: [TC-012](test-case.md#tc-012) |
| [S04-AC01](../../../srs/ecommerce-lite/quen-mat-khau.md#L67) | Hiển thị thông báo thành công sau khi đ… | Không đổi | 1: [TC-004](test-case.md#tc-004) |
| [S04-AC02](../../../srs/ecommerce-lite/quen-mat-khau.md#L68) | Yêu cầu đăng nhập lại sau khi đổi mật k… | Không đổi | 1: [TC-005](test-case.md#tc-005) |

## 6. Từ test case tới requirement
| Mã | Tình huống | Ưu tiên | Mã requirement dùng | Trạng thái | Tạo | Sửa lần cuối | Tự động hóa |
|---|---|---|---|---|---|---|---|
| [TC-001](test-case.md#tc-001) | Nhận được email chứa OTP gồm 6 chữ số khi nhập email đã đăng ký để đặt lại mật khẩu | Cao | [R01](../../../srs/ecommerce-lite/quen-mat-khau.md#L74) (Mã OTP), [R02](../../../srs/ecommerce-lite/quen-mat-khau.md#L75) (Mã OTP), [S01-AC01](../../../srs/ecommerce-lite/quen-mat-khau.md#L37) (Nhận OTP khi nhập email đã đăng ký) | Còn đúng | 2026-11-20 | 2026-11-20 | Chưa có |
| [TC-002](test-case.md#tc-002) | Chuyển đến màn hình tạo mật khẩu mới khi nhập đúng OTP còn hạn | Cao | [R02](../../../srs/ecommerce-lite/quen-mat-khau.md#L75) (Mã OTP), [S02-AC01](../../../srs/ecommerce-lite/quen-mat-khau.md#L46) (Chuyển đến màn hình tạo mật khẩu mới kh…) | Còn đúng | 2026-11-20 | 2026-11-20 | Chưa có |
| [TC-003](test-case.md#tc-003) | Chấp nhận mật khẩu mới và đăng nhập được bằng mật khẩu đó khi mật khẩu thỏa mọi quy tắc | Cao | [R03](../../../srs/ecommerce-lite/quen-mat-khau.md#L76) (Mật khẩu mới), [R04](../../../srs/ecommerce-lite/quen-mat-khau.md#L77) (Mật khẩu mới), [R05](../../../srs/ecommerce-lite/quen-mat-khau.md#L78) (Mật khẩu mới), [S03-AC01](../../../srs/ecommerce-lite/quen-mat-khau.md#L55) (Chấp nhận mật khẩu mới khi thỏa mọi quy…) | Còn đúng | 2026-11-20 | 2026-11-20 | Chưa có |
| [TC-004](test-case.md#tc-004) | Hiển thị thông báo thành công khi đổi mật khẩu thành công | Cao | [S04-AC01](../../../srs/ecommerce-lite/quen-mat-khau.md#L67) (Hiển thị thông báo thành công sau khi đ…) | Còn đúng | 2026-11-20 | 2026-11-20 | Chưa có |
| [TC-005](test-case.md#tc-005) | Yêu cầu đăng nhập lại khi vừa đổi mật khẩu thành công | Cao | [S04-AC02](../../../srs/ecommerce-lite/quen-mat-khau.md#L68) (Yêu cầu đăng nhập lại sau khi đổi mật k…) | Còn đúng | 2026-11-20 | 2026-11-20 | Chưa có |
| [TC-006](test-case.md#tc-006) | Không chấp nhận mật khẩu mới khi chỉ có 7 ký tự (ngay dưới biên 8) | Cao | [R03](../../../srs/ecommerce-lite/quen-mat-khau.md#L76) (Mật khẩu mới), [S03-AC02](../../../srs/ecommerce-lite/quen-mat-khau.md#L56) (Không chấp nhận mật khẩu mới ngắn hơn 8…) | Còn đúng | 2026-11-20 | 2026-11-20 | Chưa có |
| [TC-007](test-case.md#tc-007) | Không chấp nhận mật khẩu mới khi có 17 ký tự (ngay trên biên 16) | Cao | [R03](../../../srs/ecommerce-lite/quen-mat-khau.md#L76) (Mật khẩu mới), [S03-AC02](../../../srs/ecommerce-lite/quen-mat-khau.md#L56) (Không chấp nhận mật khẩu mới ngắn hơn 8…) | Còn đúng | 2026-11-20 | 2026-11-20 | Chưa có |
| [TC-008](test-case.md#tc-008) | Không chấp nhận mật khẩu mới khi thiếu chữ hoa | Cao | [R04](../../../srs/ecommerce-lite/quen-mat-khau.md#L77) (Mật khẩu mới), [S03-AC03](../../../srs/ecommerce-lite/quen-mat-khau.md#L57) (Không chấp nhận mật khẩu mới thiếu một…) | Còn đúng | 2026-11-20 | 2026-11-20 | Chưa có |
| [TC-009](test-case.md#tc-009) | Không chấp nhận mật khẩu mới khi thiếu chữ thường | Cao | [R04](../../../srs/ecommerce-lite/quen-mat-khau.md#L77) (Mật khẩu mới), [S03-AC03](../../../srs/ecommerce-lite/quen-mat-khau.md#L57) (Không chấp nhận mật khẩu mới thiếu một…) | Còn đúng | 2026-11-20 | 2026-11-20 | Chưa có |
| [TC-010](test-case.md#tc-010) | Không chấp nhận mật khẩu mới khi thiếu số | Cao | [R04](../../../srs/ecommerce-lite/quen-mat-khau.md#L77) (Mật khẩu mới), [S03-AC03](../../../srs/ecommerce-lite/quen-mat-khau.md#L57) (Không chấp nhận mật khẩu mới thiếu một…) | Còn đúng | 2026-11-20 | 2026-11-20 | Chưa có |
| [TC-011](test-case.md#tc-011) | Không chấp nhận mật khẩu mới khi thiếu ký tự đặc biệt | Cao | [R04](../../../srs/ecommerce-lite/quen-mat-khau.md#L77) (Mật khẩu mới), [S03-AC03](../../../srs/ecommerce-lite/quen-mat-khau.md#L57) (Không chấp nhận mật khẩu mới thiếu một…) | Còn đúng | 2026-11-20 | 2026-11-20 | Chưa có |
| [TC-012](test-case.md#tc-012) | Không chấp nhận mật khẩu mới khi trùng mật khẩu ngay trước mật khẩu hiện tại | Cao | [R05](../../../srs/ecommerce-lite/quen-mat-khau.md#L78) (Mật khẩu mới), [S03-AC04](../../../srs/ecommerce-lite/quen-mat-khau.md#L58) (Không chấp nhận mật khẩu mới trùng một…) | Còn đúng | 2026-11-20 | 2026-11-20 | Chưa có |
| [TC-013](test-case.md#tc-013) | Chấp nhận mật khẩu mới khi có đúng 8 ký tự (biên dưới) | Trung bình | [R03](../../../srs/ecommerce-lite/quen-mat-khau.md#L76) (Mật khẩu mới), [S03-AC01](../../../srs/ecommerce-lite/quen-mat-khau.md#L55) (Chấp nhận mật khẩu mới khi thỏa mọi quy…) | Còn đúng | 2026-11-20 | 2026-11-20 | Chưa có |
| [TC-014](test-case.md#tc-014) | Chấp nhận mật khẩu mới khi có đúng 16 ký tự (biên trên) | Trung bình | [R03](../../../srs/ecommerce-lite/quen-mat-khau.md#L76) (Mật khẩu mới), [S03-AC01](../../../srs/ecommerce-lite/quen-mat-khau.md#L55) (Chấp nhận mật khẩu mới khi thỏa mọi quy…) | Còn đúng | 2026-11-20 | 2026-11-20 | Chưa có |

## 7. Lịch sử thay đổi
Ghi mỗi lần chạy `chot`. **Thời điểm chốt** là giờ máy lúc bấm chốt (kèm múi giờ), không phải giờ BA trả lời hay giờ requirement đổi; mốc cũ chỉ có ngày thì ghi "không rõ giờ". **Commit gốc** là commit đang đứng lúc chốt ("+ sửa chưa commit" nghĩa là còn thay đổi chưa commit); muốn xem từng chữ đã đổi, dùng git. **Ngày BA trả lời** chỉ ghi khi biết.

| Thời điểm chốt (giờ máy) | Commit gốc | Ngày BA trả lời | Đối tượng | Nội dung | Dựa trên | Mã requirement đổi | Test case mới / sửa / bỏ |
|---|---|---|---|---|---|---|---|
| 2026-11-20 17:27:06 (+07:00) | `f59f280` + sửa chưa commit | — | checklist, test-case | Lập test case đầu tiên từ SRS FORGOT (14 TC, chỉ phần đã rõ) | SRS 2026-11-20; bảng soát ?; TL đến ? | R01 (mới), R02 (mới), R03 (mới), R04 (mới), R05 (mới), S01-AC01 (mới), S02-AC01 (mới), S03-AC01 (mới), S03-AC02 (mới), S03-AC03 (mới), S03-AC04 (mới), S04-AC01 (mới), S04-AC02 (mới) | mới 14; sửa 0; bỏ 0 |
