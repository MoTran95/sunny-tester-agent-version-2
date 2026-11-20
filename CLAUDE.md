# CLAUDE.md — sunny-tester-kit

Đọc ĐẦU TIÊN mọi phiên. Trao đổi với người dùng bằng **tiếng Việt**. Chạy được trên Windows và Mac: lệnh trong repo viết `python`, máy không có `python` (thường là Mac) thì gõ `python3`; đường dẫn viết gạch xuôi `/`.

## Quy trình bắt buộc với MỌI yêu cầu

0. **Dự án đang làm** (repo nhiều dự án, mỗi dự án là một hệ thống đang test): đọc `.du-an-hien-tai` ở gốc repo (một dòng slug, không commit, mỗi máy một file).
   - **Chưa có file (máy mới):** trước tiên gửi nguyên đoạn "Lời chào trong chat" trong `docs/bat-dau.md` (lời chào, không chứa thông tin dự án nào; đường dẫn `docs/bat-dau.html` gửi thành link bấm được), rồi hỏi dự án nào. **Chọn hoặc tạo xong dự án:** chạy `python -X utf8 scripts/build_docs.py`, gửi link trang tổng `testing/<slug>/index.html#huong-dan` kèm một câu "từ giờ chỉ cần mở trang này; hướng dẫn ở mục Hướng dẫn và quy ước chung" **trước mọi việc khác**, **riêng câu này** (không gộp câu khác, không đưa tài liệu/feature của dự án nào làm lựa chọn khi chưa chọn dự án); liệt kê dự án trong `memories/project/overview.md` + "dự án mới". Ghi slug vào file. Dự án mới: `memories/conventions/nhieu-du-an.md` (`scripts/tao-du-an.py`).
   - **Có file:** dùng luôn; người dùng nhắc dự án khác → hỏi xác nhận đổi rồi ghi lại.
   - **Tên người test** (`.nguoi-test` ở gốc repo, một dòng, không commit; script ghi vào Người viết/người chạy): chưa có thì hỏi tên **sau** câu chọn dự án, lần đầu cần ghi tên vào tài liệu; không tự điền tên ai.
   - **Tài khoản test** (`.env`): chọn/tạo dự án xong, dự án chưa có tài khoản → hỏi trong chat rồi lưu; cách hỏi và lệnh ghi ở `memories/conventions/nhieu-du-an.md` mục "Tài khoản test".
' '<mk>' | python -X utf8 scripts/nhap-tai-khoan.py --url … --ma … --user … --mat-khau-tu-stdin` (script tự tạo `.env`). Người dùng chọn terminal → mở tab (`run_in_terminal`) chạy `... --ma <MÃ> --go-mat-khau`. Không nhắc lại mật khẩu trong câu trả lời, không ghi vào file nào khác.
   - **Không dùng kiến thức dự án khác** (nghiệp vụ, tài khoản, dữ liệu test, từ ngữ, thông báo, **con số ngưỡng**): chỉ đọc `memories/modules/<slug>/`, `srs/<slug>/`, `testing/<slug>/`, `evidence/<slug>/` của dự án hiện tại. Skill và script dùng chung không chứa thông tin dự án nào; `scripts/kiem-tra-lan-du-an.py` (nằm trong `kiem-tra-bo-nho.py`) bắt chỗ lẫn.
1. Đọc `CLAUDE.md` (file này).
2. Đọc `memories/MEMORY.md` — **bảng** `File | Khi | Chứa` cho AI. Chỉ 2 file ★ luôn đọc (`user/working-preferences.md`, `project/overview.md`).
3. Mở **chỉ các file có cột "Khi" khớp việc** (phần chung + dự án hiện tại); không bỏ sót file bản đồ chỉ là liên quan, không đọc tràn lan. Dùng skill: đọc theo bảng "Đọc gì cho từng việc" trong `SKILL.md`.
4. Làm việc. 5. Cập nhật memory trước khi kết thúc lượt, rồi `python -X utf8 scripts/kiem-tra-bo-nho.py`. Nếu lượt này sửa file md của `srs/`, `testing/` hoặc `evidence/`: chạy thêm `python -X utf8 scripts/build_docs.py --all` (sinh lại mọi trang HTML: tài liệu, kết quả chạy, bug, trang tổng). `kiem-tra-bo-nho.py` báo lỗi nếu còn trang cũ; hook pre-commit (`.githooks`, bật bằng `git config core.hooksPath .githooks`) tự sinh lại trước mỗi commit.

Bản đồ mâu thuẫn code → tin code, sửa memory. Đem bộ sang dự án khác/đưa người khác: `python -X utf8 scripts/xuat-bo-loi.py <thư-mục>` (bộ lõi không dữ liệu dự án, không thông tin cá nhân; ranh giới `scripts/bo-loi.json`). Máy mới / "kiểm tra máy mới": `docs/cai-dat-may-moi.md` (Windows và Mac), `python -X utf8 scripts/kiem-tra-may-moi.py`. `kiem-tra-bo-nho.py` còn kiểm: không lẫn thông tin giữa dự án, không mật khẩu `.env` lọt vào file, bug đúng khuôn. Phiên than nặng: nạp sẵn ~74 nghìn token, phần plugin tài khoản chỉ ~3–6%, không tắt được từ repo (`memories/project/session-speed.md`, `memories/user/connectors-and-plugins.md`).

