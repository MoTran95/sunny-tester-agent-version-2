# Connector/plugin: mặc định tắt, hỏi trước khi bật
Đọc khi: việc cần connector/plugin; người dùng than chậm/tốn token.

- Chỉ bật connector/plugin khi người dùng yêu cầu hoặc thật cần, **và hỏi trước**. Kiểm thử bằng skill của repo + trình duyệt có sẵn + script Python không cần connector nào.
- Plugin/skill gắn với tài khoản claude.ai **không tắt được từ repo** (đã đo: `syncClaudeAiPlugins=false`, `disableClaudeAiConnectors=true`, `permissions.deny` đều không đổi phần nạp sẵn đầu phiên). Tắt tay trong app thì có tác dụng nhưng chỉ bớt khoảng 3–6% token; phần lớn phần nạp sẵn là prompt hệ thống + schema công cụ, không tắt được.
- Muốn đo: `python -X utf8 scripts/do-toc-do-phien.py` ở đầu một phiên mới.
