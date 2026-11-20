#!/usr/bin/env python3
"""Tự soạn đoạn "Lần N" cho mục `## Lịch sử re-test` của bug từ file kết quả `result-*.json` của lần chạy.

Mặc định chỉ IN bản xem trước. Thêm `--ghi` mới ghi vào cuối file bug (tạo mục nếu chưa có, đánh số lần tiếp theo).
Không sửa phần khác của bug, không đổi trạng thái chính thức của bug.

Ví dụ (từ gốc repo):
    python -X utf8 .claude/skills/lap-ke-hoach-retest/scripts/ghi-lich-su-retest.py \\
        testing/<dự-án>/<tính-năng>/bug/BUG-001.md --ket-qua evidence/<dự-án>/chay-test/result-20261119-161706.json \\
        --phien-ban 1.3.0 [--ghi-chu "câu thêm"] [--ghi]

Quy ước đọc kết quả: ý chính (`main`) = điều kiện đóng bug; ý phụ (`minor`) = biến thể, không tính vào điều kiện đóng.
Ý chính nào sai hoặc ca "Không kết luận" thì KHÔNG đề nghị Đóng. Nhiều file kết quả (nhiều ca) thì gộp thành một lần.
Sau khi ghi: chạy `build_docs.py --all` và `kiem-tra-bug.py --du-an` (script nhắc).
"""
import argparse
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SECTION = "## Lịch sử re-test"


def norm(path):
    return str(path).replace("\\", "/")


def build_entry(bug_text, results_files, version, note, n):
    runs = []
    for f in results_files:
        data = json.loads(Path(f).read_text(encoding="utf-8"))
        runs.append((f, data))
    stamp = runs[0][1].get("timestamp", "")
    m = re.match(r"(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2})", stamp)
    when = f"{m.group(1)} lúc {m.group(2)}" if m else stamp or "(không rõ giờ)"

    main_checks, minor_checks, images, errors, verdicts = [], [], [], [], []
    for _, data in runs:
        for r in data.get("results", []):
            verdicts.append(r.get("verdict", ""))
            main_checks += [c for c in r.get("checks", []) if c.get("kind") == "main"]
            minor_checks += [c for c in r.get("checks", []) if c.get("kind") != "main"]
            images += r.get("images", [])
            errors += r.get("error_images", [])
    no_verdict = any(v in ("Không kết luận", "Chưa có script") for v in verdicts)
    main_fail = [c for c in main_checks if not c["passed"]]

    if no_verdict:
        head = "KHÔNG KẾT LUẬN được (script lỗi, phiên hết hạn hoặc điều kiện trước sai), chưa đề nghị Đóng hay Mở lại"
    elif main_fail:
        head = "KHÔNG ĐẠT, đề nghị Mở lại"
    else:
        head = "ĐẠT, đề nghị Đóng"

    lines = [f"**Lần {n}: {when}: {head}.** Chạy tự động"
             + (f", số phiên bản hệ thống đọc được là {version}" if version else ", chưa đọc được số phiên bản hệ thống") + "."]
    bug_build = re.search(r"Số build:\s*([^\r\n]+)", bug_text)
    if version and bug_build and version.strip() == bug_build.group(1).strip():
        lines.append(f"Số phiên bản GIỐNG bản lúc tạo bug ({version}): không phân biệt được bản sửa bằng số build; "
                     "chưa biết bản sửa đã được triển khai lên địa chỉ này chưa, nên kết quả chưa đủ căn cứ nói bản sửa đúng hay sai.")
    if note:
        lines.append(note)
    if main_checks:
        lines.append(f"- Điều kiện đóng bug: {len(main_checks) - len(main_fail)}/{len(main_checks)} ý đạt.")
        for c in main_fail:
            lines.append(f"  - Không đạt: {c['title']}" + (f" ({c['note']})" if c.get("note") else ""))
    if minor_checks:
        lines.append("- Biến thể và ý phụ (không tính vào điều kiện đóng):")
        for c in minor_checks:
            lines.append(f"  - {'Đạt' if c['passed'] else 'Không đạt'}: {c['title']}" + (f" ({c['note']})" if c.get("note") else ""))
    for f, _ in runs:
        lines.append(f"- Kết quả chạy: `{norm(f)}`")
    if errors:
        lines.append("- Ảnh tô đỏ chỗ lỗi: " + ", ".join(f"`{norm(p)}`" for p in dict.fromkeys(errors)))
    if images:
        lines.append("- Ảnh màn hình: " + ", ".join(f"`{norm(p)}`" for p in dict.fromkeys(images)))
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Soạn đoạn Lịch sử re-test từ file kết quả")
    ap.add_argument("bug", help="file BUG-nnn.md")
    ap.add_argument("--ket-qua", nargs="+", required=True, help="một hoặc nhiều file result-*.json của lần chạy")
    ap.add_argument("--phien-ban", help="số phiên bản hệ thống đang chạy (runner in ở đầu lần chạy)")
    ap.add_argument("--ghi-chu", help="câu thêm (ví dụ: người dùng báo bản sửa đã deploy lúc …)")
    ap.add_argument("--ghi", action="store_true", help="ghi vào cuối file bug (mặc định chỉ in bản xem trước)")
    args = ap.parse_args()

    bug = Path(args.bug)
    missing = [f for f in args.ket_qua if not Path(f).exists()]
    if not bug.exists() or missing:
        print("Không có file: " + ", ".join([str(bug)] * (not bug.exists()) + missing))
        return 1
    raw = bug.read_text(encoding="utf-8")
    nl = "\r\n" if "\r\n" in raw else "\n"
    text = raw.replace("\r\n", "\n")

    has_section = SECTION in text
    numbers = [int(x) for x in re.findall(r"^\*\*Lần (\d+)", text, re.M)]
    n = (max(numbers) + 1) if numbers else 1
    entry = build_entry(text, args.ket_qua, args.phien_ban, args.ghi_chu, n)

    if not args.ghi:
        print("(xem trước, chưa ghi; thêm --ghi để ghi vào " + bug.name + ")\n")
        print(entry)
        return 0

    plan = bug.parent.parent / "retest" / f"{bug.stem}-ke-hoach.md"
    addition = ""
    if not has_section:
        addition += f"\n{SECTION}\n"
        if plan.exists():
            addition += f"Kế hoạch: [{plan.name}](../retest/{plan.name}).\n"
        addition += "Trạng thái chính thức của bug do công cụ của team giữ; mục này chỉ là lịch sử các lần re-test.\n"
    addition += "\n" + entry + "\n"
    new = text.rstrip("\n") + "\n" + addition
    bug.write_text(new.replace("\n", nl), encoding="utf-8", newline="")
    print(f"Đã ghi Lần {n} vào {bug}. Chạy tiếp:")
    print("  python -X utf8 scripts/build_docs.py --all")
    print("  python -X utf8 .claude/skills/tao-bug-report/scripts/kiem-tra-bug.py --du-an")
    return 0


if __name__ == "__main__":
    sys.exit(main())
