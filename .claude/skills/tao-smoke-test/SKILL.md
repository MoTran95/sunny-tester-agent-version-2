---
name: tao-smoke-test
description: Đề xuất, cập nhật và chạy bộ smoke test (một file smoke-test.md) chọn từ test case có sẵn — case mà hỏng thì việc test khác vô nghĩa, kèm thời gian ước tính và tiêu chí trả build. Dùng khi nghe "đề xuất smoke test", "lập bộ smoke", "cập nhật smoke test", "chạy smoke". Không dùng để viết test case hay chọn regression.
---

# Tạo và cập nhật bộ smoke test

**Mục đích của smoke:** trả lời một câu hỏi — *build này đủ ổn để bắt đầu test sâu chưa?* Một case vào smoke khi **hỏng thì việc test khác vô nghĩa hoặc bị chặn**, không phải vì nó nhanh hay dễ. Smoke **rộng và nông**: mỗi chức năng chỉ kiểm luồng cơ bản.

**Thời gian chỉ là mục tiêu tham khảo, không cứng** (người dùng chốt): vượt mục tiêu mà case cần cho mục đích thì giữ case, ghi lý do. Không bỏ case quan trọng chỉ vì thời gian.

**Chỉ MỘT file smoke** cho mỗi dự án (`testing/<dự-án>/smoke-test.md`): sửa trực tiếp và cập nhật, không tạo file phụ (người dùng chốt). Mốc truy vết và lịch sử nằm trong chính file.

**Smoke Đạt không có nghĩa cả hệ thống ổn**, chỉ là phần nó phủ dùng được. Luôn nói rõ phần chưa phủ.

## Đầu vào (hỏi nếu thiếu, không đoán)

| Cần | Lấy ở đâu | Nếu chưa có |
|---|---|---|
| Dự án | `.du-an-hien-tai` | Hỏi theo `CLAUDE.md` bước 0 |
| Thời gian mục tiêu | Người dùng | Hỏi (một câu); là mục tiêu tham khảo |
| Release note của build | Người dùng dán | Hỏi. Chưa có thì phần "Theo build" làm theo bước 4 (gợi ý từ requirement đổi, người dùng đồng ý mới đưa vào), không tự đoán chỗ đổi |
| Danh sách chức năng + hành trình then chốt | `memories/modules/<slug>/overview.md`, SRS đã có, hoặc người dùng | Hỏi một câu: "Hành trình nào mà hỏng thì không test được gì?" |
| Nguồn case | Test case đã có ở `testing/<dự-án>/*/test-case.md`, hoặc bộ người dùng đưa (mục cuối) | Không có test case nào thì dừng, nói rõ |

## Quy trình

