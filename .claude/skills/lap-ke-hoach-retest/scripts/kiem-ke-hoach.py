#!/usr/bin/env python3
"""Kiểm file kế hoạch re-test của một bug: mọi chỗ trong mục "Phạm vi ảnh hưởng" của bug đều có trong kế hoạch.

Cách dùng (từ gốc repo):
    python -X utf8 .claude/skills/lap-ke-hoach-retest/scripts/kiem-ke-hoach.py testing/<dự-án>/<tính-năng>/retest/BUG-001-ke-hoach.md

Quy ước:
- File kế hoạch nằm ở `<tính-năng>/retest/BUG-nnn-ke-hoach.md`; bug tương ứng ở `<tính-năng>/bug/BUG-nnn.md` (hoặc `--bug`).
- Mỗi gạch đầu dòng trong "## Phạm vi ảnh hưởng" của bug có một "khóa": chữ trong cặp dấu huyền đầu tiên
  (ví dụ `NV0001`); không có dấu huyền thì lấy chữ trước dấu hai chấm. Khóa phải xuất hiện trong cột
  "Bước tái hiện cần làm lại" của kế hoạch VÀ trong cột "Đạt thì / Không đạt thì" (chỗ chưa đạt thì chưa đóng).
- Nếu có script `<tính-năng>/auto/retest-bug-nnn.py`: mọi khóa cũng phải có trong script và script không còn chỗ mẫu `"<…>"` chưa điền.
- Biến thể tối đa 3 (đánh số 1. 2. 3. trong cột "Biến thể nên thử").
- Bảng phải đủ 5 cột; có dòng "Build có bản sửa:" (có thể là `[chưa có số build]`).
Thoát mã 0 = đạt, 1 = có lỗi. Chỉ đọc, không sửa file.
"""
import argparse
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HEADER_COLS = ["Mã bug", "Bước tái hiện cần làm lại", "Biến thể nên thử", "Bằng chứng cần lưu", "Đạt thì / Không đạt thì"]


def section(text, title):
    out, on = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            on = line[3:].strip().lower().startswith(title.lower())
            continue
        if on:
            out.append(line)
    return out


def scope_keys(bug_text):
    keys = []
    for line in section(bug_text, "Phạm vi ảnh hưởng"):
        m = re.match(r"^\s*[-*]\s+(.*)", line)
        if not m:
            continue
        item = m.group(1)
        tick = re.search(r"`([^`]+)`", item)
        keys.append((tick.group(1) if tick else item.split(":")[0].strip()).strip())
    return keys


def split_row(line):
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return cells


def main():
    ap = argparse.ArgumentParser(description="Kiểm kế hoạch re-test với Phạm vi ảnh hưởng của bug")
    ap.add_argument("plan", help="file kế hoạch .md")
    ap.add_argument("--bug", help="file bug (mặc định suy từ tên file kế hoạch)")
    args = ap.parse_args()

    plan = Path(args.plan)
    if not plan.exists():
        print(f"Không có file {plan}")
        return 1
    m = re.match(r"^(BUG-\d+)", plan.name, re.I)
    bug_path = Path(args.bug) if args.bug else (plan.parent.parent / "bug" / f"{m.group(1).upper()}.md" if m else None)
    problems = []
    if not bug_path or not bug_path.exists():
        print(f"Không tìm thấy file bug ({bug_path}); dùng --bug <file>.")
        return 1

    plan_text = plan.read_text(encoding="utf-8")
    bug_text = bug_path.read_text(encoding="utf-8")

    rows = [l for l in plan_text.splitlines() if l.startswith("|")]
    if len(rows) < 3:
        problems.append("chưa có bảng 5 cột (cần dòng tiêu đề, dòng ngăn và ít nhất một dòng bug)")
    else:
        head = split_row(rows[0])
        if [h.replace("*", "").strip() for h in head] != HEADER_COLS:
            problems.append("hàng tiêu đề bảng không đúng 5 cột: " + " | ".join(HEADER_COLS))
        data = [split_row(r) for r in rows[2:]]
        for cells in data:
            if len(cells) != 5:
                problems.append(f"dòng bảng có {len(cells)} cột, cần 5: {cells[0][:40]}")
        if len(data) == 1 and len(data[0]) == 5:
            cells = data[0]
            variants = [x for x in re.split(r"<br\s*/?>", cells[2]) if re.match(r"^\s*\d+\.\s", x)]
            if len(variants) > 3:
                problems.append(f"có {len(variants)} biến thể, tối đa 3")
            for key in scope_keys(bug_text):
                if key.lower() not in cells[1].lower():
                    problems.append(f"chỗ trong Phạm vi ảnh hưởng chưa có trong cột 'Bước tái hiện cần làm lại': {key}")
                if key.lower() not in cells[4].lower():
                    problems.append(f"chỗ trong Phạm vi ảnh hưởng chưa nêu trong cột 'Đạt thì / Không đạt thì': {key}")
            if re.search(r"đóng", cells[4], re.I) is None or re.search(r"mở lại", cells[4], re.I) is None:
                problems.append("cột cuối phải nói rõ Đóng (đạt) và Mở lại (không đạt)")
        elif len(data) != 1:
            problems.append("mỗi file kế hoạch một bug: bảng cần đúng một dòng bug")

    if not scope_keys(bug_text):
        problems.append("bug không có mục 'Phạm vi ảnh hưởng' (hoặc không có gạch đầu dòng): hỏi người dùng phạm vi, không tự đoán")
    if not re.search(r"Build có bản sửa:", plan_text):
        problems.append("thiếu dòng 'Build có bản sửa:' (nếu chưa có thì ghi [chưa có số build])")
    if not section(bug_text, "Các bước tái hiện"):
        problems.append("bug thiếu mục 'Các bước tái hiện': đánh dấu và hỏi người dùng")

    keys = scope_keys(bug_text)
    # Script re-test (nếu đã có) phải phủ đủ từng chỗ trong phạm vi và không còn chỗ mẫu chưa điền.
    script = plan.parent.parent / "auto" / f"retest-{bug_path.stem.lower()}.py"
    note = f"Chưa có script re-test {script.parent.name}/{script.name} (làm tay hoặc viết theo assets/mau-retest-bug.py)."
    if script.exists():
        script_text = script.read_text(encoding="utf-8")
        note = f"Script re-test: {script.name}."
        for key in keys:
            if key.lower() not in script_text.lower():
                problems.append(f"chỗ trong Phạm vi ảnh hưởng chưa có trong script {script.name}: {key}")
        if re.search(r"[\"']<[^>\n]{2,60}>[\"']", script_text):
            problems.append(f"script {script.name} còn chỗ mẫu chưa điền (dạng \"<…>\")")
    if problems:
        print(f"KHÔNG ĐẠT ({plan.name} so với {bug_path.name}):")
        for p in problems:
            print("  -", p)
        return 1
    print(f"ĐẠT: {plan.name} phủ đủ {len(keys)} chỗ trong Phạm vi ảnh hưởng của {bug_path.name} ({', '.join(keys)}).")
    print("  "+note)
    return 0


if __name__ == "__main__":
    sys.exit(main())
