# Quy tắc đã chốt với người dùng (chạy test tự động)

Mỗi dòng là điều người dùng đã xác nhận hoặc bài học đã trả giá. Không đổi khi chưa hỏi.

## 1. Chọn ca và an toàn hệ thống
- Chỉ **bỏ qua ca mà chính bước làm gây chặn hệ thống** (lần sai thứ 10, nhập khi đang bị chặn, chờ hết chặn…), để tester tự làm: trạng thái `Bỏ qua`, cột Tự động hóa `Không tự động được: <lý do>`. Ca **chạm sát ngưỡng nhưng kết quả mong đợi là KHÔNG chặn** vẫn làm.
- **Số lần nhập sai cho phép KHÔNG có mặc định.** Trần (`login.max_consecutive_failures`) và thời gian chặn (`login.block_minutes`) do requirement của dự án quy định hoặc **hỏi người kiểm thử**, rồi ghi vào `auto-config.json` của dự án; chưa khai thì thư viện từ chối mọi lần cố ý nhập sai (ca thành `Không kết luận`). Đếm **cộng dồn** (đăng nhập đúng xen giữa KHÔNG đưa về 0: cách thận trọng, vì từng thấy hệ thống không reset khác quy định). Bộ đếm `failure_counter` từ chối vượt trần hoặc khi đang chặn; về 0 khi hết thời gian chặn hoặc `run_tests.py --reset-failure-counter` (chỉ khi chắc hệ thống đã về 0). Ca có nhập sai khai `ready_account` và `wrong_attempts`; xếp ca ít sai trước; gặp mã 429 thì dừng ngay, ghi `Không kết luận` (không phải Không đạt).
- Tạo dữ liệu thật (hồ sơ nháp…) chỉ khi người dùng cho phép rõ; công cụ chặn nếu chưa hỏi. Mỗi ca bấm Lưu dùng hết một hồ sơ: ghi `auto-data.json`.
- Tải file (ffmpeg, font) cần người dùng đồng ý, nêu tên file, nguồn, dung lượng.

## 2. Đăng nhập và mật khẩu
- Chỉ nhập tài khoản test của dự án vào địa chỉ **do người dùng nêu và có nhãn môi trường thử** (staging, dev, test, qa, sandbox, preview). Địa chỉ khác → không nhập, nhờ người dùng tự chạy `auto_login.py`.
- **Mình tự nhập được cả mật khẩu thật lẫn mật khẩu sai của tài khoản test** (người dùng dặn lại 2026-11-20), trong giới hạn địa chỉ ở trên; không bao giờ in/ghi lại.
- Mật khẩu chỉ nằm trong `.env`; chỉ thư viện đọc. Script ca, kết quả, ảnh, bug, chat **không bao giờ** chứa mật khẩu; mật khẩu sai dùng chữ giả (`Sai@Matkhau1`). `ctx.sign_in(tài khoản)` và `ctx.submit_login(..., password_of=…, variant=…)` để script không thấy mật khẩu.
- Phiên sống ngắn (thời hạn khai ở `session_minutes` của dự án): runner kiểm phiên đầu lượt (thoát mã 3 nếu hết). Đăng xuất làm mất phiên phía máy chủ → khai `invalidates_sessions` hoặc dùng `ctx.sign_in` riêng cho ca đó (mỗi lần đăng nhập là phiên riêng).

## 3. Kết luận từng ca
- Giá trị: `Đạt`, `Đạt kèm ý phụ sai`, `Không đạt`, `Không kết luận`, `Chưa có script`. `Đạt kèm lỗi đã biết` chỉ ở smoke và chỉ cho ý được miễn trong tiêu chí trả build.
- Ý chính sai → Không đạt; ý phụ sai → chỉ ghi nhận. Trang kết quả theo tính năng: ca còn lỗi đã biết ghi `Không đạt` kèm bug (khác smoke).
- Chờ phần tử bằng `wait_text`/`poll_until` (trang hay ở "Đang tải…" vài giây), không chờ giây cố định; không `except: pass`.
- Trạng thái test case: `Chưa chạy`, `Đạt`, `Không đạt`, `Bị chặn` (chưa test được vì **bug của case khác**; ghi link bug ở Kết quả thực tế), `Bỏ qua`.

