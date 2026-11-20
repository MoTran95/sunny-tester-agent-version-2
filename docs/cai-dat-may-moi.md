# Cài đặt repo trên máy mới (Windows hoặc Mac)

Mục tiêu: lần đầu mở repo trên máy khác, Claude bắt tay làm việc ngay, không mất thời gian dò lỗi cài đặt hay chờ bạn bấm cho phép từng lệnh. Làm một lần, khoảng 10–15 phút.

Lệnh trong tài liệu này viết cho cả hai hệ điều hành. Chỗ khác nhau được ghi riêng **Windows (PowerShell)** và **Mac (Terminal)**. Trên Mac, lệnh `python` thường là `python3`; mọi chỗ trong repo viết `python` thì Mac gõ `python3`.

## 1. Cài phần mềm (một lần cho mỗi máy)
| Cần | Để làm gì | Windows | Mac |
|---|---|---|---|
| Git | Lấy repo, commit, push | git-scm.com → Git for Windows | gõ `git --version` trong Terminal, máy tự đề nghị cài công cụ dòng lệnh |
| Python 3.10 trở lên | Chạy các script | python.org (tick "Add python.exe to PATH") hoặc Microsoft Store | python.org hoặc `brew install python` |
| Chrome hoặc Edge | Playwright dùng lại trình duyệt có sẵn, không tải thêm | thường đã có | cài Google Chrome |
| App Claude (desktop) | Làm việc với Claude | claude.ai/download | claude.ai/download |

Pillow, fonttools, brotli (build báo cáo, cắt font), Playwright (chạy test tự động) và MarkItDown (đọc Word/PDF thành Markdown) cài **một lần bằng một lệnh** ở mục 3, vào thư mục `.venv` trong repo (không commit, không đụng Python hệ thống).

Windows: gõ `python` mà mở Microsoft Store thay vì chạy nghĩa là Python chưa được cài, hoặc bị "App execution aliases" chặn. Cài Python rồi mở lại PowerShell.

## 2. Lấy repo
Windows giới hạn đường dẫn 260 ký tự, repo có tên ảnh dài: đặt `core.longpaths` **trước khi clone** và nên clone vào thư mục ngắn.

**Windows (PowerShell):**
```powershell
git config --global core.longpaths true
```
```powershell
git clone <địa-chỉ-repo-của-bạn> D:\AI\sunny-tester-kit
```

**Mac (Terminal):**
```bash
git clone <địa-chỉ-repo-của-bạn> ~/AI/sunny-tester-kit
```

## 3. Cài thư viện (một lần)
Mở Terminal trong thư mục repo rồi chạy (cần mạng, vài phút):

**Windows:**
```powershell
python scripts/cai-dat-may-moi.py
```

**Mac:**
```bash
python3 scripts/cai-dat-may-moi.py
```

Lệnh này tạo `.venv`, cài thư viện trong `scripts/requirements-tu-dong.txt`, bật hook git và `core.longpaths` cho repo (Mac: thêm quyền chạy cho hook). Chạy lại nhiều lần được. Sau đó gõ `python -X utf8 scripts/run_tests.py …` ở đâu cũng được: script thấy Python hệ thống chưa có Playwright thì tự chạy lại bằng `.venv`. Máy cũ đã có venv ở `~/.venvs/playwright` thì vẫn dùng được, không cần cài lại.

## 4. Chọn dự án và tạo file tài khoản test `.env`
Repo chứa nhiều dự án (mỗi dự án là một hệ thống đang test, danh sách ở `memories/project/overview.md`). Mở phiên Claude đầu tiên trên máy mới, **Claude sẽ hỏi bạn đang làm dự án nào** rồi ghi vào file `.du-an-hien-tai` (chỉ nằm trên máy này, không commit). Các phiên sau không hỏi lại; muốn đổi thì nói tên dự án khác.

**Tên người test:** tạo file `.nguoi-test` ở gốc repo, một dòng là tên của bạn (cũng không commit). Tên này được ghi vào cột Người viết của test case, người chạy của mỗi lượt và lịch sử thay đổi. Chưa có file thì ghi "Chưa ghi tên" (không lấy tên tài khoản Git).
- Dự án đã có: chọn trong danh sách.
- Dự án mới: Claude hỏi tên, URL, tên thư mục ngắn rồi tạo thư mục riêng (`scripts/tao-du-an.py`). Claude **không dùng kiến thức của dự án khác** (nghiệp vụ, tài khoản, từ ngữ, con số) cho dự án mới.

