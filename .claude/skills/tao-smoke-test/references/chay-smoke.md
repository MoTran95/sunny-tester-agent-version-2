# Chạy smoke trên hệ thống (giao thức)

Đọc khi người dùng nhờ chạy smoke. Chọn case: `SKILL.md`. Chỉ chạy khi được nhờ.

## Hỏi một lần cho cả lượt
- Địa chỉ hệ thống đang test (do người dùng nêu, có nhãn môi trường thử như staging) và số bản đọc ở chân trang.
- Dữ liệu sẽ bị đổi (ví dụ tạo hồ sơ nháp): hỏi rõ trước; dọn lại sau lượt nếu case gốc yêu cầu.
- Không nhập sai thông tin đăng nhập quá trần bộ đếm, không làm gì có thể chặn tài khoản (`memories/pitfalls/dont-trigger-lockouts.md`).

## Cách A: có script `auto/` cho các case smoke (nên dùng, 0 token mỗi lượt)
1. `python -X utf8 scripts/auto_login.py <mã…> --headless` (phiên ngắn, chạy ngay sau đó).
2. `python -X utf8 scripts/run_tests.py --project <slug> --smoke`; đọc phần cuối kết quả, không đọc cả log.
3. Ghi lượt: `python -X utf8 scripts/build_report.py add-run --project <slug> --build "<số bản>" --results-files <result-*.json> --status "N=Đạt kèm lỗi đã biết" --bug "N=BUG-nnn" --note "<câu đầy đủ: môi trường, bản, ngày, case nào không kết luận và vì sao>" --conclusion-file <kết-luận.json>` (phần Kết luận và rủi ro **bắt buộc** cho lượt smoke từ 2026-11-19, khuôn ở `chay-test-tu-dong/references/quy-tac-da-chot.md`; thiếu thì không ghi lượt) (N = cột # của bảng smoke). Ca ra `Không kết luận` giữ nguyên, không ép thành Đạt.
4. Sinh trang: `python -X utf8 scripts/build_docs.py --all`; báo người dùng link `smoke-ket-qua.html`.

## Cách B: chưa có script (chạy tay, AI không gõ mật khẩu)
1. Đọc case gốc một lần: `python -X utf8 scripts/truy-vet.py tra <dự-án> <tính-năng> --ma TC-005 --day-du`. Chỉ cần đạt các bước ở cột "Đạt khi" của bảng tiêu chí.
2. Đọc kết quả bằng văn bản trang trước; chụp ảnh chỉ khi Không đạt hoặc cần bằng chứng.
3. Chấm theo ý chính: `Đạt`; `Đạt kèm lỗi đã biết` (chỉ khi tiêu chí ghi ngoại lệ cho đúng case và ý được miễn); `Không đạt`; `Bị chặn` (không chạy được vì lý do ngoài case). Ý phụ lệch chỉ ghi nhận.
4. Không đạt thì dừng, các case sau `Chưa chạy`; nghi do thao tác của mình thì làm lại **một** lần, vẫn lệch thì kiểm lại test case gốc với requirement trước khi kết luận build sai.
5. Ghi lượt bằng lệnh ở Cách A bước 3 (kết quả tự soạn thành file kết quả hoặc dùng `--status`).

## Sau lượt
Báo: nhận hay trả build, case lỗi và quan sát cụ thể, ngoại lệ đã dùng, phạm vi chưa phủ. Case Không đạt: **tạo bug luôn, không hỏi** (người dùng chốt 2026-11-19) theo `tao-bug-report`, kèm ảnh `-loi` tô đỏ và video (`luu-bang-chung.py` chép video vào `evidence/<dự-án>/bug/BUG-nnn/` để có trong repo); **trước khi tạo chạy `tao-bug-report/scripts/tim-bug-lien-quan.py <dự-án> <tính-năng>/TC-xxx`**: có bug đang mở cùng chỗ thì nối bug cũ, không tạo mới; bug đã Đóng mà lỗi quay lại thì đề xuất Mở lại; ca thuộc lượt hiệu chuẩn, nguồn nháp hoặc kết quả mong đợi `CẦN XÁC NHẬN` thì vẫn tạo bug nhưng dòng đầu ghi "Nghi lỗi, chờ xác nhận" (có thể do test case); Không đạt vì chính test case viết sai (thường ở lượt hiệu chuẩn) thì sửa test case, không tạo bug; bug lên Jira chỉ khi người dùng nhờ. Lượt hiệu chuẩn (lần đầu, test case chưa chạy thật): ghi thêm kết quả vào `Kết quả thực tế` + `Trạng thái` + `Tự động hóa` của test case gốc (không làm test case bị coi là đã sửa); case sai vì test case sai thì sửa test case theo `tao-checklist-test-case`. Lượt build thường không ghi đè các cột đó.
`truy-vet-smoke.py ghi-luot` (mục "Lượt chạy" trong smoke-test.md) là cách cũ, chỉ dùng khi người dùng muốn giữ mục đó; bảng chính là `smoke-ket-qua`.
