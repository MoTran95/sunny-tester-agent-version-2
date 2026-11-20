# Cấu trúc repo
Đọc khi: thêm thư mục, đổi quyền, làm máy mới. Repo không có ứng dụng: bộ tài liệu kiểm thử + skill + memory. Cần cài: Git, Python 3 (+ Pillow cho build báo cáo HTML).

| Đường dẫn | Vai trò |
|---|---|
| `.claude/skills/` | 11 skill (`SKILL.md`, `references/`, `assets/`, `scripts/`) |
| `.claude/settings.json` | Quyền cho phép sẵn (Edit trong thư mục dự án, chạy script soát, git đọc). Commit/push/xóa vẫn hỏi |
| `memories/` | Bộ nhớ cho AI, bản đồ `MEMORY.md` |
| `srs/` `testing/` `evidence/` | SRS; bảng soát/câu hỏi/checklist/test case/truy vết; khám phá + ảnh + báo cáo HTML (mỗi dự án có thư mục con `<slug>`) |
| `docs/cai-dat-may-moi.md` | Cài máy mới |
| `scripts/xuat-bo-loi.py`, `scripts/bo-loi.json` | Xuất bộ lõi dùng chung (không dữ liệu dự án, không thông tin cá nhân) ra repo riêng; `bo-loi.json` là ranh giới chung/riêng, `kiem-tra-lan-du-an.py` đọc cùng file |
| `testing/_template-test-plan.md` | Khuôn test plan dùng chung (người dùng chọn bản đầy đủ 2026-11-19, bản gọn 1–2 trang sẽ lược từ đây khi cần); `build_docs.py` tự sinh `.html` cạnh file |
| `scripts/kiem-tra-may-moi.py` | Kiểm máy mới (Python, Pillow, Git, dự án, `.env`, skill, quyền, chạy thử script soát) |
| `scripts/do-toc-do-phien.py` | Đo phiên gần nhất từ nhật ký: ngữ cảnh đầu, file đọc, phút tới lúc làm, mở dự án khác |
| `scripts/kiem-tra-bo-nho.py` | Kiểm memory: mọi file có trong bản đồ, link không gãy, in cỡ |
| `scripts/tao-du-an.py` | Tạo thư mục dự án mới |
| `scripts/truy-vet.py` | Truy vết requirement ↔ TC (`kiem`/`chot`); cần `testing/<dự-án>/<tính-năng>/truy-vet-cau-hinh.json` |
| `scripts/truy-vet-smoke.py` | Truy vết `testing/<dự-án>/smoke-test.md` ↔ TC gốc + requirement (`kiem`/`chot`); dùng hàm của `truy-vet.py` |
| `scripts/selftest/` | Bài kiểm tự động thư viện chạy test (máy chủ giả localhost): `python -X utf8 scripts/selftest/run_selftest.py`, chạy sau mọi lần sửa `test_automation` |
| `scripts/test_automation/summary_report.py` | Báo cáo tổng kết kiểm thử `testing/<dự-án>/test-summary-report.md/.html` + `duyet-build.json` (form duyệt build, in PDF); xem `project/tu-dong-hoa-test.md` |
| `scripts/build_docs.py`, `scripts/test_automation/docs_pages.py` | Đổi md (SRS, bảng soát, câu hỏi BA, checklist, test case, truy vết, nhật ký khám phá, hướng dẫn chạy test) sang HTML cạnh file md + trang tổng `testing/<dự-án>/index.html` (thẻ từng tính năng: link tài liệu, tiến độ test case, bug, lượt chạy). 0 token, không dùng AI. `--all` mọi dự án, `--check` so nội dung (không ghi), `--stage` git add. Giao diện chung ở `test_automation/theme.py`. Hook `.githooks/pre-commit` tự sinh lại trước commit. Selftest có kiểm bộ đổi md |
| `scripts/auto_login.py`, `scripts/run_tests.py`, `scripts/test_automation/` | Chạy test case tự động bằng Playwright cho mọi dự án (`testing/<dự-án>/auto-config.json`, script ca ở `<tính-năng>/auto/`). Đăng nhập do **người dùng tự chạy**; phiên ở `.phien-dang-nhap/` (gitignore). Chi tiết: `project/tu-dong-hoa-test.md`, hướng dẫn `docs/chay-test-tu-dong.md` |
| `.du-an-hien-tai`, `.env` / `.env.example` | Dự án đang làm; tài khoản test (không commit) / mẫu khóa |

Bẫy Windows: chạy Python kèm `-X utf8`; heredoc Git Bash làm méo `\\` trong regex → viết script ra file rồi chạy.
