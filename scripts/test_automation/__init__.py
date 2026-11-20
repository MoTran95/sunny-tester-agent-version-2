"""Thư viện dùng chung để chạy test case tự động bằng Playwright, cho mọi dự án trong repo.

- config    : đọc `testing/<dự-án>/auto-config.json` và `.env`
- session   : mở trình duyệt, đăng nhập một lần, lưu/kiểm phiên
- context   : đối tượng `ctx` đưa cho từng script test case
- results   : kiểm tra, kết luận, ghi file kết quả
- runner    : lệnh chạy một ca, một tính năng hoặc cả bộ smoke

Hướng dẫn cho người dùng: docs/chay-test-tu-dong.md
"""
