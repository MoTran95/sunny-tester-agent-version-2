#!/usr/bin/env python3
"""Chạy test case tự động bằng Playwright. Ví dụ:

    python -X utf8 scripts/run_tests.py --smoke
    python -X utf8 scripts/run_tests.py --case-id dang-nhap/tc-001
    python -X utf8 scripts/run_tests.py --feature dang-nhap --project <dự-án>

Cần Playwright (xem docs/chay-test-tu-dong.md) và phiên đã lưu bởi scripts/auto_login.py.
Mã thoát: 0 đạt hết, 1 có ca Không đạt, 2 sai cấu hình, 3 phiên hết hạn, 4 có ca không kết luận được.
"""
import sys

import _venv

_venv.ensure_playwright()  # chưa có Playwright thì tự chạy lại bằng venv của repo

from test_automation.runner import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
