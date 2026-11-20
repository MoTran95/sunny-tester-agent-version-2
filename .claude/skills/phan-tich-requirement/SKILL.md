---
name: phan-tich-requirement
description: Phân tích requirement (SRS, tài liệu, ticket) trước khi viết test — tìm chỗ thiếu, mơ hồ, mâu thuẫn, số liệu sai; lập bảng phân tích requirement có trích nguyên văn và file câu hỏi cho BA, rồi dừng chờ BA; ghi câu trả lời BA khi có. Dùng khi nghe "phân tích requirement", "soát requirement", "câu hỏi cho BA", "ghi câu trả lời BA". Không dùng để khám phá website, viết SRS, test case hay bug.
---

# Phân tích requirement: bảng soát và câu hỏi cho BA

Làm **một việc**: đọc requirement trước khi viết test, tìm mọi chỗ chưa đủ căn cứ để biết kết quả đúng, rồi biến thành (1) **bảng soát** để tester tự kiểm tra và (2) **file câu hỏi** để mang đi hỏi BA. Xong thì **dừng**, chờ BA trả lời. Checklist và test case là việc của skill khác, sau khi BA trả lời.

**Cách gọi với người dùng (dặn 2026-11-19):** gọi việc này là **phân tích requirement** (không nói "soát"), file `bang-soat-requirement.md` gọi là **bảng phân tích requirement** (tên file giữ nguyên vì script đọc theo). Ngôn ngữ: **tiếng Việt**. Nền: cách làm "Tách, Xoay, Lọc" trong sách *Nền Tảng Tester Thời AI* (Phần 1) cộng các bài học từ những lần làm thật với người dùng (ghi ở `references/`). Khuôn: `assets/`.

## Quy tắc không được phá (và vì sao)

1. **Chưa có trong requirement thì chưa phải sự thật.** Quy tắc nghiệp vụ, con số, quy định ngành hay luật mà nguồn không nêu chỉ là **câu hỏi**, không phải quy tắc. *Vì AI hay tự điền chỗ bỏ ngỏ và trông rất chuyên nghiệp.*
1b. **Requirement ghi rõ thì suy luận tiếp; ghi chưa rõ thì hỏi.** Điểm xuất phát phải là điều requirement đã ghi rõ hoặc BA đã trả lời (`TL-xx`). Từ đó suy ra hệ quả đi theo tự nhiên thì ghi ✅ "suy ra từ <mã hoặc TL>" kèm một câu lý do, **không hỏi**. Lý do của tính năng (kể cả lý do bảo mật) được dùng để suy ra, nhưng không tự đặt thêm ca test bảo mật. Chỗ requirement **chưa ghi hoặc ghi chưa rõ** (con số requirement không ghi như thời gian giữ phiên, cách hiển thị requirement không tả…) thì **không lấp bằng kinh nghiệm hay thông lệ**, mà hỏi. Hệ thống làm khác điều suy ra → ghi "nghi lỗi, cần kiểm" kèm bằng chứng, không hỏi "quy tắc là gì". Khi SRS là bản nháp viết từ việc xem hệ thống, chữ "chưa rõ" trong đó có thể chỉ là chỗ chưa khám phá: xét mục đích đã ghi rõ trước khi coi là mơ hồ. *Lần soát lại tính năng đăng nhập đầu tiên mình hỏi BA "bị chặn thì chặn tài khoản đó hay tài khoản khác", "mật khẩu có cắt khoảng trắng không", "dòng gợi ý có giữ không": người dùng chê "vô tri" vì requirement đã rõ, suy luận là ra. Câu đếm số lần sai cũng suy ra được: "N lần sai liên tiếp thì bị chặn" → lần sai thứ N bị chặn, "liên tiếp" → đăng nhập đúng đếm lại, không nói thời gian → chỉ đếm số lần; mình hỏi vì để hệ thống (chặn ở lần N+1) dẫn đường thay vì đi theo câu chữ. Phần độ dài mã cũng suy ra được từ lý do bảo mật: màn hình đăng nhập chỉ báo đúng hoặc sai, không kiểm định dạng hay độ dài, nên không cần test độ dài ở đây.*
2. **Giữ mã requirement sẵn có** (`<MÃ>-S01-AC01`…). **Chưa có SRS thì tự tạo SRS trước, không hỏi** (người dùng chốt 2026-11-20: skill viết cho người khác dùng, họ không biết phải chọn SRS hay mã tạm), rồi mới phân tích trên chính SRS đó, cùng lượt:
   - Đầu vào là **tài liệu yêu cầu** (Word, PDF, ticket, đoạn dán): làm theo `srs-from-website` mục "Chỉ có tài liệu yêu cầu" (không mở trình duyệt, chép đúng câu chữ, nhãn `theo tài liệu`).
   - Đầu vào là **nhật ký/báo cáo khám phá** đã có: làm theo `srs-from-website` bước 2 nhánh "Đã có và đủ" (viết SRS từ nhật ký và ảnh sẵn có, không khám phá lại). SRS này ghi **hành vi quan sát**, chưa phải yêu cầu: khi phân tích, mọi điểm chỉ dựa vào quan sát mà chưa có tài liệu hay BA xác nhận là câu hỏi "đây có phải yêu cầu không", không coi là quy tắc.
   - Báo người dùng một câu: đã tạo SRS (link) để có mã cố định cho test case và truy vết. Chỉ dùng mã tạm R1, R2… khi người dùng **nói rõ** không muốn SRS (khi đó không có truy vết tự động). *Để truy vết về sau; người mới không phải hiểu khác biệt SRS và mã tạm.*
