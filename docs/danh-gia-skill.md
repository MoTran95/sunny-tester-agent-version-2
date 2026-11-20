# Đánh giá 11 skill trước khi đưa người khác dùng (2026-11-19)

Mục đích: xem bộ skill đã đủ để người khác cầm repo lên là dùng được chưa, chỗ nào cần sửa trước. Quy trình dùng các skill theo thứ tự: [quy-trinh-kiem-thu.md](quy-trinh-kiem-thu.md).

## Nhận xét chung

**Điểm mạnh**
- Mỗi skill làm một việc, có ranh giới rõ ("Không dùng để…" trỏ sang skill đúng), nên Claude ít chọn nhầm skill. Đã thử: câu "test lại bug 01" gọi đúng skill re-test.
- Các skill nối nhau qua file và truy vết: requirement → test case → smoke → regression → test plan → kết quả → báo cáo tổng kết. Requirement đổi thì script báo đúng chỗ cần sửa.
- Phần tính toán và kiểm tra do script làm (kiểm khuôn, đếm, sinh trang HTML), không để AI tự đếm. Chạy lại test không tốn thêm lượt AI.
- Quy tắc an toàn (mật khẩu, khóa tài khoản, không tự đặt ngưỡng, không bịa) thống nhất ở mọi skill.

**Điểm yếu chung**
- Mới chạy thật trên **một dự án** (dự án đầu). Nhiều skill ghi "chưa thử dự án thứ hai" hoặc "chưa thử từ phiên mới".
- Chưa có **cửa vào** cho người mới: không có README, không có tài liệu nói dùng skill nào trước (đã bổ sung `quy-trinh-kiem-thu.md`).
- Một số chỗ còn gắn với người dùng hiện tại hoặc do AI tự đặt mà chưa duyệt (chi tiết bên dưới).

## Từng skill

| Bước | Skill | Đánh giá | Chỗ chưa ổn |
|---|---|---|---|
| 1a | `srs-from-website` | Tốt. Có cổng "đã khám phá thì không khám phá lại", bằng chứng truy được, script soát | Khuôn `srs/_template.md` **chưa có thẻ neo** `<a id>` cho từng mã, nên cột Nguồn của test case ở dự án mới không link được tới dòng SRS (SRS dự án đầu được thêm tay). Câu "mật khẩu do người dùng gõ" chưa nói tới cách mới (script `auto_login.py` đọc `.env`). Tên skill tiếng Anh |
| 1a+ | `feature-exploration-report` | Tốt, giao diện thống nhất | Trùng phần khám phá với `srs-from-website`; khuôn nhật ký khám phá lại nằm trong skill kia. Người mới khó biết làm cái nào trước. Tên tiếng Anh |
| 1b | `phan-tich-requirement` | Rất tốt: trích nguyên văn có script kiểm, `ghi-tl.py` ghi câu trả lời BA tự động | Phần quy tắc 1b dài, kể chi tiết riêng của tính năng Đăng nhập (ví dụ cụ thể có thể đưa sang `references/bai-hoc.md`) |
| 2 | `tao-checklist-test-case` | Tốt: duyệt tình huống trong chat, một file gộp, truy vết tự động | **Tên người test ghi cứng** làm người viết mặc định (9 file). Còn **chế độ cũ hai file** chỉ để phục vụ một tính năng cũ, làm skill dài và rối |
| 3 | `tao-smoke-test` | Tốt: chọn theo mục đích, loại case nguy hiểm bằng cờ | Cách tách ý chính/ý phụ ở tiêu chí trả build **do AI đề xuất, chưa được duyệt** |
| 3 | `de-xuat-regression` | Tốt: nhãn nguồn, ba tầng, bug lọt production | Mô tả skill rất dài. Phần "chạy regression" lặp lại cách chạy của `chay-test-tu-dong` |
| 4 | `tao-test-plan` | Rất tốt: một nguồn, phiếu điền, kiểm lệch bản sinh, PDF | Cuối file có ghi chú "Đã thử / Chưa thử" (thông tin cho người bảo trì, không phải hướng dẫn) |
| 5 | `chay-test-tu-dong` | Tốt: script viết một lần, kết luận chỉ khi chạy trọn | Lượt **smoke không bắt buộc** phần "Kết luận và rủi ro", nên báo cáo tổng kết thiếu dòng của smoke |
| 6 | `tao-bug-report` | Tốt: nhãn Giả định, hỏi tối đa 3 câu, trang có nút sao chép | **Thang mức độ nghiêm trọng, ưu tiên, đường lưu và mã `BUG-nnn` do AI tự đặt, chưa được duyệt** |
| 7 | `lap-ke-hoach-retest` | Tốt, quy trình đầy đủ | Nhiều script (5) nên cần đọc kỹ; ghi chú "Đã thử / Chưa thử" ở cuối file |
| 8 | `tao-test-summary-report` | Tốt: số liệu do chương trình tính, form duyệt build | **Chưa có lệnh xuất PDF** (test plan đã có `xuat-pdf.py`). Ghi chú "Đã thử / Chưa thử" ở cuối file |

