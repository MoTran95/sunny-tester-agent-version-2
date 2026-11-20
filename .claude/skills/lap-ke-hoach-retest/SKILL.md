---
name: lap-ke-hoach-retest
description: Lập kế hoạch và chạy re-test bug đã sửa, ghi lịch sử re-test và trạng thái Đóng/Mở lại vào bug, tổng hợp nhiều bug. Dùng khi nghe "test lại bug 01", "verify bug", "build đã sửa rồi test lại", "đóng bug được chưa", "ghi lại lần re-test", "tổng hợp re-test". Không dùng để viết bug mới hay chọn regression cho cả đợt.
---

# Lập kế hoạch và chạy re-test bug đã sửa

**Re-test trả lời:** bug này đã sửa thật chưa? Làm lại **đúng bước và dữ liệu cũ** trước, rồi mới thử vài biến thể gần bug. Regression cả đợt là việc của `de-xuat-regression`. Tiếng Việt với người dùng; chỉ lỗi chức năng.

## Đầu vào
- Bug ở `testing/<slug>/<tính-năng>/bug/BUG-nnn.md` (đọc `.du-an-hien-tai` trước). "Bug 01" = `BUG-001`; mã mơ hồ thì hỏi. Chỉ đọc file bug được nhắc.
- **Bug từ công cụ khác (Jira…):** người dùng dán nội dung. Thiếu mục **Phạm vi ảnh hưởng** thì **hỏi** người dùng chỗ cần re-test, không tự lấy chỗ nào làm phạm vi. Thiếu **bước tái hiện** thì đánh dấu và hỏi (tối đa 3 câu, đủ ngữ cảnh).
- **Số build có bản sửa:** chưa có thì ghi `[chưa có số build]` và nhắc người dùng gửi.
- Chỉ dựa vào thông tin bug. Đọc thêm `memories/modules/<slug>/tu-dong-hoa.md` (địa chỉ test, trạng thái các lượt) khi định chạy.
- **Đã có file kế hoạch hoặc lịch sử re-test cho bug này** thì đọc và chạy `kiem-ke-hoach.py` kiểm lại, **không viết đè**; chỉ sửa khi bug hoặc phạm vi đổi.

## Lượt đầu khi nghe "test lại bug N" (làm theo thứ tự)
1. Đọc file bug; đọc `retest/BUG-nnn-ke-hoach.md` và mục `## Lịch sử re-test` nếu có. Chạy `tong-hop-retest.py --bug N` để biết bug đang ở bước nào (cột "Việc tiếp theo").
2. **Chưa có kế hoạch** → lập và lưu theo mục dưới. **Đã có** → chỉ kiểm lại bằng `kiem-ke-hoach.py`; sửa tại chỗ khi build, môi trường, phạm vi đổi, không viết file mới.
3. **Chưa chạy gì lên hệ thống chỉ vì nghe câu này.** Tóm tắt trong chat (build đang ghi, đã re-test mấy lần và kết quả, bước tiếp theo), rồi hỏi **một câu** có nút chọn: bản sửa đã triển khai chưa và số build là bao nhiêu; chạy luôn hay chỉ lập kế hoạch. Người dùng đã nói "chạy", nêu số build, hoặc nói rõ "chạy re-test" thì bỏ qua câu hỏi, sang mục "Khi người dùng bảo chạy".
4. Người dùng nói "chỉ lập kế hoạch / đừng ghi file / chỉ trong chat" → in bảng kế hoạch trong chat, **không tạo, không sửa file**, không đăng nhập, không chạy `run_tests.py`. Vẫn được chạy các script chỉ đọc (`kiem-ke-hoach.py` trên kế hoạch đã có, `tong-hop-retest.py`). Bug chưa có kế hoạch thì nói rõ "chưa kiểm bằng script vì chưa lưu file", đề nghị lưu khi họ muốn.
5. Báo cáo gọn: kế hoạch (link file), kết quả kiểm, câu còn hỏi. Kết quả dài để trong file, chat chỉ tóm tắt.

## Quy tắc kế hoạch
1. Mỗi bug: làm lại đúng các bước và dữ liệu cũ trước; biến thể chỉ đề xuất khi liên quan trực tiếp tới bug, **tối đa 3**.
2. **Phạm vi ảnh hưởng: re-test đủ từng chỗ**, mỗi chỗ một lượt riêng ở cột 2 và nêu ở cột 5. Còn một chỗ chưa đạt thì **chưa đóng**.
3. Chỗ bug chưa kiểm (nghi cùng nguyên nhân nhưng chưa có bằng chứng) đưa vào **biến thể**, ghi "không tính vào điều kiện đóng"; lệch thì ghi riêng.
4. Xếp theo mức độ nghiêm trọng giảm dần. Cột 5: **Đạt → Đóng**; **không đạt → Mở lại kèm số build và bằng chứng**.
5. Bằng chứng: ảnh từng chỗ trong phạm vi, số build, địa chỉ đã test (không ghi mật khẩu ở đâu cả).
6. Sau bảng: gợi ý vùng regression (luồng liên quan, bug cùng nhóm nguyên nhân, case đang ghi "Đạt kèm lỗi đã biết" vì bug này, cần đổi khi đóng).

