"""Chọn đúng Python có Playwright, để gõ `python -X utf8 scripts/run_tests.py …` ở máy nào cũng chạy được.

Các script cần Playwright (run_tests, auto_login, inspect_page, selftest) gọi `ensure_playwright()` đầu tiên:
- Python đang chạy đã có Playwright thì chạy tiếp.
- Chưa có thì tìm venv `.venv` trong repo (do `scripts/cai-dat-may-moi.py` tạo), rồi `~/.venvs/playwright` (cách cũ),
  và chạy lại chính lệnh đó bằng venv. Không tìm thấy thì báo cách cài và thoát mã 2.
"""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_FLAG = "TEST_AUTOMATION_RELAUNCHED"


def venv_pythons():
    """Danh sách python của các venv có thể dùng, theo thứ tự ưu tiên (chỉ những file có thật)."""
    found = []
    for base in (ROOT / ".venv", Path.home() / ".venvs" / "playwright"):
        for rel in ("Scripts/python.exe", "bin/python"):
            candidate = base / rel
            if candidate.exists():
                found.append(candidate)
    return found


def ensure_playwright():
    try:
        import playwright  # noqa: F401
        return
    except ImportError:
        pass
    if not os.environ.get(_FLAG):
        current = Path(sys.executable).resolve()
        for python in venv_pythons():
            if python.resolve() == current:
                continue
            print(f"(Python này chưa có Playwright, chạy lại bằng {python})", file=sys.stderr)
            env = dict(os.environ, **{_FLAG: "1"})
            sys.exit(subprocess.call([str(python), "-X", "utf8", *sys.argv], env=env))
    print("Chưa cài Playwright. Chạy một lần: python scripts/cai-dat-may-moi.py (Mac: python3; xem docs/cai-dat-may-moi.md).", file=sys.stderr)
    sys.exit(2)
