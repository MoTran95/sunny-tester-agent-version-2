# MEMORY — bản đồ cho AI (không phải tài liệu cho người)
Chỉ 2 file **LUÔN ĐỌC** (★). Còn lại mở khi việc khớp cột "Khi". Chỉ mở mục của dự án hiện tại (`.du-an-hien-tai`). Thêm/đổi tên/xóa file → sửa bảng này cùng lượt, rồi `python -X utf8 scripts/kiem-tra-bo-nho.py`.

## Chung
| File (trong `memories/`) | Khi | Chứa |
|---|---|---|
| ★ `user/working-preferences.md` | mọi việc | quy tắc cốt lõi: tiếng Việt, hỏi không đoán, mật khẩu, tối đa 3 lần, commit khi nhờ |
| ★ `project/overview.md` | mọi việc | repo là gì, danh sách dự án |
| `user/document-preferences.md` | viết báo cáo/SRS/bảng soát/checklist/bug | cách người dùng muốn tài liệu |
| `user/connectors-and-plugins.md` | cần connector/plugin; chậm | Notion/Docs tắt; tắt plugin từ repo không được (đã đo) |
| `conventions/nhieu-du-an.md` | máy mới, đổi/tạo dự án, hỏi/ghi tài khoản test `.env` | chọn dự án, tài khoản test, không lẫn kiến thức |
| `conventions/dieu-huong-html.md` | sửa trang HTML, thanh điều hướng, trang tổng | thanh trên, tab, menu, chèn ở đâu |
| `conventions/memory-writing-rules.md` | trước khi ghi/sửa memory | khuôn viết cho AI, độ dài |
| `conventions/thiet-ke-skill.md` | được nhờ thiết kế/tạo skill mới | tìm hiểu chất lượng, tối ưu token, dùng chung nhiều dự án |
| `conventions/ba-question-wording.md` | viết câu hỏi BA | xưng hô, từ chung, khuôn |
| `project/skills.md` | **sửa** skill (chỉ dùng skill thì đọc `SKILL.md` của skill đó, không mở file này) | 11 skill (có `chay-test-tu-dong`, `de-xuat-regression`, `lap-ke-hoach-retest`, `tao-test-summary-report`, `tao-test-plan`), script, trạng thái đã thử |
| `project/srs-process.md` | làm SRS; hỏi vì sao khuôn thế | quyết định khuôn/ID, bẫy |
| `project/truy-vet-requirement.md` | requirement đổi; sửa checklist/TC; sửa smoke | `truy-vet.py`, `truy-vet-smoke.py`, neo TC, lịch sử, bẫy |
| `project/tu-dong-hoa-test.md` | sửa thư viện `test_automation`, thêm dự án | cấu trúc, bẫy chung; quy tắc chốt ở skill `chay-test-tu-dong`; trạng thái từng dự án ở `modules/<slug>/tu-dong-hoa.md` |
| `project/session-speed.md` | than chậm/tốn token; sửa skill/khuôn | số đo, đã làm, rủi ro |
| `project/git-remote.md` | commit/push | remote, `.env` loại trừ |
| `project/architecture.md` | thêm thư mục, đổi quyền, máy mới | cấu trúc, script |
| `project/cong-cu-markitdown.md` | đọc docx/pdf/xlsx/pptx; cài máy | cách dùng, bẫy |
| `decisions/decision-log.md` | trước khi đề xuất đổi hướng | quyết định + lý do + phương án loại |
| `pitfalls/dont-trigger-lockouts.md` | trước thao tác có thể gây khóa | bài học khóa đăng nhập |
| `modules/_template.md` | tạo file module | khuôn |

Sản phẩm dùng chung cho người đọc (không phải memory): `testing/chien-luoc-phan-tich-requirement.md` (sách Sunny; đọc khi nhắc "sách"); `docs/bat-dau.md` (hướng dẫn người mới, nguồn duy nhất về cách dùng); `docs/quy-trinh-kiem-thu.md` (bản đồ bước → skill cho người bảo trì); `docs/danh-gia-skill.md` (đánh giá, rà soát). Khuôn test plan: `testing/_template-test-plan.md` (skill `tao-test-plan`).

## Dự án `ecommerce-lite` (chỉ khi `.du-an-hien-tai` = ecommerce-lite)
| File | Khi | Chứa |
|---|---|---|
| `modules/ecommerce-lite/overview.md` | đầu tiên | hệ thống, tài khoản, thư mục |
| `modules/ecommerce-lite/tu-ngu-cau-hoi-ba.md` | viết câu hỏi BA | từ đã chốt với BA của dự án này |
| `modules/ecommerce-lite/feature-dang-nhap.md` | làm tiếp Đăng nhập (test plan, test case, chạy test) | trạng thái, sự thật đã thấy, bẫy |
