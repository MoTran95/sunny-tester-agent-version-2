# Nguồn, trích dẫn và câu trả lời

## 1. Ba nhãn nguồn
Mọi điều ghi trong bảng soát phải rơi vào một trong ba loại (theo sách, Phần 6 và 7):

| Nhãn | Nghĩa | Việc làm |
|---|---|---|
| **Có trong tài liệu** | Trích được từ requirement kèm vị trí | Vào dòng ✅, kèm trích nguyên văn |
| **Suy luận** | Tài liệu chỉ cho phép hiểu theo một cách | Ghi một câu giải thích vì sao suy ra được; đọc lại cho hợp lý |
| **Giả định** | Tài liệu không nói | **Không** vào dòng ✅. Chuyển thành câu hỏi, và ghi "mình đang hiểu" kèm "mình đoán" |

Không dùng kiến thức chung để thêm quy tắc nghiệp vụ, quy định ngành hay luật mà nguồn không nêu. Khi người dùng **hỏi hẳn** một gợi ý dựa trên kiến thức chung (ví dụ "ngân hàng thường làm thế nào"), trả lời rõ rằng đó chỉ là lập luận chung, không có nguồn trích dẫn được, và khuyên đưa thành câu hỏi cho BA.

## 2. Trích nguyên văn
- Chép **đúng từng ký tự** từ nguồn, kể cả dấu `` ` ``, `**`, dấu gạch, ký tự toán (`−`, `×`, `≤`). Không viết lại câu.
- Đặt trong dấu `“…”` ở cột cuối của bảng (cột có tiêu đề chứa chữ "Trích"). Script `kiem-tra.py` chỉ kiểm trong cột này.
- Chọn đoạn **liên tục** ngắn nhất đủ chứng minh dòng đó. Không nối hai đoạn rời bằng dấu `…`.
- Trong ô bảng, ký tự `|` phải viết `\|` (escape từng ô, **không** escape cả dòng).
- Trích đoạn mô tả hành vi quan sát thì nói rõ đó là số hệ thống đang hiển thị, không phải kết quả mong đợi, khi hai số khác nhau.

## 3. Mã requirement
- Dùng nguyên mã sẵn có. Không đổi, không đánh số lại.
- Chỉ gán mã tạm R1, R2… khi tài liệu chưa có mã, theo thứ tự xuất hiện, và ghi chú đó là mã tạm.
- Mỗi mã requirement phải có mặt ít nhất một lần trong bảng soát hoặc phụ lục. Dùng `--ma` của script để kiểm.

## 4. Ghi câu trả lời `TL-xx`
Khi nhận câu trả lời (từ BA, người dùng, Dev), thêm một dòng vào bảng "Câu trả lời đã nhận":

| Cột | Nội dung |
|---|---|
| Mã | `TL-01`, `TL-02`… không dùng lại |
| Nội dung trả lời | Một hai câu, đúng ý người trả lời |
| Nguồn | **Ai** nói, **ngày**, **ở đâu**. Nếu là người dùng (tester) tự chốt thì ghi "chưa có xác nhận của BA" |
| Áp dụng cho | Các mã câu hỏi và mã requirement bị ảnh hưởng |
| Còn lại | Chỗ chưa trả lời, người cần xác nhận, hệ quả |

Quy tắc đi kèm:
- Câu trả lời mới **thay** câu cũ thì giữ dòng cũ, ghi "đã bị thay thế bởi TL-xx".
- Đổi các dòng ❓ liên quan thành ✅ và ghi "theo TL-xx". Nếu hệ thống hiện tại cho kết quả khác thì ghi **"khác hệ thống hiện tại"**; đó chỉ là nghi lỗi **nếu BA xác nhận**, không tự kết luận lỗi. Có thể chỉ là một nguyên nhân chung nên đừng đếm thành nhiều lỗi riêng.
- Quyết định của người dùng khác với điều mình khuyên: **tôn trọng và làm theo**, đồng thời nói rõ hệ quả (hệ thống khác ở những chỗ nào, số nào hiển thị đổi).
- Quyết định tester tự chốt đưa vào Phần A của file câu hỏi để BA xác nhận.
- **Không sửa SRS tại chỗ** khi chưa có BA hoặc team xác nhận (quy tắc của repo: nhãn chỉ được nâng khi BA hoặc dev xác nhận).
- Theo sách (Quy tắc 5, Phần 2): kết luận cuối cùng nên nằm ở nơi cả team nhìn thấy (ticket, kênh chung). Nhắc người dùng ghi lại ở đó và đính link vào dòng `TL-xx`.
