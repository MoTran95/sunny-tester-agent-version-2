"""Khám phá đăng nhập Ecommerce Lite (chạy một lần). Mật khẩu chỉ đọc qua cfg.get_credentials, không in."""
import json
import sys
from pathlib import Path

ROOT = Path("D:/AI/sunny-tester-kit")
sys.path.insert(0, str(ROOT / "scripts"))
import _venv  # noqa

_venv.ensure_playwright()
from test_automation import config, failure_counter, session  # noqa
from playwright.sync_api import sync_playwright  # noqa

sys.stdout.reconfigure(encoding="utf-8")
cfg = config.load("ecommerce-lite")
user, pw = cfg.get_credentials("SHOPPER")
SHOTS = ROOT / "evidence/ecommerce-lite/features/dang-nhap/screenshots"
SHOTS.mkdir(parents=True, exist_ok=True)
out = {}


def swap(p):
    for i, ch in enumerate(p):
        if ch.isalpha():
            return p[:i] + ch.swapcase() + p[i + 1:]
    return p


def attempt(browser, name, email, password, via="button", remember=False, counted=True, shot=None):
    ctx = browser.new_context(viewport={"width": 1024, "height": 768})
    page = ctx.new_page()
    page.goto(cfg.url + "/", wait_until="domcontentloaded")
    page.locator("#email").fill(email)
    page.locator("#password").fill(password)
    if remember:
        page.locator("#remember").check()
    with page.expect_response(lambda r: "/api/auth/login" in r.url, timeout=20000) as info:
        if via == "enter":
            page.locator("#password").press("Enter")
        else:
            page.locator("#sign-in-button").click()
    r = info.value
    status = r.status
    try:
        body = r.json()
        body = {k: v for k, v in body.items() if k != "token"}
        if "user" in body:
            body["user"] = {k: v for k, v in body["user"].items() if k in ("name", "role", "email")}
    except Exception:  # noqa
        body = None
    if counted:
        failure_counter.record(cfg, status)
    page.wait_for_timeout(1500)
    err = page.locator("#login-error")
    res = {
        "status": status, "body": body,
        "error_text": err.inner_text() if err.is_visible() else None,
        "email_kept": page.locator("#email").input_value() if page.locator("#email").is_visible() else None,
        "password_after": (len(page.locator("#password").input_value()) if page.locator("#password").is_visible() else None),
        "toast": page.locator("#toast-region").inner_text(),
        "url": page.url,
    }
    if shot:
        page.screenshot(path=str(SHOTS / shot))
    return ctx, page, res


