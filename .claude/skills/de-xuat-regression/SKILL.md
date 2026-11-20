---
name: de-xuat-regression
description: Đề xuất và cập nhật bộ regression ba tầng (lõi, vùng bị ảnh hưởng, toàn bộ) chọn từ test case có sẵn, có phân tích ảnh hưởng gắn nhãn nguồn và truy vết; chạy và ghi kết quả từng tầng; thêm case từ bug lọt production. Dùng khi nghe "đề xuất regression", "phân tích ảnh hưởng release note", "cập nhật regression", "chạy regression Tầng 1", "bug lọt production". Không dùng để viết test case, chọn smoke hay phân tích requirement.
---

# Đề xuất và cập nhật bộ regression

**Regression trả lời:** sau khi hệ thống đổi, phần đang chạy đúng có còn đúng không? Không đợt nào cũng chạy hết, nên chia ba tầng:

| Tầng | Nghĩa | Khi nào chạy |
|---|---|---|
| 1 | **Lõi**: luồng chính mà hỏng thì không test được việc khác | Mọi đợt |
| 2 | **Vùng bị ảnh hưởng**: nhóm case theo vùng chức năng | Chỉ vùng mà thay đổi chạm tới |
| 3 | **Toàn bộ** test case | Chỉ khi có lý do (đổi lớn ở chỗ dùng chung, sắp lên bản chính thức, Tầng 1-2 thấy nhiều lỗi) |

**Chỉ MỘT file** `testing/<dự-án>/regression-test.md` (giống smoke): sửa trực tiếp, không tạo file phụ; mốc truy vết và lịch sử nằm trong file. Smoke là bước trước regression.

## Đầu vào (hỏi nếu thiếu, không đoán; tối đa 3 câu, mỗi câu đủ ngữ cảnh)

| Cần | Lấy ở đâu | Nếu chưa có |
|---|---|---|
| Dự án | `.du-an-hien-tai` | Hỏi theo `CLAUDE.md` bước 0 |
| Release note / ticket / bug đã sửa | Người dùng dán | **Chưa có thì không bịa thay đổi**: viết bảng phân tích theo **vùng chức năng** ("nếu vùng này đổi thì ảnh hưởng gì"), ghi rõ trong file; khi có release note thì thêm mục "Theo đợt phát hành" |
| Bộ regression | Test case đã có `testing/<dự-án>/*/test-case.md` (tính năng có `truy-vet-cau-hinh.json`), hoặc danh sách người dùng dán (mã, tên, module) | Không có thì dừng, nói rõ |
| Thông tin thêm (module dùng chung, tích hợp ngoài, chỗ hay lỗi) | `memories/modules/<slug>/`, SRS, người dùng | Hỏi một câu; không có thì phần đó ghi Giả định |

## Ràng buộc (người dùng chốt)

- Với mỗi thay đổi (hoặc mỗi vùng) xét ba hướng: **chức năng dùng chung phần đó**, **chức năng đứng sau trong luồng**, **tích hợp bên ngoài**.
- **Chỉ chọn case có trong bộ regression.** Vùng rủi ro mà thiếu case thì ghi vào "Case đề xuất viết thêm", **không tự viết** (hỏi người dùng trước khi thêm test case).
- **Chỉ dựa vào nguồn đã có.** Mỗi dòng phân tích ảnh hưởng gắn nhãn: **Có trong tài liệu** (release note, SRS, bảng soát, test case hoặc thông tin thêm nói rõ), **Suy luận** (suy từ tên module/chức năng, cần Dev xác nhận), **Giả định** (không có căn cứ). Một dòng ghép hai ý thì ghi nhãn cho từng ý.
- Thiếu thông tin tới mức không làm tiếp được thì dừng và hỏi (tối đa 3 câu).

## Quy trình

