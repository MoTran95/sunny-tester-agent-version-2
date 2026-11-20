# Câu hỏi cho BA — Đăng nhập (Ecommerce Lite)

| | |
|---|---|
| Ngày soạn | 2026-11-20 |
| Dùng để | Gửi BA. Mỗi câu có tình huống thật, câu hỏi, cách mình đang hiểu và lý do hỏi |
| Nguồn | [SRS Đăng nhập](../../../srs/ecommerce-lite/dang-nhap.md) và [bảng phân tích requirement](bang-soat-requirement.md). Mã cũ ghi ở cuối mỗi câu để tra chéo |
| Cách dùng | Gửi **Phần A** trước. **Phần B** gom hỏi một lần sau. **Phần C** là việc mình tự kiểm tra trên hệ thống, chưa cần hỏi BA |
| Tình trạng | Chưa gửi BA. Chưa có câu trả lời nào |

## Đọc trước 1 phút
Màn hình đăng nhập của cửa hàng Ecommerce Lite cho khách vào bằng email và mật khẩu, giữ phiên khi tải lại trang và cho đăng xuất. Hiện chưa có tài liệu yêu cầu chính thức: mọi điều dưới đây là mình **quan sát được** trên môi trường thử, chưa có xác nhận. Mình chưa biết nhóm dùng từ nào cho các khái niệm, nên giữ nguyên chữ trên màn hình trong dấu ngoặc kép.

**Quy ước từ ngữ trong file này:** chữ đang hiện trên màn hình để trong dấu ngoặc kép; "phiên" là khoảng thời gian người dùng còn đăng nhập sau khi vào được.

---

# Phần A. Hỏi ngay (4 câu)

Các câu này làm đổi kết quả đúng, nên cần trả lời sớm.

## A1. Đăng nhập sai bao nhiêu lần thì bị chặn?

**Người trả lời gợi ý:** BA

Mình thử đăng nhập sai ba lần liên tiếp: một lần sai mật khẩu, một lần email không có thật, một lần đúng mật khẩu nhưng đổi hoa thành thường một chữ. Cả ba lần đều chỉ hiện "Email or password is incorrect.". Đăng nhập đúng ngay sau đó vẫn vào được. Mình dừng ở ba lần vì sợ khóa cả môi trường thử.

**Hỏi:** Anh/chị cho mình hỏi: hệ thống có chặn đăng nhập khi sai nhiều lần không? Nếu có thì sai mấy lần, chặn bao lâu, và đăng nhập đúng xen giữa có đếm lại từ đầu không?

**Mình đang hiểu:** mình chưa biết gì về giới hạn này, chưa đoán con số nào.

**Vì sao hỏi:** nếu có giới hạn thì phải có ca test lần sai thứ N và câu thông báo chặn; nếu không có thì không cần.

**Anh/chị chọn:**

- [ ] Có giới hạn: ___ lần sai, chặn ___ phút
- [ ] Không có giới hạn
- [ ] Khác: ______

**Câu trả lời của BA:** ______

*Mã cũ: LOGIN-S02-AC04, LOGIN-Q01.*

---

## A2. Đăng nhập xong thì giữ được bao lâu?

**Người trả lời gợi ý:** BA

Sau khi đăng nhập đúng, trình duyệt giữ một cookie phiên có ngày hết hạn. Mình chưa đo con số chính xác và chưa chờ cho đến lúc hết hạn.

**Hỏi:** Anh/chị cho mình hỏi: yêu cầu là phiên giữ bao lâu, và khi hết hạn thì người dùng thấy gì?

**Mình đang hiểu:** mình chưa biết con số. Mình đoán hết hạn thì quay về form đăng nhập giống như khi bấm "Sign out", nhưng đây chỉ là đoán.

**Vì sao hỏi:** cần con số để biết ca nào kiểm hết hạn và chờ bao lâu.

**Câu trả lời của BA:** ______

*Mã cũ: LOGIN-R03, LOGIN-Q03.*

---

## A3. Ô "Remember me on this device" để làm gì?

**Người trả lời gợi ý:** BA và Dev

Mình đăng nhập hai lần, một lần tích ô này và một lần không. Cả hai lần đều thành công, cùng một cookie phiên và thời hạn cookie giống nhau. Mình không thấy ô này làm khác đi điều gì.

**Hỏi:** Anh/chị cho mình hỏi: tích ô này thì hệ thống phải làm khác thế nào so với không tích?

**Mình đang hiểu:** mình đoán tích thì phiên giữ lâu hơn, nhưng hệ thống hiện chưa làm vậy.

**Vì sao hỏi:** nếu ô này phải kéo dài phiên mà hệ thống không làm thì đó là lỗi cần báo; nếu ô này chưa dùng thì không cần test.

**Anh/chị chọn:**

- [ ] Tích thì phiên giữ lâu hơn
- [ ] Tích thì chỉ nhớ email cho lần sau
- [ ] Chưa làm gì (ô này chưa hoạt động ở bản thử)
- [ ] Khác: ______

**Câu trả lời của BA:** ______

*Mã cũ: LOGIN-S01-AC04, LOGIN-Q02.*

---

## A4. Có tài khoản vai trò khác ngoài khách không?

**Người trả lời gợi ý:** BA

Trang đăng nhập chỉ nhắc một tài khoản mẫu "Customer training login". Sau khi đăng nhập, tên vai trò hiện là "Customer" và thanh trên có "Shop", "My orders", "Profile".