3. **Trích nguyên văn thì chép đúng từng ký tự, rồi để script kiểm.** Không viết lại câu trong dấu trích.
4. **Tính lại mọi con số và công thức** trong requirement bằng một script nhỏ. *Lần làm thật đầu tiên bắt được 2 chỗ tài liệu tự lệch (một ca ghi "đúng bằng ngưỡng" thật ra vượt ngưỡng một chút; một kết quả tính sai) mà đọc bằng mắt không thấy.*
5. **Chỉ xét chức năng (functional).** Không tự suy diễn bảo mật, hiệu năng, trừ khi requirement nói tới.
6. **Câu hỏi phải đọc là hiểu**: kể tình huống thật có số, rồi hỏi, rồi nói mình đang hiểu thế nào. Một từ cho một khái niệm. Không để mã nội bộ (CH-02, M01) làm nội dung chính. Xem `references/viet-cau-hoi-de-doc.md`. *Bản đầu bị chê "không hiểu đang nói gì", rồi "máy móc như dịch từ tiếng Anh".*
7. **Không tự trả lời thay BA.** "Mình đang hiểu" luôn nói rõ khi đó là đoán. Quyết định của người dùng (ví dụ chọn cách làm tròn) ghi là **câu trả lời có nguồn "người dùng chốt, chưa có BA xác nhận"**, không nâng thành sự thật.
8. **Ghi hết vào bảng, nhưng hỏi có chọn lọc**: ba nhóm hỏi ngay / hỏi sau / tự kiểm tra trước. *Gửi BA mười mấy câu cùng lúc thì câu quan trọng bị chìm.*
9. **Một nguồn câu chữ**: câu hỏi viết **một lần** ở file câu hỏi; bảng soát chỉ ghi số câu, tiêu đề và nhóm (cộng câu BA đã trả lời, nếu có), **không chép lại** phần Hỏi/Mình đang hiểu. Script kiểm tiêu đề khớp. *Chép lại làm bảng phình gấp rưỡi và mỗi lần sửa phải đọc lại cả bảng.*
10. **Đừng làm quá việc được giao.** Chưa được yêu cầu thì không dựng checklist, test case, ưu tiên. *Lần làm thật đầu tiên mình dựng 62 test case khi người dùng chỉ cần phân tích và hỏi BA.*
11. **Làm từng bước nhỏ, hỏi khi chưa rõ** (tối đa 3 câu khi không làm tiếp được). Từ nghe lệch thì hỏi lại nghĩa.