## Chỗ lưu và vòng đời kế hoạch (để không rối)
- **Một bug một file duy nhất** `retest/BUG-nnn-ke-hoach.md`, luôn sửa tại chỗ; không tạo bản `-2`, `-cu`. Kế hoạch nói **cần làm gì**; mục `## Lịch sử re-test` trong file bug nói **đã làm gì ở mỗi lần** (một nguồn, không chép hai nơi).
- **Không đưa từng kế hoạch lên trang tổng** (`index.html`): trang đó đã có thẻ bug của từng tính năng, thêm sẽ dài ra theo số bug. Không sinh HTML cho kế hoạch (nó là file làm việc, không phải tài liệu giao người khác).
- **Theo dõi bằng `tong-hop-retest.py`** (in ra màn hình, không tạo file nên không bao giờ cũ): bảng mọi bug, cột "Kế hoạch" = đang theo dõi, cột "Việc tiếp theo" gợi ý bước kế.
- **Khi người dùng chốt Đóng:** sau khi chạy `can-cap-nhat-khi-dong.py` và cập nhật xong, **hỏi rồi xóa** file kế hoạch (nội dung đã nằm trong lịch sử re-test của bug). Nếu file chưa commit thì nói rõ xóa là không lấy lại được. Script `retest-bug-nnn.py` thì hỏi giữ hay xóa (giữ nếu muốn dùng lại làm case regression). Nhờ vậy thư mục `retest/` chỉ còn bug đang theo dõi.

## Lưu và kiểm kế hoạch (bắt buộc, trừ khi người dùng bảo chỉ lập trong chat)
Lưu mỗi bug một file `testing/<slug>/<tính-năng>/retest/BUG-nnn-ke-hoach.md` (đặt ngoài thư mục `bug/` để không bị kiểm khuôn bug): có dòng `Build có bản sửa: …`, bảng 5 cột đúng một dòng bug, mục "Gợi ý vùng cần regression". Rồi chạy:

`python -X utf8 .claude/skills/lap-ke-hoach-retest/scripts/kiem-ke-hoach.py testing/<slug>/<tính-năng>/retest/BUG-nnn-ke-hoach.md`

(Chạy script kiểm được cả khi chỉ lập kế hoạch trong chat; script chỉ đọc.) Script báo ĐẠT/KHÔNG ĐẠT: mọi chỗ trong Phạm vi ảnh hưởng có trong cột 2 và cột 5, biến thể ≤ 3, đủ 5 cột, có Đóng/Mở lại, có dòng build. **Nếu đã có script re-test `<tính-năng>/auto/retest-bug-nnn.py`, script kiểm cũng bắt thiếu chỗ nào trong phạm vi và chỗ mẫu `"<…>"` chưa điền** (kế hoạch, script và bug không lệch nhau). Không đạt thì sửa rồi chạy lại. Chỉ đọc, không sửa file.