## Đề xuất sửa (xếp theo mức cần)

### Nên làm trước khi đưa người khác
1. **Bỏ tên người test ghi cứng.** Người viết mặc định lấy từ cấu hình của từng máy (ví dụ tên trong `git config user.name`, hoặc hỏi một lần rồi lưu), không ghi tên một người vào skill và script.
2. **Thêm thẻ neo vào khuôn SRS** (`srs/_template.md`) và vào bước viết SRS của `srs-from-website`, để test case ở dự án mới link được tới đúng dòng SRS như dự án đầu.
3. **Duyệt các điểm AI tự đặt:** thang mức độ nghiêm trọng và ưu tiên của bug, đường lưu bug, cách tách ý chính/ý phụ của smoke. Duyệt xong thì bỏ nhãn "chưa duyệt" trong bộ nhớ.
4. **Bắt buộc phần "Kết luận và rủi ro" cho lượt smoke** như lượt tính năng và regression, để báo cáo tổng kết đủ dòng.
5. **Thêm `README.md` ở gốc repo** (trang GitHub hiện đầu tiên): repo là gì, làm Bước 0 thế nào, link tới quy trình.
6. **Chạy thử trọn quy trình trên một dự án nhỏ thứ hai**, từ một phiên mới, theo đúng các câu nói mẫu, để bắt chỗ còn dính dự án đầu.

### Nên làm cho gọn, dễ bảo trì
7. **Chuyển tính năng cũ còn hai file sang file test case gộp**, rồi bỏ chế độ cũ hai file khỏi `tao-checklist-test-case` (bớt một chế độ, hai mẫu, một nhánh script).
8. **Gom phần khám phá dùng chung:** đưa khuôn nhật ký khám phá ra chỗ chung, ghi rõ thứ tự "khám phá một lần → SRS (cần cho test case) → báo cáo HTML (tùy chọn)" ở cả hai skill.
9. **Bỏ phần chép lặp:** khối "Giữ ngữ cảnh gọn khi soát" đang chép y nguyên ở 4 skill, "Quy ước để trang HTML tự link" ở 2 skill. Đưa vào một file chung (hoặc `CLAUDE.md`) và trỏ tới.
10. **Dời ghi chú "Đã thử / Chưa thử"** ở cuối `SKILL.md` (test plan, test summary, re-test) sang bộ nhớ của người bảo trì; skill chỉ giữ hướng dẫn, đọc nhanh hơn và ít tốn hơn mỗi lần nạp.
11. **Cập nhật câu về mật khẩu** ở `srs-from-website` và `feature-exploration-report` cho khớp quyết định mới (script đọc `.env`, Claude không gõ, không đọc ra).
12. **Thêm xuất PDF bằng script cho báo cáo tổng kết**, dùng chung `xuat-pdf.py` của test plan.

