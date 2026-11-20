"""Đối tượng `ctx` đưa cho hàm `run(ctx)` của từng script test case.

Script test case KHÔNG thấy mật khẩu: dùng phiên đã lưu, hoặc `ctx.sign_in(account)` (thư viện đọc `.env`, điền form, bấm Đăng nhập đúng một lần).
"""
import re
import time
from pathlib import Path

from . import failure_counter, session
from .results import Check


class SessionExpired(Exception):
    """Phiên đã lưu không còn dùng được: không kết luận ca, cần đăng nhập lại."""


class WaitTimeout(Exception):
    """Chờ một phần tử quá hạn: có thể do trang chậm hoặc script chờ sai, chưa phải lỗi hệ thống."""


def _as_list(v):
    return [] if not v else [v] if isinstance(v, str) else list(v)


# Vẽ khung đỏ quanh từng đoạn chữ (theo vị trí thật trên màn hình), trả về [(chữ, có thấy không)]
_JS_MARK = """(items) => {
  const out = [];
  for (const [t, color] of items) {
    const green = color === "green";
    const line = green ? "#1B8F3A" : "#E5252A", fill = green ? "rgba(27,143,58,.16)" : "rgba(229,37,42,.16)";
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    let n, found = false;
    while ((n = walker.nextNode())) {
      const i = n.nodeValue.indexOf(t);
      if (i < 0) continue;
      const r = document.createRange(); r.setStart(n, i); r.setEnd(n, i + t.length);
      const b = r.getBoundingClientRect();
      if (b.width === 0 && b.height === 0) continue;
      const d = document.createElement('div'); d.className = '__loi__';
      d.style.cssText = 'position:fixed;left:' + (b.left - 5) + 'px;top:' + (b.top - 4) + 'px;width:' + (b.width + 10) + 'px;height:' + (b.height + 8) +
        'px;border:3px solid ' + line + ';border-radius:6px;background:' + fill + ';box-shadow:0 0 0 2px rgba(255,255,255,.75);z-index:2147483647;pointer-events:none';
      const tag = document.createElement('div'); tag.className = '__loi__';
      tag.textContent = green ? 'ĐẠT' : 'LỖI';
      tag.style.cssText = 'position:fixed;left:' + (b.left - 5) + 'px;top:' + (b.top - 24 < 2 ? b.bottom + 7 : b.top - 24) + 'px;background:' + line + ';color:#fff;font:700 11px/1 sans-serif;padding:3px 6px;border-radius:4px;z-index:2147483647;pointer-events:none';
      document.body.appendChild(d); document.body.appendChild(tag); found = true; break;
    }
    out.push([t, found]);
  }
  return out;
}"""


class PreconditionNotMet(Exception):
    """Điều kiện trước của ca chưa có (dữ liệu test, hồ sơ đúng trạng thái…): không kết luận ca."""


def _vary_password(password, variant):
    if variant == "as_is":
        return password
    if variant == "trailing_space":
        return password + " "
    if variant == "swap_letter_case":
        for i, ch in enumerate(password):
            if ch.isalpha():
                return password[:i] + ch.swapcase() + password[i + 1:]
        raise PreconditionNotMet("Mật khẩu đúng không có chữ cái nào để đổi hoa/thường")
    raise ValueError(f"variant không hợp lệ: {variant}")