## 4. Bằng chứng
- `check_main/check_minor(..., mark_text="chữ", error_note="Lỗi ở bước N (…): thấy <gì>, đáng ra <gì>.")`: ý sai → ảnh `-loi.png` (chỉ khung đỏ, dùng cho bug); có ý đạt khai `mark_text` → ảnh `-kiem.png` (khung xanh đạt, đỏ sai) hiện ở cột Evidence.
- Video quay mọi ca, **chỉ giữ ca Không đạt / Đạt kèm ý phụ sai** (`evidence/<dự-án>/chay-test/video/`, không vào git; video của ca có bug được chép sang `evidence/<dự-án>/bug/BUG-nnn/` bằng `tao-bug-report/scripts/luu-bang-chung.py`, có vào git). Cần ffmpeg của Playwright (`python -m playwright install ffmpeg`, xin phép); chưa có thì chạy tiếp không quay.
- Ảnh khoanh tay cho vùng nhiều dòng: `scripts/mark_error.py <ảnh> --box x1,y1,x2,y2`.

## 5. Ghi lượt và trang kết quả
- Dữ liệu gốc `testing/<dự-án>/run-results/<bộ>.json` (chỉ thêm lượt, không sửa tay); trang `smoke-ket-qua.*` (bộ smoke) hoặc `<tính-năng>/ket-qua-test-case.*`. Cột: ID, Test case, Các bước, Kết quả mong đợi, Status, Evidence, Bug, Số lần chạy (không có cột Kết quả thực tế vì đã có Status).
- Ca không test được vì bug khác: `--status "N=Bị chặn" --blocked-by "N=BUG-nnn"`; ca bỏ qua: `--status "N=Bỏ qua"`.
- **Kết luận và rủi ro** (`--conclusion-file` JSON: `headline`, `passed[]`, `not_tested[{cases,status,reason}]`, `risks[{title,detail}]`, `suggestion`) bắt buộc cho **mọi lượt** (tính năng, regression, smoke; smoke bắt buộc từ 2026-11-19 để báo cáo tổng kết có dòng của smoke). Viết để người test **đánh giá được**: số liệu cụ thể; mỗi rủi ro nói **chuyện gì xảy ra với người dùng** và đã/chưa kiểm; ca chưa có kết quả nói rõ vì sao; đề xuất ghi là đề xuất, quyết nhận/trả build là của người test hoặc PO. Cấm câu chung chung ("còn một số lỗi") và viết tắt khó hiểu. Ghi chú lượt viết câu đầy đủ (môi trường, bản, ngày, số ca đã/chưa có kết quả).
- Lượt tổng theo tính năng: `Đạt toàn bộ` / `Có case không đạt` / `Chưa chạy hết`; smoke: `Nhận build` / `Trả build` / `Chưa đủ kết luận`.

Lượt theo tính năng chỉ được ghi khi `add-run` kiểm đạt (code, không phải lời nhắc): có đủ khóa kết luận, không có cụm chung chung (một số lỗi, nhiều case…), mọi ca chưa có kết quả được liệt kê từng mã với đúng trạng thái, lý do và rủi ro đủ dài để người test đánh giá. Chạy `python -X utf8 scripts/kiem-tra-ro-mat-khau.py` để chắc không có mật khẩu lọt vào file.

## 6. Bug từ lượt chạy
- Ca **Không đạt** thật: **tạo bug luôn, không hỏi** (người dùng chốt 2026-11-19) theo `tao-bug-report`, kèm ảnh `-loi` tô đỏ và video (`luu-bang-chung.py` chép video vào `evidence/<dự-án>/bug/BUG-nnn/` để có trong repo); **trước khi tạo chạy `tao-bug-report/scripts/tim-bug-lien-quan.py <dự-án> <tính-năng>/TC-xxx`**: có bug đang mở cùng chỗ thì nối bug cũ, không tạo mới; bug đã Đóng mà lỗi quay lại thì đề xuất Mở lại; ca thuộc lượt hiệu chuẩn, nguồn nháp hoặc kết quả mong đợi `CẦN XÁC NHẬN` thì vẫn tạo bug nhưng dòng đầu ghi "Nghi lỗi, chờ xác nhận" (có thể do test case); Không đạt vì chính test case viết sai (thường ở lượt hiệu chuẩn) thì sửa test case, không tạo bug; bug lên Jira chỉ khi người dùng nhờ.
- Mỗi nguyên nhân một bug. **Chỉ gộp khi người dùng hoặc Dev xác nhận cùng chỗ sửa** (ví dụ câu báo lỗi tiếng Việt và English cùng sửa một chỗ → một bug). Mã `BUG-nnn` không dùng lại số đã bỏ.
- Đính ảnh `-loi` (tô đỏ như trang test case) và video `.webm` trong mục Đính kèm; suy luận (ví dụ cách hệ thống đếm) gắn nhãn Giả định, câu hỏi cho Dev nêu đủ nghĩa. Chi tiết nội dung bug: skill `tao-bug-report`.
- Ca Không kết luận do lỗi của mình (bộ đếm, script) **không phải bug** và không ghi Không đạt.