## Đọc gì cho từng việc
Luôn đọc: `memories/user/working-preferences.md`, `memories/project/overview.md`, và `memories/modules/<slug>/overview.md` của **dự án hiện tại** (slug trong `.du-an-hien-tai`; chưa có thì hỏi người dùng trước, xem `CLAUDE.md` bước 0). `<hệ thống>` trong các đường dẫn dưới đây chính là slug đó. **Không mở file của dự án khác, kể cả để làm mẫu**: dùng khuôn trong `assets/` (và `srs/_template.md`). Thêm theo việc:

| Việc | Đọc | Không cần đọc |
|---|---|---|
| Phân tích requirement mới | File requirement (cả file). Bộ nhớ: `memories/conventions/ba-question-wording.md`, `memories/modules/<hệ thống>/tu-ngu-cau-hoi-ba.md` và `feature-<tên>.md` nếu có. Skill: `references/quy-trinh-tach-xoay-loc.md`, `quy-tac-nguon-va-tra-loi.md`, `viet-cau-hoi-de-doc.md`, `bai-hoc.md`, hai file trong `assets/` | Bảng soát, câu hỏi của feature khác; `scripts/kiem-tra.py` (chỉ chạy, không đọc) |
| Ghi câu trả lời BA (`TL-xx`) | Bộ nhớ của feature. `references/quy-tac-nguon-va-tra-loi.md` mục 4. **Dùng `scripts/ghi-tl.py`** (mẫu `tl.json` ở đầu script); chỉ đọc các dòng bảng soát mà script in ra (`Read` với `offset`/`limit`) hoặc `scripts/truy-vet.py tra <dự-án> <tính-năng> --ma <mã>` để xem SRS + theo BA + test case của vài mã | Cả bảng soát, cả file câu hỏi, cả requirement; các file references khác; viết script Python mới để sửa bảng. Đọc thêm `viet-cau-hoi-de-doc.md` **chỉ khi** phải viết câu hỏi mới |
| Sửa câu chữ một câu hỏi | Khối câu đó trong file câu hỏi, `memories/conventions/ba-question-wording.md`, `memories/modules/<hệ thống>/tu-ngu-cau-hoi-ba.md`, `references/viet-cau-hoi-de-doc.md` | Bảng soát (chỉ sửa tiêu đề nếu tiêu đề đổi, dùng `--tim`) |
| Sửa chính skill này | `memories/project/skills.md`, file cần sửa | Sản phẩm trong `testing/` |

File trên ~30 KB mà chỉ cần một phần: tìm bằng Grep rồi đọc đoạn đó (`offset`/`limit`), đừng đọc cả file.

## Quy trình

