# Câu hỏi cho BA — Quên mật khẩu (Ecommerce Lite)

| | |
|---|---|
| Ngày soạn | 2026-11-20 |
| Dùng để | Gửi BA. Mỗi câu có tình huống, câu hỏi, cách mình đang hiểu và lý do hỏi |
| Nguồn | [quen-mat-khau.md](../../../srs/ecommerce-lite/quen-mat-khau.md) (SRS viết từ requirement) và [bảng phân tích](bang-soat-requirement.md). Mã cũ ghi ở cuối mỗi câu để tra chéo |
| Cách dùng | Gửi **Phần A** trước. **Phần B** gom hỏi một lần sau. **Phần C** là việc mình tự kiểm tra trên hệ thống, chưa cần hỏi BA |
| Tình trạng | Chưa gửi BA. Chưa có câu trả lời nào |

## Đọc trước 1 phút
Tính năng cho người dùng quên mật khẩu: nhập email đã đăng ký, nhận OTP (mã dùng một lần) gồm 6 chữ số qua email, nhập OTP đúng và còn hạn 5 phút thì được tạo mật khẩu mới, đổi xong phải đăng nhập lại. Requirement chỉ mô tả đường đi suôn sẻ, nên các câu dưới đây hỏi những chỗ requirement chưa nói.

| Thuật ngữ | Nghĩa theo requirement |
|---|---|
| OTP | Mã gồm 6 chữ số gửi đến email đã đăng ký, có hiệu lực 5 phút |
| 5 mật khẩu gần nhất | Mật khẩu mới không được trùng với 5 mật khẩu gần nhất |

**Quy ước từ ngữ trong file này:** "OTP", "mật khẩu mới", "5 mật khẩu gần nhất" dùng đúng như requirement; chữ hiển thị trên màn hình để trong ngoặc kép.

---

# Phần A. Hỏi ngay (6 câu)

Các câu này làm đổi kết quả đúng, nên cần trả lời sớm.

<a id="a1"></a>
## A1. Nhập email chưa đăng ký thì hệ thống làm gì?

**Người trả lời gợi ý:** BA

Requirement chỉ nói "nhập email đã đăng ký". Mình nhập thử `chuadangky@example.com` (email chưa có tài khoản) thì chưa biết hệ thống phản hồi sao.

**Hỏi:** Anh/chị cho mình hỏi: với email chưa đăng ký, hệ thống làm gì và hiện gì?

**Mình đang hiểu:** Mình chưa chắc. Mình đoán sẽ không gửi OTP, nhưng chưa biết màn hình báo "email không tồn tại" hay báo như thể đã gửi.

**Vì sao hỏi:** Hai cách này cho kết quả đúng khác nhau, test case phải ghi đúng một cách.

**Anh/chị chọn:**

- [ ] Báo rõ email chưa đăng ký (cho mình nguyên văn thông báo)
- [ ] Vẫn hiện như đã gửi OTP nhưng không gửi gì
- [ ] Khác: ______

**Câu trả lời của BA:** ______

*Mã cũ: FORGOT-S01-AC01, FORGOT-Q01.*

---

<a id="a2"></a>
## A2. Nhập sai OTP thì hệ thống làm gì, được sai mấy lần?

**Người trả lời gợi ý:** BA và Dev

Mình nhận OTP `123456`, rồi nhập `654321`. Requirement chỉ nói nhập đúng thì sang màn hình tạo mật khẩu mới, không nói nhập sai.

**Hỏi:** Anh/chị cho mình hỏi: nhập sai OTP thì hiện thông báo gì, và được nhập sai tối đa bao nhiêu lần? Quá số lần đó thì sao?

**Mình đang hiểu:** Nhập sai thì ở lại màn hình nhập OTP và có thông báo lỗi. Số lần tối đa mình chưa biết nên không tự đặt số.

**Vì sao hỏi:** Có giới hạn số lần thì test phải nhập sai đúng số lần đó. Mình không muốn làm khóa hệ thống khi chưa biết số.

**Câu trả lời của BA:** ______

*Mã cũ: FORGOT-S02-AC01, FORGOT-Q03.*

---

<a id="a3"></a>
## A3. OTP quá 5 phút thì hiện gì, có gửi lại OTP được không?

**Người trả lời gợi ý:** BA

Mình xin OTP lúc 10:00, đến 10:06 mới nhập đúng mã đó. Requirement nói OTP có hiệu lực 5 phút nhưng không nói gì sau 5 phút.

**Hỏi:** Anh/chị cho mình hỏi: nhập OTP quá 5 phút thì hiện thông báo gì? Có nút gửi lại OTP không, và phải chờ bao lâu giữa hai lần gửi?