with sync_playwright() as p:
    browser = session.launch_browser(p, headless=True)
    # --- 3 lần sai (tổng tối đa 3, đã khai trần 3) ---
    for key, email, password, shot in [
        ("A_sai_mat_khau", user, "Wrong#Pass1", "01-sai-mat-khau.png"),
        ("B_email_khong_ton_tai", "nobody.xyz@sunny.test", "Wrong#Pass1", "02-email-khong-ton-tai.png"),
        ("C_dung_mat_khau_doi_hoa_thuong", user, swap(pw), "03-mat-khau-doi-hoa-thuong.png"),
    ]:
        reason = failure_counter.refusal_reason(cfg)
        if reason:
            out[key] = {"dung": reason}
            continue
        ctx, page, res = attempt(browser, key, email, password, shot=shot)
        out[key] = res
        ctx.close()
        if res["status"] == 429:
            out["dung_vi_429"] = True
            break
    # --- đăng nhập đúng (không tính vào trần) ---
    ctx, page, res = attempt(browser, "D_email_viet_hoa_enter", user.upper(), pw, via="enter", counted=False, shot="04-email-viet-hoa-enter.png")
    out["D_email_viet_hoa_enter"] = res
    ctx.close()
    ctx, page, res = attempt(browser, "E_email_co_dau_cach", "  " + user + "  ", pw, counted=False)
    out["E_email_co_dau_cach"] = res
    ctx.close()
    # --- F: đăng nhập đúng không ghi nhớ; xem cookie, tải lại, đăng xuất, Back, hai tab ---
    for remember in (False, True):
        ctx, page, res = attempt(browser, "F", user, pw, remember=remember, counted=False,
                                 shot=("05-dang-nhap-dung.png" if not remember else None))
        key = "F_dang_nhap_dung_ghi_nho" if remember else "F_dang_nhap_dung"
        out[key] = res
        cookies = [{k: c.get(k) for k in ("name", "httpOnly", "secure", "sameSite", "expires")} for c in ctx.cookies()]
        out[key]["cookies"] = cookies
        out[key]["local_storage_keys"] = page.evaluate("Object.keys(localStorage)")
        out[key]["session_storage_keys"] = page.evaluate("Object.keys(sessionStorage)")
        if not remember:
            page.reload(wait_until="domcontentloaded")
            page.wait_for_timeout(2000)
            out[key]["sau_tai_lai"] = {"url": page.url, "thay_Sign_out": page.get_by_role("button", name="Sign out").is_visible(),
                                         "thay_o_mat_khau": page.locator("#password").is_visible()}
            page.screenshot(path=str(SHOTS / "06-sau-tai-lai.png"))
            # mở trang thứ hai cùng phiên
            page2 = ctx.new_page()
            page2.goto(cfg.url + "/", wait_until="domcontentloaded")
            page2.wait_for_timeout(2000)
            out[key]["tab2_thay_Sign_out"] = page2.get_by_role("button", name="Sign out").is_visible()
            # đăng xuất ở tab 1
            with page.expect_response(lambda r: "/api/auth/logout" in r.url) as lo:
                page.get_by_role("button", name="Sign out").click()
            out[key]["logout_status"] = lo.value.status
            page.wait_for_timeout(1500)
            out[key]["sau_dang_xuat"] = {"url": page.url, "thay_o_mat_khau": page.locator("#password").is_visible(),
                                           "toast": page.locator("#toast-region").inner_text()}
            page.screenshot(path=str(SHOTS / "07-sau-dang-xuat.png"))
            out[key]["api_me_sau_logout"] = page.evaluate("fetch('/api/me').then(r=>r.status)")
            # Back
            page.go_back()
            page.wait_for_timeout(1500)
            out[key]["sau_Back"] = {"url": page.url, "thay_Sign_out": page.get_by_role("button", name="Sign out").is_visible(),
                                      "thay_o_mat_khau": page.locator("#password").is_visible()}
            # tab 2 sau khi tab 1 đăng xuất
            out[key]["tab2_api_me_sau_logout_o_tab1"] = page2.evaluate("fetch('/api/me').then(r=>r.status)")
            page2.reload(wait_until="domcontentloaded")
            page2.wait_for_timeout(2000)
            out[key]["tab2_sau_tai_lai_thay_o_mat_khau"] = page2.locator("#password").is_visible()
        ctx.close()
    # --- chưa đăng nhập: liên kết sâu, địa chỉ không tồn tại ---
    ctx = browser.new_context(viewport={"width": 1024, "height": 768})
    page = ctx.new_page()
    page.goto(cfg.url + "/#profile", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    out["G_lien_ket_sau_khi_chua_dang_nhap"] = {"url": page.url, "thay_o_mat_khau": page.locator("#password").is_visible()}
    page.screenshot(path=str(SHOTS / "08-lien-ket-sau-chua-dang-nhap.png"))
    resp = page.goto(cfg.url + "/khong-ton-tai", wait_until="domcontentloaded")
    page.wait_for_timeout(1500)
    out["H_dia_chi_khong_ton_tai"] = {"status": resp.status if resp else None, "url": page.url,
                                       "text": page.locator("body").inner_text()[:200]}
    page.screenshot(path=str(SHOTS / "09-dia-chi-khong-ton-tai.png"))
    out["I_api_me_chua_dang_nhap"] = page.evaluate("fetch('/api/me').then(r=>r.status)")
    ctx.close()
    browser.close()

out["bo_dem_sai"] = failure_counter.read(cfg)
print(json.dumps(out, ensure_ascii=False, indent=1))