1. **Liệt kê test case, không đọc cả file** (file rất lớn): `python -X utf8 .claude/skills/tao-smoke-test/scripts/liet-ke-tc.py <dự-án>`. Mỗi module có một dòng đầu (số case, đã chạy bao nhiêu, `NGUỒN NHÁP` nếu requirement chưa BA xác nhận), mỗi case một dòng `Mã | Ưu tiên | cờ | số bước | ~phút | Tình huống`. Cờ: `⚠️` đang lệch hệ thống; `SAI-N` cố ý nhập sai N lần; `CHO` phải chờ lâu; `PHU` có tác dụng phụ khó đảo ngược (gửi SMS/email, phê duyệt/từ chối, xóa, thanh toán). `~phút` = số bước × ~18 giây, làm tròn 0,5, là cơ sở rồi cộng chờ cố định. Tình huống bị cắt `…` mà cần đủ ý, hoặc cần xem kỹ một case: `python -X utf8 scripts/truy-vet.py tra <dự-án> <tính-năng> --ma TC-005`.
2. **Xác định hành trình then chốt trước khi chọn case.** Viết ra 3–6 hành trình (chuỗi chức năng mà hỏng thì chặn việc test khác), lấy từ danh sách chức năng, **không lấy từ test case** (nếu lấy từ test case thì smoke chỉ phủ phần đã có case). Đối chiếu từng hành trình với test case. Hành trình then chốt **không có test case nào**: nói rõ trong chat ("smoke Đạt không bảo đảm hành trình này"), ghi vào "Phạm vi chưa phủ", và **hỏi người dùng có cho đề xuất case mới** không (ghi `Case mới` ở cột Mã case gốc, kèm kết quả Đạt/Không đạt rõ; không tự thêm khi chưa được đồng ý).
3. **Chọn phần Cố định**: với mỗi hành trình, **luồng đúng cơ bản** và kết quả cơ bản của từng nhánh chính (ví dụ mỗi kết quả khuyến nghị một case); mỗi chức năng vài case, không nhiều. **Không chọn theo cột Ưu tiên** (nhiều case đều Cao nên không phân biệt được); chọn theo "hỏng thì chặn chức năng nào", và cột "Vì sao chọn" phải nêu đúng điều đó.
4. **Chọn phần Theo build**: có release note thì chọn thêm case ở chỗ vừa đổi lớn. **Chưa có release note**: chạy `python -X utf8 scripts/truy-vet.py kiem <dự-án> <tính-năng>` cho từng tính năng; mã requirement/test case báo "đã đổi/Cần xem lại" từ lần chốt trước là gợi ý chỗ đổi. Nói trong chat đó là gợi ý **suy ra từ requirement đổi, không phải từ build**, người dùng đồng ý mới đưa vào bảng. Không có gợi ý nào thì để trống và nói rõ. (Lưu ý: `kiem` ghi lại `truy-vet.md` của tính năng.)
5. **Loại** (suy ra từ cờ, không chép tay danh sách mã):
   - **Khóa tài khoản/kích hoạt giới hạn**: `SAI-N` với N≥2, hoặc `CHO` (chờ lâu): loại (xem `memories/pitfalls/dont-trigger-lockouts.md`). `SAI-1` là luồng lỗi, không phải luồng cơ bản: để test sâu; chỉ chọn khi chức năng không còn case nào khác và người dùng đồng ý trước.
   - **Tác dụng phụ** (`PHU`): gửi SMS/email thật, phê duyệt/từ chối, xóa, thanh toán: không đưa vào smoke trừ khi chạy trên môi trường thử và người dùng đồng ý; ghi rõ dữ liệu bị đổi.
   - **Lệch hệ thống** (`⚠️`): sẽ Không đạt mỗi lượt và chặn build vì lỗi chưa xác nhận. Tránh nếu có case khác; nếu là case duy nhất cho chức năng đó thì chọn nhưng ghi cách xử lý vào tiêu chí trả build (hỏi người dùng chốt: giữ chặn build hay "Đạt kèm lỗi đã biết"). Nếu bỏ một case chính vì ⚠️ để lấy case khác, nói rõ trong chat để người dùng chốt. **⚠️ dựa trên quan sát của một bản build cũ**: xem mục "Mỗi khi đổi build".
   - **Nguồn nháp** (`NGUỒN NHÁP`) hoặc case chưa chạy thật: được chọn, nhưng ghi vào dòng "Tình trạng" của file và coi **lượt chạy đầu là lượt hiệu chuẩn** (case Không đạt thì kiểm lại test case trước khi kết luận trả build).
   - Case sát ranh giới/ngoại lệ/luồng lỗi: để test sâu.
   - **Chỉ dùng chức năng có trong danh sách chức năng của dự án.** Chức năng ngoài danh sách thì không thêm; chức năng trong danh sách mà chưa có test case thì làm theo bước 2.
