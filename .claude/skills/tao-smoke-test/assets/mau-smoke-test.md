# Bộ smoke test — <Tên hệ thống> (bản <số bản của hệ thống đang test>)

| | |
|---|---|
| Ngày lập | <YYYY-MM-DD> |
| Người lập | <tên> |
| Hệ thống | <tên hệ thống, địa chỉ> |
| Thời gian mục tiêu (tham khảo, không cứng) | **khoảng <N> phút** (<ai chốt>) |
| Nguồn case | Chỉ chọn từ test case đã có: <liệt kê module + link + số case>. Mã TC có thể trùng giữa module nên cột Mã case gốc ghi kèm tên module |
| Case mới đề xuất | <Không có / liệt kê> |
| Release note | <**Chưa có**, nên chưa có dòng nào thuộc phần Theo build / tóm tắt chỗ đổi> |
| Truy vết | Cột Mã case gốc link tới đúng dòng test case gốc; mục "Truy vết" và "Lịch sử tạo và cập nhật" ở cuối file. Chỉ một file này, mốc nằm trong file |
| Tình trạng | Mọi case gốc đang ở trạng thái "Chưa chạy" (<đã chạy thật bao nhiêu>); thời gian là **ước lượng**. <Module nào dựa trên requirement nháp chưa BA xác nhận: lượt chạy đầu là lượt hiệu chuẩn, case Không đạt thì kiểm lại test case trước khi kết luận trả build> |

**Mục đích.** Smoke test trả lời một câu: build này đủ ổn để bắt đầu test sâu chưa? Một case được chọn khi nó hỏng thì việc test khác vô nghĩa hoặc bị chặn, không phải vì nó nhanh hay dễ. Thời gian chỉ là mục tiêu để giữ smoke nông và gọn; nếu một case cần cho mục đích mà làm vượt mục tiêu thì giữ case, chấp nhận vượt và ghi lý do.

**Cách đọc.** <Thứ tự chạy và lý do (dùng lại phiên đăng nhập/dữ liệu); mật khẩu không ghi vào tài liệu>.

| # | Smoke case | Mã case gốc | Phần | Vì sao chọn | Thời gian ước tính | Nên tự động hoá? |
|---|---|---|---|---|---|---|
| 1 | <Câu đầy đủ: hệ thống làm gì khi người dùng làm gì> | [<Module> · TC-001](<thư-mục>/test-case.md#tc-001) | Cố định | <Hỏng thì chặn gì> | <n> phút | <Nên/Không: lý do> |

**Theo build:** <chưa có dòng nào vì chưa có release note; gợi ý chỗ đổi từ `truy-vet.py kiem` (suy ra từ requirement, không phải từ build), người dùng đồng ý mới đưa vào bảng / các dòng đã thêm>.

**Phạm vi chưa phủ:** <hành trình then chốt và chức năng chưa có test case nên smoke chưa kiểm; nêu rõ "smoke Đạt không bảo đảm các hành trình này">.

## Thời gian ước tính (tham khảo)

| Khoản | Phút (ước lượng) |
|---|---|
| <n> smoke case (<cộng từng case>) | <tổng> |
| Chuẩn bị chung, không phải case: <việc, làm một lần> | <n> |
| **Tổng** | **<tổng>, <so với mục tiêu khoảng N>** |

Ước lượng theo số bước (mỗi bước khoảng 15–20 giây, trang tải 3–5 giây, thêm thời gian đăng nhập), chưa đo bằng chạy thật. Không dùng con số này để cắt case.

## Tiêu chí trả build

Chạy theo thứ tự bảng. **Case nào Không đạt thì dừng ngay, trả build, không chạy tiếp.** "Đạt" chỉ xét **ý chính** (theo số bước của case gốc); ý phụ chỉ ghi vào Kết quả thực tế, không dừng. *Phần tách ý chính/ý phụ là đề xuất, chờ người dùng duyệt.*

| Case | Đạt khi (ý chính; ý phụ ghi trong ngoặc) | Không đạt thì dừng vì |
|---|---|---|
| <# và tên ngắn> | <Bước nào, kết quả gì lấy từ case gốc. (Ý phụ: …) Nếu case đang lệch hệ thống: ngoại lệ đã chốt, liệt kê chính xác ý được miễn> | <hệ quả> |

Đạt cả <n> thì nhận build để test sâu.

## Lượt chạy

Mỗi lần chạy smoke cho một build ghi một dòng: `python -X utf8 scripts/truy-vet-smoke.py ghi-luot <dự-án> --build "<số bản ở chân trang>" --status "1=Đạt,2=Không đạt" [--note "…"]` (số là cột # của bảng; case không nêu coi là Chưa chạy; script tự tính nhận hay trả build). Cách chạy: skill `tao-smoke-test`, mục "Chạy smoke".

<!-- LUOT-CHAY:BAT-DAU (tự sinh bởi scripts/truy-vet-smoke.py ghi-luot, không sửa tay) -->
<!-- LUOT-CHAY:KET-THUC -->

## Truy vết về test case và requirement

Bảng tự sinh khi chốt (đừng sửa tay). Chỉ mã có điểm nhảy trong tài liệu nguồn mới có link.

<!-- TRUY-VET:BAT-DAU (tự sinh bởi scripts/truy-vet-smoke.py, không sửa tay) -->
<!-- TRUY-VET:KET-THUC -->

## Khi requirement hoặc test case đổi

Chạy `python -X utf8 scripts/truy-vet-smoke.py kiem <dự-án>` (chỉ đọc, in vài dòng). Case báo "Cần xem lại" hoặc "Test case đã sửa": đọc lại test case gốc rồi giữ, đổi hoặc bỏ; sửa thẳng bảng trong file này, rồi `python -X utf8 scripts/truy-vet-smoke.py chot <dự-án> -m "đã làm gì"`. Case mới chưa có test case gốc thì viết test case gốc trước rồi link.

## Lịch sử tạo và cập nhật

<!-- LICH-SU:BAT-DAU (tự sinh bởi scripts/truy-vet-smoke.py, không sửa tay) -->
<!-- LICH-SU:KET-THUC -->
