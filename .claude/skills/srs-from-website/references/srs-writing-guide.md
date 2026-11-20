# Hướng dẫn viết SRS

Khuôn: `srs/_template.md`. Quy tắc ID và ghi nguồn: `srs/id-and-source-rules.md`. Hai file đó là **nguồn chuẩn duy nhất** — đọc trước khi viết, đừng chép lại vào đây. File này chỉ thêm lời khuyên cách viết và các lỗi đã mắc.

## 1. SRS ở đây là gì
Tài liệu về **hành vi quan sát được** của hệ thống, chưa phải yêu cầu nghiệp vụ chính thức. Dùng để: người mới (tester) hiểu hệ thống; làm nền để sau này viết test case gắn vào từng tiêu chí chấp nhận (AC). Chỉ khi BA/dev xác nhận mới thêm nhãn `đã xác nhận`.

## 2. Cách viết một AC (một dòng trong bảng)
Ba phần, tiếng Việt thường, câu đầy đủ:
- **Bối cảnh** — tình trạng *trước khi* làm ("Chưa đăng nhập", "Đang bị chặn theo AC07").
- **Người dùng làm** — thao tác cụ thể: nhập gì (giá trị thật), bấm gì, mở gì.
- **Hệ thống phản hồi** — điều đã nhìn thấy; chép **nguyên văn** thông báo trong `…` ngay trong ô này; ghi cả điều **không** xảy ra nếu đáng chú ý ("không có thông báo đăng nhập thành công").

Một AC = **một** tình huống kiểm chứng được. Có "và" nối hai hành vi khác nhau thì tách. Chỉ nêu giá trị cụ thể đã thử, kèm phạm vi ("mới thử với một link/một tài khoản").

**Cột "Liên quan": ID có đủ mã feature.** Viết `CART-R01`, hoặc dải `CART-R01–R04` (gạch dài – hoặc —, hoặc "đến"; dải AC: `CART-S01-AC03–AC05`): `scripts/check-srs.py` mở dải thành từng ID rồi kiểm như tham chiếu thường (ID giữa dải chưa định nghĩa → lỗi; dải ngược → lỗi). **Không** dùng dạng rút gọn không có mã (`R01`, `AC04`) — script bỏ qua nên không kiểm được. Không dùng gạch ngang `-` làm dấu dải (lẫn với dấu gạch trong ID).

Tốt: *Nhập mã không có thật (`P999999`) + mật khẩu bất kỳ → cùng khung lỗi như AC01: hệ thống không cho biết mã sai hay mật khẩu sai.*
Chưa tốt: *Hệ thống xử lý đúng khi đăng nhập sai.* (không kiểm chứng được, "đúng" là phán xét.)

## 3. Văn phong và từ ngữ
- Người đọc có thể chưa biết gì về lĩnh vực: giải thích vai trò/thuật ngữ nghiệp vụ lần đầu.
- **Không** dùng làm tên cột/nhãn các thuật ngữ khó hiểu: Given/When/Then, "Cho trước/Khi/Thì", FR/BR, `NK#`, `DN-`, `BC-`. Nếu cần nhắc thuật ngữ kiểm thử, giải thích một lần trong đoạn "Cách đọc".
- Tránh các từ đã bị người dùng chê: "giải phẫu", "dây chuyền", "tick" (dùng "đánh dấu"), "giả lập" (dùng "mô phỏng"). Dùng đúng thuật ngữ IT thông dụng (xem bảng thuật ngữ trong `.claude/skills/feature-exploration-report/references/report-structure.md`).
- Link nguồn có chữ **đọc được**: `Ảnh 07`, `Nhật ký, hàng 14`, không phải mã viết tắt.

## 4. Bằng chứng
- Mỗi AC/quy tắc/thông báo có ID bằng chứng (`<MÃ>-E01`…). Bảng bằng chứng gồm: loại · tài khoản · thao tác đã làm · **tệp (link bấm được, đường dẫn tương đối từ file SRS)** · **cách kiểm lại** (làm theo là thấy lại đúng kết quả).
- Bằng chứng không có ảnh (Network, `localStorage`, thuộc tính HTML, tệp giao diện) ghi đúng loại và nói "không có ảnh" cùng cách mở lại bằng F12.
- Thông báo chỉ thấy trong tệp giao diện (chưa thấy trên màn hình) ghi rõ trong bảng thông báo: "chỉ thấy trong tệp giao diện".
- Không có bằng chứng thì **không** viết AC; đưa vào "Chưa khám phá" kèm lý do thật.

## 5. Câu hỏi cho team (`Q`)
Mỗi điểm chưa rõ có: đã thấy gì · vì sao chưa rõ · câu hỏi cụ thể cần ai trả lời · liên quan tới ID nào · trạng thái. Có manh mối (ví dụ "Workspace") thì ghi vào cột "đã thấy", đừng tự kết luận nghĩa.

## 6. Cập nhật SRS khi feature đổi
Sửa **tại chỗ**, ID giữ nguyên, thêm dòng ở "Lịch sử thay đổi". Đổi câu chữ → giữ ID. Đổi ý nghĩa → ID mới, mục cũ `đã bỏ` ("thay bằng …"). Khám phá lại phần đổi và lưu **bộ ảnh/nhật ký mới** (không ghi đè bộ cũ); bằng chứng mới nhận ID E mới. Rà các AC bị ảnh hưởng, đổi nhãn nếu chưa kiểm lại.

## 7. Số liệu phải khớp
Số lượng story/AC/quy tắc/thông báo/câu hỏi/bằng chứng ghi ở "Lịch sử thay đổi" phải khớp file (đã từng ghi sai "27 AC" khi thực tế 24). Chạy `scripts/check-srs.py` để đếm.
