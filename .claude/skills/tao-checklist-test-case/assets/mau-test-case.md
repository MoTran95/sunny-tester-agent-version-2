# Test case chi tiết — Đặt số lượng sản phẩm vào giỏ (ví dụ mẫu)

| | |
|---|---|
| Ngày lập | YYYY-MM-DD (mẫu) |
| Hệ thống | Web bán hàng (ví dụ trung lập, không phải requirement thật) |
| Nguồn | Checklist cùng thư mục (mã TC giữ nguyên, số lượng giữ nguyên) |
| Tình trạng | Chưa chạy thử trên hệ thống |

**Cách đọc.** Mỗi dòng là một test case đứng riêng. Ba cột cuối (`Kết quả thực tế`, `Trạng thái`, `Người viết`) để ghi khi chạy test; `Trạng thái` chọn một: Chưa chạy, Đạt, Không đạt, Bị chặn, Bỏ qua.

<!-- BANG-TC:BAT-DAU (bảng test case; tiêu đề cột là cố định để script đọc) -->
| Mã | Tình huống | Ưu tiên | Điều kiện trước | Các bước | Dữ liệu test | Kết quả mong đợi | Nguồn | Kết quả thực tế | Trạng thái | Người viết | Tự động hóa |
|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-001 | Nhập số lượng hợp lệ `5` rồi bấm Thêm vào giỏ: giỏ hiện 5 sản phẩm | Cao | Dùng trình duyệt vào được trang sản phẩm mẫu. Giỏ hàng đang trống. | 1. Mở trang sản phẩm.<br>2. Ở ô `Số lượng` nhập `5`.<br>3. Bấm nút `Thêm vào giỏ`.<br>4. Nhìn biểu tượng giỏ hàng. | Số lượng: `5` | Bước 3: thêm thành công, không có thông báo lỗi.<br>Bước 4: giỏ hiện 5 sản phẩm. | Có trong tài liệu: R1 (Số lượng từ 1 đến 10) |   | Chưa chạy | Nguyễn Văn A | Chưa có |
| TC-002 | Nhập số lượng ở biên dưới `1`: thêm được, giỏ hiện 1 sản phẩm | Cao | Dùng trình duyệt vào được trang sản phẩm mẫu. Giỏ hàng đang trống. | 1. Mở trang sản phẩm.<br>2. Ở ô `Số lượng` nhập `1`.<br>3. Bấm nút `Thêm vào giỏ`.<br>4. Nhìn biểu tượng giỏ hàng. | Số lượng: `1` (biên dưới) | Bước 3: thêm thành công, không có thông báo lỗi.<br>Bước 4: giỏ hiện 1 sản phẩm. | Có trong tài liệu: R1 (Số lượng từ 1 đến 10) |   | Chưa chạy | Nguyễn Văn A | Chưa có |
| TC-003 | Nhập số lượng ngay dưới biên `0`: không thêm, báo "Số lượng tối thiểu là 1." | Cao | Dùng trình duyệt vào được trang sản phẩm mẫu. Giỏ hàng đang trống. | 1. Mở trang sản phẩm.<br>2. Ở ô `Số lượng` nhập `0`.<br>3. Bấm nút `Thêm vào giỏ`.<br>4. Nhìn thông báo và biểu tượng giỏ hàng. | Số lượng: `0` (ngay dưới biên) | Bước 3: không thêm vào giỏ.<br>Bước 4: hiện thông báo "Số lượng tối thiểu là 1."; giỏ vẫn trống. | Có trong tài liệu: R1 (Số lượng từ 1 đến 10), R2 (Báo khi dưới 1) |   | Chưa chạy | Nguyễn Văn A | Chưa có |
| TC-004 | Nhập số lượng ở biên trên `10`: thêm được, giỏ hiện 10 sản phẩm | Cao | Dùng trình duyệt vào được trang sản phẩm mẫu. Giỏ hàng đang trống. | 1. Mở trang sản phẩm.<br>2. Ở ô `Số lượng` nhập `10`.<br>3. Bấm nút `Thêm vào giỏ`.<br>4. Nhìn biểu tượng giỏ hàng. | Số lượng: `10` (biên trên) | Bước 3: thêm thành công, không có thông báo lỗi.<br>Bước 4: giỏ hiện 10 sản phẩm. | Có trong tài liệu: R1 (Số lượng từ 1 đến 10) |   | Chưa chạy | Nguyễn Văn A | Chưa có |
| TC-005 | Nhập số lượng ngay trên biên `11`: không thêm, báo "Số lượng tối đa là 10." | Cao | Dùng trình duyệt vào được trang sản phẩm mẫu. Giỏ hàng đang trống. | 1. Mở trang sản phẩm.<br>2. Ở ô `Số lượng` nhập `11`.<br>3. Bấm nút `Thêm vào giỏ`.<br>4. Nhìn thông báo, biểu tượng giỏ hàng và nội dung ô `Số lượng`. | Số lượng: `11` (ngay trên biên) | Bước 3: không thêm vào giỏ.<br>Bước 4: hiện thông báo "Số lượng tối đa là 10."; giỏ vẫn trống. Nội dung ô `Số lượng` sau khi báo lỗi: CẦN XÁC NHẬN (xem Câu hỏi cho BA, câu 2). | Có trong tài liệu: R1 (Số lượng từ 1 đến 10), R3 (Báo khi trên 10) |   | Chưa chạy | Nguyễn Văn A | Chưa có |
| TC-006 | Để trống ô Số lượng rồi bấm Thêm vào giỏ: báo "Vui lòng nhập số lượng." | Trung bình | Dùng trình duyệt vào được trang sản phẩm mẫu. Giỏ hàng đang trống. | 1. Mở trang sản phẩm.<br>2. Để trống ô `Số lượng`.<br>3. Bấm nút `Thêm vào giỏ`.<br>4. Nhìn thông báo và biểu tượng giỏ hàng. | Số lượng: để trống | Bước 3: không thêm vào giỏ.<br>Bước 4: hiện thông báo "Vui lòng nhập số lượng."; giỏ vẫn trống. | Có trong tài liệu: R4 (Báo khi để trống) |   | Chưa chạy | Nguyễn Văn A | Chưa có |
| TC-007 | Giỏ đã có 5 sản phẩm, thêm lần hai `3` sản phẩm: giỏ hiện 8 sản phẩm | Trung bình | Dùng trình duyệt vào được trang sản phẩm mẫu. Giỏ hàng đang có đúng 5 sản phẩm này (cách tạo: thêm `5` như một lần thêm hợp lệ). | 1. Mở trang sản phẩm.<br>2. Ở ô `Số lượng` nhập `3`.<br>3. Bấm nút `Thêm vào giỏ`.<br>4. Nhìn biểu tượng giỏ hàng. | Số lượng lần hai: `3` | Bước 3: thêm thành công, không có thông báo lỗi.<br>Bước 4: giỏ hiện 8 sản phẩm. | Suy luận: R1 (Số lượng từ 1 đến 10), vì R1 áp dụng cho mỗi lần thêm nên lần hai `3` cũng là một lần thêm hợp lệ |   | Chưa chạy | Nguyễn Văn A | Chưa có |
<!-- BANG-TC:KET-THUC -->

## Câu hỏi cho BA
1. Giỏ đã có 8 sản phẩm, thêm lần hai 3 sản phẩm thì tổng 11: có bị chặn không? Mình đang hiểu là chỉ kiểm mỗi lần thêm (R1). Liên quan: R1 (đã có ở checklist, không phải TC riêng).
2. Sau khi báo "Số lượng tối đa là 10." ở TC-005, ô `Số lượng` giữ chữ `11` hay bị xóa? Requirement không nói. Liên quan: TC-005, R3.

## Ghi nhận riêng (không tự gộp, xóa hay thêm test case)
- Ví dụ: checklist TC-00x gộp hai giá trị không hợp lệ; test case dùng giá trị đầu, giá trị còn lại chưa có case (cần thêm mã TC mới nếu muốn kiểm).

## Tự kiểm
- 7 test case. Chạy `kiem-tra-tc.py` để kiểm đầy đủ.
