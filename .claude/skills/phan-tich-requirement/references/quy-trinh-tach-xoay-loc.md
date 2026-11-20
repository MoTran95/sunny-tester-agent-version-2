# Tách, Xoay, Lọc: cách soát một requirement

Tóm tắt bằng lời của mình từ sách *Nền Tảng Tester Thời AI*, Phần 1, cộng các điều học được ở các lần làm thật đầu tiên. Đây là **static testing**: đọc soát khi chưa chạy phần mềm. Mục tiêu là tìm chỗ có rủi ro, không phải tạo thật nhiều câu hỏi. Đi hết các đơn vị và các góc liên quan thì dừng.

## 1. Trước khi tách: năm câu tự hỏi
1. Tính năng làm cho ai, giải quyết chuyện gì? Biết điều này mới biết chỗ nào hỏng là nặng.
2. Có mấy ý cần kiểm tra? Mỗi ý một mã.
3. Ai làm, nhập gì, hệ thống xử lý ra sao, hiện ra gì, lưu gì?
4. Đọc tới đâu thấy lấn cấn?
5. Nếu người dùng không đi đúng đường thì sao?

## 2. Sáu dấu hiệu lấn cấn
| Dấu hiệu | Nghĩa | Ví dụ minh họa |
|---|---|---|
| Mơ hồ | Đọc xong vẫn không biết thế nào là đúng | So hạn mức theo số làm tròn hay số thật |
| Thiếu | Có đầu mà không có đuôi | Chưa nói khi đơn hàng vừa "Hết hàng" vừa "Đã thanh toán" |
| Mâu thuẫn | Hai chỗ nói khác nhau | Dữ liệu trả về "Hết hàng" nhưng màn hình không hiện nhãn |
| Không nhất quán | Cùng một thứ, mỗi nơi ghi một kiểu | Mức giảm ghi `15,00%`, câu thông báo ghi `15%` |
| Không chính xác | Con số hay quy tắc ghi sai | Ca "đúng 50,00%" thật ra là 50,0000003% |
| Trùng lặp | Một ý viết ở hai chỗ, dễ lệch khi sửa một chỗ | |

## 3. Tách
Chia requirement thành từng đơn vị nhỏ, mỗi đơn vị một mã. Đơn vị nào chứa hai ba ý thì tách tiếp. **Tài liệu đã có mã thì dùng nguyên mã**; chưa có thì gán R1, R2… theo thứ tự xuất hiện.

## 4. Xoay sáu nút (chỉ chức năng)
Với mỗi đơn vị, hỏi "Nếu như…?" qua sáu nút. Nút nào không liên quan thì bỏ, không ép ra câu hỏi.

| Nút | Xoay thế nào |
|---|---|
| Người | Vai trò khác, quyền khác, dữ liệu cũ đã có |
| Dữ liệu | Để trống, sai định dạng, ngay ở biên, quá dài, trùng, tổ hợp nhiều điều kiện |
| Thời điểm | Quá sớm, quá muộn, hết hạn, làm hai lần, kết quả đổi theo ngày chạy |
| Đường đi | Bỏ một bước, quay lại, hủy giữa chừng, đổi ô này kéo theo ô khác |
| Môi trường | Nơi hiển thị, dữ liệu API và màn hình, tích hợp bên ngoài (chỉ phần chức năng) |
| Kết quả | Thất bại thì sao, thành công rồi cái gì khác đổi theo, nơi nào hiển thị |

**Giới hạn theo yêu cầu của người dùng:** bỏ các câu về bảo mật và hiệu năng (độ trễ, mạng chậm, dò dữ liệu) trừ khi requirement nói tới. Ghép với các góc hay dùng: người dùng và quyền (Người); dữ liệu đầu vào (Dữ liệu); quy tắc xử lý (Dữ liệu, Thời điểm); thông báo và hiển thị, dữ liệu lưu (Kết quả); trạng thái (Thời điểm, Đường đi); tích hợp (Môi trường).

**Chỗ hay bị sót:** tổ hợp nhiều luật cùng vi phạm; ca sát ranh giới và cách làm tròn; màn hình khác dữ liệu hệ thống trả về; trạng thái sau khi lưu; quy tắc nhắc tới nhưng phần mô tả lại ghi "ngoài phạm vi" hay "chưa khám phá"; thông báo chỉ thấy trong mã nguồn chưa thấy trên màn hình (chỉ đáng hỏi khi hành vi trên màn hình chưa rõ, xem mục 5).

