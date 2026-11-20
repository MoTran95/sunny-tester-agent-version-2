---
name: tao-test-plan
description: Lập test plan (kế hoạch kiểm thử 12 mục, HTML không logo, in PDF) ngay sau phân tích requirement; số liệu tự đọc từ tài liệu dự án, chỗ chưa biết hỏi người test qua phiếu; cập nhật khi đã có test case, smoke, regression. Dùng khi nghe "lập test plan", "kế hoạch kiểm thử", "sếp yêu cầu test plan", "cập nhật test plan", "bản gọn test plan", "xuất PDF test plan". Không dùng để chạy test hay báo cáo kết quả.
---

# Lập kế hoạch kiểm thử (test plan)

**Test plan là phần CHƯA test.** Nó trả lời: sẽ test cái gì, bằng cách nào, khi nào xong, rủi ro gì, ai làm. Kết quả test nằm ở báo cáo tổng kết (`tao-test-summary-report`), không nằm ở đây. Tiếng Việt với người dùng; chỉ test chức năng, trừ khi sếp yêu cầu khác.

## Bước 0: dự án
Đọc `.du-an-hien-tai` (chưa có thì làm theo `CLAUDE.md` bước 0). Chỉ đọc `memories/modules/<slug>/`, `srs/<slug>/`, `testing/<slug>/`, `evidence/<slug>/` của dự án đó. Skill này không chứa thông tin dự án nào.

## Quy tắc người dùng đã chốt (2026-11-19)
1. **Không ghi kết quả test**: không số case đã chạy/Đạt/Không đạt, không mã bug đã ghi, không "lượt chạy", không cột "Hiện trạng". Rủi ro viết dạng "có thể", dựa trên requirement và khám phá, **không rút từ lượt chạy** (kể cả đổi chữ thành "có thể"). Script kiểm bắt các mẫu này.
2. **Viết như bản thật** gửi được ngay: không khung "bản nháp", không nhãn "Giả định H…". Điều người lập tự quyết viết thẳng; điều đang coi là đúng gom ở mục 9.2.
3. **Không logo**, không thanh điều hướng nội bộ, không dòng "Trang tự sinh…" (file `test-plan*.md` tự dùng kiểu gửi ra ngoài: `docs_pages.py` `clean=True`). Có nút In / Lưu PDF; ô chờ điền `……………` được tô để dễ thấy.
4. **Không tự đặt con số hay tên người**: ngưỡng tiêu chí kết thúc, tên BA/Dev/người duyệt, ngày, mã kế hoạch, số bản trình duyệt, công cụ bug. Chưa có thì để ô trống rồi hỏi người test. Số đã có sẵn ở dự án (trần nhập sai, thời gian chặn, thời hạn phiên) lấy từ `memories/modules/<slug>/` và `testing/<slug>/auto-config.json`.
5. Điều người test quyết "tùy người quyết theo nguồn lực/thời gian" thì ghi đúng như vậy kèm nơi ghi lại (báo cáo tổng kết), không ép thành con số.
6. **Mọi tài liệu nhắc tới có link bấm được**; file kết quả chưa có thì ghi tên trong dấu `…` không link.
7. Văn phong: tiếng Việt thường, câu đủ ý, không Given/When/Then, không mã nội bộ làm nội dung chính. Mật khẩu không ghi vào tài liệu.

## Cách làm việc: một nguồn, ba lớp
`test-plan.md` là file **sinh ra**, không sửa tay. Số liệu và câu trả lời không gõ vào file chữ:
- `testing/<slug>/test-plan-nguon.txt`: phần chữ do Claude viết (khuôn `assets/mau-test-plan-nguon.txt`), có các dấu `{{…}}` (danh sách ở đầu `scripts/sinh-test-plan.py`).
- Số liệu (số test case, mã requirement, bộ smoke/regression, độ phủ, mã chưa có case, link SRS) do **script đọc từ tài liệu dự án** mỗi lần sinh. `kiem` báo lệch nếu số đổi hoặc ai sửa tay.
- `testing/<slug>/test-plan-thong-tin.json`: câu trả lời của người test (khóa → chữ; khóa ở `references/khoa-thong-tin.json`). Thiếu khóa thì ô để `……………`. Cập nhật test plan không mất câu trả lời.