1. **Liệt kê case, không đọc cả file test case**: `python -X utf8 .claude/skills/tao-smoke-test/scripts/liet-ke-tc.py <dự-án>` (cờ `⚠️`, `SAI-N`, `CHO`, `PHU`, `NGUỒN NHÁP`). Cần xem kỹ một case: `python -X utf8 scripts/truy-vet.py tra <dự-án> <tính-năng> --ma TC-005`. Mã requirement của từng case: cột Nguồn, hoặc bảng "Truy vết" của file regression đã có (mọi mã trong các bảng truy vết đều là **link bấm được** tới đúng dòng tài liệu; bảng mới nào cũng phải làm link).
2. **Phân tích ảnh hưởng** (đầu ra phần 1): bảng `Nếu vùng/thay đổi này đổi | Vùng có thể bị ảnh hưởng | Lý do | Nhãn nguồn`. Mỗi thay đổi trong release note có ít nhất một dòng; chưa có release note thì mỗi vùng chức năng một dòng. Dùng SRS để biết ai dùng chung, luồng nào đứng sau, API/tích hợp nào; chỗ SRS không nói thì ghi Suy luận hoặc Giả định, **không viết như đã biết**.
3. **Chia vùng Tầng 2** từ chính các mã requirement (nhóm story/AC/quy tắc). Mỗi vùng một tên ngắn, câu "Chọn khi …" nói điều gì đổi thì phải chạy vùng này.
4. **Chọn Tầng 1**: luồng chính mỗi chức năng (đường đúng, mỗi kết quả chính, cửa vào/cửa ra, cầu nối sang chức năng sau). Không chọn theo cột Ưu tiên (nhiều case đều Cao); chọn theo "hỏng thì chặn gì". Mỗi case một dòng kèm lý do.
5. **Mọi case còn lại thuộc một vùng của Tầng 2**: script bắt case chưa xếp. Tầng 3 là một dòng ("toàn bộ N case") không liệt kê.
6. **Loại/cảnh báo theo cờ** (không chép tay mã): `SAI-N` với N≥2 hoặc `CHO` (chặn/khóa tài khoản): không đưa vào Tầng 1; nếu thuộc vùng Tầng 2 thì ghi "người dùng tự chạy tay, không chạy tự động trọn gói"; nhiều ca `SAI-1` chạy liền nhau thì ghi quy tắc xả bộ đếm (đăng nhập đúng xen kẽ) vào "Lưu ý khi chạy"; `PHU` (tác dụng phụ khó đảo ngược): không vào Tầng 1; `⚠️` (hệ thống đang làm khác): ghi cách xử lý, Tầng 1 tránh nếu có case khác; `NGUỒN NHÁP`: ghi vào dòng Tình trạng, lượt chạy đầu là hiệu chuẩn. Số ngưỡng (lần sai, thời gian chặn) lấy từ requirement của dự án, **không tự đặt**.
7. **Case đề xuất viết thêm**: mã requirement chưa có case (`truy-vet.py kiem` báo), vùng rủi ro không có case (tích hợp, luồng đứng sau). Mỗi dòng: vùng, vì sao thiếu, đề xuất. Chưa viết.
8. **Câu hỏi cho Dev** (tối đa 5, nói vì sao hỏi và sẽ làm gì tùy câu trả lời): chỗ dùng chung có thật không, hai chỗ tính cùng công thức không, tích hợp nào bị chạm, cấu hình hay hằng số.
9. **Viết file**: chép `assets/mau-regression-test.md` thành `testing/<dự-án>/regression-test.md`, điền. Bảng tầng đúng 4 cột `Tầng | Vùng | Mã case gốc | Lý do chọn`: Tầng 1 mỗi dòng một case; Tầng 2 mỗi dòng một vùng, ô Mã case gốc nhiều link ngăn bằng `<br>`; Tầng 3 một dòng không link. **Mã case gốc luôn là link** `[Tên module · TC-005](thư-mục/test-case.md#tc-005)` kèm tên tình huống (hai module có thể trùng mã TC). Câu chữ đọc là hiểu, không dùng mã nội bộ làm nội dung chính.
10. **Chốt truy vết** (sau khi đã chốt truy vết từng tính năng): `python -X utf8 scripts/truy-vet-regression.py chot <dự-án> -m "đã làm gì"` (ghi mốc, lịch sử, bảng vùng → mã requirement).
11. **Tự kiểm** trước khi trả lời: mỗi thay đổi (hoặc vùng) có ít nhất một dòng phân tích có nhãn; mọi mã case trong bảng có trong test case đã có (`kiem` 0 vấn đề); mọi case thuộc Tầng 1 hoặc một vùng; thông tin ngoài nguồn đã ghi Giả định; số ngưỡng có nguồn.

## Cập nhật khi requirement hoặc test case đổi

`python -X utf8 scripts/truy-vet-regression.py kiem <dự-án>` (CHỈ ĐỌC, in vài dòng; **không đọc cả file regression**). Script in: mã requirement đã đổi, case nào dựa vào mã đó (kèm tầng/vùng) và **gợi ý phạm vi đợt này** (Tầng 1 + vùng bị chạm; suy ra từ requirement đổi, không phải từ build); test case đã sửa; test case mới chưa xếp tầng/vùng; test case không còn. Xử lý: case mới → xếp vào Tầng 1 hoặc một vùng (hoặc tạo vùng mới); case đổi → đọc lại, giữ/đổi tầng/bỏ, sửa "Lý do chọn" và bảng phân tích ảnh hưởng nếu không còn đúng; rồi `chot`. `truy-vet.py kiem/chot` của tính năng tự nhắc chạy lệnh này khi file regression có dùng tính năng đó. Giới hạn: chỉ bắt thay đổi đã ghi vào SRS, bảng soát hoặc test case; hệ thống đổi mà tài liệu chưa đổi thì dựa vào release note và câu hỏi Dev.

