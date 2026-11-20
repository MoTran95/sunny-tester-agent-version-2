# [Đặt lịch hẹn] Nút Xác nhận vẫn bật khi chưa chọn giờ

> Ví dụ trung lập để minh họa hình dạng. Dữ liệu và hệ thống trong ví dụ là bịa, không dùng làm nội dung thật. Kết quả mong đợi bên dưới có nguồn, nên đây là lỗi đã rõ; nếu không có nguồn thì đổi thành `Chưa xác định` + câu hỏi cho BA và ghi ngay dưới tiêu đề "Nghi lỗi, chờ BA chốt".

## Test case liên quan
TC-014 (Nút Xác nhận bị tắt khi chưa chọn giờ hẹn). Không có test case: ghi "Không có".

## Môi trường
- Hệ thống: bản thử nghiệm đặt lịch hẹn, địa chỉ `https://example.test/` (người dùng cung cấp)
- Trình duyệt: Chrome 126 trên Windows 11
- Số build: 2.4.1
- Tài khoản: `USER-TEST-01`

## Điều kiện trước
- Tài khoản `USER-TEST-01` đã có sẵn một dịch vụ cần đặt lịch (theo TC-014)
- Chưa có lịch hẹn nào trong ngày được chọn

## Các bước tái hiện
1. Đăng nhập bằng tài khoản `USER-TEST-01`.
2. Vào màn hình "Đặt lịch hẹn", chọn dịch vụ "Khám tổng quát".
3. Chọn ngày hẹn 20/12/2026, **không chọn giờ** (ô "Giờ hẹn" vẫn hiện "Chọn giờ").
4. Quan sát nút "Xác nhận" và bấm vào nút đó.

## Kết quả mong đợi
Nút "Xác nhận" bị tắt (mờ, không bấm được) cho đến khi chọn giờ hẹn.

## Kết quả thực tế
Ở bước 4, nút "Xác nhận" sáng bình thường và bấm được. Sau khi bấm, hệ thống hiện thông báo "Đặt lịch thành công" và trong danh sách lịch hẹn có thêm một dòng ngày 20/12/2026 với cột "Giờ" để trống. [Giả định: dòng mới nằm ở trạng thái "Chờ xác nhận" như các lịch hẹn khác, vì ghi chú không nói trạng thái]

## Phạm vi ảnh hưởng
Không có: chỉ một chỗ.

(Khi cùng một lỗi gốc xuất hiện ở nhiều chỗ **và ghi chú nói rõ chung nguyên nhân hoặc Dev đã xác nhận**, liệt kê từng chỗ, ví dụ:
- Màn hình "Đặt lịch hẹn": nút Xác nhận bật khi chưa chọn giờ.
- Màn hình "Đổi lịch hẹn": nút Lưu bật khi xóa giờ đã chọn.)

## Ảnh hưởng nghiệp vụ
Người dùng tạo được lịch hẹn không có giờ, nên nhân viên không biết khung giờ phục vụ. [Giả định: lịch không có giờ không thể được xếp nhân viên, vì ghi chú không nêu cách hệ thống xử lý lịch này]

## Mức độ nghiêm trọng
**Lớn.** Chức năng chính (đặt lịch) cho phép lưu dữ liệu không đầy đủ, người dùng thấy "Đặt lịch thành công" nhưng lịch không dùng được. Còn cách đi vòng: người dùng sửa lại lịch rồi chọn giờ [Giả định: có chức năng sửa lịch hẹn đã tạo].

## Mức độ ưu tiên đề xuất
**Cao** — lịch không có giờ dễ lọt vào dữ liệu thật. (Đề xuất; team hoặc PO sẽ chốt.)

## Tần suất
Luôn xảy ra (3/3 lần thử).

## Đính kèm cần có
- [ ] Ảnh màn hình bước 3: ô "Giờ hẹn" chưa chọn, nút "Xác nhận" sáng; cần bản tô đỏ nút "Xác nhận" (lỗi ở bước 3) — `Cần bổ sung`
- [ ] Ảnh thông báo "Đặt lịch thành công" và dòng lịch hẹn không có giờ: ảnh gốc `evidence/<dự-án>/bug/BUG-001-thanh-cong.png`; ảnh đã tô đỏ chỗ dòng lịch hẹn không có giờ (lỗi ở bước 4 của các bước tái hiện): `evidence/<dự-án>/bug/BUG-001-thanh-cong-loi.png`
- [ ] Bản ghi dữ liệu: dòng lịch hẹn vừa tạo (mã lịch hẹn, cột giờ trống) — `Cần bổ sung`
- [ ] Log / phản hồi mạng của lần bấm Xác nhận — `Cần bổ sung`
- [ ] Video thao tác 4 bước — không bắt buộc

## Câu hỏi còn mở
**Cho BA** (khi kết quả mong đợi không có trong nguồn; ví dụ này đã có nguồn nên bỏ trống):
- (Không có)

**Cho Dev**:
- Mình thấy hai lỗi giống nhau: nút "Xác nhận" ở màn hình "Đặt lịch hẹn" (bug này) và nút "Lưu" ở màn hình "Đổi lịch hẹn" (BUG-002) đều vẫn bật khi chưa chọn giờ. Anh/chị cho mình hỏi: hai nút này có dùng chung một đoạn xử lý không, tức là một nguyên nhân và sửa một chỗ là hết cả hai? Nếu đúng thì mình gộp thành một bug; nếu hai chỗ riêng thì mình giữ hai bug như hiện tại.

## Thông tin đã gắn nhãn Giả định (cần kiểm lại)
1. Dòng lịch hẹn mới nằm ở trạng thái "Chờ xác nhận" (mục Kết quả thực tế).
2. Lịch không có giờ không thể được xếp nhân viên (mục Ảnh hưởng nghiệp vụ).
3. Có chức năng sửa lịch hẹn đã tạo (mục Mức độ nghiêm trọng).
