"""Đọc cấu hình dự án và tài khoản test.

Quy ước `.env` (gốc repo, không commit): `<TIỀN_TỐ>_URL`, `<TIỀN_TỐ>_<MÃ>_USER`, `<TIỀN_TỐ>_<MÃ>_PASSWORD`.
Tiền tố do cấu hình dự án quy định (`tien_to_env`), ví dụ CUA_HANG_MAU.
Mật khẩu chỉ được lấy qua `CauHinh.thong_tin_dang_nhap`, và chỉ module `phien` (đăng nhập) gọi hàm này.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # gốc repo; các hàm bên dưới đọc biến này lúc gọi

REQUIRED_KEYS = ["env_prefix", "default_url", "login"]
REQUIRED_LOGIN_KEYS = ["id_labels", "button_labels", "login_api", "session_check_api", "session_minutes"]
# Đăng nhập tay (`login.mode = "manual"`: SSO, mã xác nhận, captcha): người test tự đăng nhập trong cửa sổ trình duyệt,
# thư viện chỉ chờ rồi lưu phiên; không cần nhãn ô, nút, API đăng nhập và không đọc mật khẩu.
REQUIRED_LOGIN_KEYS_MANUAL = ["session_check_api", "session_minutes"]


class ConfigError(Exception):
    pass


def default_author():
    """Tên người test của máy này (ghi vào cột Người viết, lượt chạy, lịch sử): dòng đầu file `.nguoi-test` ở gốc repo
    (không commit, mỗi máy một file). Chưa có thì "Chưa ghi tên" (không lấy tên tài khoản Git: có thể là biệt danh, lọt vào
    tài liệu gửi ra ngoài). Claude hỏi tên rồi tạo file này (CLAUDE.md bước 0)."""
    f = ROOT / ".nguoi-test"
    if f.exists():
        name = f.read_text(encoding="utf-8").strip().splitlines()[:1]
        if name and name[0].strip():
            return name[0].strip()
    return "Chưa ghi tên"


def read_env():
    path = ROOT / ".env"
    if not path.exists():
        return {}
    results = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        results[key.strip()] = value.strip().strip('"').strip("'")
    return results


def current_project():
    f = ROOT / ".du-an-hien-tai"
    if not f.exists():
        raise ConfigError("Chưa có .du-an-hien-tai; truyền --project <slug>.")
    return f.read_text(encoding="utf-8").strip()


class Config:
    def __init__(self, project, data, env):
        self.project = project
        self.data = data
        self._env = env
        self.env_prefix = data["env_prefix"]
        self.url = (env.get(f"{self.env_prefix}_URL") or data["default_url"]).rstrip("/")
        # Tùy chọn: nơi đọc số phiên bản hệ thống (GET, không cần đăng nhập), ví dụ "/api/health" và "version".
        self.health_api = data.get("health_api", "")
        self.version_field = data.get("version_field", "version")
        login_cfg = data["login"]
        self.login_mode = login_cfg.get("mode", "form")
        self.id_labels = login_cfg.get("id_labels", [])
        self.button_labels = login_cfg.get("button_labels", [])
        self.login_api = login_cfg.get("login_api", "")
        self.session_check_api = login_cfg["session_check_api"]
        self.session_minutes = login_cfg["session_minutes"]
        # Không có mặc định: do requirement hoặc người kiểm thử quyết (xem failure_counter.py). None = chưa khai.
        self.max_consecutive_failures = login_cfg.get("max_consecutive_failures")
        self.block_minutes = login_cfg.get("block_minutes")

    def banner(self):
        """Dòng đầu mỗi lần chạy: dự án và địa chỉ đang dùng (để không chạy nhầm dự án); cảnh báo nếu khác dự án hiện tại của máy."""
        line = f"Dự án: {self.project} · địa chỉ: {self.url}"
        marker = ROOT / ".du-an-hien-tai"
        if marker.exists():
            current = marker.read_text(encoding="utf-8").strip()
            if current and current != self.project:
                line += f"\n  LƯU Ý: dự án hiện tại của máy này là `{current}`, đang chạy cho `{self.project}` (do --project). Chắc đúng dự án chứ?"
        return line

    @property
    def project_dir(self):
        return ROOT / "testing" / self.project

    @property
    def test_data(self):
        """Dữ liệu test của dự án (id hồ sơ nháp…), file `testing/<dự-án>/auto-data.json`, không bắt buộc."""
        f = self.project_dir / "auto-data.json"
        return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}

    @property
    def sessions_dir(self):
        return ROOT / ".phien-dang-nhap" / self.project

    @property
    def screenshots_dir(self):
        return ROOT / "evidence" / self.project / "chay-test"

    def available_accounts(self):
        code = set()
        pattern = re.compile(rf"{re.escape(self.env_prefix)}_([A-Za-z0-9]+)_PASSWORD")
        for key in self._env:
            m = pattern.fullmatch(key)
            if m:
                code.add(m.group(1).upper())
        return sorted(code)

    def get_credentials(self, code):
        """(tên đăng nhập, mật khẩu). Chỉ dùng trong module phien."""
        code = code.upper()
        password = self._env.get(f"{self.env_prefix}_{code}_PASSWORD")
        if password is None:
            raise ConfigError(f"Không có tài khoản {code} trong .env. Hiện có: {', '.join(self.available_accounts()) or '(chưa có)'}")
        return self._env.get(f"{self.env_prefix}_{code}_USER") or code, password


def load(project=None):
    project = project or current_project()
    f = ROOT / "testing" / project / "auto-config.json"
    if not f.exists():
        raise ConfigError(
            f"Chưa có {f.relative_to(ROOT)}. Tạo file này theo mẫu ở docs/chay-test-tu-dong.md (mục Thêm dự án mới)."
        )
    data = json.loads(f.read_text(encoding="utf-8"))
    missing = [k for k in REQUIRED_KEYS if k not in data]
    if not missing:
        manual = data["login"].get("mode") == "manual"
        missing = [f"login.{k}" for k in (REQUIRED_LOGIN_KEYS_MANUAL if manual else REQUIRED_LOGIN_KEYS) if k not in data["login"]]
    if missing:
        raise ConfigError(f"{f.relative_to(ROOT)} thiếu khóa: {', '.join(missing)}")
    placeholders = _placeholder_keys(data)
    if placeholders:
        raise ConfigError(f"{f.relative_to(ROOT)} còn chỗ chưa điền (dạng <…>): {', '.join(placeholders)}")
    return Config(project, data, read_env())


def load_for_docs(project=None):
    """Cấu hình đủ để SINH TRANG (bug, trang tổng, kết quả, báo cáo tổng kết), không cần phần đăng nhập.

    Dự án mới chưa điền `auto-config.json` (còn `<…>`, thiếu khóa, chưa có file) vẫn có trang tài liệu;
    chỉ việc chạy test tự động mới cần `load()` đầy đủ. `cfg.ready` = False khi cấu hình chạy test chưa xong,
    `cfg.not_ready_reason` nói vì sao.
    """
    project = project or current_project()
    try:
        cfg = load(project)
        cfg.ready, cfg.not_ready_reason = True, ""
        return cfg
    except ConfigError as error:
        reason = str(error)
    f = ROOT / "testing" / project / "auto-config.json"
    try:
        data = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
    except ValueError:
        data = {}
    data = dict(data)
    data.setdefault("env_prefix", project.upper().replace("-", "_"))
    url = data.get("default_url", "")
    data["default_url"] = "" if (not isinstance(url, str) or "<" in url) else url
    login_cfg = dict(data.get("login") or {})
    login_cfg.setdefault("session_check_api", "")
    login_cfg.setdefault("session_minutes", 0)
    data["login"] = login_cfg
    cfg = Config(project, data, read_env())
    cfg.ready, cfg.not_ready_reason = False, reason
    return cfg


def _placeholder_keys(value, path=""):
    """Khóa nào trong file cấu hình còn giá trị mẫu `<…>` do scripts/tao-du-an.py tạo ra."""
    found = []
    if isinstance(value, dict):
        for key, child in value.items():
            found += _placeholder_keys(child, f"{path}.{key}" if path else str(key))
    elif isinstance(value, list):
        for i, child in enumerate(value):
            found += _placeholder_keys(child, f"{path}[{i}]")
    elif isinstance(value, str) and "<" in value and ">" in value:
        found.append(path)
    return found