## Rule: bug lọt production mà chưa có test case thì thêm vào regression (người dùng chốt 2026-11-19)

Bug đã lọt ra production tức là bộ test không bắt được nó. Nếu chưa có test case nào chặn đúng bug đó thì **phải viết case mới và đưa vào bộ regression** để lần phát hành sau không lọt lại. Đã có case chặn được thì không thêm; chỉ kiểm vì sao case đó không bắt được hoặc không được chạy (xem câu 1 bên dưới), rồi nâng tầng hoặc sửa case nếu cần.

**Đầu vào (người dùng dán; thiếu thì hỏi, tối đa 3 câu):** mã bug, mô tả, các bước tái hiện, điều kiện xảy ra, bản sửa (đã xác nhận chưa), và các case hiện có của module đó (tự lấy bằng `liet-ke-tc.py` + `truy-vet.py tra`, không bắt dán lại). **Chỉ dựa vào thông tin bug đã có**, không bịa điều kiện; **kết quả mong đợi lấy theo bản sửa đã xác nhận**, chưa có xác nhận thì ghi `CẦN XÁC NHẬN` (case vẫn được thêm, đánh dấu để chốt sau).

**Đầu ra (trong chat, để người dùng duyệt; không tự ghi vào test-case.md khi chưa được đồng ý):**
1. **Vì sao bộ test hiện tại bỏ lọt** (1 đến 3 câu): thiếu dữ liệu, thiếu trạng thái, thiếu bước, hay case có nhưng không được chạy.
2. **Test case mới**, bảng 7 cột: `Mã | Tình huống | Điều kiện trước | Các bước | Dữ liệu | Kết quả mong đợi | Mã bug gốc`. Tái hiện **đúng điều kiện gây bug**, đủ để tự đứng được (người khác chạy được mà không cần đọc bug). Tình huống viết đủ câu theo quy ước của `tao-checklist-test-case`.
3. **Tầng regression đề xuất** (Tầng 1 lõi hay vùng nào của Tầng 2) và lý do. Gợi ý: bug ở luồng chính mà hỏng thì chặn việc khác → Tầng 1; bug ở chức năng riêng → vùng tương ứng của Tầng 2 (tạo vùng mới nếu chưa có).

**Sau khi người dùng đồng ý:**
- Chuyển case sang bảng test case của tính năng bằng cách làm của skill `tao-checklist-test-case` (13 cột; mã TC kế tiếp; khai báo dòng "Dòng thêm sau khi requirement đổi" cho `kiem-tra-tc.py`). **Mã bug gốc ghi ở cột Nguồn** (một dòng `Bug lọt production <mã>`, có link tới bug report hoặc ticket nếu có file/URL) **cùng mã requirement bị bug chạm** (để truy vết bắt được khi requirement đổi). Bug cho thấy requirement còn thiếu một điều → ghi vào bảng soát/SRS, không chỉ thêm case.
- Thêm case vào `regression-test.md`: ở cột "Lý do chọn" bắt đầu bằng `Bug lọt production <mã>: <vì sao nên nằm ở tầng này>`. Case sinh từ bug production **không bị bỏ khỏi bộ regression** khi chưa có quyết định của người dùng.
- Chạy `truy-vet.py chot` của tính năng, rồi `truy-vet-regression.py chot -m "thêm case TC-xxx từ bug <mã>"`.

## Chạy regression và ghi kết quả

Chỉ khi người dùng nhờ ("chạy Tầng 1"…). Chạy theo `chay-test-tu-dong` (đọc `references/quy-tac-da-chot.md` của skill đó: địa chỉ phải do người dùng nêu trong phiên và có nhãn môi trường thử, xác nhận lại nếu chưa nêu; mật khẩu chỉ nằm trong `.env`, không hiện trong chat; không chạm ngưỡng chặn).

