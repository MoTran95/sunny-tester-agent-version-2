#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Kiểm test plan trước khi trả cho người dùng: đúng khuôn, không lẫn kết quả test, không nhãn nháp, link không gãy; liệt kê chỗ còn trống để hỏi người test.

  python -X utf8 .claude/skills/tao-test-plan/scripts/kiem-tra-test-plan.py <dự-án> [--file test-plan-1.4.0.md]

Mặc định kiểm `testing/<dự-án>/test-plan.md`. In:
  LỖI      phải sửa (thiếu mục, có kết quả test, nhãn nháp, chỗ điền `<...>` chưa điền, link gãy, trang HTML còn logo)
  CÒN TRỐNG các ô `……` chưa điền (không phải lỗi: người test chưa cung cấp; hỏi họ, không tự đặt số hay tên)
Thoát mã 1 nếu có LỖI.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]

SECTIONS = [  # (số, từ khóa trong tiêu đề)
    (1, "Mục tiêu"), (2, "Phạm vi"), (3, "Cách kiểm thử"), (4, "Môi trường"), (5, "Tiêu chí"), (6, "Phân công"),
    (7, "Quản lý bug"), (8, "Sản phẩm bàn giao"), (9, "Rủi ro"), (10, "Truy vết"), (11, "Phê duyệt"), (12, "Lịch sử"),
]

# Test plan là phần CHƯA test: không được có kết quả test (người dùng dặn 2026-11-19).
RESULT_PATTERNS = [
    (r"\b\d+\s+(?:case\s+)?(?:Đạt|Không đạt|Bị chặn|Bỏ qua|Chưa chạy)\b", "số case theo kết quả (Đạt/Không đạt/…)"),
    (r"\b(?:Đạt|Không đạt|Bị chặn)\s*:\s*\d+", "kết quả dạng Đạt: n"),
    (r"đã chạy\s+\d+|\d+\s+(?:trên|/)\s*\d+\s*(?:case|test case|ca)\b.*đã chạy|đã chạy\s+(?:smoke|regression|\d)", "nói đã chạy test"),
    (r"\bBUG-\d+", "mã bug đã ghi (bug là kết quả test)"),
    (r"[Ll]ượt\s*\d+|\blượt chạy\s+\d", "nhắc lượt chạy cụ thể"),
    (r"Hiện trạng|Tình trạng thực hiện\b|Đạt kèm ý phụ sai|chưa kết luận|Không kết luận", "cột/dòng hiện trạng hoặc kết luận lượt chạy"),
]
DRAFT_PATTERNS = [
    (r"Giả định H\d|\(H\d+\)", "nhãn giả định/mã câu hỏi H…"),
    (r"❓", "dấu ❓ (dùng `……………` cho ô chờ điền)"),
    (r"Bản nháp để thử|soạn bằng Claude|chờ sếp xác nhận|bản nháp để", "chú thích nháp/thử"),
    (r"Khuôn dùng\b.*_template", "dòng 'Khuôn dùng' (không cần trong bản gửi đi)"),
]
PLACEHOLDER = re.compile(r"<(?!/?(?:a|br|b|i|code|details|summary|table|tr|td|th)\b)[^>\n]{1,80}>")
BLANK = re.compile(r"…{2,}")


def strip_code(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "``", text)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project")
    ap.add_argument("--file", default="test-plan.md")
    a = ap.parse_args()
    f = ROOT / "testing" / a.project / a.file
    if not f.exists():
        print(f"Không thấy {f}")
        return 1
    raw = f.read_text(encoding="utf-8")
    text = strip_code(raw)
    errors, blanks = [], []
    lines = raw.splitlines()

    heads = {}
    for i, ln in enumerate(lines, 1):
        m = re.match(r"^##\s+(\d+)\.\s+(.*)", ln)
        if m:
            heads[int(m.group(1))] = (i, m.group(2))
    gon = a.file.endswith("-gon.md")
    for n, kw in SECTIONS:
        if gon and n not in (1, 2, 3, 5, 9, 10):
            continue
        if n not in heads:
            errors.append(f"thiếu mục {n} ({kw})")
        elif kw.lower() not in heads[n][1].lower():
            errors.append(f"dòng {heads[n][0]}: mục {n} phải có chữ '{kw}' trong tiêu đề, đang là '{heads[n][1]}'")
    if not lines or not lines[0].startswith("# "):
        errors.append("dòng đầu phải là tiêu đề `# Kế hoạch kiểm thử (Test plan) — …`")

    for i, ln in enumerate(strip_code("\n".join(lines)).splitlines(), 1):
        for pat, why in RESULT_PATTERNS + DRAFT_PATTERNS:
            if re.search(pat, ln):
                errors.append(f"dòng {i}: {why}: «{lines[i - 1].strip()[:90]}»")
        if PLACEHOLDER.search(ln):
            errors.append(f"dòng {i}: còn chỗ điền chưa điền `{PLACEHOLDER.search(ln).group(0)}`")
        if BLANK.search(ln):
            blanks.append((i, lines[i - 1].strip()))

    for m in re.finditer(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", raw):
        target = m.group(1)
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        if not (f.parent / target).exists():
            line = raw[: m.start()].count("\n") + 1
            errors.append(f"dòng {line}: link gãy → {target}")

    if "{{" in raw:
        errors.append("còn dấu {{…}} chưa được thay: chạy lại `sinh-test-plan.py sinh`")
    stem = f.stem
    nguon = f.parent / f"{stem}-nguon.txt"
    if nguon.exists() and not gon:
        r = subprocess.run([sys.executable, "-X", "utf8", str(Path(__file__).with_name("sinh-test-plan.py")), "kiem", a.project, "--ten", stem], capture_output=True, text=True, encoding="utf-8")
        if r.returncode != 0:
            errors.append((r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout + r.stderr).strip() else "test-plan.md lệch bản sinh từ nguồn")
    elif not gon:
        print(f"LƯU Ý  chưa có {stem}-nguon.txt: số liệu trong test plan đang gõ tay, không tự đối chiếu được với nguồn (nên chuyển sang nguồn, xem SKILL.md bước 3)")
        print()

    html = f.with_suffix(".html")
    if not html.exists():
        errors.append("chưa có trang HTML cạnh file md: chạy `python -X utf8 scripts/build_docs.py --all`")
    else:
        h = html.read_text(encoding="utf-8")
        if 'class="brand"' in h:
            errors.append("trang HTML còn logo (test plan không có logo): kiểm `clean` trong docs_pages.py")
        if "Trang tự sinh từ file markdown" in h:
            errors.append("trang HTML còn dòng 'Trang tự sinh…' (test plan gửi đi không có dòng này)")

    for e in errors:
        print("LỖI    ", e)
    print(f"\nCÒN TRỐNG: {len(blanks)} dòng có ô `……` chưa điền" + (" (hỏi người test, không tự đặt số hay tên):" if blanks else "."))
    for i, ln in blanks:
        print(f"  dòng {i}: {ln[:110]}")
    print(f"\n{len(errors)} lỗi.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