6. **Ước lượng thời gian**: lấy `~phút` ở bước 1 làm cơ sở (mọi phiên ước lượng cùng cách), cộng chờ cố định và việc chuẩn bị dùng chung (tạo dữ liệu một lần; cách làm xem `memories/modules/<slug>/`, không có thì ghi "ước lượng, cần đo"). Ghi rõ là **ước lượng**. Không dùng để cắt case.
7. **Xếp thứ tự chạy** để dùng lại phiên đăng nhập và dữ liệu; case cần mở đầu ở trạng thái chưa đăng nhập xếp đầu, case cần đổi tài khoản hoặc đăng xuất xếp cuối; ghi việc đăng xuất/đổi tài khoản giữa các case vào đoạn "Cách đọc" của file.
8. **Viết file**: chép `assets/mau-smoke-test.md` thành `testing/<dự-án>/smoke-test.md`, điền. Quy ước:
   - Bảng đúng 7 cột; cột **Phần** chỉ ghi `Cố định` hoặc `Theo build`; **Mã case gốc là link** `[Tên module · TC-005](thư-mục/test-case.md#tc-005)` (hai module có thể trùng mã TC nên luôn kèm tên module); case mới ghi `Case mới`, case của bộ ngoài repo ghi `Ngoài repo: <tên nguồn> · <mã>`.
   - Cột "Smoke case" là câu đầy đủ rõ nghĩa (hệ thống làm gì khi người dùng làm gì), không viết tắt mã.
   - Cột "Vì sao chọn" nói theo **mục đích** (hỏng thì chặn gì). Điểm lệch hệ thống ghi ở đây.
   - Cột "Nên tự động hoá?": Nên/Không + lý do ngắn (mật khẩu lấy từ biến môi trường, không ghi vào script).
   - **Phạm vi chưa phủ** (một dòng): hành trình/chức năng chưa có test case (bước 2), và mã SRS mà `truy-vet.py kiem` báo "chưa có test case". "Bản" ở tiêu đề là bản của hệ thống đang test.
   - Dòng "Tình trạng": ghi nguồn nháp (nếu có) và số case gốc đã chạy thật.
9. **Tiêu chí trả build**: bảng 3 cột `Case | Đạt khi (ý chính) | Không đạt thì dừng vì`. Case gốc thường dài hơn luồng cơ bản nên phải tách: **ý chính** (chọn từ "Kết quả mong đợi" của case gốc, ghi theo số bước) quyết định Đạt/Không đạt và dừng build; **ý phụ** (chi tiết giao diện, dòng chữ phụ, số liệu phụ) chỉ ghi nhận, không dừng. Không chép lại cả kết quả gốc. Phần tách ý chính/phụ là đề xuất, người dùng duyệt. Case lệch hệ thống: ghi cách xử lý đã chốt và liệt kê **chính xác** ý được miễn.
10. **Truy vết + lịch sử**: dự án cần `truy-vet-cau-hinh.json` cho từng tính năng và neo `<a id="tc-005">` ở ô Mã của test case (theo `tao-checklist-test-case`). Rồi `python -X utf8 scripts/truy-vet-smoke.py chot <dự-án> -m "đã làm gì"` (ghi lịch sử, mục Truy vết, mốc).
11. **Tự kiểm** trước khi trả lời: mỗi case có mã case gốc (hoặc ghi rõ là case mới/ngoài repo); hành trình then chốt không có case đã nêu; chỉ dùng chức năng trong danh sách; thời gian ghi là ước lượng; mỗi dòng tiêu chí có "Đạt khi"; chạy `python -X utf8 scripts/truy-vet-smoke.py kiem <dự-án>` (0 vấn đề; các dòng "(lưu ý)" đọc rồi nói với người dùng). **Tổng thời gian so với mục tiêu chỉ để tham khảo**.

## Chạy smoke (execute)

