#!/usr/bin/env python3
"""Lưu bằng chứng (ảnh lỗi tô đỏ + video) của một bug vào repo, để bug mở ở máy nào cũng có đủ.

Video của lượt chạy nằm ở `evidence/<dự-án>/chay-test/video/` (không vào git, chỉ có trên máy đã chạy).
Script chép video (và ảnh lỗi khi tạo bug từ lượt chạy) sang `evidence/<dự-án>/bug/BUG-nnn/` (có vào git)
rồi sửa đường dẫn trong file bug.

Tạo bug từ lượt chạy (thêm ảnh lỗi + video của ca vào mục "Đính kèm cần có"):
    python -X utf8 .claude/skills/tao-bug-report/scripts/luu-bang-chung.py <BUG-nnn.md> --ket-qua <result-*.json> --ca <tính-năng>/tc-005 [--ghi]
Bug đã có nhắc video trong thư mục video/ (chép sang thư mục bug, đổi đường dẫn):
    python -X utf8 .claude/skills/tao-bug-report/scripts/luu-bang-chung.py <BUG-nnn.md> [--ghi]
Không có --ghi: chỉ in sẽ làm gì. Không ghi đè tệp đã có trong thư mục bug.
"""
import argparse
import io
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
ATTACH = re.compile(r"^## Đính kèm")


def read(p):
    t = io.open(p, encoding="utf-8", newline="").read()
    return t, ("\r\n" if "\r\n" in t else "\n")


def rel(p):
    return os.path.relpath(p, ROOT).replace(os.sep, "/")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("bug")
    ap.add_argument("--ket-qua", nargs="*", default=[], help="file result-*.json của lượt chạy")
    ap.add_argument("--ca", help="mã ca trong file kết quả, ví dụ dang-nhap/tc-005")
    ap.add_argument("--ghi", action="store_true")
    a = ap.parse_args()

    bug = os.path.abspath(a.bug)
    parts = rel(bug).split("/")
    if len(parts) < 3 or parts[0] != "testing":
        sys.exit("File bug phải nằm trong testing/<dự-án>/…/bug/BUG-nnn.md")
    slug, code = parts[1], os.path.splitext(parts[-1])[0]
    dest_dir = os.path.join(ROOT, "evidence", slug, "bug", code)
    text, eol = read(bug)
    text = text.replace("\r\n", "\n")
    plan, new_lines = [], []   # (nguồn, đích); dòng thêm vào Đính kèm

    # 1. video đang trỏ vào thư mục không vào git -> chép sang thư mục bug, đổi đường dẫn
    for m in sorted(set(re.findall(r"evidence/[^\s`)]+/video/[^\s`)]+\.webm", text))):
        src = os.path.join(ROOT, m)
        dst = os.path.join(dest_dir, os.path.basename(m))
        if not os.path.exists(src) and not os.path.exists(dst):
            print(f"  THIẾU video trên máy này, không chép được: {m} (ghi 'Cần bổ sung' nếu không lấy lại được)")
            continue
        plan.append((src, dst))
        text = text.replace(m, rel(dst))

    # 2. tạo bug từ lượt chạy: ảnh lỗi tô đỏ + video của đúng ca
    if a.ket_qua:
        if not a.ca:
            sys.exit("Dùng --ket-qua thì cần --ca <tính-năng>/tc-xxx")
        found = False
        for f in a.ket_qua:
            data = json.loads(io.open(f, encoding="utf-8").read())
            for r in data.get("results", []):
                if r.get("case_id", "").lower() != a.ca.lower():
                    continue
                found = True
                caps = r.get("error_image_captions", {})
                for img in r.get("error_images", []):
                    img_rel = img.replace("\\", "/")
                    if img_rel not in text:
                        cap = caps.get(img) or caps.get(img_rel) or "lỗi ở bước … (ghi rõ)"
                        new_lines.append(f"- [x] Ảnh lỗi đã tô đỏ ({cap}): `{img_rel}`")
                for v in r.get("videos", []):
                    v_rel = v.replace("\\", "/")
                    dst = os.path.join(dest_dir, os.path.basename(v_rel))
                    if rel(dst) not in text:
                        plan.append((os.path.join(ROOT, v_rel), dst))
                        new_lines.append(f"- [x] Video quay lại các bước của ca {a.ca} (lượt {data.get('timestamp', '')}): `{rel(dst)}`")
                if not r.get("videos"):
                    new_lines.append(f"- [ ] Video của ca {a.ca} — `Cần bổ sung` (lượt chạy không quay video, ví dụ do --no-video)")
        if not found:
            sys.exit(f"Không thấy ca {a.ca} trong file kết quả")

    if new_lines:
        lines = text.split("\n")
        idx = next((i for i, l in enumerate(lines) if ATTACH.match(l)), None)
        if idx is None:
            sys.exit("File bug không có mục '## Đính kèm cần có' (khuôn assets/mau-bug-report.md)")
        end = next((j for j in range(idx + 1, len(lines)) if lines[j].startswith("## ")), len(lines))
        while end > idx + 1 and not lines[end - 1].strip():
            end -= 1
        lines[end:end] = new_lines
        text = "\n".join(lines)

    for src, dst in plan:
        print(f"  chép {rel(src)} -> {rel(dst)}" + (" (đã có, giữ nguyên)" if os.path.exists(dst) else ""))
    for l in new_lines:
        print("  thêm vào Đính kèm:", l)
    if not plan and not new_lines:
        print("Không có gì phải làm: bằng chứng đã nằm trong thư mục của bug.")
        return 0
    if not a.ghi:
        print("(xem trước; thêm --ghi để chép tệp và sửa file bug)")
        return 0
    os.makedirs(dest_dir, exist_ok=True)
    for src, dst in plan:
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
    io.open(bug, "w", encoding="utf-8", newline="").write(text.replace("\n", eol))
    print(f"Đã ghi. Chạy tiếp: python -X utf8 scripts/build_docs.py --all")
    return 0


if __name__ == "__main__":
    sys.exit(main())
