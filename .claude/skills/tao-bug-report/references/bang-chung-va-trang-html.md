# Bằng chứng, trang HTML của bug và nối vào bảng kết quả

## Ảnh bằng chứng tô đỏ chỗ lỗi
Người đọc phải nhìn ảnh là thấy ngay lỗi ở đâu. Giữ ảnh gốc, thêm ảnh `-loi`.
- **Script test tự làm** (khi có script `auto/`): `check_main`/`check_minor` khai `mark_text="chữ lỗi"` và `error_note="Lỗi ở bước 5 (…): <thấy gì>, đáng ra <đúng là gì>."`. Ý sai → runner chụp ảnh `-loi.png` chỉ có khung đỏ + nhãn "LỖI" đúng chỗ chữ sai (trường `error_images`, chú thích ở `error_image_captions` trong `result-*.json`). Ý đạt có `mark_text` → ảnh `-kiem.png` (khung xanh) chỉ để hiện ở trang kết quả, không dùng cho bug.
- **Ảnh đã chụp sẵn hoặc vùng nhiều dòng:** `python -X utf8 scripts/mark_error.py <ảnh.png> --box x1,y1,x2,y2 [--label LỖI] [--out <ảnh>]` (góc trên-trái và dưới-phải, đơn vị điểm ảnh; tô cả khung lỗi thay vì từng chữ). Xem ảnh kết quả bằng `Read` để chắc khung đúng chỗ rồi mới đính kèm.
- Trong "Đính kèm cần có" mỗi ảnh lỗi ghi một dòng, ví dụ: `- [x] Ảnh đã tô đỏ chỗ DEFAULT (lỗi ở bước 5 của các bước tái hiện): evidence/<dự-án>/…/x-loi.png`. Khuôn chú thích: **"Lỗi ở bước N (việc đang làm): thấy <gì>, đáng ra <đúng là gì>."**

## Video
Ca Không đạt chạy tự động có video `.webm` ở `evidence/<dự-án>/chay-test/video/` (thư mục này không vào git). **Chép vào thư mục của bug bằng `scripts/luu-bang-chung.py`** (`evidence/<dự-án>/bug/BUG-nnn/`, có vào git) để bug mở ở máy nào cũng có video; script tự ghi dòng `- [x] Video quay lại các bước …: <đường dẫn>` và dòng ảnh lỗi tô đỏ; trang bug hiện trình phát. Chưa có video thì ghi `Cần bổ sung`; không chạy lại ca có thể gây chặn hay đổi dữ liệu chỉ để lấy video.

## Trang HTML của bug
Sau khi lưu file md: `python -X utf8 scripts/build_docs.py --all` (hoặc riêng `build_report.py bug-pages`) dựng `BUG-nnn.html` cạnh file md. Trang **tự sinh, không sửa tay**; sửa md rồi chạy lại. Có: huy hiệu mức độ nghiêm trọng/ưu tiên/tần suất; mỗi mục một thẻ có nút **Sao chép** (dán công cụ quản lý bug, chat), "Sao chép tiêu đề", "Sao chép cả bug (md)"; ảnh nhỏ (ảnh `-loi` viền đỏ), video có trình phát; `[Giả định: …]` tô vàng; chế độ sáng/tối; logo theo `docs/thuong-hieu/brand.json`. Báo link trang HTML cho người dùng (không chỉ link md).

## Bug đến từ lượt smoke hoặc lượt chạy tự động
- Bảng `testing/<dự-án>/smoke-ket-qua.*` (hoặc `<tính-năng>/ket-qua-test-case.*`) sinh từ `run-results/<bộ>.json`. Lượt đã ghi mà chưa có bug thì dựng lại bằng lệnh ghi lượt kèm `--bug "N=BUG-nnn"` (cột Bug link tới trang HTML của bug), `--error-images "N=<ảnh -loi>"`, `--error-captions "N=Lỗi ở bước …"` (N = cột # của `smoke-test.md`, hoặc số của mã TC với `--suite <tính-năng>`). **Hỏi người dùng trước khi dựng lại lượt đã ghi.** Điền `Trạng thái` của test case thì cũng hỏi trước.
- Mỗi nguyên nhân một bug, `BUG-nnn` không dùng lại số; ca `Không kết luận` do lỗi của mình (script, bộ đếm) không phải bug.
- Ca không test được vì bug này: ghi ở Phạm vi ảnh hưởng; trên trang kết quả đặt `Bị chặn` kèm link bug: `add-run --status "N=Bị chặn" --blocked-by "N=BUG-nnn"`; trong test case ghi "Bị chặn bởi BUG-nnn".
- Suy luận từ số liệu (ví dụ cách hệ thống đếm lần sai) gắn `[Giả định: …]`.
Quy tắc đầy đủ của lượt chạy tự động: skill `chay-test-tu-dong`, `references/quy-tac-da-chot.md` mục 6.