0. **Đọc đúng những file cần cho việc này** (bảng "Đọc gì cho từng việc" ngay dưới), sau `CLAUDE.md` và `memories/MEMORY.md`. Không đọc thêm cho chắc.
1. **Chốt đầu vào** (hỏi nếu thiếu): đường dẫn requirement; hệ thống và feature; requirement đã có mã chưa (chưa có SRS thì tự tạo theo quy tắc 2, không hỏi); đã có bản phân tích trước chưa (có thì sang "Khi có câu trả lời"). Nếu `ba-question-wording.md` thiếu hoặc người dùng muốn đổi từ ngữ thì hỏi: xưng hô, từ team dùng cho các khái niệm chính, rồi cập nhật file đó.
2. **Đọc để hiểu**, rồi liệt kê mọi đơn vị cần soát (mỗi AC, quy tắc, thông báo là một đơn vị). Dùng năm câu tự hỏi và sáu dấu hiệu lấn cấn trong `references/quy-trinh-tach-xoay-loc.md`.
3. **Tính lại số liệu** bằng script nhỏ (để trong thư mục tạm, không lưu vào repo). Ghi các chỗ lệch.
4. **Soát từng đơn vị**: Tách (một ý một mã) → Xoay (qua sáu nút, chỉ nút liên quan) → Lọc. Quyết ✅ đã rõ hay ❓ cần hỏi theo `references/quy-trinh-tach-xoay-loc.md`. Chỗ rõ một nửa thì tách hai dòng.
   - **Một mã nằm trên nhiều dòng** (phần ✅ và phần ❓, hoặc nhiều câu trả lời): chỉ dòng đầu ghi đủ ô Tình huống và ô trích; từ dòng thứ hai ghi ngắn kiểu `**Phần còn chưa rõ** của dòng trên` (hoặc `**Phần theo câu trả lời của BA (TL-xx)** của dòng trên`, thêm "ý thứ hai" nếu trùng nhãn) và ô trích ghi `—`. Không chép lại y nguyên: người đọc tưởng bị lặp (người dùng đã chê 2026-11-18). `kiem-tra.py` báo LỖI nếu chép lại.
5. **Soạn file câu hỏi** `testing/<hệ thống>/<feature>/cau-hoi-cho-ba.md` theo `assets/mau-cau-hoi-cho-ba.md` và `references/viet-cau-hoi-de-doc.md`. Chia Phần A (hỏi ngay), B (hỏi sau), C (tự kiểm tra trước).
6. **Lập bảng soát** `testing/<hệ thống>/<feature>/bang-soat-requirement.md` theo `assets/mau-bang-soat.md`. Cột câu hỏi chỉ ghi `**A1. <tiêu đề>** (<nhóm>)`, tiêu đề đúng chữ như ở file câu hỏi.
7. **Kiểm bằng script**, sửa hết lỗi:
   ```bash
   python -X utf8 .claude/skills/phan-tich-requirement/scripts/kiem-tra.py \
     --nguon <file requirement> \
     --bang-soat testing/<hệ thống>/<feature>/bang-soat-requirement.md \
     --cau-hoi testing/<hệ thống>/<feature>/cau-hoi-cho-ba.md \
     --ma "<biểu thức chính quy của mã, ví dụ CART-S\d\d-AC\d\d>"
   ```
   Script báo: bảng lệch số cột, trích dẫn không khớp nguyên văn, mã requirement chưa có mặt, câu hỏi thiếu trường, bảng soát lệch với file câu hỏi, từ dịch máy và mã nội bộ lọt vào câu hỏi. Rồi soát tay: đọc to vài câu hỏi xem có nghe lạ không; mở thử file trong khung xem trước.
8. **Cập nhật bộ nhớ**: `memories/modules/<hệ thống>/feature-<tên>.md` (điều học được, bẫy, trạng thái), một dòng trong `MEMORY.md`.
9. **Trả lời người dùng** bằng tóm tắt ngắn và link file (không dán cả bảng vào chat): số dòng ✅ và ❓, các câu nhóm hỏi ngay, chỗ cần họ quyết, việc họ làm tiếp. Nói rõ **chưa gửi BA** và chưa viết checklist hay test case. Rồi dừng.

## Khi có câu trả lời (từ BA hoặc người dùng)

