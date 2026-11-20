# Bộ regression test — <Tên hệ thống> (bản <số bản>)

| | |
|---|---|
| Ngày lập | <YYYY-MM-DD> |
| Người lập | <tên> |
| Hệ thống | <tên và địa chỉ môi trường thử> |
| Phạm vi | <các tính năng đã có test case, số case mỗi tính năng; chỉ chọn từ test case đã có> |
| Release note | <Chưa có: bảng phân tích viết theo vùng chức năng. / Có: nguồn> |
| Truy vết | Mục "Truy vết" và "Lịch sử" ở cuối file; mốc nằm trong file. Khi requirement hoặc test case đổi: `python -X utf8 scripts/truy-vet-regression.py kiem <dự-án>` |
| Tình trạng | <Bản đề xuất chờ người dùng duyệt / số case đã chạy thật / nguồn nháp> |

**Mục đích.** Regression trả lời: sau khi hệ thống đổi, phần đang chạy đúng có còn đúng không? Ba tầng:

| Tầng | Nghĩa | Khi nào chạy |
|---|---|---|
| Tầng 1 | **Lõi**: luồng chính mà hỏng thì không test được việc khác | Mọi đợt phát hành |
| Tầng 2 | **Vùng bị ảnh hưởng**: nhóm case theo vùng chức năng | Chỉ vùng mà thay đổi chạm tới |
| Tầng 3 | **Toàn bộ** <N> case | Chỉ khi có lý do |

## Phân tích ảnh hưởng

Nhãn nguồn: **Có trong tài liệu** · **Suy luận** (cần Dev xác nhận) · **Giả định** (không có căn cứ).

| Thay đổi hoặc nếu vùng này đổi | Vùng có thể bị ảnh hưởng | Lý do | Nhãn nguồn |
|---|---|---|---|
| <…> | <chức năng dùng chung · chức năng đứng sau trong luồng · tích hợp ngoài> | <…> | <nhãn> |

## Danh sách regression theo tầng

| Tầng | Vùng | Mã case gốc | Lý do chọn |
|---|---|---|---|
| Tầng 1 | <vùng> | [<Tên module> · TC-001](<thư-mục>/test-case.md#tc-001) <tình huống> | <hỏng thì chặn gì> |
| Tầng 2 | <vùng> | [<Tên module> · TC-010](<thư-mục>/test-case.md#tc-010) <tình huống><br>[<Tên module> · TC-011](<thư-mục>/test-case.md#tc-011) <tình huống> | Chọn khi <điều gì đổi> |
| Tầng 3 | Toàn bộ | Cả <N> test case của các tính năng | Chỉ đề xuất khi có lý do: <…> |

**Cách chọn phạm vi cho một đợt.** Mặc định Tầng 1. Có release note hoặc có mã requirement đổi thì thêm các vùng Tầng 2 mà bảng phân tích chỉ ra. Tầng 3 chỉ khi có lý do.

**Rule: bug lọt production.** Bug đã lọt ra production mà chưa có test case nào chặn đúng bug đó thì phải viết case mới và đưa vào bộ này (Tầng 1 nếu hỏng thì chặn việc khác, không thì vào vùng tương ứng của Tầng 2). Case sinh từ bug ghi ở cột "Lý do chọn" bắt đầu bằng `Bug lọt production <mã bug>:` và ở cột Nguồn của test case gốc; không bị bỏ khỏi bộ khi chưa có quyết định của người dùng. Cách làm: skill `de-xuat-regression`, mục "Rule: bug lọt production".

## Lưu ý khi chạy

- <bộ đếm nhập sai, case có ⚠️, nguồn nháp, thứ tự chạy để dùng lại phiên, ca người dùng tự chạy tay>

## Case đề xuất viết thêm

| Vùng rủi ro | Vì sao thiếu | Đề xuất |
|---|---|---|
| <…> | <…> | <…> |

## Câu hỏi nên hỏi Dev để khoanh vùng chính xác hơn

1. <…>

## Lượt chạy

Mỗi lần chạy một tầng ghi một dòng bằng `python -X utf8 scripts/truy-vet-regression.py ghi-luot <dự-án> --tang "Tầng 1" --build "<số bản>" --ket-qua "<tính-năng>/TC-005=Đạt,..." [--ghi-chu "..."]` (case của tầng không nêu coi là Chưa chạy). **Trang kết quả đầy đủ** (từng case, ảnh, bug, kết luận và rủi ro): `regression-tang-<N>-ket-qua.html`, sinh bằng `build_report.py add-run --suite regression-tang-<N>` (xem skill `de-xuat-regression`, mục "Chạy regression và ghi kết quả"). Kết quả từng case cũng nằm ở cột Trạng thái, Kết quả thực tế của test case gốc và thư mục `evidence/<dự-án>/chay-test/`.

<!-- LUOT-CHAY:BAT-DAU (tự sinh bởi scripts/truy-vet-regression.py ghi-luot, không sửa tay) -->
<!-- LUOT-CHAY:KET-THUC -->



<!-- TRUY-VET:BAT-DAU (tự sinh bởi scripts/truy-vet-regression.py, không sửa tay) -->
<!-- TRUY-VET:KET-THUC -->

## Khi requirement hoặc test case đổi

Chạy `python -X utf8 scripts/truy-vet-regression.py kiem <dự-án>`, xử lý theo skill `de-xuat-regression`, rồi `chot -m "đã làm gì"`.

## Lịch sử tạo và cập nhật

<!-- LICH-SU:BAT-DAU (tự sinh bởi scripts/truy-vet-regression.py, không sửa tay) -->
<!-- LICH-SU:KET-THUC -->
