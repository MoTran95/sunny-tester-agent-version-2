# Hướng dẫn cho người mới: test một dự án cùng Claude

Trang này để bạn xem lại khi quên. Bạn không cần nhớ tên skill hay lệnh nào: chỉ cần **nói việc muốn làm bằng tiếng Việt** trong app Claude, Claude tự chọn đúng cách làm.

## Lời chào trong chat

*(Trợ lý gửi đoạn này khi bạn mở repo lần đầu trên một máy mới; chọn xong dự án thì gửi tiếp link trang tổng của dự án.)*

> **Chào bạn, mình là trợ lý Sunny Testing, mình sẽ cùng bạn test dự án trong repo này.**
>
> Cách dùng rất đơn giản: bạn nói việc cần làm bằng tiếng Việt, mỗi lần một việc, ví dụ "Phân tích requirement file này", "Viết test case cho tính năng Đăng nhập", "Chạy smoke trên <địa chỉ staging>, build 1.2.3". Mình làm, lưu kết quả vào repo, rồi gửi bạn **một link trang tổng** để xem.
>
> Thứ tự thường đi: phân tích requirement và hỏi BA → lập test plan → viết test case → chọn bộ smoke, regression → chạy test (ca nào không đạt mình tạo bug luôn, kèm ảnh chụp và video) → re-test → báo cáo tổng kết.
>
> Có vài việc **bạn tự làm**: gõ mật khẩu vào file `.env` (không gửi qua chat), cho mình địa chỉ môi trường thử, duyệt danh sách tình huống trước khi mình viết test case, chốt đóng hay mở lại bug, và quyết định nhận build. Bug mình lưu trong repo; bạn nhờ thì mình tạo thêm trên Jira. Chỗ nào chưa rõ mình sẽ hỏi, không tự đoán.
>
> **Đọc trước trang hướng dẫn cho người mới:** `docs/bat-dau.html` (khoảng 5 phút: thứ tự công việc, câu nói mẫu, việc bạn tự làm).
>
> Khi bạn chọn xong dự án, mình gửi link **trang tổng** của dự án. Từ đó bạn chỉ cần mở một trang đó để xem mọi thứ, kể cả hướng dẫn (mục **Hướng dẫn và quy ước chung**).
>
> Trước tiên, cho mình biết bạn đang test dự án nào nhé.

## 1. Chuẩn bị (làm một lần)

| Việc | Làm thế nào |
|---|---|
| Cài máy | Làm theo trang **Cài đặt repo trên máy mới** (Windows hoặc Mac, khoảng 15 phút). Xong thì chạy `python -X utf8 scripts/kiem-tra-may-moi.py`, đạt khi báo "0 mục THIẾU" |
| Ghi tên bạn | Tạo file `.nguoi-test` ở gốc repo, một dòng là tên bạn. Tên này ghi vào cột Người viết và người chạy test |
| Mở repo | Mở thư mục repo trong app Claude (desktop, tab Code) |
| Chọn dự án | Lần đầu Claude hỏi bạn test dự án nào. Dự án chưa có thì chọn "dự án mới", Claude tạo đủ thư mục. Muốn đổi dự án thì nói tên dự án khác |
| Tài khoản test | **Chỉ cần khi chạy test tự động.** Chép `.env.example` thành `.env` rồi tự điền tài khoản, mật khẩu. Không gửi mật khẩu qua chat |

## 2. SRS và phân tích requirement là gì

**SRS** (Software Requirements Specification, tài liệu đặc tả yêu cầu) là tài liệu ghi **hệ thống phải làm gì**, viết theo một khuôn chung: mỗi tình huống một dòng, có **mã cố định** (ví dụ `CART-S01-AC02`: tính năng giỏ hàng, câu chuyện người dùng số 1, tình huống số 2) và **bằng chứng** (ảnh chụp màn hình, hoặc đoạn trích từ tài liệu gốc).

**Vì sao phải tạo SRS:**
- **Test case có căn cứ.** Mỗi test case ghi rõ dựa vào dòng SRS nào, nên ai đọc cũng biết kết quả mong đợi lấy từ đâu, không phải "theo cảm giác".
- **Requirement đổi thì biết ngay phải sửa gì.** Nhờ mã cố định, Claude so được bản cũ và bản mới, báo đúng test case, bộ smoke, bộ regression bị ảnh hưởng thay vì soát lại từ đầu.
- **Một nguồn chung cho cả team.** Yêu cầu nằm rải rác ở Word, ticket, tin nhắn, hoặc hệ thống chưa có tài liệu, đều được gom về một chỗ đọc là hiểu.

**Có SRS bằng ba cách:** đã có tài liệu theo khuôn thì dùng luôn; có tài liệu dạng văn bản chưa có mã thì nhờ "Chuyển tài liệu yêu cầu này thành SRS"; chưa có tài liệu nào thì nhờ Claude khám phá hệ thống rồi viết SRS từ những gì thấy được.

**Phân tích requirement** là đọc kỹ SRS (hoặc tài liệu yêu cầu) **trước khi viết test** để tìm chỗ thiếu, mơ hồ, mâu thuẫn, số liệu sai. Kết quả là **bảng phân tích requirement** (dòng nào đã rõ, dòng nào cần hỏi) và **file câu hỏi cho BA**. Hỏi xong mới viết test case, để test case không dựa trên điều đoán.

## 3. Thứ tự công việc và câu nói mẫu