### Tùy chọn
13. **Đổi tên hai skill tiếng Anh cho đồng bộ** (ví dụ `srs-from-website` → `tao-srs-tu-website`, `feature-exploration-report` → `bao-cao-kham-pha`). Lợi: người mới đọc tên là hiểu. Hại: phải sửa mọi chỗ trỏ tới tên cũ (skill khác, bộ nhớ, tài liệu), dễ sót.
14. **Rút gọn mô tả (description) của `de-xuat-regression` và `tao-checklist-test-case`**: mô tả được nạp vào mọi phiên, càng dài càng tốn.

## Đã làm (2026-11-19, sáu mục "nên làm trước")

| Mục | Kết quả |
|---|---|
| 1. Bỏ tên ghi cứng | Xong. Tên người test lấy từ file `.nguoi-test` ở gốc repo (mỗi máy một file, không commit), không có thì lấy `git config user.name`. `kiem-tra-may-moi.py` nhắc tạo file |
| 2. Thẻ neo SRS | Xong. Khuôn `srs/_template.md` có neo mẫu (và bỏ đường dẫn, số bản của dự án đầu còn sót); `check-srs.py` cảnh báo dòng thiếu neo, `--them-neo` tự chèn. SRS cũ đã được chèn neo, truy vết không đổi |
| 3. Duyệt điểm Claude tự đặt | Xong. Đường lưu và mã bug giữ nguyên; thang mức độ: mỗi team tự chọn (dự án mới hỏi một lần, thang riêng khai ở `testing/<dự-án>/thang-muc-do-bug.json`, script kiểm bug đọc file này); cách tách ý chính/ý phụ của smoke đã duyệt |
| 4. Kết luận bắt buộc cho smoke | Xong. Ghi lượt smoke thiếu phần Kết luận và rủi ro thì bị từ chối; bài tự kiểm của bộ chạy test ALL OK |
| 5. README | Xong: `README.md` ở gốc repo |
| 6. Chạy thử dự án thứ hai | Đã chạy trên bản sao repo với dự án giả "Thư viện — Mượn sách" (chỉ có requirement, không có website). Đi hết các bước, không bước nào bị chặn hẳn, nhưng lộ ra các lỗi dưới đây |

## Lỗi tìm được khi chạy thử dự án thứ hai

Cả 10 lỗi **đã sửa 2026-11-19** và thử lại trên chính dự án giả đó (lỗi 1–3 trước, lỗi 4–10 sau).

**Nặng (đã sửa)**
1. **Thiếu trang HTML của bug, trang tổng và báo cáo tổng kết mà không báo gì.** Dự án mới chưa điền `auto-config.json` (phần đăng nhập) thì `build_docs.py` bỏ qua các trang này; `build_docs.py --check` và `kiem-tra-bo-nho.py` vẫn báo "khớp, 0 lỗi". *Đã sửa:* các trang này chỉ cần phần tài liệu của cấu hình (`config.load_for_docs`), trang tổng ghi "chưa khai địa chỉ"; `build_docs.py --check` nay báo thiếu trang bug, trang tổng.
2. **Báo cáo tổng kết dừng sai lý do:** báo "auto-config.json còn chỗ chưa điền" thay vì "chưa có lượt chạy nào". *Đã sửa:* `build_report.py summary` kiểm lượt chạy trước và báo đúng câu đó.
3. **`ghi-tl.py` ghi câu trả lời BA đầu tiên không được** (khuôn bảng soát chưa có dòng TL nào) và **tính lại Tổng kết thành 0** khi mã requirement không có dấu `` ` `` (khuôn cho phép cả hai cách). `kiem-tra.py` cũng không bắt Tổng kết đếm sai. *Đã sửa:* `ghi-tl.py` tự dựng bảng câu trả lời khi chưa có, nhận mã có hoặc không có dấu `` ` ``, không đếm được thì không sửa số; `kiem-tra.py` báo lỗi khi số ở Tổng kết lệch bảng soát.

