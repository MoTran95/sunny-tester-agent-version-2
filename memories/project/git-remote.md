# Git và remote
Đọc khi: commit/push.

- Remote `origin`: chưa ghi. Người dùng repo này tự thêm (`git remote add origin <địa chỉ>`) rồi ghi địa chỉ và nhánh chính vào đây.
- `.gitignore`: `.env`, `.du-an-hien-tai`, `.nguoi-test`, `.claude/settings.local.json`, `.phien-dang-nhap/`. Mật khẩu test **không** lên git.
- Trước khi commit file mới: không chép mật khẩu từ `.env`. Commit/push **chỉ khi người dùng nhờ**. Cảnh báo LF→CRLF trên Windows là bình thường.