## Khám phá xong tự tạo báo cáo khám phá + đưa link (người dùng dặn 2026-11-20)
Người dùng nhờ khám phá một tính năng: làm xong **tự** dựng báo cáo khám phá HTML (skill `feature-exploration-report`, từ nhật ký và ảnh vừa có) cùng lượt, rồi đưa link trang tổng `testing/<slug>/index.html#tn-<tính-năng>` kèm "bấm nút Báo cáo khám phá trong thẻ tính năng". Không chờ nhắc.

## Trả kết quả HTML: một link trang tổng (người dùng dặn 2026-11-19)
Việc làm ra hoặc sửa trang HTML của dự án (tài liệu, test case, kết quả chạy, bug, smoke, regression, test plan, báo cáo tổng kết, báo cáo khám phá): trong câu trả lời chỉ đưa **một link** tới trang tổng `testing/<slug>/index.html`, kèm điểm nhảy tới đúng phần: `#tn-<tính-năng>` (tài liệu, kết quả, bug của tính năng), `#smoke`, `#regression`, `#test-plan`, `#bao-cao-tong-ket`, `#huong-dan`. Người dùng mở một file là tới được mọi trang; **không liệt kê nhiều file HTML**. File md dùng để sửa thì vẫn link được khi cần. Trang tổng tự có link tới mọi trang của dự án; `build_docs.py --check` (trong `kiem-tra-bo-nho.py`) báo LỖI nếu có trang thiếu link.

## Giao diện trang HTML là chuẩn chung mọi dự án (người dùng dặn 2026-11-20)
Làm trang tổng/trang con cho dự án nào cũng **dùng đúng bộ có sẵn** (`theme.py` màu, font Be Vietnam Pro, logo; `dieu_huong.py` thanh trên, breadcrumb, tab, menu; `build_docs.py` sinh), **không tự dựng lại**. Muốn đổi giao diện/điều hướng: sửa một chỗ trong thư viện rồi `build_docs.py --all`, không sửa tay từng HTML, không đọc HTML sinh ra (0 token). Chi tiết: `memories/conventions/dieu-huong-html.md`.

## Giữ ngữ cảnh gọn (mọi skill)
- Script soát chỉ in kết luận ngắn: **0 lỗi thì không đọc lại file vừa sinh**; chỉ đọc đúng dòng script báo (`Read` với `offset`/`limit`).
- Không `cat` cả file; file lớn thì `Grep` rồi đọc đoạn cần. Xem vài mã SRS/bảng phân tích/test case: `python -X utf8 scripts/truy-vet.py tra <dự-án> <tính-năng> --ma …`.
- Lệnh có thể in nhiều thì thêm `| head -40`; soát tay chỉ phần script không kiểm được, lấy mẫu vài dòng.

## Giảm token khi đọc file (MarkItDown)
Word, PowerPoint, HTML, PDF chữ hoặc nhiều file → đổi sang Markdown trước: `python -X utf8 scripts/doi-sang-markdown.py <file> -o <thư-mục-tạm>/<tên>.md` (ra thư mục tạm, chỉ file/URL đã biết nguồn). Không dùng cho `.txt`/`.md`, Excel lớn (pandas), PDF scan/nhiều hình, việc sửa file giữ định dạng. Máy khác: `memories/project/cong-cu-markitdown.md`.

## Memory (`memories/`) chỉ cho AI đọc
- Viết **ngắn, bảng/gạch đầu dòng**; một file một chủ đề; chỉ điều **không suy ra nhanh từ code/SRS** (lý do, ràng buộc, quyết định, bẫy, sở thích người dùng). Không chép lại code hay nội dung đã có ở `srs/`, `testing/`, `evidence/`.
- Tài liệu cho **người đọc** (`srs/`, `testing/`, `evidence/`, `docs/`, báo cáo HTML) vẫn viết đầy đủ, đọc là hiểu.
- Thêm/đổi tên/xóa file memory → sửa bảng trong `MEMORY.md` cùng lượt. Chi tiết: `memories/conventions/memory-writing-rules.md`.
- **Ghi ngay điều người dùng dặn, trong cùng lượt**: mọi quy tắc, chỉnh sửa hay quyết định người dùng đưa ra trong chat phải vào đúng chỗ: quy tắc chung → skill hoặc `memories/user|conventions`; riêng một dự án → `memories/modules/<slug>/`. Điều chỉ nằm trong chat sẽ mất khi sang máy khác hoặc phiên khác. Sở thích/hiểu biết riêng của máy (thư mục `.claude` ngoài repo) không đi theo repo.
- **Không tự đặt con số cho ngưỡng an toàn** (số lần nhập sai, thời gian chặn, thời gian chờ…): lấy từ requirement của dự án hoặc hỏi người test, rồi ghi ở file của dự án (`testing/<slug>/auto-config.json`, `memories/modules/<slug>/`).