**Vừa (đã sửa)**
4. **Requirement dạng văn bản chưa có chỗ rõ ràng:** khuôn SRS chỉ có nhãn "đã thấy / chưa rõ / đã bỏ" (cho hệ thống đã khám phá), nên SRS viết từ tài liệu yêu cầu bị báo lỗi thiếu nhãn. Cần thêm nhãn kiểu "theo tài liệu yêu cầu"; `--them-neo` cũng nên chèn neo cho dòng bằng chứng.
5. **Chưa có khuôn `truy-vet-cau-hinh.json`** (người mới phải đọc code để biết các khóa); `ten-tinh-nang.json` để trống mà không ai nhắc, nên test plan hiện tên thư mục thay vì tên tính năng.
6. `check-srs.py` vượt giới hạn 260 ký tự đường dẫn trên Windows khi repo nằm ở thư mục sâu (không chuẩn hóa `..`); `kiem-tra-may-moi.py` kiểm SRS của dự án đầu kể cả khi đang làm dự án khác.
7. `tao-du-an.py` chèn mục dự án mới vào `memories/MEMORY.md` sau đoạn ghi chú của dự án đầu (lẫn vị trí).

**Nhỏ (đã sửa)**
8. Dấu vết dự án đầu trong khuôn dùng chung: `scripts/tao-du-an.py` (ví dụ nhãn ô đăng nhập chép vào `auto-config.json` của dự án mới, `kiem-tra-lan-du-an.py` không bắt), `srs/id-and-source-rules.md` mục 5 (bảng mã tính năng của dự án đầu), `thang-muc-do.md` (nhắc một mã bug cụ thể), khuôn regression (ví dụ `dang-nhap/TC-005`).
9. `liet-ke-tc.py` không gắn cờ nguồn nháp khi SRS ghi "nháp" ở mục Tình trạng; xóa khối chú thích đầu nguồn test plan để lại dòng trống làm `kiem-tra-test-plan.py` báo lỗi.
10. README nói phải có `.env` ngay bước đầu, nhưng chỉ cần khi chạy test tự động.

### Cách đã sửa lỗi 4–10
| Lỗi | Đã sửa |
|---|---|
| 4 | Nhãn mới `theo tài liệu` và cách viết SRS từ tài liệu yêu cầu (`srs/id-and-source-rules.md` mục 2e, skill `srs-from-website` mục "Chỉ có tài liệu yêu cầu", bước mới trong quy trình). `check-srs.py --them-neo` chèn cả neo `e01` cho dòng bằng chứng |
| 5 | Lệnh `truy-vet.py khoi-tao <dự-án> <tính-năng> --tien-to <MÃ> --ten "<Tên>"` tạo cấu hình truy vết và ghi tên tính năng; `tao-du-an.py` nhắc lệnh này |
| 6 | `check-srs.py` chuẩn hóa đường dẫn (thử ở thư mục sâu: 0 lỗi); `kiem-tra-may-moi.py` chạy thử trên SRS của dự án đang làm, không dùng dự án đầu |
| 7 | Bản đồ bộ nhớ tách phần dùng chung khỏi phần riêng dự án; dự án mới nối vào cuối không còn lẫn |
| 8 | Bỏ ví dụ riêng dự án đầu khỏi khuôn và skill dùng chung (ví dụ trung lập `CART-…`, "Tên đăng nhập"); bảng mã tính năng chuyển về bộ nhớ từng dự án. `kiem-tra-lan-du-an.py` nay bắt cả nhãn ô đăng nhập, mã tính năng, và quét thêm khuôn `srs/`, `testing/_template*`, `scripts/tao-du-an.py` |
| 9 | `liet-ke-tc.py` đọc dòng Tình trạng của SRS để gắn cờ nguồn nháp ("nháp, đã có xác nhận của BA" không tính); bản sinh test plan bỏ dòng trống đầu |
| 10 | README và `kiem-tra-may-moi.py`: `.env` chỉ cần khi chạy test tự động (thiếu thì là lưu ý, không phải thiếu) |

## Rà soát lần 2: lỗ hổng, chỗ có thể làm sai kết quả, chỗ tốn token (2026-11-19)

