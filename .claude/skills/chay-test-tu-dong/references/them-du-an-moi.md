# Thêm dự án mới hoặc máy mới vào bộ chạy test

## Máy mới (một lần)
1. Python 3.10+ rồi chạy một lệnh (Windows `python`, Mac `python3`): `python scripts/cai-dat-may-moi.py` (tạo `.venv`, cài Playwright, MarkItDown, Pillow, fonttools; bật hook git và `core.longpaths`). Dùng Chrome hoặc Edge có sẵn. Chạy Python kèm `-X utf8`; `run_tests.py`, `auto_login.py`, `inspect_page.py` tự chạy lại bằng `.venv` nếu Python hệ thống chưa có Playwright. **Trước khi clone** máy Windows: `git config --global core.longpaths true`.
2. Video ca lỗi (tùy chọn, hỏi người dùng): `.venv/Scripts/python.exe -m playwright install ffmpeg` (Mac: `.venv/bin/python`) (~1,6 MiB).
3. Hook sinh lại trang HTML trước mỗi commit: script cài đặt đã bật (`git config core.hooksPath .githooks`).
4. `.env` (không commit): `<TIỀN_TỐ>_URL`, `<TIỀN_TỐ>_<MÃ>_USER`, `<TIỀN_TỐ>_<MÃ>_PASSWORD`; mẫu ở `.env.example`. Người dùng tự điền mật khẩu.
5. `python -X utf8 scripts/kiem-tra-may-moi.py` (kiểm tổng thể) và `python -X utf8 scripts/selftest/run_selftest.py` (`ALL OK`).

## Dự án mới (`<slug>`)
1. Tạo dự án: `python -X utf8 scripts/tao-du-an.py <slug> "<Tên>" <địa chỉ>` (xem `memories/conventions/nhieu-du-an.md`): tạo thư mục, bộ nhớ, ghi `.du-an-hien-tai`, và **khuôn** `testing/<slug>/auto-config.json`, `auto-data.json`, `ten-tinh-nang.json`, khối khóa trong `.env.example`.
2. Điền các chỗ `<…>` trong `testing/<slug>/auto-config.json` (chưa điền thì thư viện từ chối chạy, nói rõ khóa nào):
   `{"env_prefix": "...", "default_url": "https://<địa chỉ có nhãn staging/dev>", "login": {"id_labels": ["Tên đăng nhập", "Username"], "button_labels": ["Đăng nhập", "Sign in"], "login_api": "/api/auth/sign-in", "session_check_api": "/api/me", "session_minutes": 10, "max_consecutive_failures": 9}}`
   Tùy chọn (ngoài `login`): `"health_api": "/api/health", "version_field": "version"` để runner in số phiên bản hệ thống đang chạy trước khi chạy ca (`--bug-build X` so với bản lúc tạo bug); không khai thì bỏ qua.
   (nhãn ô và API lấy từ hệ thống thật bằng `scripts/inspect_page.py`; nhãn cả hai ngôn ngữ nếu có).
   Đăng nhập SSO, mã xác nhận, captcha: `"login": {"mode": "manual", "session_check_api": "…", "session_minutes": …}`; người test chạy `auto_login.py <mã> --manual` (tự đăng nhập, script chỉ chờ rồi lưu phiên).
   **Trần nhập sai và thời gian chặn** (`max_consecutive_failures`, `block_minutes`): lấy từ requirement hoặc hỏi người test; chưa khai thì ca cố ý nhập sai bị từ chối. Không đặt số mặc định.
3. `testing/<slug>/auto-data.json`: `{"version": "<số bản ở chân trang>", …id dữ liệu test…}`; bản mới đổi số ở đây.
4. Test case theo `tao-checklist-test-case` (12 cột; cột Tự động hóa); script ca ở `testing/<slug>/<tính-năng>/auto/tc-xxx.py` dựng từ `assets/mau-ca-tu-dong.py`.
5. Bộ smoke theo `tao-smoke-test`; chạy `--smoke`; ghi lượt bằng `build_report.py add-run`.
6. Tên hiển thị tiếng Việt của tính năng: thêm vào `testing/<slug>/ten-tinh-nang.json` (`{"dang-nhap": "Đăng nhập"}`); chưa khai thì trang hiện tên thư mục.
7. `python -X utf8 scripts/build_docs.py --all` rồi mở `testing/<slug>/index.html`.

## Thương hiệu
Mặc định logo Sunny (`docs/thuong-hieu/brand.json`). Dự án của thương hiệu khác: tạo `testing/<slug>/brand.json` chỉ gồm khóa muốn đổi (`name`, `logo`, `logo_enabled`); đường dẫn tính từ gốc repo. Màu và font là giao diện chung ở `theme.py`.