**Mình đang hiểu:** OTP quá 5 phút bị từ chối như OTP sai. Mình chưa biết có chức năng gửi lại hay không.

**Vì sao hỏi:** Có gửi lại thì phải thêm test case cho nút đó. Thông báo hết hạn khác thông báo sai OTP thì phải ghi riêng.

**Câu trả lời của BA:** ______

*Mã cũ: FORGOT-R02, FORGOT-S02-AC01, FORGOT-Q04.*

---

<a id="a4"></a>
## A4. Xin OTP mới thì OTP cũ còn dùng được không, OTP dùng rồi có dùng lại được không?

**Người trả lời gợi ý:** BA

Mình xin OTP lúc 10:00 được mã `111111`, lúc 10:02 xin lại được mã `222222`. Lúc 10:03 mình nhập `111111`.

**Hỏi:** Anh/chị cho mình hỏi: OTP cũ còn dùng được hay bị hủy khi có OTP mới? Và OTP đã dùng đổi mật khẩu xong, trong vòng 5 phút có dùng lại được không?

**Mình đang hiểu:** Mình chưa chắc. Mình đoán chỉ OTP mới nhất còn dùng được và mỗi OTP chỉ dùng một lần, nhưng requirement không ghi.

**Vì sao hỏi:** Hai trường hợp này đổi kết quả đúng khi nhập OTP, và test phải ghi đúng một cách.

**Câu trả lời của BA:** ______

*Mã cũ: FORGOT-R02, FORGOT-Q05.*

---

<a id="a5"></a>
## A5. Ký tự đặc biệt hợp lệ gồm những ký tự nào?

**Người trả lời gợi ý:** BA

Requirement bắt mật khẩu mới có "ký tự đặc biệt" nhưng không liệt kê. Mình thử `Abcdef1!` thì không biết `!` có tính không, còn `Abcdef1 ` (có dấu cách) hay `Abcdef1é` thì càng không chắc.

**Hỏi:** Anh/chị cho mình hỏi: những ký tự nào được tính là ký tự đặc biệt? Dấu cách và chữ có dấu có tính không?

**Mình đang hiểu:** Mình chưa chắc. Mình đoán là các dấu như `! @ # $ %`, nhưng không có danh sách chính thức.

**Vì sao hỏi:** Không có danh sách thì không biết mật khẩu nào hợp lệ để kiểm.

**Câu trả lời của BA:** ______

*Mã cũ: FORGOT-R04, FORGOT-S03-AC03, FORGOT-Q06.*

---

<a id="a6"></a>
## A6. Mật khẩu đang dùng có nằm trong 5 mật khẩu gần nhất không?

**Người trả lời gợi ý:** BA

Tài khoản đang dùng mật khẩu `Abcd@1234`, và trước đó đã dùng 4 mật khẩu khác. Mình đặt mật khẩu mới là `Abcd@1234`.

**Hỏi:** Anh/chị cho mình hỏi: "5 mật khẩu gần nhất" có tính cả mật khẩu đang dùng không, hay chỉ tính 5 mật khẩu trước đó?

**Mình đang hiểu:** Mình đoán có tính cả mật khẩu đang dùng, nhưng chưa chắc. Tài khoản mới đổi dưới 5 lần thì mình hiểu là chỉ so với những mật khẩu đã có.

**Vì sao hỏi:** Hai cách hiểu cho kết quả khác ở mật khẩu thứ 5 và thứ 6 trở về trước, nên test phải dùng đúng mật khẩu.

**Anh/chị chọn:**

- [ ] Tính cả mật khẩu đang dùng (đang dùng + 4 mật khẩu trước)
- [ ] Chỉ tính 5 mật khẩu trước mật khẩu đang dùng
- [ ] Khác: ______

**Câu trả lời của BA:** ______

*Mã cũ: FORGOT-R05, FORGOT-S03-AC04, FORGOT-Q07.*

---

# Phần B. Hỏi sau, gom một lần (3 câu)

Các câu này chủ yếu về câu chữ thông báo và hiển thị.

<a id="b1"></a>
## B1. Để trống hoặc nhập email sai dạng thì hiện gì?

**Người trả lời gợi ý:** BA

Mình để trống ô email, hoặc nhập `abc` (không có `@`), rồi bấm yêu cầu OTP. Requirement không nói.

**Hỏi:** Anh/chị cho mình hỏi: hai trường hợp này hệ thống hiện thông báo gì?

**Mình đang hiểu:** Mình chưa chắc. Mình đoán sẽ không gửi OTP và có thông báo lỗi.

**Vì sao hỏi:** Cần nguyên văn thông báo để test case ghi đúng chữ.

**Câu trả lời của BA:** ______