| Bước | Việc | Nói với Claude | Bạn cần làm |
|---|---|---|---|
| 1 | Hiểu requirement | Có tài liệu: "Phân tích requirement file <đường dẫn>". Tài liệu chỉ là văn bản, chưa có mã: "Chuyển tài liệu yêu cầu này thành SRS". Chưa có tài liệu: "Khám phá tính năng X trên <địa chỉ staging> rồi viết SRS" | Gửi câu hỏi Claude soạn cho BA; BA trả lời thì dán lại: "Ghi câu trả lời BA cho tính năng X. A1: …" |
| 2 | Lập test plan | "Lập test plan cho build 1.2.3". Sau bước 4: "Cập nhật test plan" để điền số test case, smoke, regression | Điền phiếu: ngưỡng tiêu chí, tên người, ngày (Claude không tự đặt) |
| 3 | Viết test case | "Viết test case cho tính năng X" | Duyệt danh sách tình huống Claude in trong chat (gật hoặc sửa) |
| 4 | Chọn bộ smoke, regression | "Đề xuất bộ smoke test", "Đề xuất regression cho release note này: …" | Chốt các case Claude hỏi |
| 5 | Chạy test | "Chạy smoke trên <địa chỉ staging>, build 1.2.3", "Chạy regression Tầng 1" | Cho địa chỉ môi trường thử (có chữ staging, dev, test…) và số build |
| 6 | Bug | Ca **không đạt** khi chạy: Claude **tạo bug luôn**, kèm ảnh chụp lỗi (tô đỏ chỗ sai) và video. Lỗi bạn tự thấy: dán ghi chú "Viết bug: …". Muốn có trên Jira: "Tạo bug 01 trên Jira" | Đọc lại các dòng có nhãn **Giả định** |
| 7 | Re-test | "Build 1.2.4 đã sửa bug 01, test lại" | Chốt **Đóng** hay **Mở lại** |
| 8 | Báo cáo tổng kết | "Tạo test summary report cho build 1.2.3" | Người duyệt chọn Nhận / Không nhận / Nhận có điều kiện ngay trên trang |

**Vì sao test plan đứng thứ 2:** test plan trả lời "sẽ test gì, test thế nào, khi nào xong, rủi ro gì", nên lập ngay sau khi hiểu requirement để định hướng việc viết test case. Lúc đó số test case, smoke, regression còn ghi "Chưa có"; làm xong bước 4 thì nhờ cập nhật để điền số, phần bạn đã điền được giữ nguyên.

Mỗi build mới, nên chạy theo thứ tự: smoke → (nếu đạt) regression Tầng 1 và vùng bị ảnh hưởng → test case của tính năng mới.

**Requirement đổi:** nói "Requirement tính năng X đổi mục …, cập nhật test case, smoke, regression". Claude tìm đúng test case bị ảnh hưởng, không phải làm lại từ đầu.

**Bug lọt ra production:** nói "Bug lọt production, viết case chặn bug này quay lại". Claude đề xuất case mới và chỗ đặt trong bộ regression để bạn duyệt.

## 4. Xem kết quả ở đâu

Chỉ cần mở **một file**: trang tổng `testing/<tên-dự-án>/index.html`. Trang này có link tới mọi thứ của dự án: tài liệu requirement, test case, kết quả từng lượt chạy (ảnh, video ca lỗi), bug, bộ smoke, regression, test plan, báo cáo tổng kết. Mỗi lần làm xong, Claude gửi một link tới đúng phần của trang này.

Trang HTML đều tự sinh từ file `.md`. Muốn sửa nội dung thì nhờ Claude, hoặc sửa file `.md`, không sửa trang HTML.

## 5. Claude sẽ làm và sẽ không làm gì

| Claude làm | Claude không làm |
|---|---|
| Hỏi lại khi requirement chưa rõ (tối đa 3 câu một lần, có lựa chọn kèm đề xuất) | Tự bịa quy tắc nghiệp vụ, con số, kết quả mong đợi |
| Ghi nhãn "Giả định" hoặc "Suy luận" ở chỗ tự thêm | Gõ, đọc ra hay ghi mật khẩu vào tài liệu |
| Chạy test trên địa chỉ bạn nêu, có nhãn môi trường thử | Chạy trên môi trường thật, làm khóa tài khoản, đổi dữ liệu của người khác |
| Tạo bug ngay khi ca test không đạt, kèm ảnh chụp và video | Tạo bug khi ca chỉ "không kết luận được" (script lỗi, phiên hết hạn…): khi đó Claude báo lý do |
| Dừng chờ bạn duyệt ở các bước cần bạn quyết | Tự đóng bug, tự quyết nhận build, tạo bug trên Jira khi bạn chưa nhờ |
| Chỉ test chức năng | Tự thêm ca bảo mật, hiệu năng khi không được yêu cầu |
| Lưu mọi kết quả vào repo | Commit, push khi bạn chưa nhờ |

Số lần nhập sai cho phép, thời gian bị chặn và các ngưỡng an toàn khác lấy từ requirement hoặc do bạn cung cấp. Claude không tự đặt.

## 6. Mẹo để dùng cho đúng

- **Mỗi lần một việc.** Xong việc này rồi mới nhờ việc tiếp theo; Claude sẽ gợi ý bước kế.
- **Trả lời câu hỏi của Claude cho rõ.** Claude hỏi vì thiếu thông tin thật, không phải để hỏi cho có. Chưa biết thì nói "chưa biết", Claude sẽ ghi là câu hỏi còn mở.
- **Đã khám phá rồi thì không khám phá lại.** Muốn khám phá lại, nói rõ "tính năng X đã đổi phần …".
- **Một dự án không dùng thông tin của dự án khác.** Đổi dự án thì nói rõ tên dự án.
- **Muốn lưu lại thì nhờ commit:** "Commit giúp mình".
- **Quên cách dùng:** mở lại trang này từ trang tổng, mục Hướng dẫn và quy ước chung.