Chỉ khi người dùng nhờ chạy; **đọc `references/chay-smoke.md` trước khi chạy**. Case có script `auto/` thì chạy bằng skill `chay-test-tu-dong` (`run_tests.py --smoke`, ghi lượt bằng `build_report.py add-run`, trang `smoke-ket-qua.html`); không có script thì chạy tay theo giao thức. Địa chỉ phải do người dùng nêu và có nhãn môi trường thử; mật khẩu không bao giờ hiện trong chat.

## Cập nhật khi requirement/test case đổi

`python -X utf8 scripts/truy-vet-smoke.py kiem <dự-án>` (CHỈ ĐỌC, in vài dòng; **không đọc cả `smoke-test.md`** để kiểm). Case báo "Cần xem lại" hoặc "Test case đã sửa": đọc lại test case gốc (`truy-vet.py tra`), giữ/đổi/bỏ, sửa thẳng bảng trong file, rồi `chot -m "…"`. Chốt smoke **sau** khi đã chốt truy vết của tính năng đó. (`truy-vet.py kiem/chot` của tính năng sẽ nhắc chạy lệnh này nếu smoke có dùng tính năng đó.)

## Mỗi khi đổi build

- Chạy lại `liet-ke-tc.py`: **⚠️ đã hết** (hệ thống đã sửa) thì cân nhắc đưa case lại và bỏ ngoại lệ "Đạt kèm lỗi đã biết"; **lệch mới** ở case smoke thì ghi vào "Vì sao chọn" và hỏi người dùng cách xử lý.
- Lượt chạy đầu của smoke (hoặc của build mới) là lượt hiệu chuẩn nếu test case chưa chạy thật: kiểm lại test case khi Không đạt.

## Giới hạn của truy vết (nói với người dùng khi cần)

- Chỉ bắt thay đổi được ghi trong SRS/bảng soát (băm theo mã). Hệ thống đổi hành vi mà SRS chưa cập nhật, hoặc test case không có mã requirement ở cột Nguồn (vd chỉ "Suy luận"), thì không bắt được (`kiem` có dòng lưu ý cho case sau).
- Không tự chạy: phải có người/skill chạy `kiem`.

## Bộ test case do người dùng đưa vào (ngoài định dạng repo)

Không có link tới dòng, không có truy vết tự động. Cột Mã case gốc ghi `Ngoài repo: <tên file/sheet> · <mã của người dùng>`; vẫn áp dụng đủ quy tắc chọn/loại (đọc kết quả mong đợi để tự gắn cờ: nhập sai nhiều lần, ⚠️ nếu họ ghi, tác dụng phụ). Hỏi người dùng có muốn đưa bộ này vào định dạng repo (skill `tao-checklist-test-case`) để có truy vết không. `kiem` chỉ in lưu ý cho các dòng này.

## Trả lời người dùng

File dài lưu trong repo; chat chỉ **tóm tắt + link** (bảng case ngắn, tổng thời gian ước lượng, hành trình then chốt chưa phủ, case/ý cần người dùng chốt, vài dòng case đã xem xét rồi loại kèm lý do; danh sách loại **không ghi vào file**, vì suy ra được từ cờ). Không dán cả file. Dự án đã có `testing/<dự-án>/test-plan.md` thì cuối câu trả lời nhắc người dùng nói "Cập nhật test plan" để test plan có số liệu mới (test plan lập ở bước 2, trước khi có bộ này). Commit chỉ khi người dùng nhờ.

## Đọc gì cho từng việc

| Việc | Đọc |
|---|---|
| Chọn/loại case | kết quả `liet-ke-tc.py`; `memories/pitfalls/dont-trigger-lockouts.md` nếu có case nhập sai |
| Hiểu một case | `truy-vet.py tra` (không mở cả `test-case.md`) |
| Chạy smoke trên hệ thống | `references/chay-smoke.md`; `kiem` in "Lượt chạy gần nhất" nên không cần đọc cả `smoke-test.md` |
| Dự án chưa có truy vết | `memories/project/truy-vet-requirement.md` |
| Khuôn | `assets/` |
