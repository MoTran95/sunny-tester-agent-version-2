# Quy tắc viết checklist

> **Từ 2026-11-18 (file gộp):** feature mới không có `checklist.md` riêng. Các quy tắc dưới đây vẫn áp dụng cho các cột `Tình huống`, `Ưu tiên`, `Kỹ thuật`, `Nguồn` của **bảng gộp 13 cột** trong `test-case.md` (`Mã | Tình huống | Ưu tiên | Kỹ thuật | Điều kiện trước | Các bước | Dữ liệu test | Kết quả mong đợi | Nguồn | Kết quả thực tế | Trạng thái | Người viết | Tự động hóa`). Mục "Chưa đưa vào" và "Câu hỏi cho BA" nằm cuối `test-case.md`. Bảng 5 cột dưới đây chỉ còn cho feature cũ có hai file (Đăng nhập).

## Khuôn bảng (5 cột, tiêu đề cố định để script đọc)
`| Mã | Tình huống | Ưu tiên | Kỹ thuật | Nguồn |`
- **Mã:** `TC-001`, `TC-002`… liên tục, không nhảy số, không dùng lại. Dòng **Cao xếp trước**, rồi Trung bình, rồi Thấp (script `sinh-bang.py` tự đánh mã sau khi xếp).
- **Tình huống (= tên test case):** câu đầy đủ rõ nghĩa dạng `<Hệ thống làm gì/hiển thị gì> khi <người dùng làm gì/điều kiện>`, ví dụ `Đăng nhập thành công khi nhập đúng tên và mật khẩu`. Không rút gọn kiểu `điều kiện: kết quả`, không dùng mã nội bộ; con số chi tiết để cột Dữ liệu test (trong tên chỉ giữ số làm nên ca, đặt trong ngoặc). Một mục tiêu một dòng, **một** giá trị không hợp lệ hoặc **một** đường không được phép.
- **Ưu tiên:** `Cao`, `Trung bình`, `Thấp` (tiêu chí trong `ky-thuat-thiet-ke.md`).
- **Kỹ thuật:** đúng một trong `EP`, `BVA`, `Bảng quyết định`, `Chuyển trạng thái`, `Use case`, `Đoán lỗi`.
- **Nguồn (file gộp, từ 2026-11-18):** tối đa bốn dòng trong một ô, nối bằng `<br>`, viết bằng **câu thường** (người dùng chê dòng toàn mã và tên ngắn là khó hiểu, khó truy vết):
  1. **Căn cứ chính**, bắt đầu bằng nhãn: `Có trong tài liệu: <câu nói điều SRS ghi> ([SRS, <mã tiêu chí>](<đường dẫn SRS>#<neo>)).` hoặc `Suy luận: <một câu lý do, điểm xuất phát là điều nguồn đã ghi> ([SRS, …](…)).` Mã tiêu chí (`S01-AC03`) link tới đúng dòng của SRS; nếu căn cứ là quy tắc thì ghi `[SRS, quy tắc R01](…#cart-r01)`.
  2. Nếu có: **câu trả lời đã chốt chi phối kết quả**, ví dụ `Làm tròn lên 2 chữ số: [TL-02](bảng-soát.md#…) (tester chọn, BA chưa xác nhận).`
  3. Nếu có: `⚠️ Hệ thống đang hiện <điều thấy>.` khi bản đang chạy làm khác kết quả mong đợi (nghi lỗi, chưa phải lỗi đã xác nhận).
  4. Nếu có mã phụ: `Tra thêm: quy tắc R02; thông báo M06.` (không link). `kiem-tra-tc.py` tính phủ requirement theo các mã này nên mã phụ không được bỏ.
  Link cần **thẻ neo** `<a id="<tiền-tố>-<mã>"></a>` (chữ thường, ví dụ `cart-s01-ac03`) đặt ở ô đầu mỗi dòng mã của SRS, như đã làm cho dòng bằng chứng `E..`; SRS chưa có thì thêm bằng `python -X utf8 .claude/skills/srs-from-website/scripts/check-srs.py <SRS> --them-neo` (không đổi nội dung; `truy-vet.py` bỏ thẻ neo khi băm nên không làm mã bị tính là đổi). Đầu file có đoạn "Cách đọc cột Nguồn" giải thích `S01-AC03`, `R`, `M`, `TL`. **Không có dòng `Giả định` trong bảng.** Tên ngắn trong `truy-vet-cau-hinh.json` vẫn dùng cho `truy-vet.md`, không ghi vào cột Nguồn nữa.

## Đầu file, sau bảng
- Đầu file: bảng nhỏ (Ngày lập, Hệ thống, Nguồn, "Chỉ làm: checklist, chưa viết bước chi tiết"), đoạn "Cách đọc cột Nguồn", lưu ý an toàn nếu có ca có thể gây khóa.
- Sau bảng: **Câu hỏi cho BA** (mỗi câu kèm mã requirement liên quan; xem dưới), **Chưa đưa vào** (phần chưa chốt), **Tự kiểm**.

## Câu hỏi cho BA và phần chưa chốt
- **Không có bảng soát:** mọi chỗ nguồn không nói thành `Giả định` → đưa vào "Câu hỏi cho BA", mỗi câu ghi mã requirement liên quan. Câu hỏi viết đọc là hiểu (tình huống thật, nêu cách mình đang hiểu); khuôn đầy đủ ở skill `phan-tich-requirement`.
- **Có bảng soát:** chỉ viết dòng đã rõ/đã chốt (✅). Phần ❓ không viết dòng, chỉ liệt kê ở "Chưa đưa vào" kèm mã câu hỏi sẵn có (ví dụ B4); không lập câu hỏi mới trùng.
- Điều requirement ghi rõ thì **suy luận tiếp** (ghi `Suy luận`), không hỏi. Chỗ nguồn **chưa ghi** (con số, cách hiển thị) thì hỏi, không lấp bằng kinh nghiệm.

## Tự kiểm trước khi trả lời (script `kiem-tra-tc.py` làm phần cơ học)
- Mỗi mã requirement (và mã câu trả lời đã chốt cần phủ) có ít nhất một dòng.
- Không trùng mã. Dòng nào cũng có nhãn nguồn. Không có dòng `Giả định` trong bảng.
- Kỹ thuật và ưu tiên đúng danh sách; Cao xếp trước.
- Mỗi dòng một giá trị không hợp lệ; chưa có dòng nào thêm quy tắc mà nguồn không nêu.
