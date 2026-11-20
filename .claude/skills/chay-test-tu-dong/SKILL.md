---
name: chay-test-tu-dong
description: Viết script và chạy test case tự động bằng Playwright (smoke, regression, theo tính năng), ghi lượt chạy, sinh trang kết quả có kết luận, ảnh, video, tạo bug khi ca Không đạt. Dùng khi nghe "chạy test", "chạy test tự động", "chạy smoke bằng script", "viết script cho test case", "ghi lượt chạy", "sinh lại trang HTML", "thêm dự án vào bộ chạy test". Không dùng để viết test case, chọn bộ smoke/regression hay soạn nội dung bug.
---

# Chạy test tự động (Playwright, dùng chung nhiều dự án)

Tiếng Việt với người dùng; tên hàm, biến, khóa JSON, lệnh trong code bằng tiếng Anh. Công cụ nằm trong repo (`scripts/test_automation/`, `scripts/*.py`); skill chỉ nói **cách dùng và quy tắc đã chốt**, không chép lại code.

## Năm nguyên tắc (vì sao: người dùng muốn chất lượng cao mà ít token)
1. **Viết script ca một lần, chạy lại 0 token.** Ghi lượt, sinh trang, kiểm đều do chương trình; AI chỉ viết script ca, kết luận và bug.
2. **Chỉ kết luận Đạt/Không đạt khi script chạy trọn.** Script lỗi, chờ quá hạn, phiên hết hạn, điều kiện trước sai, bị bộ đếm từ chối → `Không kết luận`, không bao giờ "Không đạt giả".
3. **Chỉ tin điều đã quan sát**, không tin quy tắc BA khi thiết kế cơ chế an toàn (bài học bộ đếm nhập sai).
4. **Không làm hệ thống đang test hỏng:** không chạm ngưỡng chặn, không tạo dữ liệu thật khi chưa được cho phép rõ (hỏi, dừng, không đi đường vòng). **Ngoài hai điều có nguy cơ (khóa tài khoản, sửa dữ liệu người khác) thì tự làm, không hỏi lại**; ca cần ngưỡng chưa có thì bỏ qua, ghi "Chưa làm" kèm lý do.
5. **Trang HTML là sản phẩm tự sinh, không sửa tay.** Sửa nguồn (md, JSON, bug md) rồi `python -X utf8 scripts/build_docs.py --all`.

## Giữ token thấp (bắt buộc)
- Đọc đúng ca cần: `python -X utf8 scripts/truy-vet.py tra <dự-án> <tính-năng> --ma TC-xxx --day-du`; không mở cả `test-case.md`.
- Chạy lệnh rồi chỉ đọc phần cuối (`| tail`, `| grep "^|\|Tổng"`); không đọc cả log, không dán JSON kết quả vào chat.
- Xem ảnh (`Read`) chỉ khi kết quả bất ngờ hoặc cần kiểm khung tô; không xem ảnh ca Đạt. **Luôn lưu ảnh/video cho mọi ca (kể cả Đạt) để người dùng kiểm lại: `references/quy-tac-da-chot.md` mục 7.**
- Chạy nhóm nhỏ bằng `--case-id`; chạy lại chỉ ca lỗi; không chạy cả bộ "để thử".
- Ca cùng nhóm dùng chung một file hàm (như `login_common.py`); script ca dựng từ `assets/mau-ca-tu-dong.py`.
- Kết luận, rủi ro, câu hỏi cho Dev viết **một lần** vào file; trang web sinh từ file đó, không viết lại mỗi lần.

## Đọc gì cho từng việc
Sau `CLAUDE.md` và `memories/MEMORY.md` (đọc `.du-an-hien-tai`); chỉ file của dự án hiện tại.

| Việc | Đọc |
|---|---|
| Lần đầu dùng skill trong phiên, hoặc không chắc quy tắc | `references/quy-tac-da-chot.md` (ngắn, đọc hết) |
| Dự án mới / máy mới | `references/them-du-an-moi.md` |
| Cần cờ lệnh đầy đủ | `docs/chay-test-tu-dong.md` (chỉ mục cần) |
| Sửa thư viện `test_automation` | `memories/project/tu-dong-hoa-test.md`, rồi chạy `python -X utf8 scripts/selftest/run_selftest.py` (mong đợi `RESULT: ALL OK`) |

