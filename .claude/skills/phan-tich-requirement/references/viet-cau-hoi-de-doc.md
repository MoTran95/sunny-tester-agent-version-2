# Viết câu hỏi cho BA: đọc là hiểu, nghe như người nói

Người đọc có hai kiểu: **tester** cần kiểm tra từng dòng, và **BA** cần hình dung được rồi trả lời nhanh. Cả hai không cần biết mã nội bộ hay đọc lại tài liệu gốc. Đọc trước `memories/conventions/ba-question-wording.md` để lấy xưng hô và từ đã chốt.

## 1. Khuôn một câu hỏi (nhãn trường cố định, script đọc theo nhãn này)

**Phần A và B** (khối riêng cho mỗi câu):
```
## A1. <Tiêu đề là một câu hỏi nói thường>

**Người trả lời gợi ý:** BA | Dev | BA và Dev

<Kể tình huống thật có số: "Mình thử …". Có thể kèm một bảng nhỏ.>

**Hỏi:** Anh/chị cho mình hỏi: …?

**Mình đang hiểu:** … (nói rõ khi là đoán: "mình đoán", "mình chưa chắc")

**Vì sao hỏi:** … (một hai câu)

**Anh/chị chọn:**
- [ ] … 
- [ ] Khác: ______

**Câu trả lời của BA:** ______

*Mã cũ: CH-02, KN-05.*
```
**Phần C** (mình tự kiểm tra trước):
```
## C1. <Tiêu đề>

- **Cần xem:** (hoặc **Cần làm:**) việc mình làm trên hệ thống
- **Mình đang hiểu:** …
- **Nếu không tìm ra, hỏi BA:** …

*Mã cũ: KN-04.*
```
Dòng `*Mã cũ: …*` chỉ để tra chéo với mã trong bảng soát. Không đặt mã đó trong nội dung câu hỏi.

## 2. Giọng văn: nhắn tin cho đồng nghiệp
- **Số liệu trước, câu hỏi sau.** Kể điều mình thấy rồi mới hỏi.
- **Câu ngắn**, một ý một câu (khoảng 25 chữ trở xuống). Chủ ngữ rõ: "mình", "anh/chị", "màn hình", "hệ thống".
- Một câu hỏi một ý. Có nhiều ý thì tách thành các câu hỏi liền nhau, hoặc cho lựa chọn đánh dấu.
- **Gợi ý sẵn lựa chọn** để BA chỉ cần chọn.
- Nói thẳng chỗ mình chưa chắc. Không giả vờ biết.
- Xưng "mình", gọi BA "anh/chị" (chưa biết giới tính). Không dùng "người test".

## 3. Từ ngữ
- **Một từ cho một khái niệm** trong cả file. Lấy từ trong bảng "Từ đã chốt" của `ba-question-wording.md`. Từ mới thì hỏi người dùng rồi thêm vào bảng.
- **Chữ đang hiện trên màn hình** (tên khung, tên ô, nhãn, câu thông báo) giữ nguyên trong dấu ngoặc kép.
- Thuật ngữ của nghiệp vụ (tên loại phí, tên trạng thái…) giải thích một lần ở đầu file, theo đúng lời của tài liệu gốc.
- **Tránh** các từ dịch máy: "tiến hành", "nhằm", "đối với", "dựa trên", "thực hiện việc", "kết quả mong đợi" (nói "kết quả đúng" hoặc "phải ra"), "phạm vi" (nói "phần mình cần test"), "ngưỡng" lẫn "hạn mức" lẫn "mức tối đa".
- **Tránh** danh từ hóa ("việc làm tròn", "sự hiển thị") khi có động từ ("làm tròn", "hiện").
- **Tránh** câu bị động dài và câu nhiều vế lồng nhau.
- Không viết tắt khó hiểu. Không để mã nội bộ (CH-02, M01, R05) làm nội dung chính.

## 4. Trước và sau (ví dụ thật)
**Trước** (nghe như dịch máy):
> Khi tiền giảm tính ra nhiều chữ số lẻ, hệ thống nên làm tròn thế nào, và nên so với mức giảm tối đa bằng số đã làm tròn hay số thật? Cách làm tròn này có áp dụng cả khi hiển thị trên màn hình không?

**Sau:**
> Mình thử mã giảm 15% cho đơn 333.400 đ. Số thật là 50.010 đ, vượt mức giảm tối đa 50.000 đ. Màn hình ghi "Giảm 50.010 đ" và vẫn cho dùng mã. Nếu làm tròn xuống đến nghìn đồng thì ra 50.000 đ, vừa đủ.
> **Hỏi:** Anh/chị cho mình hỏi: hệ thống nên làm tròn kiểu nào, và có làm tròn cả số hiển thị không?
> **Mình đang hiểu:** Mình tạm chọn làm tròn xuống đến nghìn đồng, cho cả số hiển thị và khi so với mức tối đa. Hệ thống hiện đang không làm tròn.

**Trước:**
> Khi mã giảm hết hạn đúng lúc khách đang thanh toán, màn hình phải hiển thị thế nào?

**Sau:**
> Mình thử mã SALE10 có hạn đến 31/12, rồi để giỏ hàng mở qua 0 giờ ngày 1/1 và bấm Thanh toán. Dữ liệu hệ thống trả về là "mã hết hạn". Nhưng màn hình không báo gì: vẫn hiện số tiền đã giảm, lại hiện dòng "Đang xử lý…" mãi.
> **Hỏi:** Anh/chị cho mình hỏi: trường hợp này màn hình phải hiện gì ạ?

## 5. Bảng soát lấy câu hỏi từ đây
Cột "Câu hỏi gửi BA" trong bảng soát chỉ ghi **số câu, tiêu đề và nhóm**, đúng chữ như tiêu đề `## A1. …` ở file câu hỏi. Không chép lại **Hỏi**, **Mình đang hiểu**, **Cần xem**, **Nếu không tìm ra, hỏi BA**: các phần đó chỉ nằm ở file câu hỏi. Vì vậy tiêu đề phải tự đọc là hiểu (một câu hỏi nói thường), vì người đọc bảng soát chỉ thấy tiêu đề. Đổi tiêu đề thì sửa ở file câu hỏi rồi sửa theo trong bảng soát; `kiem-tra.py` báo nếu lệch.

## 6. Tự kiểm trước khi giao
- Đọc to ba bốn câu. Câu nào nghe lạ thì viết lại.
- Mỗi câu có số liệu hoặc tình huống cụ thể, không chỉ phát biểu chung.
- Phần "Mình đang hiểu" nói rõ chỗ nào là đoán.
- Không có mã nội bộ trong **Hỏi** và **Mình đang hiểu**. Chạy `kiem-tra.py` (nó cảnh báo từ dịch máy và mã nội bộ).
- Số trong ví dụ đã được tính lại bằng script.
- Một người chưa đọc tài liệu gốc vẫn hiểu câu hỏi.
