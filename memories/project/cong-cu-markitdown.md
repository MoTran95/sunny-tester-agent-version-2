# MarkItDown (docx/pdf/xlsx/pptx → Markdown)
Đọc khi: cần đọc Office/PDF; cài máy mới. Quy tắc dùng ngắn gọn nằm ở `CLAUDE.md`.

- Gói `markitdown[pdf,docx,pptx,xlsx,xls]` 0.1.9 (Microsoft, MIT) cài trong `.venv` của repo bằng `scripts/cai-dat-may-moi.py` (máy cũ này còn venv riêng `~/.venvs/markitdown`, vẫn dùng được). Lệnh chạy được ở máy nào: `python -X utf8 scripts/doi-sang-markdown.py <file> -o <thư-mục-tạm>\<tên>.md` (tự tìm venv có MarkItDown, đặt `PYTHONUTF8=1`).
- Cài: `pdf, docx, pptx, xlsx, xls`. Cố ý bỏ Azure, âm thanh, YouTube.
- Soát an toàn 2026-11-18: băm khớp PyPI, không `eval/exec` đáng ngờ; `subprocess` chỉ gọi `exiftool` (tùy chọn); `requests` chỉ khi đưa URL. Chỉ đưa file/URL đã biết nguồn; không `convert_uri` với đầu vào lạ.
- Bẫy: Windows in console làm tiếng Việt thành `?` → luôn `-o` ra file + `PYTHONUTF8=1`, rồi đọc file. Ghi `.md` ra thư mục tạm, không cạnh file gốc.
- Không dùng cho `.txt`/`.md`, Excel lớn (pandas), PDF scan/nhiều hình (đọc ảnh trang), việc sửa file giữ định dạng.
- Chưa thử trên docx/pdf thật; chưa đo tiết kiệm; chưa có quyền cho phép sẵn lệnh này.