### A. Có thể làm sai kết quả
| # | Lỗ hổng | Vì sao nguy hiểm | Đề xuất |
|---|---|---|---|
| A1 | Requirement đổi mà không ai chạy lệnh truy vết | `truy-vet.py`, `truy-vet-smoke.py`, `truy-vet-regression.py` chỉ chạy khi có người gọi; `kiem-tra-bo-nho.py` không gọi chúng. Test case, smoke, regression có thể đã lỗi thời mà không ai biết, rồi chạy test theo kết quả mong đợi cũ | Thêm chế độ chỉ đọc (không ghi file) cho ba lệnh `kiem` và gọi trong `kiem-tra-bo-nho.py` |
| A2 | Test plan lệch số liệu | Test plan giờ lập ở bước 2, số liệu đổi sau bước 3–4; `kiem-tra-test-plan.py` bắt được lệch nhưng không nằm trong `kiem-tra-bo-nho.py`. Gửi sếp bản số cũ | Gọi `sinh-test-plan.py kiem` trong `kiem-tra-bo-nho.py` (chỉ báo, không tự sinh) |
| A3 | Tự tạo bug khi Không đạt có thể tạo bug trùng hoặc bug sai | Phân biệt "đã có bug cùng nguyên nhân" và "test case viết sai" đang dựa vào phán đoán. Ví dụ ca Đăng nhập TC-001 đang "Đạt kèm lỗi đã biết" vì BUG-001: chạy lại sẽ Không đạt và dễ sinh bug trùng; lượt hiệu chuẩn (nguồn nháp) dễ sinh bug do test case sai | Script tra nhanh "bug đang mở có nhắc test case này" chạy trước khi tạo bug; lượt hiệu chuẩn và ca `CẦN XÁC NHẬN` thì tạo bug nhưng ghi rõ "nghi lỗi, chờ xác nhận" ở đầu bug |
| A4 | Hai tài liệu hướng dẫn trùng nội dung | `docs/bat-dau.md` và `docs/quy-trinh-kiem-thu.md` cùng mô tả 8 bước; mỗi lần đổi quy trình phải sửa cả hai, dễ lệch (đã phải sửa đôi 4 lần trong ngày) | Giữ một bản cho người dùng (`bat-dau.md`), bỏ hoặc rút `quy-trinh-kiem-thu.md` thành bảng skill cho người bảo trì |
| A5 | Tạo bug trên Jira chưa thử lần nào | Connector Atlassian chưa đăng nhập; cách map trường chưa kiểm | Thử một lần với bug giả trên dự án Jira thử khi bạn sẵn sàng |
| A6 | Tên người test lấy từ `git config user.name` khi chưa có `.nguoi-test` | Tên tài khoản Git (ví dụ biệt danh) lọt vào tài liệu gửi ra ngoài | Chưa có `.nguoi-test` thì hỏi tên một lần thay vì lấy tên Git |
| A7 | Mục Tổng kết của bảng phân tích requirement theo khuôn cũ không được đối chiếu | `kiem-tra.py` chỉ kiểm các nhãn đúng khuôn mới; một bảng cũ dùng "Tổng AC" nên không được kiểm | Đổi nhãn bảng đó theo khuôn (nhỏ) |

