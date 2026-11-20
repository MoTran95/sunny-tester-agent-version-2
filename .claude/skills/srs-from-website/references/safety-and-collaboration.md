# An toàn và cách phối hợp với người dùng

Các quy tắc dưới đây đến từ sự cố và chỉ dẫn thật trong các phiên làm việc. Lý do được ghi để áp dụng đúng tinh thần, không máy móc.

## 1. Mật khẩu: tài khoản test thì mình tự nhập (người dùng dặn lại 2026-11-20, thay quy tắc cũ "người dùng gõ")
- Với **tài khoản test**, mình **tự nhập cả mật khẩu thật lẫn mật khẩu sai** khi khám phá, chạy tay hay chạy script, **chỉ trên địa chỉ do người dùng nêu và có nhãn môi trường thử** (staging, dev, test, qa, sandbox, preview) hoặc localhost. Địa chỉ khác, tài khoản thật của người dùng → không nhập, nhờ người dùng tự làm.
- Mật khẩu thật: ưu tiên để script/công cụ đọc từ `.env` rồi điền (không in ra); khi duyệt tay bằng trình duyệt tích hợp thì dùng mật khẩu người dùng đã đưa cho tài khoản test. Mật khẩu sai dùng chữ giả (ví dụ `Sai@Matkhau1`).
- **Không in/nhắc lại mật khẩu** trong chat, nhật ký, tài liệu, bug, script; ảnh có mật khẩu mẫu hiện trên trang thì che. Không đọc thân yêu cầu POST đăng nhập.
- Nhập sai lặp lại vẫn theo mục 2 (tối đa 3 lần, kiểm sau từng lần, không tự đặt ngưỡng).
- Công cụ trình duyệt tự chặn việc nhập mật khẩu → theo mục 6 (không đi đường vòng), ghi "Chưa khám phá" kèm lý do và nhờ người dùng làm ca đó.

## 2. Không gây khóa hệ thống / đổi dữ liệu người khác
Người dùng đã dặn: khám phá **đầy đủ**, chỉ tránh việc **làm khóa hệ thống** hoặc **đổi dữ liệu của người khác**.
- Thao tác lặp có thể kích hoạt giới hạn (đăng nhập sai lặp lại, gửi hàng loạt…) → **tối đa 3 lần**, kiểm tra phản hồi **sau từng lần** (không chạy lô), rồi **dừng và hỏi người dùng** trước khi tiếp tục. Không tự nâng ngưỡng.
- Đừng tin "dùng dữ liệu giả thì an toàn": giới hạn có thể theo IP/trình duyệt/toàn hệ thống. Sự cố đã xảy ra: nhiều lần đăng nhập sai bằng mã không tồn tại → bị chặn tạm (HTTP 429). Xem `memories/pitfalls/dont-trigger-lockouts.md`.
- Muốn biết có giới hạn không mà không kích hoạt: đọc tệp giao diện công khai (tìm thông báo kiểu `locked`/`too many`), hoặc hỏi team.
- Lỡ kích hoạt → **báo ngay**, nói rõ thời điểm, thời gian ảnh hưởng, ai có thể bị ảnh hưởng, và việc dữ liệu có đổi không.

## 3. Hỏi trước khi làm
Hỏi và chờ đồng ý trước: tạo/sửa dữ liệu thật; tải file; thao tác có thể gửi ra ngoài (SMS, email); bấm Đăng xuất làm mất phiên sẵn có của người dùng (nói rõ họ sẽ phải đăng nhập lại); mọi việc có thể khóa/giới hạn. Dữ liệu test do mình tạo ghi rõ mã để nhận ra.

## 4. Tích hợp và hỏi khi chưa rõ
- Cổng bên thứ ba (SMS, email, danh tính…) là **thật hay mô phỏng** chưa biết thì hỏi, đừng suy đoán.
- Người dùng nói bằng giọng nói nên có từ nghe lệch (ví dụ "thiết khai" ≈ thiết kế, "sự khoai mạnh"): **hỏi lại nghĩa**, không tự suy diễn.
- Làm **từng bước nhỏ**, báo cáo, chờ phản hồi; đừng dựng cả quy trình một lúc.

## 5. Trung thực khi báo cáo
- Nói rõ cái gì mình **tự thấy**, cái gì **người dùng thao tác** (mình chỉ thấy kết quả sau), cái gì **suy ra từ tệp giao diện**.
- Nếu kết quả hai lần giống nhau và không chắc lần bấm có gửi đi (ví dụ ca B) → ghi nhận kèm lưu ý, hoặc kiểm tra bằng số lệnh gọi mạng.
- Không kết luận "lỗi"/"đúng thiết kế" khi chưa có tài liệu nghiệp vụ: viết "đã thấy / vì sao chưa rõ / cần làm rõ".

## 6. Khi công cụ chặn một thao tác
Công cụ trình duyệt có thể tự chặn một thao tác (từng gặp: bấm một nút gửi yêu cầu bằng JS bị chặn với lý do "Destructive or Unwanted Actions"). Lệnh chặn nghĩa là hệ thống an toàn đang coi thao tác đó là nguy hiểm — **không phải trở ngại kỹ thuật để lách**.
- **Không đi đường vòng**: không đổi sang cách khác để làm cùng việc (bấm bằng tọa độ thay vì `ref`, gọi thẳng API bằng `fetch` POST, sửa DOM để bật nút…).
- Dừng thao tác đó, ghi vào mục "Chưa khám phá" của SRS: **thao tác đã thử**, **công cụ chặn**, lý do thật là "bị công cụ chặn". Nếu cần phủ ca này, nói với người dùng và chờ họ **cho phép rõ** hoặc tự làm.
- Báo cho người dùng khi tổng kết: ca nào bị chặn, vì sao SRS chưa có AC cho ca đó. Không gộp vào nhóm "ngại rủi ro nhỏ" (quy tắc 7 của SKILL.md).
