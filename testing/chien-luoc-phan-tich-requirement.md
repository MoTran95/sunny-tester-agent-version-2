# Chiến lược phân tích requirement (theo sách "Nền Tảng Tester Thời AI — Version 2")

| | |
|---|---|
| Nguồn | [Trang sách trên Notion](https://app.notion.com/p/N-n-T-ng-Tester-Th-i-AI-Version-2-413fcb30974e81348bd1ed948fa2c505?source=copy_link) |
| Ngày tổng hợp | 2026-11-17 |
| Mục đích | Để bạn xem lại sau: cách phân tích requirement và đặt câu hỏi cho BA, trước khi viết test case |
| Phạm vi | Chỉ bước phân tích và câu hỏi. Chưa viết checklist hay test case |
| Cách trình bày | Mình **tóm tắt bằng lời của mình**, không chép lại ví dụ của sách. Chỗ nào là ý của sách thì ghi tên mục. Chỗ nào là đề xuất của mình thì ghi rõ "đề xuất" |
| Mức đã đọc | Khoảng **một phần ba** cuốn sách (xem mục 10). Chưa đọc hết, nên đây là chiến lược cho bước phân tích, chưa phải toàn bộ sách |

## 1. Bước phân tích để làm gì
- Đây là **kiểm thử tĩnh**: đọc soát requirement khi chưa chạy phần mềm (Phần 1, "Việc đầu tiên khi nhận requirement").
- Đầu ra của bước này gồm hai thứ: **bảng soát requirement** và **câu hỏi cho BA**. Chưa viết test case (Phần 1, "Thứ tự làm việc ba bước").
- Việc cần tìm: chỗ **thiếu, mơ hồ, mâu thuẫn**, và chỗ chưa đủ để biết thế nào là đúng.
- Mục tiêu là tìm chỗ có rủi ro, không phải tạo thật nhiều câu hỏi. Đi hết các câu và các góc liên quan thì dừng (Phần 1, "Dùng sáu nút trong ba bước").

## 2. Sáu nguyên tắc nền
1. **Chưa có trong requirement thì chưa phải sự thật.** Điều rút ra từ kinh nghiệm cũng chỉ là thắc mắc cần hỏi, không phải quy tắc (Phần 1, "Ghi lại bằng bảng soát requirement").
2. **Không tự trả lời thay BA.** Kết quả mong đợi phải cụ thể, nhưng không được tự đặt con số khi requirement không nói. Để trống và hỏi (Phần 2, Quy tắc 2).
3. **Ghi hết vào bảng, nhưng hỏi có chọn lọc.** Câu chưa hỏi ngay vẫn nằm trong bảng để không bị quên (Phần 1, "Không phải câu nào cũng cần hỏi BA ngay").
4. **Mỗi dòng có nhãn nguồn.** Có ba nhãn: có trong tài liệu (kèm vị trí), suy luận (kèm một câu giải thích), giả định (tài liệu không nói). Dòng giả định không vào bảng chính mà chuyển thành câu hỏi cho BA (Phần 6, "Ba cái nhãn"; Phần 7, "Khối chống bịa").
5. **Chốt câu trả lời ở nơi cả team nhìn thấy** (ticket hoặc kênh chung). Nhắn riêng được, nhưng kết luận phải ghi lại ở nơi công khai và đính link vào bảng (Phần 2, Quy tắc 5).
6. **Với kết quả do AI tạo, người phải đối chiếu từng trích dẫn với tài liệu gốc.** AI nói đã đọc chưa có nghĩa là đã làm đúng (Phần 6, "Bốn chỗ AI hay sai").

## 3. Quy trình: Tách, Xoay, Lọc
### 3.1 Trước khi tách: đọc để hiểu
Năm câu tự hỏi (Phần 1, "Năm câu mình tự hỏi khi cầm requirement"):

| # | Câu tự hỏi |
|---|---|
| 1 | Tính năng làm cho ai, giải quyết chuyện gì? (câu quan trọng nhất, vì cho biết chỗ nào hỏng là nặng) |
| 2 | Có mấy ý cần kiểm tra? Đánh mã từng ý |
| 3 | Ai làm, nhập gì, hệ thống xử lý ra sao, hiện ra gì, lưu gì? |
| 4 | Đọc tới đâu thấy lấn cấn? |
| 5 | Nếu người dùng không đi đúng đường thì sao? |

Sáu dấu hiệu lấn cấn (Phần 1, "Sáu dấu hiệu làm mình lấn cấn"):

| Dấu hiệu | Nghĩa |
|---|---|
| Mơ hồ | Đọc xong vẫn không biết thế nào là đúng |
| Thiếu | Có đầu mà không có đuôi |
| Mâu thuẫn | Hai chỗ nói khác nhau |
| Không nhất quán | Cùng một thứ nhưng mỗi nơi gọi một tên |
| Không chính xác | Con số hoặc quy tắc ghi sai |
| Trùng lặp | Một ý viết ở hai chỗ (nguy cơ lệch khi một chỗ được sửa) |

### 3.2 Bước 1, Tách
Chia requirement thành từng ý nhỏ, mỗi ý một mã. Ý nào chứa hai, ba việc thì tách tiếp.
**Ví dụ:** SRS đã có mã (`CART-S01-AC01`, `CART-R01`, `CART-M01`…) thì dùng nguyên mã, không gán mã mới.

### 3.3 Bước 2, Xoay sáu nút
Với mỗi ý, đặt câu "Nếu như…?" qua sáu nút. Nút nào không liên quan thì bỏ qua, không ép ra câu hỏi (Phần 1, "Phương pháp Xoay 6 nút").

| Nút | Xoay thế nào |
|---|---|
| Người | Quyền khác, vai trò khác, chưa đăng nhập, dữ liệu cũ đã có |
| Dữ liệu | Để trống, sai định dạng, ngay ở biên, quá dài, trùng |
| Thời điểm | Quá sớm, quá muộn, hết hạn, làm hai lần, hai người cùng lúc |
| Đường đi | Bỏ một bước, quay lại, hủy giữa chừng, làm lại từ đầu |
| Môi trường | Mạng, thiết bị, trình duyệt |
| Kết quả | Thất bại thì sao, thành công rồi thì cái gì khác đổi theo |

**Đề xuất (của mình, không phải của sách):** theo yêu cầu của bạn là chỉ xét **functional**, dùng các nút theo hướng chức năng. Bỏ các câu về bảo mật và hiệu năng (ví dụ mạng chậm, độ trễ, dò dữ liệu). Ghép với các góc bạn đã dùng trong prompt ban đầu:

| Góc trong prompt của bạn | Nút gần nhất |
|---|---|
| Người dùng và quyền | Người |
| Dữ liệu đầu vào | Dữ liệu |
| Quy tắc xử lý | Dữ liệu, Thời điểm |
| Thông báo và hiển thị | Kết quả |
| Dữ liệu lưu | Kết quả |
| Trạng thái | Thời điểm, Đường đi |
| Tích hợp | Môi trường (chỉ phần chức năng) |

### 3.4 Bước 3, Lọc
Mỗi câu hỏi được xếp vào một trong ba nhóm (Phần 1, "Không phải câu nào cũng cần hỏi BA ngay"):

| Nhóm | Gồm | Làm gì |
|---|---|---|
| **Hỏi ngay** | Hai nguồn nói khác nhau; hiểu sai thì ảnh hưởng nặng (tiền, dữ liệu người dùng); câu trả lời làm Dev phải code khác | Gửi BA trước khi Dev code |
| **Gom hỏi sau** | Chi tiết hiển thị (câu chữ, vị trí); hiểu sai thì ảnh hưởng nhẹ | Gom lại, hỏi một lần |
| **Tự tìm trước** | Có thể đã có câu trả lời ở nơi khác (tài liệu chung, hệ thống đang chạy, hỏi Dev nếu là chuyện kỹ thuật) | Tự tra. Không ra thì chuyển sang một trong hai nhóm trên |

Ba câu để xếp nhóm: (1) dễ hiểu sai không, sai thì ai bị ảnh hưởng và nặng đến đâu; (2) câu trả lời có làm Dev code khác không; (3) mình có tự tìm được ở chỗ khác không.

Sách ghi rõ đây là **cách của tác giả**, không phải chuẩn bắt buộc. Nhiều team làm tương tự qua buổi refinement hoặc Example Mapping, nên có thể mang bảng soát vào buổi đó.

## 4. Bảng soát requirement (mẫu)
Mẫu của sách có các cột: mã, nút hoặc dấu hiệu, thắc mắc, đã rõ chưa, ưu tiên, câu hỏi gửi BA. Trạng thái chỉ có hai: **đã rõ** (requirement trả lời đủ để biết thế nào là đúng) và **cần hỏi**.

**Đề xuất cho bảng của bạn** (thêm cột nguồn vì bạn yêu cầu trích nguyên văn):

| Mã | Nút / dấu hiệu | Thắc mắc | Đã rõ chưa | Nhóm | Câu hỏi gửi BA | Nguồn (mã kèm trích nguyên văn) |
|---|---|---|---|---|---|---|
| CART-S01-AC02 | — | — | ✅ | — | — | … |
| CART-S01-AC06 | Không chính xác | Ca "giảm đúng 50,00%" thực ra hơn 50% một chút | ❓ | Hỏi ngay | … | … |

Mỗi dòng bám vào **một mã requirement**. Số dòng của bảng phụ thuộc vào số ý được tách, không phụ thuộc số test case.

## 5. Cách hỏi BA để dễ trả lời (Phần 1, "Gửi câu hỏi cho BA sao cho dễ trả lời")
1. Gửi nhóm **Hỏi ngay** trước, đánh số gọn trong một tin nhắn.
2. Ghi **mã** của từng câu để BA biết đang nói đoạn nào.
3. **Gợi ý sẵn lựa chọn** để BA chỉ cần chọn.
4. Hỏi ở nơi cả team cùng thấy, gắn tên BA và Dev phụ trách.
5. Nếu Dev trả lời "by design" cho một quy tắc nghiệp vụ thì vẫn cần BA hoặc PO xác nhận, không đóng vấn đề (Phần 2, Quy tắc 6).

## 6. Sau khi BA trả lời
- Đổi ❓ thành ✅ và ghi câu trả lời (kèm link tới nơi BA trả lời). Dòng ✅ mới sẵn sàng thành test case.
- Sách khuyên **checklist trước, chi tiết sau** (Phần 5): viết checklist ngắn, BA và Dev xác nhận, rồi mới viết test case chi tiết. Case còn chờ BA vẫn nằm trong checklist để không bị quên, nhưng chưa viết chi tiết.
- Workflow của sách có **điểm dừng** sau mỗi bước: sau phân tích thì chờ BA trả lời, sau checklist thì chờ xác nhận (Phần 8, "Quy trình test một tính năng").

## 7. Quy tắc khi dùng AI để phân tích (Phần 6 và 7)
- AI hay tự điền chỗ requirement bỏ ngỏ nên phải bắt nó gắn nhãn nguồn từng dòng.
- Prompt gồm: nhiệm vụ, nguồn dữ liệu, bối cảnh, ràng buộc, đầu ra, tự kiểm. Một prompt chỉ làm một nhiệm vụ.
- Khối ràng buộc cố định: chỉ dựa vào nguồn đã đưa; không dùng kiến thức chung để thêm quy tắc nghiệp vụ; giả định thì chuyển thành câu hỏi; thiếu tới mức không làm tiếp được thì hỏi lại tối đa 3 câu.
- Dùng **góc gợi ý** ("chỉ dùng góc nào liên quan"), không dùng danh sách "bắt buộc phải có", vì danh sách bắt buộc ép AI bịa quy tắc.
- Ràng buộc phải **đo được** (ví dụ "mỗi requirement có ít nhất một dòng").
- Bạn đã áp dụng gần hết các điểm này trong prompt phân tích ban đầu.

## 8. Áp dụng vào một dự án
Mỗi dự án có thể có file đối chiếu riêng trong `testing/<dự-án>/` (ví dụ `ap-dung-sach-vao-<tính-năng>.md`): sách khuyên gì, tính năng đó đã làm gì, khoảng cách, đề xuất xếp nhóm câu hỏi. Sách này chỉ giữ phần dùng chung.

## 9. Chỗ sách và cách đang làm khác nhau, cần bạn quyết
| Chủ đề | Sách | Cách đang làm | Bạn chọn |
|---|---|---|---|
| Gộp hay tách test case | **Gộp** khi cùng bước, cùng một quy tắc, chỉ khác dữ liệu (dùng bảng dữ liệu, mỗi dòng có kết quả mong đợi riêng). **Tách** khi khác quy tắc, khi thử giá trị không hợp lệ, hoặc khi cần chặn riêng (Phần 5, "Khi nào gộp, khi nào tách") | Luật của bạn: không gộp, kể cả khi chỉ khác dữ liệu | Giữ luật của bạn, hay theo sách ở các nhóm chỉ khác dữ liệu? |
| Phạm vi các nút | Có ví dụ về bảo mật và môi trường (mạng, thiết bị) | Bạn yêu cầu chỉ functional | Giữ functional (đã áp dụng ở mục 3.3) |
| Thang ưu tiên | Ba nhóm cho câu hỏi | Cao / Trung bình / Thấp | Đề xuất: nhóm hỏi cho câu hỏi, Cao / Trung bình / Thấp cho test case |
| Cột kỹ thuật trong checklist | Có (EP, BVA, bảng quyết định…) | Chưa có | Thêm ở bước checklist, không cần ở bước phân tích |
| Câu hỏi từ kinh nghiệm | Ghi chung bảng, đánh dấu là kinh nghiệm | Đang tách riêng (KN) | Giữ tách riêng nhưng gắn nhóm hỏi |

## 10. Phần sách đã đọc và chưa đọc
- **Đã đọc:** Phần 1 (toàn bộ), Phần 2 (mở đầu và Quy tắc 1 đến 6), Phần 3 (chỉ đoạn chọn kỹ thuật theo dấu hiệu), Phần 5 (checklist, gộp hoặc tách, trạng thái khi chạy), Phần 6 (AI giúp được gì, chỗ AI hay sai, ba nhãn), Phần 7 (khung prompt, mười quy tắc, khối chống bịa), Phần 8 (workflow và bộ skill gợi ý).
- **Chưa đọc:** Phần 0; chi tiết các kỹ thuật EP, BVA, bảng quyết định, chuyển trạng thái, use case ở Phần 3 và các bài tập; Phần 4 (smoke, regression); phần báo bug của Phần 5; phần bảo mật dữ liệu của Phần 6; các prompt mẫu và bài tập của Phần 7; hướng dẫn cài đặt và skill mẫu của Phần 8; Phần 9.
- Nếu cần phần nào trong số chưa đọc cho bước tiếp theo (đặc biệt Phần 3 khi làm checklist), bạn báo mình đọc thêm.