1. **Chốt phạm vi:** tầng nào (mặc định Tầng 1); case nào chưa có script `auto/` (viết thêm theo khuôn `assets/mau-ca-tu-dong.py` của `chay-test-tu-dong`); case nào cần tạo dữ liệu thật (hồ sơ nháp…) thì **hỏi trước**, dùng một lần thì ghi rõ trong script; vùng chặn tạm / `SAI-N` / `CHO` thì để người dùng tự chạy. Hỏi một lần cho cả hai việc (địa chỉ, dữ liệu), mỗi câu đủ ngữ cảnh.
2. **Đăng nhập một lần rồi chạy ngay** (phiên sống ngắn): `python -X utf8 scripts/auto_login.py <tài khoản…> --headless`, rồi `python -X utf8 scripts/run_tests.py --project <slug> --case-id <tính-năng>/tc-xxx …` (dùng Python của `.venv` nếu máy báo thiếu Playwright). **Thứ tự:** case chưa có phiên trước; case nhập sai ít → nhiều; **case làm mất phiên (đăng xuất) xếp cuối**.
3. **Điều kiện trước sai thì `Không kết luận`**, không `Không đạt` giả; sửa script chỉ khi điều kiện script đòi **vượt** điều kiện trong test case gốc (ghi rõ đã sửa gì). Kết quả khác kết quả mong đợi mà điều kiện trước đúng thì là `Không đạt` thật: **tạo bug luôn, không hỏi** (người dùng chốt 2026-11-19) theo `tao-bug-report`, kèm ảnh `-loi` tô đỏ và video (`luu-bang-chung.py` chép video vào `evidence/<dự-án>/bug/BUG-nnn/` để có trong repo); **trước khi tạo chạy `tao-bug-report/scripts/tim-bug-lien-quan.py <dự-án> <tính-năng>/TC-xxx`**: có bug đang mở cùng chỗ thì nối bug cũ, không tạo mới; bug đã Đóng mà lỗi quay lại thì đề xuất Mở lại; ca thuộc lượt hiệu chuẩn, nguồn nháp hoặc kết quả mong đợi `CẦN XÁC NHẬN` thì vẫn tạo bug nhưng dòng đầu ghi "Nghi lỗi, chờ xác nhận" (có thể do test case); Không đạt vì chính test case viết sai (thường ở lượt hiệu chuẩn) thì sửa test case, không tạo bug; bug lên Jira chỉ khi người dùng nhờ.
4. **Ghi kết quả vào test case gốc** (cột Kết quả thực tế, Trạng thái, Tự động hóa) cho case mới có script hoặc đổi kết quả; chỉ cột ghi khi chạy nên truy vết không coi là sửa.
5. **Ghi lượt, HAI nơi:**
   - Tóm tắt trong file: `python -X utf8 scripts/truy-vet-regression.py ghi-luot <dự-án> --tang "Tầng 1" --build "<số bản>" --ket-qua "<tính-năng>/TC-005=Đạt,…" --ghi-chu "…"`.
   - **Trang kết quả** (bắt buộc, người dùng đòi vì chỉ có tóm tắt thì họ "chưa thấy file HTML"): viết file kết luận JSON (`headline`, `passed`, `not_tested` liệt kê từng mã RG, `risks`, `suggestion`; không câu chung chung) rồi `python -X utf8 scripts/build_report.py add-run --suite regression-tang-<N> --build … --results-files <các result-*.json theo thời gian> --bug "2=BUG-001" --note "…" --conclusion-file …`. ID trong trang là **RG-01…** theo thứ tự dòng trong bảng tầng (số của `--bug`, `--status` là số RG). Ra `testing/<dự-án>/regression-tang-<N>-ket-qua.md/.html` và `run-results/regression-tang-<N>.json`; kết luận lượt: `Đạt toàn bộ` / `Có case không đạt` / `Chưa chạy hết`.
6. **Sinh lại và kiểm:** `python -X utf8 scripts/build_docs.py --all` (trang tổng có thẻ "Bộ regression test": link tới file regression, trang kết quả từng tầng, dòng lượt gần nhất), `kiem-tra-bo-nho.py`, `kiem-tra-ro-mat-khau.py`. Báo người dùng **một link trang tổng** `testing/<slug>/index.html` (kèm điểm nhảy tới đúng phần, xem CLAUDE.md mục "Trả kết quả HTML"), không liệt kê nhiều file HTML.

## Trả lời người dùng

File dài lưu trong repo; chat chỉ **tóm tắt + link**: số case mỗi tầng, vùng ảnh hưởng chính, case/ý cần người dùng chốt, case đề xuất viết thêm, câu hỏi cho Dev. Không dán cả file. Dự án đã có `testing/<dự-án>/test-plan.md` thì cuối câu trả lời nhắc người dùng nói "Cập nhật test plan" để test plan có số liệu mới (test plan lập ở bước 2, trước khi có bộ này). Commit chỉ khi người dùng nhờ.
