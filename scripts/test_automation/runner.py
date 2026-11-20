"""Lệnh chạy test case tự động: một ca, một tính năng hoặc cả bộ smoke.

Quy ước script test case: `testing/<dự-án>/<tính-năng>/auto/<mã-ca>.py` (mã ca viết thường, ví dụ tc-001) có
    CASE_INFO = {"ma": "TC-001", "ten": "...", "tai_khoan": ["NV01"]}   # [] = không cần đăng nhập
    def run(ctx): ...                                                      # dùng ctx.goto, ctx.wait_text, ctx.check_main...
Tùy chọn trong CASE_INFO: "invalidates_sessions": ["NV01"] nếu ca làm mất phiên (ví dụ bấm Đăng xuất).
"""
import argparse
import importlib.util
import re
import sys
import time
import traceback

from . import config, failure_counter, results, session
from .results import CaseResult
from .context import WaitTimeout, SessionExpired, PreconditionNotMet, Context


def read_system_version(cfg):
    """Số phiên bản hệ thống đang chạy (GET `health_api` của dự án, chỉ đọc). Không khai hoặc không đọc được → (None, lý do)."""
    if not cfg.health_api:
        return None, "dự án chưa khai health_api trong auto-config.json"
    import json
    import urllib.request
    try:
        with urllib.request.urlopen(cfg.url + cfg.health_api, timeout=15) as response:
            value = json.loads(response.read().decode("utf-8")).get(cfg.version_field)
    except Exception as error:  # noqa: BLE001
        return None, f"{type(error).__name__}: {error}"
    return (str(value), "") if value else (None, f"phản hồi không có trường {cfg.version_field}")


def print_system_version(cfg, bug_build=None):
    version, reason = read_system_version(cfg)
    if version is None:
        print(f"Số phiên bản hệ thống: không đọc được ({reason}).")
        return
    print(f"Số phiên bản hệ thống đang chạy: {version} (đọc từ {cfg.health_api}).")
    if bug_build:
        if str(bug_build) == version:
            print(f"  LƯU Ý: GIỐNG bản lúc bug được tạo ({bug_build}). Không phân biệt được bản sửa bằng số build; hãy chắc bản sửa đã được triển khai lên địa chỉ này.")
        else:
            print(f"  Khác bản lúc bug được tạo ({bug_build}).")


def read_smoke_table(cfg):
    """Đọc bảng smoke-test.md: [(số, tính năng, mã ca)] theo thứ tự cột #."""
    f = cfg.project_dir / "smoke-test.md"
    if not f.exists():
        raise config.ConfigError(f"Không có {f.relative_to(config.ROOT)}")
    seen = {}
    for line in f.read_text(encoding="utf-8").splitlines():
        m_so = re.match(r"^\|\s*(\d+)\s*\|", line)
        m_ca = re.search(r"\]\(([\w-]+)/test-case\.md#(tc-\d+)\)", line)
        if m_so and m_ca and m_so.group(1) not in seen:
            seen[m_so.group(1)] = (m_ca.group(1), m_ca.group(2))
    return [(number, *seen[number]) for number in sorted(seen, key=int)]


def find_cases_by_feature(cfg, feature):
    dir_path = cfg.project_dir / feature / "auto"
    return [(None, feature, f.stem) for f in sorted(dir_path.glob("tc-*.py"))] if dir_path.exists() else []