## 5. Quyết ✅ hay ❓
**Bước đầu: requirement đã ghi rõ chưa?**
- **Ghi rõ** (hoặc BA đã trả lời): suy ra hệ quả theo logic, kể cả từ lý do của tính năng (lý do bảo mật cũng được). Ghi ✅ "suy ra từ <mã hoặc TL>" kèm một câu lý do. Không hỏi. Ví dụ: requirement ghi đăng nhập sai nhiều lần thì bị chặn → chặn đúng tài khoản đó; mọi lỗi đăng nhập báo chung một câu để không lộ ô nào sai (lý do bảo mật) → để trống ô cũng báo câu chung.
- **Chưa ghi hoặc ghi chưa rõ**: không lấp bằng kinh nghiệm hay thông lệ, đánh ❓ và hỏi. Ví dụ: phiên đăng nhập giữ được bao lâu (requirement không ghi con số); câu báo bị chặn ghi số phút cố định hay số phút còn lại.
- **Lý do bảo mật của màn hình đăng nhập:** chỉ báo đúng hoặc sai, không kiểm định dạng hay độ dài, không lộ ô nào sai. Nên không hỏi và không test độ dài, định dạng của mã hay mật khẩu ở màn hình đăng nhập (đó là việc của phần đăng ký).
- **Đi theo câu chữ, không theo hệ thống.** Requirement ghi "N lần sai liên tiếp thì bị chặn" → lần sai thứ N bị chặn; "liên tiếp" → đăng nhập đúng xen giữa đếm lại từ 0; không nhắc thời gian → chỉ đếm số lần. Hệ thống chặn ở lần thứ N+1 thì là nghi lỗi, không phải lý do để hỏi BA.
- **Hệ thống làm khác điều suy ra**: ghi "nghi lỗi, cần kiểm" kèm bằng chứng, không biến thành câu hỏi "quy tắc là gì".
- **Áp lý do của câu trả lời cho mục cùng loại.** BA nói độ dài tên đăng nhập thuộc phần đăng ký → độ dài, ký tự cho phép của mật khẩu cũng thuộc phần đăng ký; ở màn hình đăng nhập chỉ có đúng hoặc sai. Không hỏi lại.
- **Câu chỉ có trong mã nguồn không làm hành vi thành chưa rõ.** Bị đăng xuất thì về form đăng nhập để đăng nhập lại: SRS ghi rõ, đủ. Không hỏi "có phải báo câu X (chỉ thấy trong tệp giao diện) không".
- SRS là bản nháp ghi lại hệ thống thì chữ "chưa rõ" trong đó có thể chỉ là chỗ chưa khám phá. Xét mục đích đã ghi rõ trước khi coi là mơ hồ.

- **✅ Đã rõ:** requirement trả lời đủ để biết thế nào là đúng (điều kiện, kết quả, và thông báo nguyên văn nếu có). Trong phạm vi hành vi đã quan sát nếu tài liệu là bản nháp ghi lại hệ thống, và nói rõ điều đó.
- **❓ Cần hỏi:** requirement chưa nói, nói chưa rõ, nói hai kiểu, số liệu tự lệch, hoặc tài liệu ghi `chưa rõ` / `chưa kiểm`. Ý rút từ kinh nghiệm cũng đánh ❓.
- Một đơn vị **rõ một nửa** thì tách hai dòng: dòng ✅ cho phần rõ, các dòng ❓ cho từng chỗ chưa rõ.
- Mỗi dòng ❓ có **một dấu hiệu** (mục 2) và một câu hỏi.

## 6. Lọc: ba nhóm câu hỏi
| Nhóm | Gồm | Làm gì |
|---|---|---|
| **A. Hỏi ngay** | Hai nguồn nói khác nhau; hiểu sai thì **đổi kết quả đúng** (nhãn, quyết định, tiền); câu trả lời làm Dev code khác | Gửi BA sớm |
| **B. Hỏi sau (gom lại)** | Câu chữ, định dạng hiển thị, phần ngoài phạm vi hiện tại; hiểu sai ảnh hưởng nhẹ | Gom một lần |
| **C. Tự kiểm tra trước** | Có thể tự tìm câu trả lời: xem hệ thống đang chạy, tra tài liệu chung, hỏi Dev nếu là chuyện kỹ thuật | Tự làm trước; không tìm ra thì hỏi BA |

Ba câu để xếp nhóm: (1) dễ hiểu sai không, sai thì ai bị ảnh hưởng và nặng đến đâu; (2) câu trả lời có làm Dev code khác không; (3) mình có tự tìm được ở chỗ khác không.

**Lưu ý nhóm C:** xem hệ thống chỉ cho biết hệ thống **đang làm gì**, không chứng minh là **đúng**. Nếu hành vi quan sát có vẻ là lỗi (ví dụ màn hình không hiện kết quả mà dữ liệu thì có) thì vẫn phải hỏi BA. Khi tự kiểm tra trên hệ thống thật: chỉ dùng dữ liệu của mình, không làm khóa hệ thống, không gõ mật khẩu thay người dùng (xem `srs-from-website/references/safety-and-collaboration.md`).

## 7. Tính lại số liệu
Với mọi con số, công thức, ví dụ có số trong requirement: viết script Python nhỏ (để trong thư mục tạm) tính lại từ chính công thức của tài liệu, so với số tài liệu ghi.
- Số "đúng X%" có thật đúng X% không (kiểm bằng phân số hoặc số thập phân đủ dài).
- Kết quả có khớp công thức của chính tài liệu với **điều kiện nền đã ghi** không (một ca lệch vì mang theo trạng thái dư của lượt thử trước).
- Ví dụ có ghi đủ điều kiện (lương, chi phí, nợ…) để dựng lại không.
Chỗ lệch ghi thành dòng ❓ dấu hiệu "Không chính xác", kèm phép tính để BA hoặc người viết tài liệu kiểm lại.
Khi người dùng chọn một quy tắc làm đổi nhiều số (ví dụ làm tròn lên cả khi hiển thị), tính lại toàn bộ các số bị ảnh hưởng và lập bảng "hiện tại / đúng theo quy tắc mới".