**Không đọc lại cả bảng soát, không viết script mới.** (1) Viết một file `tl.json` nhỏ (nội dung, câu hỏi và mã áp dụng, câu BA trả lời nguyên văn; mẫu và các trường ở đầu `scripts/ghi-tl.py`), đặt `id` rõ để chạy lại không thêm trùng. (2) Chạy `python -X utf8 scripts/ghi-tl.py --bang-soat … --cau-hoi … --nguon … --du-lieu tl.json` (thêm `--thu` để xem trước). Script tự: thêm dòng `TL-xx` vào mục "Câu trả lời đã nhận" (kèm điểm nhảy `<a id>`), chèn `**BA trả lời:**` vào mọi dòng có câu đó, điền "Câu trả lời của BA" ở file câu hỏi, tính lại số ở mục Tổng kết, thêm dòng Lịch sử, chạy `kiem-tra.py`, rồi in các dòng bảng soát còn cần sửa. (3) Chỉ **phần cần hiểu nghĩa** làm tay bằng `Edit` trên đúng các dòng script in ra (xem thêm bằng `truy-vet.py tra … --ma <mã>` nếu cần ngữ cảnh): đổi ❓ thành ✅ "theo TL-xx", ghi "khác hệ thống hiện tại", cập nhật hai số Tổng kết đếm tay (dòng suy ra, mục không mã). Mỗi câu trả lời là `TL-xx`: nội dung, **nguồn** (ai nói, ngày, ở đâu), áp dụng cho mã nào, còn lại gì. Đổi các dòng ❓ liên quan thành ✅ "theo TL-xx". Nếu hệ thống hiện tại cho kết quả khác câu trả lời, ghi "khác hệ thống hiện tại" và **không tự kết luận lỗi** (chỉ là nghi lỗi nếu BA xác nhận). Nếu câu trả lời làm đổi số hiển thị, liệt kê số nào đổi. Ở cột "Câu hỏi gửi BA" của các dòng liên quan, thêm dòng `**BA trả lời:** <nguyên văn> (TL-xx)` ngay sau tiêu đề câu hỏi (người dùng yêu cầu 2026-11-18). Hỏi **ai là người chốt**; quyết định của tester chưa có BA xác nhận thì nói rõ như vậy và đưa vào Phần A để BA xác nhận. Không sửa SRS tại chỗ khi chưa có BA hoặc team xác nhận. Chi tiết: `references/quy-tac-nguon-va-tra-loi.md`.


## Quy ước để trang HTML tự link (đã chốt; `scripts/build_docs.py` dựa vào đây)

- Mã requirement (`<TIỀN_TỐ>-S01-AC02`, `-R06`, `-M06`, `-E20`) đứng ở **ô đầu** của dòng bảng; trang HTML tự gắn neo theo số dòng md và biến mọi chỗ nhắc mã (bản ngắn `S01-AC02` cũng được) thành link tới dòng đó. Không đổi số dòng của file đã chốt mà không cần (link truy vết dạng `file.md#L66` theo số dòng).
- Câu trả lời BA: mỗi `TL-nn` ở ô đầu một dòng của bảng trong bảng soát. Câu hỏi cho BA: mỗi câu có `<a id="a1"></a>` (chữ A/B/C + số, chữ thường) ngay trước tiêu đề câu.
- Sau khi sửa file md của tài liệu này: `python -X utf8 scripts/build_docs.py --all` (trang HTML phải luôn khớp md; `kiem-tra-bo-nho.py` báo lỗi nếu còn trang cũ).

## Tệp trong skill
- `references/quy-trinh-tach-xoay-loc.md` — năm câu tự hỏi, sáu dấu hiệu, sáu nút (chỉ chức năng), cách quyết ✅/❓, ba nhóm câu hỏi, cách tính lại số liệu.
- `references/quy-tac-nguon-va-tra-loi.md` — nhãn nguồn, cách trích nguyên văn, mã requirement, ghi câu trả lời `TL-xx`, quyết định của người dùng.
- `references/viet-cau-hoi-de-doc.md` — khuôn câu hỏi, giọng văn, từ ngữ, ví dụ trước và sau, danh sách tự kiểm.
- `references/bai-hoc.md` — các bẫy đã gặp (bảng hỏng, làm quá, câu chữ máy móc…).
- `assets/mau-bang-soat.md`, `assets/mau-cau-hoi-cho-ba.md` — khuôn hai file đầu ra (nhãn trường là cố định để script đọc).
- `scripts/kiem-tra.py` — soát đầu ra.
- Bộ nhớ ngoài skill: `memories/conventions/ba-question-wording.md` (xưng hô, từ đã chốt).
