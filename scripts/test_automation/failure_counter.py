"""Bộ đếm số lần đăng nhập sai liên tiếp, để không chạm ngưỡng chặn của hệ thống đang test.

KHÔNG có con số mặc định. Trần nhập sai (`login.max_consecutive_failures`) và thời gian chặn (`login.block_minutes`)
do requirement của dự án quy định, hoặc người kiểm thử cho biết; ghi vào `testing/<dự-án>/auto-config.json`.
Chưa khai thì thư viện TỪ CHỐI mọi lần cố ý nhập sai (ca thành "Không kết luận" kèm lý do), không tự đoán.

Quy tắc đếm (thận trọng, vì chỉ tin điều đã quan sát):
- Cộng dồn tổng số lần sai kể từ lần bộ đếm về 0. Đăng nhập đúng KHÔNG đưa bộ đếm về 0 (dự án đầu tiên 2026-11-19 đã thấy
  hệ thống không reset khi đăng nhập đúng, khác quy định BA; đếm cộng dồn luôn dừng sớm hơn, nên an toàn hơn).
- Bộ đếm về 0 khi hết thời gian chặn sau một lần 429 (cần `block_minutes`), hoặc người test đặt lại bằng tay
  (`python -X utf8 scripts/run_tests.py --reset-failure-counter`, chỉ khi chắc hệ thống đã về 0).
- Hệ thống trả 429 mà chưa khai `block_minutes`: không biết chặn bao lâu, dừng mọi lần nhập sai tới khi người test đặt lại.
- Trước mỗi lần cố ý nhập sai, thư viện hỏi bộ đếm; vượt trần thì từ chối.

Bộ đếm chỉ đếm những gì thư viện này gửi trên máy này; lần nhập tay của người khác hoặc máy khác không thấy được.
Tệp: `.phien-dang-nhap/<dự-án>/failure-counter.json` (đã .gitignore).
"""
import json
import time

UNKNOWN_BLOCK = "Hệ thống đã chặn đăng nhập nhưng chưa khai `login.block_minutes`: hỏi người kiểm thử hoặc xem requirement bao lâu, rồi đặt lại bộ đếm bằng --reset-failure-counter khi chắc đã hết chặn"
NO_CAP = "chưa khai trần nhập sai `login.max_consecutive_failures` trong auto-config.json: lấy từ requirement hoặc hỏi người kiểm thử, không tự đặt số"


def _file(cfg):
    return cfg.sessions_dir / "failure-counter.json"


def read(cfg):
    try:
        state = json.loads(_file(cfg).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"consecutive_failures": 0, "blocked_until": 0}
    if state.get("blocked_until", 0) and time.time() >= state["blocked_until"]:
        state = {"consecutive_failures": 0, "blocked_until": 0}   # hết chặn: coi như đếm lại từ 0 (theo quy định thời gian chặn của dự án)
        _write(cfg, state)
    return state


def reset(cfg):
    """Người dùng chắc chắn bộ đếm của hệ thống đã về 0 (đã chờ hết chặn, hoặc hệ thống mới)."""
    _write(cfg, {"consecutive_failures": 0, "blocked_until": 0})


def _write(cfg, state):
    cfg.sessions_dir.mkdir(parents=True, exist_ok=True)
    _file(cfg).write_text(json.dumps(state), encoding="utf-8")


def seconds_blocked(cfg):
    """Số giây còn bị chặn theo ghi nhận gần nhất (0 nếu không)."""
    return max(0, int(read(cfg).get("blocked_until", 0) - time.time()))


def block_message(cfg):
    """None nếu không đang chặn; ngược lại câu giải thích (kể cả khi chặn mà chưa biết bao lâu)."""
    state = read(cfg)
    if state.get("blocked_unknown"):
        return UNKNOWN_BLOCK
    wait = seconds_blocked(cfg)
    if wait:
        return f"hệ thống đang chặn đăng nhập theo ghi nhận trước đó, còn khoảng {wait} giây"
    return None


def refusal_reason(cfg):
    """None nếu được phép cố ý nhập sai thêm một lần; ngược lại câu giải thích vì sao từ chối."""
    maximum = cfg.max_consecutive_failures
    if maximum is None:
        return NO_CAP
    blocked = block_message(cfg)
    if blocked:
        return blocked
    state = read(cfg)
    if state.get("consecutive_failures", 0) + 1 > maximum:
        return (f"đã {state['consecutive_failures']} lần sai, thêm một lần nữa vượt trần {maximum} "
                "(đăng nhập đúng không đưa bộ đếm về 0; chờ hệ thống hết chặn hoặc đặt lại bằng tay nếu chắc chắn)")
    return None


def record(cfg, status):
    """Ghi kết quả một lần gửi form đăng nhập theo mã trả về của máy chủ."""
    state = read(cfg)
    if status in (400, 401):
        state["consecutive_failures"] = state.get("consecutive_failures", 0) + 1
    elif status == 429:
        if cfg.max_consecutive_failures is not None:
            state["consecutive_failures"] = cfg.max_consecutive_failures
        if cfg.block_minutes:
            state["blocked_until"] = time.time() + cfg.block_minutes * 60
        else:
            state["blocked_unknown"] = True
    else:
        return
    _write(cfg, state)
