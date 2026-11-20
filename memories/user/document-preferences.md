# Người dùng muốn tài liệu viết thế nào (chi tiết)
Đọc khi: viết báo cáo, SRS, bảng soát, checklist, câu hỏi BA.

## Báo cáo khám phá
- MD: sơ đồ Mermaid, ảnh bằng chứng, luồng end-to-end như người dùng thật; không bịa, chưa rõ thì hỏi.
- HTML: giải thích vai trò cho người mới chưa biết lĩnh vực; ảnh khoanh nút đánh số; sơ đồ luồng đánh số bước; đường end-to-end; điểm mơ hồ có lý do + bằng chứng.
- **Giao diện HTML giữ nguyên ở mọi máy, mọi dự án** (font **Be Vietnam Pro** từ 2026-11-19 vì font cũ lỗi dấu tiếng Việt, màu, kiểu sơ đồ) — người dùng báo khi Mac đổi font. Cách làm: `decisions/decision-log.md`, skill `feature-exploration-report` `references/so-do.md`.
- Phải mở được trong khung xem trước của app (≤512 KiB).
- Từ bị chê: "giải phẫu", "dây chuyền", "tick" (script skill chặn). Thuật ngữ IT đúng ngữ cảnh.

## SRS
- Truy nguồn được (ID thống nhất, bằng chứng có link), kiểu story + AC, không tách nhiều bảng khó đọc.
- Khám phá đầy đủ, chỉ tránh đổi dữ liệu người khác/khóa hệ thống; không "bỏ ngõ" vì rủi ro nhỏ (`project/srs-process.md`).

## Bảng gửi người dùng/BA (bài học bảng soát đầu tiên)
Bản đầu quá cô đọng (mã nội bộ, mã thông báo, thuật ngữ nghiệp vụ không giải thích) nên người dùng không hiểu. Quy tắc:
- Mỗi dòng có **cột Tình huống** (làm gì, dữ liệu cụ thể), nội dung **câu đủ ý**.
- Chép **nội dung thông báo** thay vì mã M01…; giải thích thuật ngữ nghiệp vụ ở bảng thuật ngữ đầu file.
- Mã nội bộ (KN-02, CH-03) chỉ để tra chéo, không làm nội dung chính; nhãn chữ thường ("Hỏi BA ngay", "Tự kiểm tra trên hệ thống trước") thay tên riêng của sách.
- Gộp cột phụ cho gọn (6 cột). Cột "Câu hỏi gửi BA" ghi luôn câu BA đã trả lời.
- **Một mã nhiều dòng thì không chép lại ô** (chốt 2026-11-18, người dùng chê "duplicate"): dòng thứ hai trở đi ô Tình huống ghi ngắn "Phần … của dòng trên", ô trích ghi `—`; mã câu hỏi (B15…) kèm link "mở câu" tới file câu hỏi. `kiem-tra.py` mục 8 báo lỗi nếu chép lại. Khi thêm dòng mới vào bảng soát/SRS phải tự áp dụng, không đợi bị nhắc.