*Mã cũ: FORGOT-S01-AC01, FORGOT-Q02.*

---

<a id="b2"></a>
## B2. Mật khẩu mới không hợp lệ thì hiện thông báo gì, có ô nhập lại mật khẩu không?

**Người trả lời gợi ý:** BA

Mình nhập mật khẩu mới `Abc@12` (6 ký tự), hoặc thiếu chữ hoa, hoặc trùng mật khẩu cũ. Requirement nói "phải có", "không được trùng" nhưng không nói màn hình hiện gì.

**Hỏi:** Anh/chị cho mình hỏi: mỗi trường hợp sai (độ dài, thiếu loại ký tự, trùng mật khẩu cũ) hiện thông báo gì? Màn hình có ô nhập lại mật khẩu để xác nhận không?

**Mình đang hiểu:** Mật khẩu không hợp lệ thì không được đổi và ở lại màn hình tạo mật khẩu mới. Thông báo và ô xác nhận thì mình chưa biết.

**Vì sao hỏi:** Cần nguyên văn từng thông báo để test case ghi đúng chữ; có ô xác nhận thì phải thêm ca nhập hai ô khác nhau.

**Câu trả lời của BA:** ______

*Mã cũ: FORGOT-S03-AC02, FORGOT-S03-AC03, FORGOT-S03-AC04, FORGOT-Q06.*

---

<a id="b3"></a>
## B3. Đổi mật khẩu xong hiện thông báo gì, chuyển đến đâu, mật khẩu cũ còn đăng nhập được không?

**Người trả lời gợi ý:** BA

Requirement ghi "hiển thị thông báo thành công và yêu cầu người dùng đăng nhập lại" nhưng không có nguyên văn, không nói chuyển đến trang nào.

**Hỏi:** Anh/chị cho mình hỏi: nguyên văn thông báo thành công là gì? Sau đó hệ thống chuyển đến trang nào (ví dụ trang đăng nhập)? Mật khẩu cũ có còn đăng nhập được không?

**Mình đang hiểu:** Mình đoán chuyển về trang đăng nhập và chỉ mật khẩu mới đăng nhập được, nhưng chưa chắc.

**Vì sao hỏi:** Cần nguyên văn thông báo và biết đúng trang đích để test case ghi chính xác.

**Câu trả lời của BA:** ______

*Mã cũ: FORGOT-S04-AC01, FORGOT-S04-AC02, FORGOT-Q08.*

---

# Phần C. Mình tự kiểm tra trên hệ thống trước (1 mục)

Câu nào xem hệ thống đang chạy là tìm được câu trả lời thì mình tự làm trước, chỉ hỏi BA khi không tìm ra. Xem hệ thống chỉ cho biết hệ thống **đang làm gì**, không chứng minh là **đúng**.

<a id="c1"></a>
## C1. Hệ thống Ecommerce Lite có chạy được chức năng Quên mật khẩu không?

- **Cần xem:** Ở lượt khám phá đăng nhập trước, mình đã bấm "Forgot password?" trên màn hình đăng nhập và thấy thông báo nhỏ `Password recovery is disabled in the training environment.`, không chuyển trang. Không cần khám phá lại.
- **Mình đang hiểu:** Môi trường staging này chưa có chức năng Quên mật khẩu, nên chưa chạy test case được trên đó.
- **Nếu không tìm ra, hỏi BA:** Anh/chị cho mình hỏi: khi nào môi trường test có chức năng Quên mật khẩu, và bản nào đang chạy chức năng này để mình đối chiếu?

*Mã cũ: FORGOT-S01-AC01.*

---

## Đối chiếu mã cũ và mã mới
| Mã mới | Mã cũ | Nhóm |
|---|---|---|
| A1 | FORGOT-Q01 | Hỏi ngay |
| A2 | FORGOT-Q03 | Hỏi ngay |
| A3 | FORGOT-Q04 | Hỏi ngay |
| A4 | FORGOT-Q05 | Hỏi ngay |
| A5 | FORGOT-Q06 (phần ký tự đặc biệt) | Hỏi ngay |
| A6 | FORGOT-Q07 | Hỏi ngay |
| B1 | FORGOT-Q02 | Hỏi sau |
| B2 | FORGOT-Q06 (phần thông báo, ô xác nhận) | Hỏi sau |
| B3 | FORGOT-Q08 | Hỏi sau |
| C1 | — (từ lượt khám phá đăng nhập) | Tự kiểm tra |

## Lịch sử thay đổi
| Ngày | Thay đổi |
|---|---|
| 2026-11-20 | Tạo mới: 6 câu hỏi ngay, 3 câu hỏi sau, 1 mục tự kiểm tra |
