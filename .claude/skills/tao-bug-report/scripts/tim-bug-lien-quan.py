#!/usr/bin/env python3
"""Trước khi tạo bug cho một ca Không đạt: tìm bug đã có nhắc tới đúng test case đó, để không tạo bug trùng.

    python -X utf8 .claude/skills/tao-bug-report/scripts/tim-bug-lien-quan.py <dự-án> <tính-năng>/TC-005 [<tính-năng>/TC-006 ...]

In mỗi bug có nhắc mã test case (trong thư mục bug của đúng tính năng): mã, tiêu đề, trạng thái đã ghi (mục `## Trạng thái`,
không có thì "Chưa ghi"). Bug chưa Đóng = **đang mở**: nếu ca lần này sai cùng chỗ thì nối bug cũ (`--bug "N=BUG-nnn"`),
không tạo bug mới. Bug đã Đóng mà lỗi quay lại: đề xuất Mở lại bug đó (skill lap-ke-hoach-retest), hỏi người dùng.
Cũng báo nếu test case đang ghi "Đạt kèm lỗi đã biết" ở smoke (lỗi đã có bug). Chỉ đọc. Thoát mã 1 nếu có bug đang mở.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def status_of(text):
    m = re.search(r"^## Trạng thái\s*\n+\s*\*\*([^*]+?)\.?\*\*", text, re.M)
    return m.group(1).strip() if m else "Chưa ghi"


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    slug, targets = sys.argv[1], sys.argv[2:]
    any_open = False
    smoke = os.path.join(ROOT, "testing", slug, "smoke-test.md")
    smoke_text = read(smoke) if os.path.exists(smoke) else ""
    for target in targets:
        feature, _, tc = target.partition("/")
        tc = tc.upper()
        if not feature or not re.fullmatch(r"TC-\d+", tc):
            print(f"{target}: cần dạng <tính-năng>/TC-005")
            continue
        bug_dir = os.path.join(ROOT, "testing", slug, feature, "bug")
        hits = []
        for name in sorted(os.listdir(bug_dir)) if os.path.isdir(bug_dir) else []:
            if not re.fullmatch(r"BUG-\d+\.md", name):
                continue
            text = read(os.path.join(bug_dir, name))
            if re.search(rf"(?<![\w-]){re.escape(tc)}(?!\d)", text, re.I):
                title = text.splitlines()[0].lstrip("# ").strip() if text else ""
                st = status_of(text)
                hits.append((name[:-3], st, title))
        if not hits:
            print(f"{target}: chưa có bug nào nhắc test case này → tạo bug mới.")
        for code, st, title in hits:
            mo = st != "Đóng"
            any_open |= mo
            hint = ("ĐANG MỞ: lỗi cùng chỗ thì nối bug này, không tạo mới" if mo
                    else "đã Đóng: lỗi quay lại thì đề xuất Mở lại bug này (hỏi người dùng)")
            print(f"{target}: {code} [{st}] {title[:100]} → {hint}")
        known = [l for l in smoke_text.splitlines() if f"{feature}/test-case.md#{tc.lower()}" in l and "lỗi đã biết" in l.lower()]
        if known:
            print(f"{target}: smoke đang ghi 'Đạt kèm lỗi đã biết' cho ca này (lỗi đã có bug, xem tiêu chí trả build).")
    return 1 if any_open else 0


if __name__ == "__main__":
    sys.exit(main())