def load_script(path):
    dir_path = str(path.parent)
    if dir_path not in sys.path:
        sys.path.insert(0, dir_path)  # cho phép script dùng module chung cùng thư mục (ví dụ reco_common.py)
    spec = importlib.util.spec_from_file_location("auto_" + path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not hasattr(mod, "CASE_INFO") or not hasattr(mod, "run"):
        raise ValueError("Script thiếu CASE_INFO hoặc hàm run(ctx)")
    return mod


def run_single_case(browser, cfg, number, feature, case_code, record_video=True):
    label = f"{feature}/{case_code}"
    kq = CaseResult(case_id=label, smoke_number=number or "")
    path = cfg.project_dir / feature / "auto" / f"{case_code}.py"
    if not path.exists():
        kq.verdict, kq.reason = results.NO_SCRIPT, f"Chưa có {path.relative_to(config.ROOT)}"
        return kq
    start = time.time()
    ctx = None
    mod = None
    try:
        mod = load_script(path)
        kq.code, kq.title = mod.CASE_INFO.get("code", case_code.upper()), mod.CASE_INFO.get("title", "")
        info = dict(mod.CASE_INFO)
        info.setdefault("record_video", record_video)
        ctx = Context(cfg, browser, info, kq, f"{feature}-{case_code}")
        if mod.CASE_INFO.get("ready_account"):
            ctx.verify_account_ready(mod.CASE_INFO["ready_account"])  # ca có nhập sai: chắc tài khoản dùng được, chưa bị chặn
        mod.run(ctx)
        kq.compute_verdict()
        try:
            ctx.capture_error_screenshots()  # ý sai có khai mark_text → thêm ảnh tô đỏ chỗ lỗi
        except Exception as error:  # noqa: BLE001
            print(f"  (không chụp được ảnh tô đỏ chỗ lỗi: {type(error).__name__}: {error})")
    except SessionExpired as error:
        kq.verdict, kq.reason = results.NO_VERDICT, f"Phiên hết hạn: {error}. Đăng nhập lại rồi chạy tiếp"
    except PreconditionNotMet as error:
        kq.verdict, kq.reason = results.NO_VERDICT, str(error)
    except WaitTimeout as error:
        kq.verdict, kq.reason = results.NO_VERDICT, f"{error}. Xem ảnh, kiểm script hay trang chậm trước khi kết luận"
        _capture_error_screenshot(ctx, kq)
    except Exception as error:  # noqa: BLE001
        first_line = (str(error).splitlines() or [""])[0]
        kq.verdict, kq.reason = results.NO_VERDICT, f"Lỗi script: {type(error).__name__}: {first_line}"
        print(traceback.format_exc())
        _capture_error_screenshot(ctx, kq)
    finally:
        if ctx:
            ctx.line()
            try:
                ctx.finalize_videos(keep=kq.verdict in (results.FAIL, results.PASS_MINOR_FAIL))
            except Exception as error:  # noqa: BLE001
                print(f"  (không xử lý được video: {type(error).__name__}: {error})")
        if mod is not None:
            for account in mod.CASE_INFO.get("invalidates_sessions", []):
                session.delete_session(cfg, account)  # phiên đã mất ở máy chủ, đừng dùng lại nhầm
        kq.seconds = round(time.time() - start, 1)
    return kq


def _capture_error_screenshot(ctx, kq):
    if ctx is None:
        return
    try:
        ctx.screenshot("loi")
    except Exception:  # noqa: BLE001
        pass


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Chạy test case tự động (Playwright)")
    ap.add_argument("--project", help="slug dự án (mặc định đọc .du-an-hien-tai)")
    ap.add_argument("--reset-failure-counter", action="store_true",
                    help="đặt bộ đếm lần nhập sai về 0 (chỉ khi chắc hệ thống đã về 0, ví dụ đã chờ hết chặn) rồi thoát")
    group = ap.add_mutually_exclusive_group(required=False)
    group.add_argument("--smoke", action="store_true", help="chạy các ca trong smoke-test.md theo thứ tự")
    group.add_argument("--feature", help="chạy mọi script trong <tính-năng>/auto/, ví dụ dang-nhap")
    group.add_argument("--case-id", action="append", help="một ca dạng <tính-năng>/<mã>, ví dụ dang-nhap/tc-001 (dùng nhiều lần được)")
    ap.add_argument("--no-video", action="store_true", help="không quay video (mặc định quay mọi ca, chỉ giữ video của ca Không đạt hoặc Đạt kèm ý phụ sai)")
    ap.add_argument("--headed", action="store_true", help="hiện cửa sổ trình duyệt (gỡ lỗi)")
    ap.add_argument("--record-run", action="store_true",
                    help="(chỉ với --smoke) ghi kết quả thành một lượt mới và sinh lại smoke-ket-qua.md + .html; cần --conclusion-file")
    ap.add_argument("--conclusion-file", help="file JSON kết luận và rủi ro của lượt (bắt buộc khi --record-run)")
    ap.add_argument("--bug-build", help="số bản lúc bug được tạo (re-test): in so với số phiên bản hệ thống đang chạy trước khi chạy ca")
    ap.add_argument("--build", help="số bản đang test, bắt buộc khi --record-run (mặc định lấy `version` trong auto-data.json)")
    ap.add_argument("--run-by", default=None, help="người chạy, ghi vào lượt; mặc định lấy từ .nguoi-test")
    args = ap.parse_args(argv)
    if args.reset_failure_counter:
        cfg = config.load(args.project)
        failure_counter.reset(cfg)
        print("Đã đặt bộ đếm lần nhập sai về 0.")
        return results.EXIT_OK
    if not (args.smoke or args.feature or args.case_id):
        ap.error("cần một trong --smoke, --feature, --case-id (hoặc --reset-failure-counter)")
    if args.record_run and not args.smoke:
        print("--record-run chỉ dùng với --smoke (chạy cả bộ để lượt đủ case).")
        return results.EXIT_CONFIG

    try:
        cfg = config.load(args.project)
        print(cfg.banner())
        print_system_version(cfg, args.bug_build)
        if args.smoke:
            entries = read_smoke_table(cfg)
        elif args.feature:
            entries = find_cases_by_feature(cfg, args.feature)
        else:
            entries = []
            for case_id in args.case_id:
                feature, _, case_code = case_id.partition("/")
                if not case_code:
                    raise config.ConfigError(f"--case-id phải dạng <tính-năng>/<mã>, nhận được '{case_id}'")
                entries.append((None, feature, case_code.lower()))
    except config.ConfigError as error:
        print(error)
        return results.EXIT_CONFIG
    if not entries:
        print("Không có ca nào để chạy.")
        return results.EXIT_CONFIG

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Chưa cài Playwright. Xem docs/chay-test-tu-dong.md, mục Cài một lần.")
        return results.EXIT_CONFIG

    result_list = []
    with sync_playwright() as p:
        browser = session.launch_browser(p, headless=not args.headed)

        # Kiểm nhanh phiên của mọi tài khoản cần dùng trước khi chạy ca nào.
        needed = set()
        for _, feature, case_code in entries:
            path = cfg.project_dir / feature / "auto" / f"{case_code}.py"
            if path.exists():
                try:
                    needed.update(t.upper() for t in load_script(path).CASE_INFO.get("accounts", []))
                except Exception:  # noqa: BLE001
                    pass  # lỗi script sẽ báo ở ca đó
        bad_sessions = {account: session.session_status(browser, cfg, account) for account in sorted(needed)}
        bad_sessions = {account: state for account, state in bad_sessions.items() if state != "ok"}
        if bad_sessions:
            print("Phiên chưa dùng được, chưa chạy ca nào:")
            for account, state in bad_sessions.items():
                print(f"  {account}: {'chưa có phiên đã lưu' if state == 'missing' else 'đã hết hạn'}")
            print("Đăng nhập lại: python -X utf8 scripts/auto_login.py " + " ".join(bad_sessions) + (" --manual" if cfg.login_mode == "manual" else " --headless"))
            print(f"(phiên chỉ sống khoảng {cfg.session_minutes} phút, chạy test ngay sau khi đăng nhập)")
            browser.close()
            return results.EXIT_SESSION

        for number, feature, case_code in entries:
            kq = run_single_case(browser, cfg, number, feature, case_code, record_video=not args.no_video)
            if kq.checks:
                results.print_details(kq)
            else:
                print(f"--- {kq.case_id}: {kq.verdict}" + (f" ({kq.reason})" if kq.reason else ""))
            result_list.append(kq)
        browser.close()

    results.print_table(result_list)
    f = results.write_json(cfg, result_list)
    print(f"Kết quả chi tiết: {f.relative_to(config.ROOT)}")
    if args.record_run:
        from dataclasses import asdict

        from . import report

        build = args.build or cfg.test_data.get("version")
        if not build:
            print("Không ghi lượt: thiếu --build (và auto-data.json không có `version`).")
        elif not args.conclusion_file:
            print("Chưa ghi lượt: lượt smoke cần phần Kết luận và rủi ro. Viết file JSON kết luận rồi chạy:\n"
                  f"  python -X utf8 scripts/build_report.py add-run --suite smoke --build {build} "
                  f"--results-files {f.relative_to(config.ROOT)} --conclusion-file <kết-luận.json>")
        else:
            import json as _json
            try:
                run_record = report.add_run(cfg, "smoke", build, [asdict(kq) for kq in result_list], run_by=args.run_by or config.default_author(),
                                              sources=[str(f.relative_to(config.ROOT))],
                                              conclusion=_json.loads(open(args.conclusion_file, encoding="utf-8").read()))
                print(f"Đã ghi lượt {run_record['number']} (build {build}): {run_record['verdict']} — xem testing/{cfg.project}/smoke-ket-qua.md và .html")
            except report.ConclusionError as error:
                print(error)
    return results.exit_code(result_list)
