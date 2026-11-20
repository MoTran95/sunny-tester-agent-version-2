# Chỗ làm việc của tester với Claude

Repo này giúp tester làm trọn một vòng kiểm thử cùng Claude: phân tích requirement, hỏi BA, lập test plan, viết test case, chọn bộ smoke và regression, chạy test tự động bằng Playwright, viết bug, re-test, và làm báo cáo tổng kết để duyệt build. Mỗi việc là một **skill** (11 skill trong `.claude/skills/`). Bạn chỉ cần nói việc muốn làm bằng tiếng Việt, Claude tự chọn skill.

Một repo chứa **nhiều dự án** (mỗi dự án là một hệ thống đang test). Thông tin của dự án này không dùng cho dự án khác.

## Bắt đầu trong 3 bước

1. **Cài máy** theo [docs/cai-dat-may-moi.md](docs/cai-dat-may-moi.md) (Windows hoặc Mac, khoảng 15 phút), rồi kiểm:
   ```powershell
   python -X utf8 scripts/kiem-tra-may-moi.py
   ```
2. **Ghi tên của bạn** vào file `.nguoi-test` ở gốc repo (một dòng; chỉ nằm trên máy bạn, không đưa lên Git). Tên này ghi vào cột Người viết và người chạy test.
   Tài khoản test (file `.env`) **chỉ cần khi chạy test tự động**: lần đầu vào dự án Claude hỏi địa chỉ, tên đăng nhập, mật khẩu trong chat rồi tự tạo `.env` (hoặc nói "để sau"; muốn gõ mật khẩu ẩn thì nói "gõ ở terminal"). Chỉ dùng tài khoản test, vì chat được lưu trong lịch sử phiên. Phân tích requirement, viết test case, bug, test plan không cần.
3. **Mở repo trong app Claude** (desktop, tab Code) và gõ việc cần làm. Lần đầu Claude hỏi bạn đang làm dự án nào, hoặc tạo dự án mới.

## Dùng thế nào

Người mới đọc [docs/bat-dau.md](docs/bat-dau.md) (cũng có trên trang tổng của dự án, mục Hướng dẫn và quy ước chung): thứ tự công việc, câu nói mẫu, việc bạn tự làm, chỗ xem kết quả. Vài câu mẫu:

| Muốn | Nói với Claude |
|---|---|
| Phân tích requirement, soạn câu hỏi BA | "Phân tích requirement file <đường dẫn>" |
| Viết test case | "Viết test case cho tính năng X" |
| Bộ smoke | "Đề xuất bộ smoke test" |
| Chạy test | "Chạy smoke trên <địa chỉ staging>, build 1.2.3" |
| Viết bug | "TC-005 tính năng X không đạt, tạo bug" |
| Báo cáo tổng kết | "Tạo test summary report cho build 1.2.3" |

## Thư mục

| Thư mục | Chứa |
|---|---|
| `srs/<dự-án>/` | SRS: tài liệu ghi hệ thống phải làm gì, mỗi tình huống một mã cố định, để test case có căn cứ và biết test case nào phải sửa khi requirement đổi (giải thích ở `docs/bat-dau.md` mục 2) |
| `testing/<dự-án>/` | Bảng phân tích requirement, câu hỏi BA, test case, smoke, regression, test plan, kết quả, bug, báo cáo tổng kết. Trang tổng: `testing/<dự-án>/index.html` |
| `evidence/<dự-án>/` | Nhật ký khám phá, ảnh, video |
| `docs/` | Hướng dẫn cho người dùng |
| `scripts/` | Công cụ dùng chung (chạy test, sinh trang HTML, truy vết, kiểm tra) |
| `.claude/skills/` | 11 skill |
| `memories/` | Ghi chú cho Claude (người không cần đọc) |

Trang HTML đều sinh tự động từ file `.md`; muốn sửa thì sửa file `.md` (hoặc nhờ Claude), không sửa trang HTML.

## Đem bộ này sang dự án khác hoặc đưa người khác

Repo này có dữ liệu dự án trong lịch sử Git, nên đừng đưa thẳng repo. Xuất **bộ lõi** (quy trình, quy tắc, skill, script, khuôn, hướng dẫn; không có dữ liệu dự án nào và không có thông tin cá nhân) ra một thư mục riêng:

```powershell
python -X utf8 scripts/xuat-bo-loi.py D:/AI/sunny-tester-kit
```

Script tự soát và báo nếu còn sót thông tin dự án hoặc cá nhân. Thư mục đích thành một repo Git mới (chưa commit). Sau khi cải tiến skill ở repo này, chạy lại lệnh trên để cập nhật bộ lõi; dự án mà người dùng bộ lõi tự tạo trong đó được giữ nguyên.

## Quy tắc an toàn

- Claude chỉ chạy test trên địa chỉ bạn nêu và có nhãn môi trường thử (staging, test…).
- Mật khẩu chỉ nằm trong `.env` (Claude tạo file từ thông tin bạn đưa); Claude không gõ vào form đăng nhập, không đọc ra, không ghi vào tài liệu.
- Không làm khóa tài khoản, không đổi dữ liệu người khác; số lần nhập sai cho phép lấy từ requirement hoặc do bạn cung cấp.
- Claude không bịa: điều requirement không nói thì thành câu hỏi, chỗ tự thêm có nhãn "Giả định".
- Commit và push chỉ khi bạn nhờ.