## 7. Trang HTML luôn khớp nguồn, giao diện thống nhất
- `build_docs.py --all` sinh mọi trang: tài liệu md (SRS, bảng soát, câu hỏi BA, checklist, test case, truy vết, nhật ký khám phá, hướng dẫn), kết quả, bug, trang tổng `testing/<dự-án>/index.html`. `--check` so nội dung (không dựa giờ sửa file). Bốn lớp chặn cũ: `CLAUDE.md` bước 5, `kiem-tra-bo-nho.py`, hook `.githooks/pre-commit` (`git config core.hooksPath .githooks` một lần mỗi clone), selftest.
- Link kiểu `file.md#L66` nhảy đúng dòng; mã requirement, TL, câu hỏi BA, TC tự thành link tới dòng định nghĩa. Muốn link đúng thì md theo quy ước: mã nằm ở **ô đầu** của dòng bảng, TL ở ô đầu dòng của bảng soát, câu hỏi BA có `<a id="a1"></a>`, test case có `<a id="tc-001"></a>`.
- Giao diện (màu, font, bảng rộng, chế độ tối, logo ở góc trái) duy nhất ở `scripts/test_automation/theme.py`; font cục bộ `docs/thuong-hieu/fonts/`; thương hiệu cấu hình ở `docs/thuong-hieu/brand.json` (riêng dự án: `testing/<dự-án>/brand.json`). Muốn đổi giao diện: sửa `theme.py`, không sửa từng trang.

## 8. Bẫy môi trường
- Windows: chạy Python kèm `-X utf8`; Git Bash đổi `/duong-dan` thành `C:/Program Files/Git/…` (dùng PowerShell hoặc `MSYS_NO_PATHCONV=1`); heredoc làm méo dấu `\` (viết file bằng công cụ Write).
- Đổi tên hàng loạt: chạy selftest (từng bắt lỗi tên dùng dạng chuỗi, tham số che tên hàm, cờ lệnh lệch tên).
- Hệ thống mới có thể đổi địa chỉ/bản: kiểm `/api/health` và số bản ở `auto-data.json` trước khi chạy.

## 7. Evidence bắt buộc (người dùng dặn 2026-11-20)
- **Mọi ca có kết luận đều phải có evidence để người dùng tự kiểm lại**, kể cả ca Đạt và lượt chạy tay: ảnh (ca Đạt có ảnh xanh theo `mark_text`), video nếu có, ghi trong file kết quả (`images`, `videos`) và hiện trên trang kết quả. Chỉ ghi chữ "đã quan sát" thì **không** coi là đủ: không ghi lượt.
- "Chỉ xem ảnh khi Không đạt" ở mục giữ token là việc **AI đọc** ảnh; không liên quan việc lưu ảnh. Luôn lưu, đừng luôn xem.
- Trình duyệt tích hợp của app chỉ trả ảnh cho AI, không lưu ra repo: muốn có evidence thì chạy bằng script Playwright của repo (`run_tests.py`). Chạy tay chỉ để khám phá, không dùng để ghi lượt chính thức; ngoại lệ phải ghi rõ trong ghi chú lượt và người dùng đồng ý.
- Ảnh có mật khẩu mẫu hiện trên trang (khung tài khoản mẫu) phải che trước khi lưu; không có cách che được thì chụp vùng không chứa mật khẩu hoặc dùng ảnh sau khi đăng nhập.