`.env` không đi theo git (để không lộ mật khẩu). Chọn dự án xong, **Claude hỏi địa chỉ môi trường thử, mã tài khoản, tên đăng nhập, mật khẩu trong chat rồi tự tạo `.env`**. Chỉ đưa tài khoản test, vì chat được lưu trong lịch sử phiên; muốn gõ mật khẩu ẩn (Claude không thấy) thì nói "gõ ở terminal". Chưa có tài khoản thì nói "để sau". Tự làm cũng được:

```powershell
python -X utf8 scripts/nhap-tai-khoan.py --url <địa chỉ> --ma NV01 --user <tên đăng nhập> --go-mat-khau
```

## 5. Việc phải tự làm trong app Claude
1. Mở thư mục repo trong tab Code. Khi app hỏi có tin cậy thư mục không, chọn tin cậy: app mới đọc `.claude/settings.json`, nơi đã cho phép sẵn các lệnh an toàn (sửa file trong `memories/`, `srs/`, `testing/`, `evidence/`, `docs/`, skill; chạy script soát; `git status/diff/log/show`). `git commit`, `git push`, xóa file vẫn hỏi bạn trước.
2. (Tùy chọn, ít tác dụng) Tắt tay trong phần quản lý plugin/skill của app những thứ không dùng cho kiểm thử. Đã đo: nạp sẵn ~74 nghìn token, phần của plugin/skill tài khoản chỉ vài nghìn, và **script/cấu hình trong repo không tắt được** chúng (`memories/user/connectors-and-plugins.md`).
3. Lần đầu Claude mở trang của hệ thống đang test trong trình duyệt của app: bấm cho phép trang, rồi Claude tự đăng nhập bằng tài khoản test (mật khẩu không hiện ra trong chat).

## 6. Kiểm tra máy đã sẵn sàng
```bash
python -X utf8 scripts/kiem-tra-may-moi.py
```
(Mac: `python3`.) Chạy trong thư mục repo. Script kiểm Python, Git, Playwright, MarkItDown, ffmpeg, Chrome/Edge, `core.longpaths` (Windows), quyền chạy của hook (Mac), `.env` (không in mật khẩu), skill, quyền trong `.claude/settings.json`, và chạy thử các script soát. "0 mục THIẾU" là xong. Hoặc nhờ Claude: "chạy kiểm tra máy mới".

## 7. Thói quen để phiên nào cũng nhanh
- **Mỗi việc một phiên mới.** Phiên dài làm mỗi bước sau chậm hơn.
- **Nói rõ việc và feature ngay câu đầu** (ví dụ "ghi câu trả lời BA cho CART: A7 …"). Skill đã ghi sẵn cần đọc file nào cho từng việc, không cần bảo Claude "đọc hết bộ nhớ".
- **Việc đơn giản** (push git, ghi câu trả lời BA, sửa chữ) thì hạ mức suy nghĩ (effort) trong app; phân tích requirement, khám phá thì để mức cao.

## Điều không đi theo repo (bình thường)
- Lịch sử chat và bộ nhớ tự động của Claude nằm ở thư mục `.claude` trong thư mục người dùng của từng máy. Bộ nhớ quan trọng của dự án đã nằm trong `memories/` nên máy mới vẫn đủ ngữ cảnh. **Điều bạn dặn trong chat mà chưa ghi vào `memories/` hoặc skill thì không đi theo**: vì vậy mỗi quy tắc bạn đưa ra phải được ghi vào đó ngay trong lượt.
- Đăng nhập trình duyệt, cho phép trang web, bật/tắt plugin: làm lại trên từng máy (mục 5).
- Trạng thái bộ đếm nhập sai (`.phien-dang-nhap/`): chỉ đếm những gì máy này đã gửi; máy khác hoặc người khác nhập sai thì không thấy được.

## Hook git để trang HTML luôn khớp file md
`scripts/cai-dat-may-moi.py` đã bật hook (hoặc tự chạy một lần trong mỗi bản clone: `git config core.hooksPath .githooks`; Mac thêm `chmod +x .githooks/pre-commit`). Từ đó mỗi lần commit, hook tự chạy `scripts/build_docs.py --all --stage` để sinh lại mọi trang HTML (tài liệu, kết quả chạy, bug, trang tổng) và đưa vào commit. `scripts/kiem-tra-may-moi.py` kiểm hook đã bật chưa. Giao diện và font: `docs/thuong-hieu/README.md`.