## Quy trình
1. **Chốt phạm vi:** địa chỉ test do người dùng nêu (có nhãn môi trường thử như staging); ca nào chạy, ca nào bỏ (ca mà chính bước làm gây chặn hệ thống); dữ liệu cần tạo (hỏi trước). Tài khoản ca cần: `python -X utf8 scripts/nhap-tai-khoan.py --trang-thai`; thiếu thì hỏi người dùng trong chat rồi ghi (cách hỏi và lệnh: `memories/conventions/nhieu-du-an.md` mục "Tài khoản test").
2. **Đăng nhập một lần:** `python -X utf8 scripts/auto_login.py <mã…> --headless` (mỗi tài khoản đúng một lần bấm; một tài khoản lỗi thì dừng). Phiên sống ngắn: chạy test ngay sau đó.
3. **Viết script ca** theo khuôn cho ca chưa có (`<tính-năng>/auto/tc-xxx.py`); ý đạt cũng khai `mark_text` để có ảnh xanh.
4. **Chạy:** `python -X utf8 scripts/run_tests.py --project <slug> --case-id <tính-năng>/tc-xxx … ` (hoặc `--smoke`, `--feature`). Ca có nhập sai: sắp từ ít sai đến nhiều sai, dừng ngay khi bị chặn.
5. **Ghi kết quả** vào test case gốc (Kết quả thực tế, Trạng thái, Tự động hóa) bằng script ghi một lần cho cả nhóm; không điền tay từng dòng.
6. **Ghi lượt và sinh trang:** `build_report.py add-run [--suite <tính-năng>] --build X --results-files … --status … --bug … --blocked-by … --conclusion-file …` (xem quy tắc kết luận ở `references/quy-tac-da-chot.md`).
7. **Bug:** ca Không đạt → **tạo bug luôn, không hỏi** (người dùng chốt 2026-11-19) theo `tao-bug-report`, kèm ảnh `-loi` tô đỏ và video (`luu-bang-chung.py` chép video vào `evidence/<dự-án>/bug/BUG-nnn/` để có trong repo); **trước khi tạo chạy `tao-bug-report/scripts/tim-bug-lien-quan.py <dự-án> <tính-năng>/TC-xxx`**: có bug đang mở cùng chỗ thì nối bug cũ, không tạo mới; bug đã Đóng mà lỗi quay lại thì đề xuất Mở lại; ca thuộc lượt hiệu chuẩn, nguồn nháp hoặc kết quả mong đợi `CẦN XÁC NHẬN` thì vẫn tạo bug nhưng dòng đầu ghi "Nghi lỗi, chờ xác nhận" (có thể do test case); Không đạt vì chính test case viết sai (thường ở lượt hiệu chuẩn) thì sửa test case, không tạo bug; bug lên Jira chỉ khi người dùng nhờ; mỗi nguyên nhân một bug; ca không test được vì bug khác → `Bị chặn` kèm link bug.
7b. **Báo cáo tổng kết (khi được nhờ; skill riêng `tao-test-summary-report`):** `python -X utf8 scripts/build_report.py summary [--build X] [--author tên]` ra `testing/<dự-án>/test-summary-report.md` + `.html` (tổng hợp mọi lượt của build mới nhất; có form người test/người duyệt build và nút In / Lưu PDF; `build_docs.py` cũng tự sinh). Quyết định duyệt do người điền trên trang rồi tải `duyet-build.json` về đặt vào `testing/<dự-án>/`; **không tự điền tên, quyết định hay ngày duyệt**. Chi tiết `docs/chay-test-tu-dong.md`.
8. **Sinh lại và kiểm:** `python -X utf8 scripts/build_docs.py --all`, rồi `python -X utf8 scripts/kiem-tra-bo-nho.py` (báo lỗi nếu còn trang cũ). Báo người dùng **một link trang tổng** `testing/<slug>/index.html` (kèm điểm nhảy tới đúng phần, xem CLAUDE.md mục "Trả kết quả HTML"), không liệt kê nhiều file HTML.

## Tự kiểm trước khi trả lời
Máy kiểm sẵn (chạy `python -X utf8 scripts/kiem-tra-bo-nho.py`): trang HTML khớp nguồn, không lẫn thông tin giữa dự án và skill, không mật khẩu lọt vào file, bug đúng khuôn; `add-run` từ chối kết luận thiếu hoặc chung chung. Phần dưới là điều máy không kiểm được.
- [ ] Không ca nào kết luận khi script lỗi/quá hạn; ca không kết luận được nêu rõ lý do.
- [ ] Không có mật khẩu trong script, kết quả, ảnh, bug hay chat; không nhập sai quá bộ đếm (trần do requirement hoặc người test chốt, không tự đặt số; cộng dồn).
- [ ] Bug đủ ảnh tô đỏ + video (nếu có), tách đúng nguyên nhân; ca bị chặn có link bug gây chặn.
- [ ] Kết luận trang kết quả có đủ: kết luận một câu, đã kiểm và đạt, chưa có kết quả và vì sao, rủi ro cho người dùng, đề xuất; câu chữ đầy đủ, không viết tắt khó hiểu.
- [ ] `build_docs.py --all --check` báo khớp; selftest `ALL OK` nếu có sửa thư viện.

## Tệp trong skill
- `references/quy-tac-da-chot.md` — quy tắc người dùng đã xác nhận (kèm lý do).
- `references/them-du-an-moi.md` — thêm dự án, máy mới, cấu hình thương hiệu.
- `assets/mau-ca-tu-dong.py` — khuôn script ca.