## Checklist / test case
- Câu hỏi BA dựa kinh nghiệm (không dấu vết trong nguồn) → tách riêng, hỏi khi cần.
- **Requirement ghi rõ thì suy luận tiếp, ghi chưa rõ thì hỏi** (chốt 2026-11-18 sau khi chê vài câu hỏi là "vô tri"). Ghi "suy ra từ <mã/TL>" kèm lý do. Lý do bảo mật dùng để suy hành vi chức năng, không tự đặt ca test bảo mật. Ví dụ: requirement ghi "N lần liên tiếp" thì cách đếm đã suy được, không hỏi; hệ thống làm khác = nghi lỗi. Skill `phan-tich-requirement` quy tắc 1b.
- **Cột `Tình huống` của test case = tên test case, câu ĐẦY ĐỦ rõ nghĩa** (2026-11-18: bản câu dài lộn xộn bị chê khó hiểu; bản rút ngắn `điều kiện: kết quả` cũng bị chê, người dùng muốn như "Đăng nhập thành công khi nhập đúng tên và mật khẩu"): dạng `<Hệ thống làm gì/hiển thị gì> khi <người dùng làm gì/điều kiện>`, ví dụ `Hiển thị thông báo lỗi khi bỏ trống ô Email`; số liệu chi tiết để cột Dữ liệu test. Đã ghi vào skill (quy tắc 13).
- **Cột `Điều kiện trước` viết gạch đầu dòng** (`- …` mỗi ý một dòng, ngắn; 2026-11-18 người dùng chê đoạn văn dài dòng): trong JSON mỗi phần tử `dieu_kien` là một dòng đã có `- ` ở đầu (script nối bằng `<br>`). **Điều kiện trước chỉ ghi dữ kiện QUAN TRỌNG để vào kiểm tra ca đó** (người dùng chốt 2026-11-18, sau 3 vòng sửa): KHÔNG ghi "đã đăng nhập" (đã nằm ở bước 1; bỏ luôn chữ "tự nhập mật khẩu" ở bước 1), KHÔNG định nghĩa dữ liệu nền chung ở đầu file. Mỗi ca 2–4 gạch ngắn: cách có dữ liệu + trạng thái dữ liệu liên quan kết quả của ca (các trường quyết định kết quả) + trạng thái đặc biệt nếu có (ô đang trống, bước trước chưa làm). Bản 4–5 gạch lặp mọi ca bị chê rối. Muốn đổi phần đầu file thì xóa file rồi sinh lại (`sinh-bang.py` chỉ thay bảng giữa hai dấu; chỉ làm được khi chưa có cột ghi khi chạy). Đã ghi vào skill `tao-checklist-test-case` (quy tắc 5, 13; mẫu `mau-du-lieu-gop.json`).
- **Cột `Nguồn` của file gộp viết bằng câu thường + link** (2026-11-18, người dùng chê "mã + tên ngắn" khó hiểu, khó truy vết): dòng 1 căn cứ chính `Có trong tài liệu: <câu> (<link "SRS, S01-AC03" trỏ tới neo <mã>-s01-ac03>).`; dòng 2 câu trả lời chi phối (TL-02) nếu có; dòng 3 `⚠️ Hệ thống đang hiện …` nếu có; dòng 4 `Tra thêm: quy tắc R02; thông báo M06.` (không link, để script tính phủ). Link cần thẻ neo `<a id="<mã>-s01-ac03"></a>` ở ô đầu mỗi dòng mã SRS; khuôn `srs/_template.md` có neo mẫu, `check-srs.py` cảnh báo dòng thiếu và `--them-neo` tự chèn (2026-11-19). Đã ghi vào skill.
- Có cột ưu tiên + lý do cần nhiều TC/câu hỏi.
- Test case có cột ghi khi chạy: Ưu tiên, Kết quả thực tế, Trạng thái, Người viết (mặc định tên trong `.nguoi-test` của máy), Tự động hóa (lưu script chạy lại cho đỡ token) — khuôn của `tao-checklist-test-case`: từ 2026-11-18 **một bảng gộp 13 cột** (có cả Kỹ thuật, không `checklist.md` riêng) cho mọi feature.

## Câu hỏi BA
Xưng hô, từ đã chốt, khuôn: `conventions/ba-question-wording.md` (bài học "câu chữ máy móc như dịch tiếng Anh").
- **Bug report (người dùng chỉnh bug đầu tiên, 2026-11-18):** tiêu đề chỉ mô tả lỗi, không thêm lý do/ngữ cảnh (không "dù BA đã chốt…"); gọi "thanh điều hướng" (không "thanh điều hướng"); dòng Trình duyệt chỉ ghi tên + số bản (+ hệ điều hành), không ghi Playwright/chế độ ẩn, không gắn Giả định; Kết quả mong đợi không chèn ngoặc nguồn (nguồn ở mục Test case liên quan); mức độ nghiêm trọng/ưu tiên ghi tiếng Việt (Nghiêm trọng/Lớn/Nhỏ/Rất nhỏ; Cao/Trung bình/Thấp), không ghi Severity/Priority; câu hỏi cho Dev viết đủ ngữ nghĩa (điều đã thấy, điều chưa biết, vì sao hỏi, sẽ làm gì tùy câu trả lời). Đã ghi vào skill `tao-bug-report` và mẫu.
