---
name: tao-bug-report
description: Viết bug report (file md + trang HTML có nút sao chép, ảnh lỗi tô đỏ, video) từ ghi chú lỗi hoặc ca test Không đạt; tự tạo khi lượt chạy có ca Không đạt (tra bug trùng trước); tạo trên Jira khi được nhờ. Không bịa, thiếu bước hoặc môi trường thì hỏi tối đa 3 câu. Dùng khi nghe "tạo bug", "viết bug", "báo lỗi", "TC-xxx fail", "tạo bug trên Jira". Không dùng để viết test case hay hỏi BA.
---

# Tạo bug report

Biến ghi chú lỗi thô (hoặc một test case Không đạt) thành bug report mà Dev đọc xong **tái hiện được ngay, không phải hỏi lại**. Tiếng Việt. Sản phẩm: `BUG-nnn.md` + trang `BUG-nnn.html` (nút Sao chép) + ảnh bằng chứng tô đỏ + video nếu có. Skill này chỉ **viết**: không tự chạy lại test, không khám phá thêm để "tìm thêm chi tiết" (người dùng không đủ lượt chạy lại, xem `memories/user/working-preferences.md`). **Khi nào tạo bug (người dùng chốt 2026-11-19):** khi người dùng nhờ, **và tự tạo luôn (không hỏi) khi một ca chạy test ra `Không đạt`** (ý chính sai, điều kiện trước đúng): mỗi nguyên nhân một bug, kèm ảnh lỗi tô đỏ và video của ca đó. **Không** tạo bug cho ca `Không kết luận` (script lỗi, phiên hết hạn, điều kiện trước sai, bộ đếm từ chối): báo lý do. Ca Không đạt: **chạy trước `python -X utf8 .claude/skills/tao-bug-report/scripts/tim-bug-lien-quan.py <dự-án> <tính-năng>/TC-xxx`**. Có bug đang mở cùng chỗ → **không tạo bug mới**, nối mã bug cũ vào lượt chạy và nói rõ; bug đã Đóng mà lỗi quay lại → đề xuất Mở lại (hỏi người dùng). Ca thuộc lượt hiệu chuẩn (test case chưa chạy thật lần nào), nguồn nháp, hoặc kết quả mong đợi `CẦN XÁC NHẬN` → vẫn tạo bug nhưng **dòng đầu ghi "Nghi lỗi, chờ xác nhận: có thể do test case hoặc requirement chưa chốt"** và nêu điều cần xác nhận ở "Câu hỏi còn mở". Bug lưu trong repo; **chỉ tạo trên Jira khi người dùng nhờ** (mục "Tạo trên Jira").

## Ba nguồn đầu vào

| Người dùng đưa | Lấy gì ở đâu |
|---|---|
| **Ghi chú lỗi thô** (kèm môi trường, có thể kèm mã test case, requirement) | Mọi dữ kiện từ ghi chú; kết quả mong đợi từ requirement/test case đi kèm |
| **Mã test case Không đạt** ("TC-014 fail, tạo bug") | Điều kiện trước, bước, kết quả mong đợi **lấy từ dòng test case đó** (`python -X utf8 scripts/truy-vet.py tra <dự-án> <tính-năng> --ma TC-014`; nguồn có câu trả lời BA thì theo câu trả lời). Kết quả thực tế từ người dùng hoặc cột `Kết quả thực tế`. Người dùng nói bước khác test case thì **theo lời họ** |
| **Mình vừa chạy trong phiên này** | Kết quả thực tế = điều **thật sự quan sát** (nguyên văn thông báo, giá trị); ảnh `-loi`, chú thích lỗi, video đã có trong `result-*.json` (`error_images`, `error_image_captions`, `videos`); môi trường chỉ ghi cái đã thấy (số bản ở giao diện). Không viết điều không thấy |

## Quy tắc không được phá (và vì sao)