class Context:
    _warned_no_ffmpeg = False

    def __init__(self, cfg, browser, info, case_results, image_prefix):
        self.cfg = cfg
        self._browser = browser
        self._info = info
        self._result = case_results
        self._image_prefix = image_prefix
        self._pages = {}
        self._accounts = [t.upper() for t in info.get("accounts", [])]
        self._failure_budget = info.get("wrong_attempts", 0)   # số lần cố ý nhập sai ca này được phép
        self._failures_used = 0
        self._record_video = info.get("record_video", True)
        self._video_dir = cfg.screenshots_dir / "video-tmp" / image_prefix
        self._videos = []

    # --- trang theo tài khoản ---
    def page_for(self, account=None):
        """Trang của tài khoản `ma` (mặc định tài khoản đầu tiên; không có tài khoản = chưa đăng nhập)."""
        account = (account or (self._accounts[0] if self._accounts else "")).upper()
        if account in self._pages:
            return self._pages[account]
        options = {"viewport": {"width": 1366, "height": 800}}
        if self._record_video:
            options["record_video_dir"] = str(self._video_dir)
            options["record_video_size"] = {"width": 1366, "height": 800}
        if account:
            if account not in self._accounts:
                raise ValueError(f"Tài khoản {account} chưa khai trong CASE_INFO['tai_khoan']")
            f = session.session_file(self.cfg, account)
            if not f.exists():
                raise SessionExpired(f"Chưa có phiên đã lưu của {account}")
            options["storage_state"] = str(f)
        context = self._browser.new_context(**options)
        if account and not session.is_session_valid(self.cfg, context):
            context.close()
            raise SessionExpired(f"Phiên của {account} đã hết hạn")
        try:
            page = context.new_page()
        except Exception as error:  # noqa: BLE001
            if not (self._record_video and "ffmpeg" in str(error).lower()):
                raise
            # chưa cài ffmpeg của Playwright: chạy tiếp không quay video (cài: python -m playwright install ffmpeg)
            context.close()
            self._record_video = False
            options.pop("record_video_dir", None)
            options.pop("record_video_size", None)
            context = self._browser.new_context(**options)
            page = context.new_page()
            if not Context._warned_no_ffmpeg:
                Context._warned_no_ffmpeg = True
                print("  (chưa cài ffmpeg cho Playwright nên không quay video; cài bằng: python -m playwright install ffmpeg)")
        self._pages[account] = page
        if self._record_video:
            self._videos.append((account, page.video))
        return page

    @property
    def page(self):
        return self.page_for()

    def sign_in(self, account, page_key=""):
        """Điền form đăng nhập bằng tài khoản test trong `.env` rồi bấm ĐÚNG MỘT LẦN, trên trang chưa đăng nhập `page_key`
        (mặc định trang ẩn danh của ca). Trang phải đang hiện form. Không thành công → không kết luận ca (điều kiện trước sai).

        Script ca không thấy mật khẩu. Đăng nhập đúng đưa bộ đếm sai về 0; đăng nhập sai chỉ xảy ra khi `.env` sai.
        """
        if self.cfg.login_mode == "manual":
            raise PreconditionNotMet("Dự án đăng nhập tay (login.mode = manual): người test chạy auto_login.py --manual trước, ca dùng phiên đã lưu (khai accounts)")
        username, password = self.cfg.get_credentials(account)
        ok, description = session.login_once(self.page_for(page_key), self.cfg, username, password)
        if not ok:
            raise PreconditionNotMet(f"Đăng nhập {account} không thành công ({description})")

    def verify_account_ready(self, account):
        """Mở đầu ca có nhập sai: đăng nhập ĐÚNG một lần trên trang riêng (rồi đóng) để chắc tài khoản dùng được và chưa bị chặn.
        KHÔNG đưa bộ đếm sai về 0 (quan sát 2026-11-19). Bị chặn theo ghi nhận hoặc đăng nhập không được → không kết luận ca.
        Runner tự gọi khi CASE_INFO có `ready_account`."""
        if self._failure_budget and self.cfg.max_consecutive_failures is None:
            raise PreconditionNotMet("Ca có nhập sai nhưng " + failure_counter.NO_CAP)
        blocked = failure_counter.block_message(self.cfg)
        if blocked:
            raise PreconditionNotMet(blocked[0].upper() + blocked[1:] + ": chờ rồi chạy lại")
        username, password = self.cfg.get_credentials(account)
        context = self._browser.new_context()
        try:
            page = context.new_page()
            page.goto(self.cfg.url + "/", wait_until="domcontentloaded")
            ok, description = session.login_once(page, self.cfg, username, password)
        finally:
            context.close()
        if not ok:
            raise PreconditionNotMet(f"Không đăng nhập đúng được {account} để bắt đầu ca ({description})")

    def submit_login(self, username, password="", *, expect_success, password_of=None, variant="as_is", via="button", page_key=""):
        """Gửi form đăng nhập ĐÚNG MỘT LẦN trên trang `page_key` (đang hiện form) và trả mã máy chủ trả về (None nếu không có yêu cầu nào).

        - `username`: chữ gõ vào ô tên đăng nhập, đúng nguyên văn (có thể để trống, có khoảng trắng, chữ thường…).
        - Mật khẩu: `password` là chữ giả gõ nguyên văn; hoặc `password_of="NV01"` lấy mật khẩu đúng trong `.env` (script không thấy)
          kèm `variant`: "as_is" | "swap_letter_case" (đổi hoa/thường một chữ cái) | "trailing_space" (thêm một dấu cách cuối).
        - `via`: "button" | "enter_in_id" | "enter_in_password".
        - `expect_success=False`: lần cố ý nhập sai. Thư viện từ chối (không kết luận ca) khi vượt trần liên tiếp của bộ đếm,
          đang bị chặn, hoặc vượt `wrong_attempts` khai trong CASE_INFO.
        Mật khẩu không bao giờ được in ra.
        """
        if not expect_success:
            reason = failure_counter.refusal_reason(self.cfg)
            if reason:
                raise PreconditionNotMet(f"Dừng, không cố ý nhập sai thêm: {reason}")
            if self._failures_used >= self._failure_budget:
                raise PreconditionNotMet(f"Dừng: ca chỉ khai được nhập sai {self._failure_budget} lần (CASE_INFO wrong_attempts)")
        if password_of:
            _, password = self.cfg.get_credentials(password_of)
            password = _vary_password(password, variant)
        page = self.page_for(page_key)
        cfg = self.cfg
        id_input = page.get_by_label(re.compile("|".join(re.escape(x) for x in cfg.id_labels), re.I)).first
        password_input = page.locator("input[type=password]").first
        id_input.fill(username)
        password_input.fill(password)
        button = page.get_by_role("button", name=re.compile("^(" + "|".join(re.escape(x) for x in cfg.button_labels) + ")$", re.I)).first

        def is_login_request(r):
            return r.request.method == "POST" and r.url.rstrip("/").endswith(cfg.login_api.rstrip("/"))

        status = None
        try:
            with page.expect_response(is_login_request, timeout=10_000) as info:
                if via == "button":
                    button.click()
                elif via == "enter_in_id":
                    id_input.press("Enter")
                else:
                    password_input.press("Enter")
            status = info.value.status
        except Exception:  # noqa: BLE001  (không có yêu cầu nào gửi đi: kiểm phía trình duyệt chặn; không đếm)
            status = None
        if status is not None:
            failure_counter.record(cfg, status)
            if status in (400, 401):
                self._failures_used += 1
        return status

    def line(self):
        for pg in self._pages.values():
            try:
                pg.context.close()  # đóng context thì file video mới được ghi xong
            except Exception:  # noqa: BLE001
                pass

    def finalize_videos(self, keep):
        """Sau khi đóng trang: giữ video (chuyển sang evidence/<dự-án>/chay-test/video/) nếu `keep`, ngược lại xóa."""
        import shutil

        for account, video in self._videos:
            try:
                src = Path(video.path())
            except Exception:  # noqa: BLE001
                continue
            if not src.exists():
                continue
            if keep:
                dest_dir = self.cfg.screenshots_dir / "video"
                dest_dir.mkdir(parents=True, exist_ok=True)
                dest = dest_dir / f"{self._image_prefix}{('-' + account.lower()) if account else ''}-{time.strftime('%Y%m%d-%H%M%S')}.webm"
                shutil.move(str(src), str(dest))
                self._result.videos.append(str(dest.relative_to(self.cfg.screenshots_dir.parents[2])).replace(chr(92), "/"))
            else:
                src.unlink(missing_ok=True)
        try:
            self._video_dir.rmdir()
            self._video_dir.parent.rmdir()
        except OSError:
            pass

    # --- thao tác ---
    def goto(self, path="/", account=None):
        self.page_for(account).goto(self.cfg.url + path, wait_until="domcontentloaded")

    def wait_text(self, plain, account=None, timeout_ms=20_000):
        """Chờ chữ hiện trên trang (trang hay ở 'Đang tải…' vài giây). Quá hạn → HetGio."""
        try:
            self.page_for(account).get_by_text(plain).first.wait_for(state="visible", timeout=timeout_ms)
        except Exception as error:  # noqa: BLE001
            raise WaitTimeout(f"Chờ chữ '{plain}' quá {timeout_ms // 1000} giây ({type(error).__name__})") from error

    def poll_until(self, fn, seconds=15, account=None):
        """Gọi ham() mỗi 0,5 giây tới khi trả giá trị đúng (hoặc hết `giay`); trả giá trị cuối cùng.

        Dùng cho dữ liệu hiện sau vài giây (số phiên bản ở chân trang, khuyến nghị cập nhật sau khi lưu…).
        Hết giờ KHÔNG ném lỗi: script tự quyết định đó là Không đạt hay không kết luận.
        """
        value = None
        for _ in range(int(seconds * 2) + 1):
            value = fn()
            if value:
                return value
            self.page_for(account).wait_for_timeout(500)
        return value

    def page_text(self, account=None):
        return self.page_for(account).inner_text("body")

    def screenshot(self, title="man-hinh", account=None):
        self.cfg.screenshots_dir.mkdir(parents=True, exist_ok=True)
        f = self.cfg.screenshots_dir / f"{self._image_prefix}-{title}-{time.strftime('%Y%m%d-%H%M%S')}.png"
        self.page_for(account).screenshot(path=str(f))
        path = str(f.relative_to(self.cfg.screenshots_dir.parents[2]))
        self._result.images.append(path)
        return path

    # --- dữ liệu test và điều kiện trước ---
    def test_data(self, key):
        """Giá trị từ `testing/<dự-án>/auto-data.json` (ví dụ id hồ sơ nháp). Thiếu/rỗng → không kết luận."""
        value = self.cfg.test_data.get(key)
        if not value:
            raise PreconditionNotMet(
                f"Chưa điền '{key}' trong testing/{self.cfg.project}/auto-data.json (xem docs/chay-test-tu-dong.md)"
            )
        return value

    def precondition(self, title, passed):
        """Kiểm điều kiện trước. Sai → KHÔNG kết luận ca (không phải Không đạt)."""
        if not passed:
            raise PreconditionNotMet(f"Điều kiện trước chưa đúng: {title}")

    # --- kiểm tra ---
    def check_main(self, title, passed, note="", mark_text=None, account=None, error_note=""):
        """Ý chính: sai là Không đạt. `mark_text`: chữ trên trang (hoặc danh sách chữ) sẽ được TÔ ĐỎ trong ảnh bằng chứng khi ý này sai.
        `error_note`: câu mô tả lỗi ở bước nào, in dưới ảnh đó (ví dụ "Lỗi ở bước 5: thanh điều hướng hiện chữ DEFAULT, đáng ra không có")."""
        self._result.checks.append(Check("main", title, bool(passed), note, _as_list(mark_text), (account or "").upper(), error_note))

    def check_minor(self, title, passed, note="", mark_text=None, account=None, error_note=""):
        """Ý phụ: sai chỉ ghi nhận, kết luận 'Đạt kèm ý phụ sai'. `mark_text`: như check_main."""
        self._result.checks.append(Check("minor", title, bool(passed), note, _as_list(mark_text), (account or "").upper(), error_note))

    def capture_error_screenshots(self):
        """Chụp ảnh có khung quanh chữ đã kiểm (chỉ ý có khai `mark_text`), gọi sau khi script chạy xong:
        - `-loi.png`: chỉ khung ĐỎ quanh chữ của các ý SAI (kèm câu mô tả lỗi), dùng làm ảnh cho bug;
        - `-kiem.png`: khung XANH quanh chữ của các ý ĐẠT và khung đỏ quanh ý sai, để người xem biết đã kiểm chỗ nào. Chỉ chụp khi có ít nhất một khung xanh.
        Chữ không còn thấy trên trang lúc này (ví dụ chữ ở bước trước) thì bỏ qua."""
        failed, caption, all_marks = {}, {}, {}
        for k in self._result.checks:
            if not k.mark_text:
                continue
            for t in k.mark_text:
                all_marks.setdefault(k.account, []).append((t, k.passed))
            if not k.passed:
                failed.setdefault(k.account, []).extend(k.mark_text)
                if k.error_note:
                    caption.setdefault(k.account, []).append(k.error_note)
        stamp = time.strftime("%Y%m%d-%H%M%S")
        for account, plain in failed.items():
            pg = self.page_for(account or None)
            seen = pg.evaluate(_JS_MARK, [[t, "red"] for t in dict.fromkeys(plain)])
            if not any(found for _, found in seen):
                continue  # không tìm thấy chữ trên trang: không chụp ảnh sai chỗ
            self.cfg.screenshots_dir.mkdir(parents=True, exist_ok=True)
            f = self.cfg.screenshots_dir / f"{self._image_prefix}-loi{('-' + account.lower()) if account else ''}-{stamp}.png"
            pg.screenshot(path=str(f))
            pg.evaluate("() => document.querySelectorAll('.__loi__').forEach(e => e.remove())")
            path = str(f.relative_to(self.cfg.screenshots_dir.parents[2]))
            self._result.error_images.append(path)
            if caption.get(account):
                self._result.error_image_captions[path] = " ".join(dict.fromkeys(caption[account]))
        for account, marks in all_marks.items():
            if not any(passed for _, passed in marks):
                continue
            pg = self.page_for(account or None)
            items = [[t, "green" if passed else "red"] for t, passed in dict.fromkeys(marks)]
            seen = dict(pg.evaluate(_JS_MARK, items))
            if not any(seen.get(t) for (t, passed) in dict.fromkeys(marks) if passed):
                pg.evaluate("() => document.querySelectorAll('.__loi__').forEach(e => e.remove())")
                continue
            self.cfg.screenshots_dir.mkdir(parents=True, exist_ok=True)
            f = self.cfg.screenshots_dir / f"{self._image_prefix}-kiem{('-' + account.lower()) if account else ''}-{stamp}.png"
            pg.screenshot(path=str(f))
            pg.evaluate("() => document.querySelectorAll('.__loi__').forEach(e => e.remove())")
            self._result.images.append(str(f.relative_to(self.cfg.screenshots_dir.parents[2])))
