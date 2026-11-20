"""Trình duyệt, đăng nhập một lần, lưu và kiểm phiên.

An toàn (memories/pitfalls/dont-trigger-lockouts.md):
- Mỗi lần gọi `dang_nhap` chỉ bấm Đăng nhập ĐÚNG MỘT LẦN, không tự thử lại.
- Không in mật khẩu, không đọc thân yêu cầu đăng nhập, không in giá trị cookie.
- File phiên chứa cookie đăng nhập: nằm ở `.phien-dang-nhap/<dự-án>/` (đã .gitignore).
"""
import re
import time

from . import config, failure_counter

MAX_WAIT_MS = 20_000


def launch_browser(p, headless=True):
    """Ưu tiên Chrome, rồi Edge có sẵn trên máy; cuối cùng Chromium của Playwright."""
    error = None
    for channel in ("chrome", "msedge", None):
        try:
            if channel:
                return p.chromium.launch(channel=channel, headless=headless)
            return p.chromium.launch(headless=headless)
        except Exception as e:  # noqa: BLE001
            error = e
    raise RuntimeError(
        "Không mở được Chrome, Edge hay Chromium của Playwright. "
        "Cài Chrome/Edge, hoặc chạy: python -m playwright install chromium\n" + str(error)
    )


def session_file(cfg, account):
    return cfg.sessions_dir / f"{account.upper()}.json"


def age_minutes(cfg, account):
    f = session_file(cfg, account)
    return (time.time() - f.stat().st_mtime) / 60 if f.exists() else None


def delete_session(cfg, account):
    f = session_file(cfg, account)
    if f.exists():
        f.unlink()


def is_session_valid(cfg, context):
    """Phiên trong context còn dùng được không (một yêu cầu GET, không đăng nhập lại)."""
    return context.request.get(cfg.url + cfg.session_check_api).status == 200


def session_status(browser, cfg, account):
    """'ok' | 'missing' | 'expired'."""
    f = session_file(cfg, account)
    if not f.exists():
        return "missing"
    context = browser.new_context(storage_state=str(f))
    try:
        return "ok" if is_session_valid(cfg, context) else "expired"
    finally:
        context.close()


def login_once(page, cfg, username, password):
    """Điền form và bấm Đăng nhập ĐÚNG MỘT LẦN. Trả về (thanh_cong, mo_ta)."""
    password_input = page.locator("input[type=password]").first
    password_input.wait_for(state="visible", timeout=MAX_WAIT_MS)
    id_input = page.get_by_label(re.compile("|".join(re.escape(x) for x in cfg.id_labels), re.I)).first
    id_input.fill(username)
    password_input.fill(password)

    button = page.get_by_role(
        "button", name=re.compile("^(" + "|".join(re.escape(x) for x in cfg.button_labels) + ")$", re.I)
    )

    def is_login_request(r):
        return r.request.method == "POST" and r.url.rstrip("/").endswith(cfg.login_api.rstrip("/"))

    with page.expect_response(is_login_request, timeout=MAX_WAIT_MS) as info:
        if button.count() > 0:
            button.first.click()
        else:
            password_input.press("Enter")
    status_code = info.value.status
    failure_counter.record(cfg, status_code)

    if status_code == 200:
        password_input.wait_for(state="detached", timeout=MAX_WAIT_MS)
        return True, "200"
    if status_code == 429:
        return False, "429: hệ thống đang chặn tạm vì đăng nhập sai nhiều lần, chờ hết chặn rồi tự thử lại"
    if status_code in (400, 401):
        return False, f"{status_code}: tên đăng nhập hoặc mật khẩu trong .env không đúng, kiểm tra lại .env"
    return False, f"mã trả về bất thường {status_code}"


def manual_login(p, cfg, account, wait_minutes=5):
    """Mở cửa sổ trình duyệt để NGƯỜI TEST tự đăng nhập (SSO, mã xác nhận, captcha…), chờ tới khi `session_check_api` trả 200
    rồi lưu phiên. Thư viện không gõ gì, không đọc mật khẩu, chỉ gửi yêu cầu GET kiểm phiên. Trả mã thoát 0 hoặc 1."""
    account = account.upper()
    cfg.sessions_dir.mkdir(parents=True, exist_ok=True)
    browser = launch_browser(p, headless=False)
    context = browser.new_context(no_viewport=True)
    try:
        page = context.new_page()
        page.goto(cfg.url + "/", wait_until="domcontentloaded")
        print(f"Cửa sổ trình duyệt đã mở. Hãy tự đăng nhập tài khoản {account} (kể cả mã xác nhận). Mình chỉ chờ tối đa {wait_minutes} phút, không gõ gì.")
        deadline = time.time() + wait_minutes * 60
        while time.time() < deadline:
            try:
                if is_session_valid(cfg, context):
                    context.storage_state(path=str(session_file(cfg, account)))
                    print(f"Đã lưu phiên của {account}. Chạy test ngay (phiên chỉ sống khoảng {cfg.session_minutes} phút).")
                    return 0
            except Exception:  # noqa: BLE001
                pass   # trang đang chuyển hướng giữa các bước đăng nhập: thử lại
            page.wait_for_timeout(2000)
        print("Hết thời gian chờ mà chưa thấy đăng nhập xong; chưa lưu phiên.")
        return 1
    finally:
        browser.close()


def login(p, cfg, account, headless=True, reuse=False, keep_open=False):
    """Đăng nhập một tài khoản, lưu phiên. Trả về (mã thoát, trinh_duyet|None, context|None).

    Mã thoát: 0 = xong, 1 = đăng nhập không thành công. Nếu giu_mo=True và thành công thì
    trình duyệt/context được trả về còn mở (người gọi tự đóng).
    """
    account = account.upper()
    username, password = cfg.get_credentials(account)
    cfg.sessions_dir.mkdir(parents=True, exist_ok=True)
    f = session_file(cfg, account)
    options = {"no_viewport": True} if not headless else {}
    use_saved_session = reuse and f.exists()
    if use_saved_session:
        options["storage_state"] = str(f)

    browser = launch_browser(p, headless)
    context = browser.new_context(**options)
    page = context.new_page()
    page.goto(cfg.url + "/", wait_until="domcontentloaded")

    already_logged_in = False
    if use_saved_session:
        already_logged_in = is_session_valid(cfg, context)
        if already_logged_in:
            page.reload(wait_until="domcontentloaded")
            print(f"[{account}] Dùng lại phiên đã lưu.")
        else:
            print(f"[{account}] Phiên đã lưu hết hạn, đăng nhập lại.")

    if not already_logged_in:
        success, description = login_once(page, cfg, username, password)
        if not success:
            print(f"[{account}] Đăng nhập không thành công, dừng (không tự thử lại) — {description}")
            browser.close()
            return 1, None, None
        print(f"[{account}] Đã đăng nhập.")

    me = context.request.get(cfg.url + cfg.session_check_api)
    if me.status != 200:
        print(f"[{account}] Cảnh báo: {cfg.session_check_api} trả về {me.status} sau khi đăng nhập, phiên có thể chưa giữ được.")
    else:
        try:
            role = me.json().get("role")
            if role:
                print(f"[{account}] Vai trò: {role}")
        except Exception:  # noqa: BLE001
            pass
    context.storage_state(path=str(f))
    print(f"[{account}] Đã lưu phiên (hết hạn sau khoảng {cfg.session_minutes} phút).")

    if keep_open:
        return 0, browser, context
    browser.close()
    return 0, None, None