## Khi người dùng bảo chạy re-test
Theo `chay-test-tu-dong` (`.claude/skills/chay-test-tu-dong/references/quy-tac-da-chot.md`):
0. **Bug đã re-test Không đạt ở cùng số build** (xem mục Lịch sử re-test của bug): hỏi người dùng số build mới / đã triển khai chưa **trước khi** chạy lượt tiếp, vì chạy lại cùng bản không cho kết quả mới.
1. Địa chỉ do người dùng nêu, có nhãn môi trường thử. Chạy kèm `--bug-build <build lúc tạo bug>`: runner in số phiên bản đang chạy (cần khai `health_api` trong `auto-config.json`) và cảnh báo nếu GIỐNG bản lỗi. Giống thì nói rõ: **không phân biệt được bản sửa bằng số build**, hỏi người dùng đã triển khai chưa; kết luận Không đạt lúc đó chưa đủ căn cứ để nói bản sửa sai.
2. **Script re-test một lệnh cho mỗi bug** (`<tính-năng>/auto/retest-bug-nnn.py`, tên không bắt đầu bằng `tc-` nên `--feature` không chạy kèm): ý chính = các chỗ trong Phạm vi ảnh hưởng, ý phụ = biến thể (lỗi script ở biến thể được ghi "chưa kiểm được", không im lặng). **Bug kiểu "chữ không được xuất hiện"**: sao chép `assets/mau-retest-bug.py` và chỉ điền phần `ĐIỀN` (tài khoản, chữ cấm, chữ phải có, biến thể). Bug kiểu khác: viết `run` theo `chay-test-tu-dong/assets/mau-ca-tu-dong.py`. Viết một lần, build mới chạy lại 0 token. Bước làm có thể chặn hệ thống thì làm tay.
3. **Phiên đăng nhập chỉ sống ~10 phút:** chạy ngay hai lệnh liền nhau: `python -X utf8 scripts/auto_login.py <các tài khoản> --headless` rồi `python -X utf8 scripts/run_tests.py --case-id <tính-năng>/retest-bug-nnn --bug-build X`. Mỗi tài khoản đăng nhập đúng một lần, không nhập sai, không gõ mật khẩu. Chỉ đọc phần kết luận (`| tail -35`).
4. Báo từng chỗ: Đạt/Không đạt kèm nguyên văn thấy được và đường dẫn ảnh. Một chỗ không đạt thì kết luận Mở lại.
5. **Ghi lịch sử re-test vào chính file bug bằng script, không gõ tay:** `python -X utf8 .claude/skills/lap-ke-hoach-retest/scripts/ghi-lich-su-retest.py <file bug> --ket-qua <result-*.json> --phien-ban <số> [--ghi-chu "…"]` in bản xem trước; xem đúng rồi thêm `--ghi` (tạo mục `## Lịch sử re-test` nếu chưa có, tự đánh số Lần N, nhiều file kết quả gộp một lần). Script tự kết luận: ý chính nào sai → đề nghị Mở lại; ca Không kết luận → không đề nghị gì; số phiên bản giống bản lúc tạo bug → ghi câu cảnh báo. Rồi `python -X utf8 scripts/build_docs.py --all` và `kiem-tra-bug.py --du-an`. Không ghi lượt vào bảng kết quả tính năng (bảng đó tính cả bộ test case).
5b. **Cập nhật trạng thái bug (người dùng chốt, không tự đổi):** sau khi báo kết quả, đề nghị: mọi chỗ Đạt → **Đóng**; còn chỗ Không đạt → **Mở lại**; script chưa kết luận được → không đề nghị. Người dùng đồng ý thì chạy `python -X utf8 .claude/skills/lap-ke-hoach-retest/scripts/dat-trang-thai-bug.py <file bug> --trang-thai "Đóng"|"Mở lại" --build <số build> [--ghi-chu "…"]` (in xem trước), đúng rồi thêm `--ghi`, rồi `build_docs.py --all`: mục `## Trạng thái` vào file bug, **cột Trạng thái ở mục 5 của test summary, dòng đếm trạng thái ở mục 2 và huy hiệu ở trang bug tự cập nhật**. Các trạng thái: `Mở` (bug mới), `Chờ re-test` (Dev báo đã sửa, chưa test), `Mở lại`, `Đóng`. Bug chưa ai chốt hiện "Chưa ghi". Công cụ của team vẫn là bản chính thức: nhắc người dùng ghi ở đó.
6. Ghi một dòng kết quả vào `memories/modules/<slug>/tu-dong-hoa.md` (ngày, build, chỗ đạt/không đạt).

## Nhiều bug cùng lúc
`python -X utf8 .claude/skills/lap-ke-hoach-retest/scripts/tong-hop-retest.py [--bug 001 004]` in bảng mọi bug của dự án: mức độ nghiêm trọng giảm dần, lần re-test gần nhất (Đạt/Không đạt/Chưa re-test), trạng thái đã chốt (Chưa ghi / Mở / Chờ re-test / Mở lại / Đóng), đã có kế hoạch và script chưa, việc tiếp theo (gợi ý). Bug chưa sửa vẫn nằm trong bảng, nên chọn bug đã sửa bằng `--bug`. Mỗi bug một file kế hoạch; thứ tự re-test theo bảng này.

## Khi người dùng chốt bug ĐÓNG
Chạy `python -X utf8 .claude/skills/lap-ke-hoach-retest/scripts/can-cap-nhat-khi-dong.py testing/<slug>/<tính-năng>/bug/BUG-nnn.md`: liệt kê mọi dòng trong tài liệu dự án còn nhắc bug đó, kèm gợi ý (ca "Đạt kèm lỗi đã biết" ở smoke/regression/test case → đổi lại Đạt; ca **Bị chặn** vì bug này → **chạy lại**; trạng thái Không đạt → kiểm lại). Đọc kết quả cùng người dùng, **việc đổi trạng thái do người dùng chốt**; sửa md nguồn rồi `build_docs.py --all` và `kiem-tra-bo-nho.py`. Ghi trạng thái **Đóng** vào file bug bằng `dat-trang-thai-bug.py` (bước 5b ở trên) để test summary hiện đúng, và nhắc người dùng ghi ở công cụ của team. Gợi ý chỉ là gợi ý (dòng nhắc nhiều bug có thể bị gắn nhầm). Cuối cùng xử lý file kế hoạch và script re-test theo mục "Chỗ lưu và vòng đời kế hoạch".