1. **Không thêm thông tin không có trong ghi chú.** Chỗ bắt buộc phải tự thêm thì gắn **`[Giả định: …]`** ngay tại chỗ. *AI hay điền cho trọn bộ rồi Dev đi tìm một điều kiện chưa từng có.* Điều lấy từ test case/requirement không phải giả định nhưng ghi nguồn ở mục Test case liên quan.
2. **Kết quả mong đợi chỉ lấy từ requirement hoặc test case** (chép câu chữ, không chèn ngoặc nguồn). Nguồn không nói điều đáng ra phải xảy ra thì **không tự đặt**: `Chưa xác định` + **một câu hỏi cho BA** ở "Câu hỏi còn mở" (khuôn: `memories/conventions/ba-question-wording.md`); khi đó là **nghi lỗi, chờ BA chốt**, nói rõ ở đầu file.
3. **Chỉ gộp nhiều chỗ vào một bug khi ghi chú nói rõ chung một nguyên nhân, hoặc Dev hoặc người kiểm thử xác nhận cùng chỗ sửa** (ví dụ câu báo lỗi tiếng Việt và English cùng sửa một chỗ → một bug, ghi cả hai ở Phạm vi ảnh hưởng và Đính kèm). Chưa chắc thì **tách bug riêng** (một file mỗi bug), mỗi bug ghi "có thể chung nguyên nhân với BUG-0xx, cần hỏi Dev" và đưa câu hỏi vào "Câu hỏi còn mở". Nhiều lỗi khác nhau → nhiều bug. `BUG-nnn` không dùng lại số đã bỏ.
4. **Thiếu bước tái hiện hoặc môi trường thì hỏi, tối đa 3 câu, rồi dừng chờ** (mỗi câu đủ ngữ cảnh, kèm lựa chọn nếu có; không hỏi lại điều đã có trong ghi chú, test case hay chat: `memories/user/working-preferences.md`). Môi trường đủ = nơi chạy + trình duyệt/thiết bị + số build; chỉ lấy cái người dùng đã nói trong lượt này hoặc mình vừa quan sát, **không đoán từ memory** (số build do người dùng hoặc giao diện cho biết). Câu hỏi nêu rõ thiếu gì kèm ví dụ cách trả lời. Chưa đủ thì không viết bản "tạm".
5. **Kết quả thực tế phải cụ thể**: màn hình nào, thao tác nào, thấy chính xác gì (nguyên văn thông báo, mã lỗi, giá trị sai và đúng, nút mờ, trang trắng…). **Cấm** câu chung chung: "không hoạt động", "bị lỗi", "sai", "lỗi hệ thống", "không như mong đợi". Ghi chú quá chung thì hỏi (tính vào 3 câu của quy tắc 4); hết lượt hỏi thì ghi `CẦN BỔ SUNG: <thiếu gì>`.
6. **Không đoán nguyên nhân gốc, không đề xuất cách sửa.** Ghi chú nêu nguyên nhân thì chép lại kèm "theo ghi chú của người dùng".
7. **Mức độ nghiêm trọng dựa trên ảnh hưởng** (ai bị, việc gì không làm được hoặc ra sai, có cách đi vòng không); **mức độ ưu tiên chỉ là đề xuất** ("team hoặc PO sẽ chốt"). Thang và cách viết: `references/thang-muc-do.md`.
8. **Tần suất chỉ ghi điều đã thử**: `Luôn xảy ra` (N/N lần), `Thỉnh thoảng (x/y lần thử)`, `Một lần`. Mới thử một lần và bị: `1/1 lần thử, chưa thử lại`. Không nêu số lần: `Chưa rõ`.
9. **Chỉ lỗi chức năng**; không tự thêm nhận xét bảo mật, hiệu năng, thẩm mỹ khi ghi chú không nói tới.
10. **Không ghi mật khẩu, mã thông báo, dữ liệu cá nhân thật**; tài khoản test chỉ ghi mã tài khoản (không ghi mật khẩu). Ảnh/log nhạy cảm thì nhắc người dùng che trước khi gửi.
11. **Đính kèm chỉ liệt kê cái có thật hoặc cái cần có** (chưa có → `Cần bổ sung`; không viết "xem ảnh đính kèm" khi chưa có ảnh). **Ảnh lỗi phải kèm bản tô đỏ** (giữ ảnh gốc, thêm `-loi`), mỗi dòng ghi **lỗi ở bước nào**; có video thì đính. Chi tiết: `references/bang-chung-va-trang-html.md`.
12. **Kết quả dài thì lưu file**, chat chỉ tóm tắt và link; riêng danh sách Giả định và câu hỏi còn mở in trong chat (người dùng duyệt ngay).
13. **Văn phong theo người dùng đã chỉnh**: tiêu đề chỉ mô tả lỗi, Trình duyệt chỉ tên + số bản, Kết quả mong đợi không ngoặc nguồn, mức độ bằng tiếng Việt, câu hỏi cho Dev đủ nghĩa → `references/van-phong.md` (đọc trước khi viết).
14. **Bug đến từ lượt smoke hoặc lượt chạy tự động thì nối vào bảng kết quả** (mã bug, ảnh tô đỏ, chú thích lỗi; ca không test được vì bug này → `Bị chặn` kèm link bug): `references/bang-chung-va-trang-html.md`. Ghi vào file dữ liệu của bảng, không sửa test case; điền `Trạng thái` của test case thì hỏi trước.

## Đọc gì cho từng việc
Sau `CLAUDE.md` và `memories/MEMORY.md` (đọc `.du-an-hien-tai`): luôn đọc `memories/user/working-preferences.md`, `memories/project/overview.md`, `memories/modules/<slug>/overview.md` của **dự án hiện tại**; không mở file dự án khác. Thêm:

| Việc | Đọc |
|---|---|
| Có mã test case | Dòng đó (`truy-vet.py tra … --ma TC-014`); **không đọc cả** `test-case.md` |
| Có mã requirement hoặc câu trả lời BA | Đúng dòng đó trong SRS/bảng soát (`Grep` kèm `| cut -c1-300`) |
| **Mọi lần viết bug** | `references/van-phong.md`; `assets/mau-bug-report.md` |
| Chấm mức độ nghiêm trọng/ưu tiên | `references/thang-muc-do.md`; dự án có `testing/<slug>/thang-muc-do-bug.json` thì dùng thang của team trong file đó |
| Có ảnh/video, dựng trang HTML, nối bảng kết quả | `references/bang-chung-va-trang-html.md` |
| Viết câu hỏi cho BA | `memories/conventions/ba-question-wording.md`, `memories/modules/<slug>/tu-ngu-cau-hoi-ba.md` |
| Cần hiểu nghiệp vụ để chấm ảnh hưởng | `memories/modules/<slug>/feature-<tên>.md` |

## Quy trình
1. **Chốt đầu vào**: ghi chú lỗi; môi trường; mã test case; requirement; hệ thống và feature (slug). Ghi chú trần vẫn làm, phần thiếu xử lý ở bước 2.
2. **Kiểm cái chặn việc viết**: thiếu bước tái hiện, môi trường, hoặc kết quả thực tế quá chung → **hỏi tối đa 3 câu rồi dừng** (quy tắc 4, 5). Có mã test case thì bước và điều kiện trước lấy từ test case.
3. **Tách hay gộp** (quy tắc 3): nhiều chỗ chung nguyên nhân đã xác nhận → một bug, mục "Phạm vi ảnh hưởng" liệt kê **từng chỗ** (màn hình, dữ liệu, kết quả sai); còn lại tách. Một bug thì ghi "Không có: chỉ một chỗ".
4. **Viết** theo `assets/mau-bug-report.md` (đúng thứ tự và tên mục) và `references/van-phong.md`. Gắn `[Giả định: …]` ở chỗ tự thêm.
5. **Lưu file và bằng chứng**: bug từ lượt chạy thì chạy `python -X utf8 .claude/skills/tao-bug-report/scripts/luu-bang-chung.py <file bug> --ket-qua <result-*.json> --ca <tính-năng>/tc-xxx --ghi` (thêm ảnh lỗi tô đỏ + video của ca vào mục Đính kèm, chép video vào `evidence/<slug>/bug/BUG-nnn/` để có trong repo; video gốc ở thư mục `video/` không vào git). **Bắt buộc có cả ảnh và video** cho bug từ lượt chạy; lượt không quay video thì dòng video ghi `Cần bổ sung`.  `testing/<slug>/<feature>/bug/BUG-<nnn>.md` (chưa rõ feature: `testing/<slug>/bug/`); `nnn` là số kế tiếp trong thư mục; một bug một file. Mã `BUG-nnn` là mã nội bộ, mã của công cụ quản lý bug của team do người dùng ghi thêm. Trước khi lưu: ảnh lỗi đã tô đỏ và có câu chú thích "Lỗi ở bước N". Sau khi lưu: `python -X utf8 scripts/build_docs.py --all` dựng trang HTML; báo **một link trang tổng** `testing/<slug>/index.html` (kèm điểm nhảy tới đúng phần, xem CLAUDE.md mục "Trả kết quả HTML"), không liệt kê nhiều file HTML.
6. **Tự kiểm** (dưới), sửa hết rồi mới trả lời.
7. **Cập nhật bộ nhớ** nếu có quy ước mới đáng ghi: `memories/modules/<slug>/feature-<tên>.md` hoặc `memories/project/skills.md`.
8. **Trả lời** ngắn: **một link trang tổng** `testing/<slug>/index.html` (kèm điểm nhảy tới đúng phần, xem CLAUDE.md mục "Trả kết quả HTML"), không liệt kê nhiều file HTML; tiêu đề; mức độ nghiêm trọng + ưu tiên đề xuất; **danh sách Giả định** (in nguyên); **câu hỏi còn mở** cho BA/Dev; đính kèm còn thiếu. Nói rõ **chưa tái hiện lại** (chỉ viết theo ghi chú). Test case Không đạt do mình chạy: kết quả đã ghi vào test case theo `chay-test-tu-dong`, không hỏi lại; test case Không đạt do người dùng tự chạy: hỏi có điền `Kết quả thực tế` và `Trạng thái` vào dòng test case không. Bug từ smoke/lượt chạy: hỏi có dựng lại lượt để nối bug vào bảng kết quả không. Commit chỉ khi người dùng nhờ.

