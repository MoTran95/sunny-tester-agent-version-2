---
name: tao-test-summary-report
description: Tạo báo cáo tổng kết kiểm thử cho một build từ các lượt chạy (smoke, regression, tính năng), bug và độ phủ requirement; trang HTML có form duyệt build và nút In / Lưu PDF. Dùng khi nghe "test summary report", "báo cáo tổng kết kiểm thử", "báo cáo tổng kết build", "ghi quyết định duyệt build". Không dùng để chạy test, viết bug hay chọn smoke/regression.
---

# Tạo báo cáo tổng kết kiểm thử (test summary report)

**Báo cáo trả lời:** build này test được tới đâu, còn rủi ro gì, và ai quyết định nhận hay không. Số liệu **do chương trình đọc từ file có sẵn**, không viết tay, không dùng AI để tính. Tiếng Việt với người dùng; chỉ lỗi chức năng.

## Bước 0: dự án
Đọc `.du-an-hien-tai` (chưa có thì làm theo `CLAUDE.md` bước 0). Chỉ đọc `testing/<slug>/` của dự án đó; skill này không chứa thông tin riêng dự án nào.

## Đầu vào cần có (kiểm trước khi sinh)
- `testing/<slug>/run-results/*.json`: ít nhất một lượt chạy đã ghi (smoke, `regression-tang-N` hoặc bộ test case của một tính năng). Chưa có lượt nào thì dừng, báo người dùng chạy theo `chay-test-tu-dong`; **không bịa số liệu**.
- Mỗi lượt nên có phần **Kết luận và rủi ro** (`conclusion`): mục 2, 7, 8 của báo cáo lấy từ đó. Lượt thiếu phần này thì các mục ấy trống: nói rõ cho người dùng, đề nghị bổ sung bằng `chay-test-tu-dong`, không tự viết thay.
- Build: không nói gì thì báo cáo lấy **build của lượt mới nhất**; người dùng nêu build khác thì thêm `--build X`. Bộ test chưa có lượt ở build đó sẽ được ghi "chưa có lượt ở build này".

## Quy trình
1. **Sinh:** `python -X utf8 scripts/build_report.py summary [--build X] [--author "Tên"]` (máy không có `python` thì `python3`). Ra `testing/<slug>/test-summary-report.md` và `.html`; `build_docs.py` cũng tự sinh lại trang này. Người viết báo cáo mặc định là người chạy lượt mới nhất; người dùng muốn tên khác thì hỏi tên rồi dùng `--author`.
2. **Đọc lại bản md** và kiểm: đủ 9 mục (thông tin chung, kết luận, kết quả theo tính năng, theo bộ test, bug, độ phủ requirement, rủi ro còn lại, đề xuất tiếp theo, duyệt build); mục 3 có đủ tính năng có test case; số bug khớp thư mục `bug/`.
3. **Trả lời người dùng:** **một link trang tổng** `testing/<slug>/index.html` (kèm điểm nhảy tới đúng phần, xem CLAUDE.md mục "Trả kết quả HTML"), không liệt kê nhiều file HTML, 3–4 số chính (tổng test case, đã có kết luận, Không đạt, bug), chỗ còn thiếu dữ liệu (lượt thiếu kết luận, bug còn "Chưa ghi" trạng thái: hỏi người dùng chốt rồi ghi bằng `dat-trang-thai-bug.py` của skill `lap-ke-hoach-retest`, không tự đoán), và cách điền duyệt build + in PDF (bên dưới). Không dán cả bảng vào chat.
4. **Sinh lại và kiểm:** `python -X utf8 scripts/build_docs.py --all` rồi `python -X utf8 scripts/kiem-tra-bo-nho.py` (báo lỗi nếu còn trang cũ).

## Duyệt build (người dùng làm, Claude không điền thay)
Mục 2 là **đề xuất của người test**; mục 9 là **quyết định của người duyệt build**. Hai bên có thể khác nhau.
1. Người dùng mở trang HTML, chọn quyết định, điền tên, chức danh, điều kiện (bắt buộc khi chọn "Nhận có điều kiện"), ghi chú, rồi bấm **Tải file duyệt**.
2. Đặt file `duyet-build.json` vào `testing/<slug>/` (ghi đè), chạy lại `build_docs.py`: quyết định vào cả md và HTML.
3. Quyết định gắn với **số lượt từng bộ test lúc duyệt**. Có lượt mới sau đó thì trang tự báo **"Đã lỗi thời"**: nhắc người dùng xem lại và duyệt lại; **không sửa `based_on` bằng tay để lách**.
4. **Không tự điền** tên người duyệt, quyết định hay ngày duyệt. Nếu chính người dùng đọc nội dung ngay trong chat ("người duyệt là …, nhận có điều kiện, điều kiện …"), chỉ ghi đúng điều họ nói vào `duyet-build.json` theo `references/khuon-duyet-build.md`; thiếu tên hoặc điều kiện thì hỏi (đủ ngữ cảnh, tối đa 3 câu).
5. Người duyệt build là ai, cố định hay đổi theo build: người dùng nêu; chưa biết thì hỏi, không đoán.

## Gửi người khác
Nút **In / Lưu PDF** trên trang (hộp thoại in của trình duyệt, chọn "Lưu dưới dạng PDF"): bản in nền sáng, ẩn nút, câu hướng dẫn thao tác, cột link tới trang khác và Phụ lục; giữ nội dung đã điền. Link tương đối trong PDF không bấm được ở máy khác (chữ vẫn đọc được). Chưa có lệnh sinh PDF bằng script; người dùng cần thì nói rõ là chưa có (có thể làm bằng Playwright sau).

## Quy tắc người dùng đã chốt (2026-11-19)
- **Không logo**, không dòng "build" hay "trang tự sinh" dưới tiêu đề: báo cáo gửi công ty. Tiêu đề chữ lớn **Báo cáo tổng kết kiểm thử**; tên dự án và build nằm ở mục 1.
- Có **người test** và **người duyệt build**; điền ngay trên HTML, lưu bằng file (cách A), không dùng dịch vụ ngoài.
- **Mọi mã có link bấm được**: TC, RG, SM (về test case gốc), BUG, mã requirement. Mã không tìm được nơi định nghĩa thì giữ chữ, không link bậy; TC trong câu của bộ smoke/regression chỉ link khi ngay trước có tên tính năng.
- Mỗi test case lấy **kết quả mới nhất trong các lượt cùng build**; tỉ lệ đạt tính trên số đã có kết luận.
- Báo cáo không tự quyết nhận hay trả build.

## Tự kiểm trước khi trả lời
- [ ] Build trong mục 1 đúng build người dùng cần; bộ test không có lượt ở build đó được ghi rõ.
- [ ] Không có logo; không có quyết định, tên, ngày duyệt nào do Claude tự điền.
- [ ] Mã trong báo cáo đều có link (trừ mã không tìm được nơi định nghĩa).
- [ ] Đã nói rõ phần thiếu dữ liệu (lượt thiếu kết luận, bug còn "Chưa ghi" trạng thái: hỏi người dùng chốt rồi ghi bằng `dat-trang-thai-bug.py` của skill `lap-ke-hoach-retest`, không tự đoán).
- [ ] `build_docs.py --all --check` báo khớp.

## Tệp trong skill
- `references/khuon-duyet-build.md`: khuôn `duyet-build.json` và các trường.
