"""Kiểm tra, kết luận và ghi kết quả chạy.

Nguyên tắc: chỉ kết luận Đạt/Không đạt khi script chạy trọn vẹn. Script lỗi, chờ quá hạn hoặc
phiên hết hạn thì KHÔNG kết luận (tránh báo Không đạt giả).
"""
import json
import time
from dataclasses import asdict, dataclass, field

PASS = "Đạt"
PASS_MINOR_FAIL = "Đạt kèm ý phụ sai"
FAIL = "Không đạt"
NO_VERDICT = "Không kết luận"
NO_SCRIPT = "Chưa có script"

# Ý nghĩa mã thoát của lệnh chạy
EXIT_OK = 0
EXIT_FAIL = 1
EXIT_CONFIG = 2
EXIT_SESSION = 3
EXIT_NO_VERDICT = 4


@dataclass
class Check:
    kind: str  # "chinh" | "phu"
    title: str
    passed: bool
    note: str = ""
    mark_text: list = field(default_factory=list)  # chữ trên trang cần tô đỏ khi ý này sai
    account: str = ""  # tài khoản/trang chứa chữ đó (rỗng = trang mặc định)
    error_note: str = ""  # câu mô tả lỗi ở bước nào, in dưới ảnh tô đỏ


@dataclass
class CaseResult:
    case_id: str  # ví dụ dang-nhap/tc-001
    code: str = ""
    title: str = ""
    smoke_number: str = ""
    verdict: str = NO_VERDICT
    reason: str = ""
    checks: list = field(default_factory=list)
    images: list = field(default_factory=list)
    error_images: list = field(default_factory=list)  # ảnh đã tô đỏ chỗ lỗi
    error_image_captions: dict = field(default_factory=dict)  # đường dẫn ảnh tô đỏ -> câu mô tả lỗi ở bước nào
    videos: list = field(default_factory=list)  # video quay lại ca (chỉ giữ khi ca Không đạt hoặc Đạt kèm ý phụ sai)
    seconds: float = 0.0

    def compute_verdict(self):
        main_checks = [k for k in self.checks if k.kind == "main"]
        minor_checks = [k for k in self.checks if k.kind == "minor"]
        if not main_checks:
            self.verdict, self.reason = NO_VERDICT, "Script không có ý chính nào (check_main)"
        elif not all(k.passed for k in main_checks):
            self.verdict = FAIL
            self.reason = "Sai ý chính: " + "; ".join(k.title for k in main_checks if not k.passed)
        elif not all(k.passed for k in minor_checks):
            self.verdict = PASS_MINOR_FAIL
            self.reason = "Sai ý phụ: " + "; ".join(k.title for k in minor_checks if not k.passed)
        else:
            self.verdict, self.reason = PASS, ""


def print_details(kq):
    print(f"--- {kq.case_id} {kq.title} ---")
    for kind, label in (("main", "Ý chính"), ("minor", "Ý phụ")):
        entries = [k for k in kq.checks if k.kind == kind]
        if entries:
            print(f"{label}:")
            for k in entries:
                print(f"  [{'ĐẠT' if k.passed else 'KHÔNG ĐẠT'}] {k.title}" + (f" — {k.note}" if k.note else ""))
    for a in kq.images:
        print(f"Ảnh: {a}")
    for a in kq.videos:
        print(f"Video: {a}")
    for a in kq.error_images:
        print(f"Ảnh tô đỏ chỗ lỗi: {a}" + (f" — {kq.error_image_captions[a]}" if a in kq.error_image_captions else ""))
    print(f"KẾT LUẬN: {kq.verdict}" + (f" ({kq.reason})" if kq.reason else ""))


def print_table(entries):
    print("\n| # smoke | Ca | Kết luận | Ghi chú |")
    print("|---|---|---|---|")
    for kq in entries:
        print(f"| {kq.smoke_number or '-'} | {kq.case_id} | {kq.verdict} | {kq.reason} |")
    counts = {}
    for kq in entries:
        counts[kq.verdict] = counts.get(kq.verdict, 0) + 1
    print("\nTổng: " + ", ".join(f"{v} {k}" for k, v in counts.items()))


def exit_code(entries):
    if any(kq.verdict == FAIL for kq in entries):
        return EXIT_FAIL
    if any(kq.verdict in (NO_VERDICT, NO_SCRIPT) for kq in entries):
        return EXIT_NO_VERDICT
    return EXIT_OK


def write_json(cfg, entries):
    cfg.screenshots_dir.mkdir(parents=True, exist_ok=True)
    f = cfg.screenshots_dir / f"result-{time.strftime('%Y%m%d-%H%M%S')}.json"
    content = {
        "project": cfg.project,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "results": [asdict(kq) for kq in entries],
    }
    f.write_text(json.dumps(content, ensure_ascii=False, indent=2), encoding="utf-8")
    return f
