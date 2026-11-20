#!/usr/bin/env python3
"""Bảng tổng hợp nhiều bug cần re-test: mức độ nghiêm trọng (giảm dần), lần re-test gần nhất, có kế hoạch/script chưa.

Chỉ đọc, chỉ in ra màn hình (không tạo file nên không bị cũ). Bug chưa có mục `## Lịch sử re-test` ghi "Chưa re-test".
Mặc định liệt kê MỌI bug của dự án (kể cả bug chưa sửa); chọn bug đã sửa bằng --bug. Cột "Trạng thái" đọc mục `## Trạng thái`
trong file bug (người dùng chốt, ghi bằng dat-trang-thai-bug.py); bug chưa có mục đó ghi "Chưa ghi".

Ví dụ (từ gốc repo):
    python -X utf8 .claude/skills/lap-ke-hoach-retest/scripts/tong-hop-retest.py                 # dự án hiện tại (.du-an-hien-tai)
    python -X utf8 .claude/skills/lap-ke-hoach-retest/scripts/tong-hop-retest.py --bug 001 004   # chỉ các bug này
    python -X utf8 .claude/skills/lap-ke-hoach-retest/scripts/tong-hop-retest.py --du-an <slug>
"""
import argparse
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[4]
RANK = {"nghiêm trọng": 0, "lớn": 1, "nặng": 1, "nhỏ": 2, "rất nhỏ": 3}


def severity(text):
    m = re.search(r"^## Mức độ nghiêm trọng\s*\n+\s*\*\*([^*]+?)\.?\*\*", text, re.M)
    word = m.group(1).strip() if m else "chưa rõ"
    return word, RANK.get(word.lower(), 4)


def last_retest(text):
    found = re.findall(r"^\*\*Lần (\d+): ([^*]+?)\.\*\*", text, re.M)
    if not found:
        return "Chưa re-test"
    n, rest = max(found, key=lambda x: int(x[0]))
    return f"Lần {n}, {rest.strip()}"


def plan_build(plan_file):
    """Số build ghi ở dòng 'Build có bản sửa:' của kế hoạch; None nếu chưa có số (còn [chưa có số build])."""
    if not plan_file.exists():
        return None
    m = re.search(r"Build có bản sửa:\s*(.+)", plan_file.read_text(encoding="utf-8"))
    if not m or "chưa có số build" in m.group(1).lower():
        return None
    nums = re.findall(r"\d+(?:\.\d+)+", m.group(1))
    return nums[0] if nums else m.group(1).strip()[:20]


def bug_status(text):
    """Trạng thái người dùng đã chốt ở mục `## Trạng thái` của file bug (ghi bằng dat-trang-thai-bug.py); chưa có thì 'Chưa ghi'."""
    m = re.search(r"^## Trạng thái\s*\n+\s*\*\*([^*]+?)\.?\*\*", text, re.M)
    return m.group(1).strip() if m else "Chưa ghi"


def next_step(plan, build, last, status="Chưa ghi"):
    """Gợi ý việc tiếp theo, suy từ file có sẵn (chỉ là gợi ý: trạng thái chính thức do công cụ của team giữ)."""
    if status == "Đóng":
        return "Đã đóng; còn file kế hoạch thì hỏi người dùng xóa" if plan else "Đã đóng, không cần làm gì thêm"
    low = last.lower()
    if not plan:
        return "Lập kế hoạch" if low == "chưa re-test" else "Đã re-test nhưng chưa có kế hoạch: lập kế hoạch cho khớp"
    if low == "chưa re-test":
        return f"Chạy re-test (build {build})" if build else "Hỏi người dùng số build có bản sửa, rồi chạy re-test"
    if "không đạt" in low:
        return f"Chạy lại với build {build} nếu chưa chạy bản này" if build else "Chờ build mới (hỏi người dùng đã triển khai chưa)"
    return "Hỏi người dùng chốt Đóng, rồi chạy can-cap-nhat-khi-dong.py"


def main():
    ap = argparse.ArgumentParser(description="Tổng hợp re-test nhiều bug")
    ap.add_argument("--du-an", help="slug dự án (mặc định đọc .du-an-hien-tai)")
    ap.add_argument("--bug", nargs="+", help="chỉ các bug này, ví dụ 001 004 hoặc BUG-001")
    args = ap.parse_args()

    slug = args.du_an or (ROOT / ".du-an-hien-tai").read_text(encoding="utf-8").strip()
    base = ROOT / "testing" / slug
    if not base.exists():
        print(f"Không có thư mục {base}")
        return 1
    want = {re.sub(r"\D", "", b).zfill(3) for b in args.bug} if args.bug else None

    rows = []
    for f in sorted(base.glob("*/bug/BUG-*.md")):
        code = f.stem
        if want and re.sub(r"\D", "", code).zfill(3) not in want:
            continue
        text = f.read_text(encoding="utf-8")
        title = (text.splitlines() or [""])[0].lstrip("# ").strip()
        sev, rank = severity(text)
        feature = f.parent.parent
        plan = (feature / "retest" / f"{code}-ke-hoach.md").exists()
        script = (feature / "auto" / f"retest-{code.lower()}.py").exists()
        last = last_retest(text)
        build = plan_build(feature / "retest" / f"{code}-ke-hoach.md")
        status = bug_status(text)
        rows.append((rank, code, title, sev, status, last, plan, script, feature.name, next_step(plan, build, last, status)))
    if not rows:
        print("Không có bug nào khớp.")
        return 0

    rows.sort(key=lambda r: (r[0], r[1]))
    print(f"Dự án {slug}: {len(rows)} bug, xếp theo mức độ nghiêm trọng giảm dần.\n")
    print("| Mã bug | Tính năng | Tiêu đề | Mức độ | Trạng thái | Re-test gần nhất | Kế hoạch | Script | Việc tiếp theo (gợi ý) |")
    print("|---|---|---|---|---|---|---|---|---|")
    for rank, code, title, sev, status, last, plan, script, feature, nxt in rows:
        print(f"| {code} | {feature} | {title[:70]} | {sev} | {status} | {last} | {'có' if plan else 'chưa'} | {'có' if script else 'chưa'} | {nxt} |")
    print("\nCột 'Trạng thái' = điều người dùng đã chốt và ghi vào file bug (dat-trang-thai-bug.py); 'Chưa ghi' = chưa ai chốt trong kho. Trạng thái chính thức do công cụ của team giữ. Cột 'Kế hoạch' = có file kế hoạch đang theo dõi (xóa khi bug đóng, xem SKILL.md). Cột gợi ý chỉ suy từ file có sẵn.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