## Quy trình
1. **Xác định đợt test:** hệ thống, bản build, tính năng trong phạm vi, ai yêu cầu. Tra `memories/` và `testing/<slug>/` trước, chỉ hỏi cái thiếu. Đợt/bản build mới giữ bản cũ: thêm `--ten test-plan-<build>` vào mọi lệnh `sinh-test-plan.py` / `kiem-tra-test-plan.py --file test-plan-<build>.md` (nguồn, JSON, md, phiếu đều đặt theo tên đó); lần đầu dùng tên mặc định `test-plan`.
2. **Thu thập từ repo** (bảng "Nguồn điền từng mục" ở `references/thong-tin-can-hoi.md`). **Ranh giới dữ liệu:** được đọc phần *kế hoạch* của tài liệu: requirement/SRS, bảng soát, câu hỏi BA, test case (mã, tình huống, ưu tiên, kỹ thuật, cờ), bảng bộ smoke và bộ regression, truy vết, memory dự án. **Không đọc phần kết quả:** cột `Kết quả thực tế`/`Trạng thái`/`Tự động hóa` của test case, mục `Lượt chạy` của smoke/regression, `*-ket-qua.md`, `run-results/`, bug, `test-summary-report.md`; chỉ ghi tên các file kết quả ở mục 8. Số test case lấy từ số dòng, không từ trạng thái.
3. **Viết nguồn:** chạy `sinh-test-plan.py khoi-tao <slug>` (tạo `testing/<slug>/test-plan-nguon.txt` từ `assets/mau-test-plan-nguon.txt`; **nếu đã có thì KHÔNG ghi đè**: sửa trực tiếp file đang có), rồi thay các chỗ `<…>` bằng nội dung từ tài liệu dự án, bỏ khối chú thích đầu và dòng chữ nghiêng hướng dẫn. Tên tính năng/thư mục trong `{{tc:…}}` lấy từ thư mục có `test-case.md`. Chưa có smoke/regression/test case thì ghi "Chưa có" ở phạm vi và rủi ro; **không đề nghị làm chúng trước**: test plan là bước 2 của quy trình, lập ngay sau phân tích requirement (người dùng chốt 2026-11-19), số liệu điền sau bằng "Cập nhật test plan". Không bịa.
4. **Sinh lần đầu:** `python -X utf8 .claude/skills/tao-test-plan/scripts/sinh-test-plan.py sinh <slug>` (máy không có `python` thì `python3`). Rồi `python -X utf8 scripts/build_docs.py --all` để ra HTML.
5. **Hỏi người test các chỗ còn trống:** tạo phiếu `… sinh-test-plan.py phieu <slug>` → `testing/<slug>/test-plan-phieu.html` (form các ô còn thiếu, có nút Tải file `test-plan-thong-tin.json`); người test điền một lần, đặt file vào `testing/<slug>/`. Nếu họ trả lời ngay trong chat thì ghi bằng `sinh-test-plan.py dat <slug> khóa=giá trị …` (gộp vào JSON, kiểm khóa, in "cũ -> mới"); ghi **nguyên văn** điều họ nói, không làm tròn hay thêm; câu trả lời mơ hồ thì hỏi lại; ghi xong **đọc lại từng ô cho họ xác nhận** trước khi `sinh`. Đặt ô trống lại bằng `khóa=` (giá trị rỗng). Hỏi theo `references/thong-tin-can-hoi.md` (đủ ngữ cảnh, không hỏi lại điều đã có). **Bẫy:** hộp chọn `AskUserQuestion` không chuyển chữ gõ ở ô "Other" về Claude, nên số/tên hỏi bằng phiếu hoặc tin nhắn thường; hộp chọn chỉ cho lựa chọn có sẵn, và **không đưa con số làm lựa chọn cho ngưỡng**.
6. **Điền và kiểm:** `sinh-test-plan.py sinh <slug>` lại, `build_docs.py --all`, rồi `python -X utf8 .claude/skills/tao-test-plan/scripts/kiem-tra-test-plan.py <slug>` (phải 0 LỖI; mục "CÒN TRỐNG" là chỗ người test chưa cung cấp, không phải lỗi), rồi `python -X utf8 scripts/kiem-tra-bo-nho.py`.
7. **Mục 9 gồm 9.1 (rủi ro, phụ thuộc: bảng) và 9.2 (giả định: gạch đầu dòng)**; khuôn nguồn đã có sẵn cả hai, không gộp giả định vào bảng 9.1.
8. **Trả lời người dùng:** **một link trang tổng** `testing/<slug>/index.html` (kèm điểm nhảy tới đúng phần, xem CLAUDE.md mục "Trả kết quả HTML"), không liệt kê nhiều file HTML, phần đã điền từ tài liệu, danh sách ô còn trống, nói rõ mục 2.2 (ngoài phạm vi) và mục 9 (rủi ro) là chỗ sếp đọc kỹ nhất. Không dán cả bảng. Commit chỉ khi người dùng nhờ.