**Hỏi:** Anh/chị cho mình hỏi: hệ thống có vai trò khác (ví dụ quản trị, nhân viên) không? Nếu có thì đăng nhập chung form này không, và mỗi vai trò thấy gì sau khi vào?

**Mình đang hiểu:** mình chưa biết. Mới thử được vai trò khách.

**Vì sao hỏi:** mỗi vai trò thấy menu khác nhau thì phải có tài khoản và ca test riêng.

**Câu trả lời của BA:** ______

*Mã cũ: LOGIN-S01-AC01, LOGIN-Q07.*

---

# Phần B. Hỏi sau, gom một lần (3 câu)

Các câu này chủ yếu về hiển thị, câu chữ, hoặc phần mình chưa test được.

## B1. Email viết hoa có tính là cùng một email không?

**Người trả lời gợi ý:** BA

Mình nhập "SHOPPER@SUNNY.TEST" (viết hoa hết) cùng mật khẩu đúng và vẫn đăng nhập được. Hệ thống trả lại email viết thường.

**Hỏi:** Anh/chị cho mình hỏi: email có được coi là không phân biệt chữ hoa, thường không?

**Mình đang hiểu:** mình đoán là không phân biệt, vì hệ thống đang làm vậy, nhưng chưa có yêu cầu nào nói rõ. Mới thử một ví dụ.

**Vì sao hỏi:** để biết đây là kết quả đúng hay chỉ là hệ thống tình cờ như vậy.

**Câu trả lời của BA:** ______

*Mã cũ: LOGIN-S01-AC02, LOGIN-R01, LOGIN-Q08.*

---

## B2. Mở địa chỉ không tồn tại thì nên hiện gì?

**Người trả lời gợi ý:** BA

Mình mở `/khong-ton-tai` khi chưa đăng nhập. Máy chủ trả mã 200 và hiện luôn trang đăng nhập, không có trang "không tìm thấy".

**Hỏi:** Anh/chị cho mình hỏi: yêu cầu có trang "không tìm thấy" riêng không, hay hiện form đăng nhập là đúng?

**Mình đang hiểu:** mình chưa chắc. Có thể do cả cửa hàng là một trang duy nhất nên mọi địa chỉ đều về trang này.

**Vì sao hỏi:** để quyết có ca test "địa chỉ không tồn tại" hay không.

**Câu trả lời của BA:** ______

*Mã cũ: LOGIN-S05-AC02, LOGIN-Q05.*

---

## B3. "Forgot password?" ở bản thật làm gì?

**Người trả lời gợi ý:** BA

Bấm "Forgot password?" chỉ hiện thông báo tạm "Password recovery is disabled in the training environment." và trang không đổi.

**Hỏi:** Anh/chị cho mình hỏi: khi tính năng này mở, người dùng sẽ làm gì tiếp (nhập email, nhận thư…)? Hay tính năng này nằm ngoài phần mình cần test?

**Mình đang hiểu:** mình đoán đây là phần riêng, chưa cần test ở màn hình đăng nhập.

**Vì sao hỏi:** để biết có cần viết ca cho phần này không.

**Câu trả lời của BA:** ______

*Mã cũ: LOGIN-S06-AC01, LOGIN-Q06.*

---

# Phần C. Mình tự kiểm tra trên hệ thống trước (1 mục)

Câu nào xem hệ thống đang chạy là tìm được câu trả lời thì mình tự làm trước, chỉ hỏi BA khi không tìm ra. Xem hệ thống chỉ cho biết hệ thống **đang làm gì**, không chứng minh là **đúng**. Chỉ dùng dữ liệu của mình, không đổi dữ liệu của người khác.

## C1. Bấm Back sau khi đăng xuất thì thấy gì?

- **Cần xem:** đăng nhập, bấm "Sign out", rồi bấm nút Back của trình duyệt; xem có quay lại thấy nội dung cửa hàng không.
- **Mình đang hiểu:** mình đoán Back chỉ cho thấy form đăng nhập vì phiên đã mất. Lần thử đầu của mình chưa ra kết quả có nghĩa.
- **Nếu không tìm ra, hỏi BA:** Anh/chị cho mình hỏi: sau khi đăng xuất, bấm Back thì người dùng phải thấy gì?

*Mã cũ: LOGIN-S04-AC03.*

---

## Đối chiếu mã cũ và mã mới
| Mã mới | Mã cũ | Nhóm |
|---|---|---|
| A1 | LOGIN-Q01 | Hỏi ngay |
| A2 | LOGIN-Q03 | Hỏi ngay |
| A3 | LOGIN-Q02 | Hỏi ngay |
| A4 | LOGIN-Q07 | Hỏi ngay |
| B1 | LOGIN-Q08 | Hỏi sau |
| B2 | LOGIN-Q05 | Hỏi sau |
| B3 | LOGIN-Q06 | Hỏi sau |
| C1 | (mới, từ chỗ chưa kiểm) | Tự kiểm tra |

`LOGIN-Q04` (email sai định dạng) không đưa thành câu hỏi: màn hình đăng nhập chỉ cần báo đúng hoặc sai, không kiểm định dạng (xem bảng phân tích, dòng `LOGIN-S03-AC02`).

## Lịch sử thay đổi
| Ngày | Thay đổi |
|---|---|
| 2026-11-20 | Tạo mới: 4 câu hỏi ngay, 3 câu hỏi sau, 1 mục tự kiểm tra |