### B. Tốn token không cần thiết
| # | Chỗ tốn | Số đo | Đề xuất |
|---|---|---|---|
| B1 | `memories/project/skills.md` được mở **mỗi lần dùng skill** (cột "Khi" ghi "dùng/sửa skill") | ~20 KB mỗi lần, trong khi hướng dẫn đã nằm trong chính skill | Đổi "Khi" thành "sửa skill"; rút file về bảng ngắn |
| B2 | Phần nạp sẵn mọi phiên | `CLAUDE.md` 6,5 KB + `MEMORY.md` 6,3 KB + hai file ★ 8,3 KB ≈ 21 KB; `working-preferences.md` lặp lại các quy tắc đã có ở `CLAUDE.md` (trả link trang tổng, lời chào, tạo bug) | Bỏ phần lặp trong `working-preferences.md`; dời đoạn "Sản phẩm của dự án cho người đọc" (~2 KB) của `MEMORY.md` vào `modules/<slug>/` |
| B3 | Mô tả (description) 11 skill nạp vào mọi phiên | ~10,6 KB; dài nhất `tao-checklist-test-case` 1,4 KB, `de-xuat-regression` 1,3 KB | Rút mỗi mô tả về 400–600 ký tự: việc làm + câu kích hoạt + không dùng cho |
| B4 | `SKILL.md` dài 8–20 KB | Có ghi chú "Đã thử/Chưa thử", khối "Giữ ngữ cảnh gọn" chép ở 4 skill, chế độ cũ hai file của một tính năng cũ | Dời ghi chú thử nghiệm sang bộ nhớ; gom khối lặp vào `CLAUDE.md`; chuyển tính năng cũ sang file gộp rồi bỏ chế độ cũ |
| B5 | `truy-vet.py kiem` ghi lại `truy-vet.md` mỗi lần chạy chỉ để đổi giờ "Lần chạy gần nhất" | Sinh thay đổi giả trong git, trang HTML sinh lại, dễ commit nhầm | Chỉ ghi file khi nội dung truy vết thật sự đổi |

### Kết quả sửa rà soát lần 2 (2026-11-19)
| # | Đã làm |
|---|---|
| A1 | `truy-vet.py kiem --chi-doc` (không ghi file, in dòng TÓM TẮT); `kiem-tra-bo-nho.py` gọi truy vết từng tính năng, `truy-vet-smoke.py kiem`, `truy-vet-regression.py kiem`: requirement đổi mà test case/smoke/regression chưa cập nhật là LỖI |
| A2 | `kiem-tra-bo-nho.py` gọi `sinh-test-plan.py kiem`: test plan lệch số liệu là LỖI |
| A3 | Script `tao-bug-report/scripts/tim-bug-lien-quan.py`: chạy trước khi tự tạo bug, báo bug đang mở (nối, không tạo trùng) hoặc đã Đóng (đề xuất Mở lại). Ca thuộc lượt hiệu chuẩn, nguồn nháp, `CẦN XÁC NHẬN`: bug ghi "Nghi lỗi, chờ xác nhận" ở dòng đầu. Đã ghi vào 5 skill |
| A4 | `quy-trinh-kiem-thu.md` rút thành bản đồ bước → skill cho người bảo trì; cách dùng chỉ viết ở `bat-dau.md` |
| A5 | **Chưa làm được**: cần đăng nhập connector Atlassian để thử tạo bug trên Jira |
| A6 | Chưa có `.nguoi-test` thì ghi "Chưa ghi tên", không lấy tên Git |
| A7 | `kiem-tra.py` đối chiếu được cả nhãn kiểu cũ ("AC chỉ có phần ✅", "Tổng AC"); bảng cũ khớp 4 số |
| B1 | File ghi chú skill chỉ đọc khi **sửa** skill |
| B2 | Phần nạp sẵn mọi phiên từ ~21 KB còn ~16 KB (bộ nhớ sở thích 7,3 → 3,6 KB; đoạn riêng dự án đầu dời khỏi bản đồ) |
| B3 | Mô tả 11 skill rút còn 300–430 ký tự mỗi mô tả |
| B4 | Bỏ khối "Giữ ngữ cảnh gọn" lặp ở 4 skill (gom một chỗ ở `CLAUDE.md`), dời ghi chú "Đã thử/Chưa thử" sang bộ nhớ. Đăng nhập đã gộp `checklist.md` vào `test-case.md` (43 dòng khớp hoàn toàn, đã chốt truy vết, smoke, regression); chế độ hai file và khuôn JSON cũ đã bỏ khỏi skill |
| B5 | Truy vết chỉ ghi file khi nội dung đổi thật, không còn thay đổi giả vì giờ chạy |

Phát hiện thêm khi kiểm: `kiem-tra-tc.py` báo lỗi TC-002 Đăng nhập vì cột "Kết quả thực tế" nhắc ca khác ("cùng lỗi với TC-001"); đã sửa script: quy tắc "mỗi case tự đứng" chỉ áp cho phần thiết kế, không áp cho cột ghi khi chạy.