## Việc khác
- **Bản gọn (1–2 trang):** `sinh-test-plan.py gon <slug>` → `test-plan-gon.md` (bảng đầu + mục 1, 2, 3, 5, 9, 10; giữ số mục của bản đầy đủ). Kiểm: `kiem-tra-test-plan.py <slug> --file test-plan-gon.md`.
- **PDF:** `python -X utf8 .claude/skills/tao-test-plan/scripts/xuat-pdf.py <slug>` → `testing/<slug>/test-plan.pdf` bằng Chrome/Edge có sẵn (không cần cài thêm; link tương đối trong PDF không bấm được ở máy khác). Không có trình duyệt thì mở HTML bấm In / Lưu PDF. Chưa có xuất Word.
- **Cập nhật:** requirement/test case đổi hoặc build mới: chạy `scripts/truy-vet.py kiem <slug> <tính-năng>`, sửa nguồn/JSON, thêm dòng ở mục 12 (ngày, người sửa, nội dung, lý do) và đổi "Cập nhật lần cuối", rồi `sinh`, `build_docs.py --all`, kiểm.
- **Dự án chưa có nguồn** (test plan viết tay từ khuôn `testing/_template-test-plan.md`): script kiểm báo "LƯU Ý chưa có test-plan-nguon.txt"; nên chuyển sang nguồn.

## Tự kiểm trước khi trả lời
- [ ] `kiem-tra-test-plan.py` 0 LỖI (gồm "khớp bản sinh"); trang HTML không logo.
- [ ] Không có kết quả test nào (số case chạy, bug, lượt chạy); rủi ro không rút từ lượt chạy.
- [ ] Không con số, tên người, ngày nào do Claude tự đặt; chỗ chưa biết còn `……………`.
- [ ] Mục 2.2 có lý do và rủi ro; mục 9 có cột "Cách giảm / ai quyết".
- [ ] Mã requirement/test case/tài liệu đều có link, không link gãy.

## Tệp trong skill
- `assets/mau-test-plan-nguon.txt`: khuôn nguồn (có dấu `{{…}}`).
- `references/thong-tin-can-hoi.md`: nguồn điền từng mục, thông tin phải hỏi người test, cách đặt câu hỏi. `references/khoa-thong-tin.json`: khóa, nhóm, câu hỏi của phiếu.
- `scripts/sinh-test-plan.py` (`khoi-tao` / `dat` / `sinh` / `kiem` / `gon` / `phieu`), `scripts/kiem-tra-test-plan.py`, `scripts/xuat-pdf.py`.
- Khuôn đọc cho người: `testing/_template-test-plan.md` (dùng chung, tự sinh HTML).