## Tạo trên Jira (chỉ khi người dùng nhờ)
Mặc định bug chỉ nằm trong repo. Người dùng nói "tạo bug 01 trên Jira", "đẩy bug lên Jira" thì:
1. Cần connector Atlassian (Jira). Chưa kết nối/chưa đăng nhập thì nói người dùng bật và đăng nhập (qua `/mcp` trong app), không tìm cách khác.
2. Hỏi (một lần, đủ ngữ cảnh) những gì chưa biết: dự án Jira (project key), loại issue (Bug), trường bắt buộc riêng của team. Ghi câu trả lời vào `memories/modules/<slug>/overview.md` để lần sau không hỏi lại.
3. Tạo issue từ đúng file bug md: tiêu đề = dòng `#` (bỏ `[Module]` nếu team không dùng), mô tả = các mục theo thứ tự trong file (môi trường, điều kiện trước, các bước, kết quả mong đợi, kết quả thực tế, phạm vi ảnh hưởng, tần suất, câu hỏi còn mở), mức độ nghiêm trọng/ưu tiên map sang trường của Jira nếu team có. **Đính kèm ảnh lỗi tô đỏ và video** nếu connector cho phép; không cho thì ghi đường dẫn trong mô tả và nhắc người dùng đính tay. Không đưa mật khẩu, dữ liệu cá nhân thật, nhãn `[Giả định: …]` chưa được người dùng duyệt thì hỏi trước khi gửi.
4. Ghi mã Jira vào file bug (dòng `Mã Jira: <KEY-123> (<link>)` dưới tiêu đề), `build_docs.py --all`, báo người dùng link Jira và link trang tổng.
Bug đã có mã Jira thì không tạo trùng; người dùng nhờ cập nhật thì sửa issue đó.

## Tự kiểm trước khi trả lời
Chạy trước: `python -X utf8 .claude/skills/tao-bug-report/scripts/kiem-tra-bug.py <file bug>` (kiểm khuôn, mức độ tiếng Việt, tần suất, câu chung chung, đếm nhãn Giả định, ảnh có thật, không có mật khẩu); sửa hết lỗi rồi mới làm danh sách dưới (script không thay việc đọc lại).

- [ ] **Kết quả thực tế** không có câu chung chung (hỏi "Dev đọc câu này có thấy màn hình lúc đó không?").
- [ ] Mọi thông tin tự thêm có nhãn `[Giả định: …]` và xuất hiện đủ trong danh sách Giả định cuối file (đếm hai bên bằng nhau).
- [ ] Kết quả mong đợi có nguồn; không có thì `Chưa xác định` + câu hỏi BA.
- [ ] Mọi bước tái hiện bắt nguồn từ ghi chú hoặc test case; bước đầu đủ môi trường/tài khoản để làm theo.
- [ ] Không có mật khẩu, nguyên nhân gốc tự đoán, hay cách sửa.
- [ ] Gộp chỉ khi đã xác nhận; tách riêng thì có câu hỏi cho Dev.
- [ ] Đủ các mục theo mẫu; tần suất đúng một trong ba dạng.
- [ ] Danh sách tự kiểm văn phong ở cuối `references/van-phong.md` đã qua; ảnh lỗi đã tô đỏ và `Read` kiểm khung.
- [ ] Trang HTML đã dựng lại sau lần sửa md cuối; bug từ smoke/lượt chạy đã được hỏi để nối vào bảng kết quả.

## Tệp trong skill
- `scripts/kiem-tra-bug.py` — kiểm tự động một hoặc mọi bug của dự án (`--du-an`); báo lỗi khi video còn trỏ vào thư mục không vào git.
- `scripts/tim-bug-lien-quan.py` — tìm bug đã có nhắc test case (trước khi tạo bug từ lượt chạy), báo bug đang mở để nối thay vì tạo trùng.
- `scripts/luu-bang-chung.py` — thêm ảnh lỗi + video của ca vào bug, chép video vào `evidence/<slug>/bug/BUG-nnn/`.
- `assets/mau-bug-report.md` — hình dạng file bug (ví dụ trung lập, đủ nhãn Giả định, câu hỏi BA/Dev, phạm vi ảnh hưởng, ảnh tô đỏ kèm lỗi ở bước nào).
- `references/` — `van-phong.md`, `thang-muc-do.md`, `bang-chung-va-trang-html.md`.
- Công cụ dùng chung của repo: `scripts/build_docs.py`, `scripts/build_report.py` (`add-run`, `bug-pages`), `scripts/mark_error.py`, `scripts/test_automation/bug_page.py`, `docs/chay-test-tu-dong.md`.
- Khuôn bug: `assets/`; văn phong: `references/van-phong.md`.
