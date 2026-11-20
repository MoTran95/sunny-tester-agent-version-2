#!/usr/bin/env python3
"""Kiểm bộ nhớ `memories/` (chỉ cho AI đọc): bản đồ khớp file thật, link không gãy, quy tắc cốt lõi còn.

    python -X utf8 scripts/kiem-tra-bo-nho.py

- Mọi file .md trong memories/ (trừ MEMORY.md) phải có trong MEMORY.md; mọi file nêu trong MEMORY.md phải tồn tại.
- Link/đường dẫn `memories/...` hay `../` trong các file memory phải trỏ tới file có thật.
- Mỗi quy tắc cốt lõi (CỐT_LOI) phải xuất hiện đúng ở file chỉ định (bắt việc lỡ xóa khi gọn).
- In cỡ từng file (KB) và tổng; phần LUÔN ĐỌC (★ trong bản đồ + CLAUDE.md + MEMORY.md).
Thoát mã 1 nếu có lỗi.
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEM = os.path.join(ROOT, "memories")

# (file trong memories/, cụm phải còn trong file đó, ý nghĩa)
CỐT_LOI = [
    ("user/working-preferences.md", "tiếng Việt", "giao tiếp tiếng Việt"),
    ("user/working-preferences.md", "Không hỏi lại điều đã có câu trả lời", "cách đặt câu hỏi: đủ ngữ cảnh, có lựa chọn, không hỏi lại"),
    ("user/working-preferences.md", "tự nhập cả mật khẩu thật lẫn mật khẩu sai", "tài khoản test thì tự nhập mật khẩu thật và sai, không in/ghi"),
    ("user/working-preferences.md", "không tự đặt con số", "số lần nhập sai do requirement hoặc người test chốt, không tự đặt"),
    ("user/working-preferences.md", "Commit/push chỉ khi người dùng nhờ", "commit khi được nhờ"),
    ("user/working-preferences.md", "hỏi, không suy diễn", "hỏi không suy diễn"),
    ("user/working-preferences.md", "đọc là hiểu", "tài liệu đọc là hiểu"),
    ("user/working-preferences.md", "hỏi trước khi bật", "connector hỏi trước khi bật"),
    ("conventions/nhieu-du-an.md", "hỏi riêng câu này", "hỏi riêng câu dự án trên máy mới"),
    ("conventions/nhieu-du-an.md", "Không lẫn kiến thức", "không lẫn dự án"),
    ("conventions/ba-question-wording.md", "anh/chị", "xưng hô với BA"),
    ("pitfalls/dont-trigger-lockouts.md", "không tự đặt số", "bài học khóa đăng nhập"),
    ("decisions/decision-log.md", "Open Sans", "quyết định font báo cáo"),
    ("user/document-preferences.md", "suy luận tiếp", "requirement rõ thì suy luận, chưa rõ thì hỏi"),
    ("project/srs-process.md", "không làm trước", "không làm bước chưa được yêu cầu"),
]


def doc(p):
    with io.open(p, encoding="utf-8") as f:
        return f.read()


def main():
    loi = []
    files = []
    for d, _, fs in os.walk(MEM):
        for f in fs:
            if f.endswith(".md"):
                files.append(os.path.relpath(os.path.join(d, f), MEM).replace("\\", "/"))
    files.sort()
    mm = doc(os.path.join(MEM, "MEMORY.md"))
    nhac = set(re.findall(r"`([A-Za-z0-9_./-]+\.md)`", mm))
    for f in files:
        if f != "MEMORY.md" and f not in mm:
            loi.append(f"{f}: chưa có trong MEMORY.md")
    for n in sorted(nhac):
        if "/" not in n:  # tên trần (checklist.md…) của sản phẩm trong testing/, không kiểm
            continue
        if n.startswith(("testing/", "srs/", "evidence/", ".claude/", "docs/")):
            if not os.path.exists(os.path.join(ROOT, n)):
                loi.append(f"MEMORY.md nêu {n} nhưng không có")
        elif not os.path.exists(os.path.join(MEM, n)) and "<" not in n:
            loi.append(f"MEMORY.md nêu {n} nhưng không có trong memories/")
    # đường dẫn tới file repo trong các file memory
    for f in files:
        txt = doc(os.path.join(MEM, f))
        for m in re.findall(r"`((?:srs|testing|evidence|docs|scripts)/[A-Za-z0-9_./-]+\.(?:md|py|json|html))`", txt):
            if "<" in m:
                continue
            if not os.path.exists(os.path.join(ROOT, m)):
                loi.append(f"{f}: đường dẫn không tồn tại: {m}")
        for m in re.findall(r"\]\((?!http|#)([^)]+)\)", txt):
            t = os.path.normpath(os.path.join(MEM, os.path.dirname(f), m.split("#")[0]))
            if not os.path.exists(t):
                loi.append(f"{f}: link gãy: {m}")
    for f, cum, y in CỐT_LOI:
        p = os.path.join(MEM, f)
        if not os.path.exists(p) or cum not in doc(p):
            loi.append(f"mất quy tắc cốt lõi ({y}): cần cụm \"{cum}\" trong {f}")

    tong = 0
    print("Cỡ (KB):")
    for f in files:
        kb = os.path.getsize(os.path.join(MEM, f)) / 1024
        tong += kb
        print(f"  {kb:5.1f}  {f}")
    luon = ["MEMORY.md", "user/working-preferences.md", "project/overview.md"]
    luon_kb = sum(os.path.getsize(os.path.join(MEM, f)) for f in luon) / 1024
    luon_kb += os.path.getsize(os.path.join(ROOT, "CLAUDE.md")) / 1024
    # trang HTML sinh từ md và dữ liệu phải khớp nguồn (không cũ): sửa bằng python -X utf8 scripts/build_docs.py --all
    import subprocess
    r = subprocess.run([sys.executable, "-X", "utf8", os.path.join(ROOT, "scripts", "build_docs.py"), "--all", "--check"], capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        chi_tiet = " | ".join(x.strip() for x in (r.stdout or r.stderr).strip().splitlines())[:500]
        loi.append("trang HTML cũ hơn file md hoặc dữ liệu. Chạy: python -X utf8 scripts/build_docs.py --all (" + chi_tiet + ")")
    # thông tin dự án không được lẫn sang skill dùng chung hoặc sang dự án khác
    r2 = subprocess.run([sys.executable, "-X", "utf8", os.path.join(ROOT, "scripts", "kiem-tra-lan-du-an.py")], capture_output=True, text=True, encoding="utf-8")
    if r2.returncode != 0:
        loi.append("thông tin dự án bị lẫn: " + " | ".join(x.strip() for x in r2.stdout.strip().splitlines())[:600])
    # không có mật khẩu của .env trong file văn bản; bug của dự án hiện tại đúng quy tắc skill tao-bug-report
    r3 = subprocess.run([sys.executable, "-X", "utf8", os.path.join(ROOT, "scripts", "kiem-tra-ro-mat-khau.py")], capture_output=True, text=True, encoding="utf-8")
    if r3.returncode != 0:
        loi.append("mật khẩu lọt vào file: " + " | ".join(x.strip() for x in r3.stdout.strip().splitlines())[:600])
    bug_script = os.path.join(ROOT, ".claude", "skills", "tao-bug-report", "scripts", "kiem-tra-bug.py")
    if os.path.exists(bug_script):
        r4 = subprocess.run([sys.executable, "-X", "utf8", bug_script, "--du-an"], capture_output=True, text=True, encoding="utf-8")
        if r4.returncode != 0:
            loi.append("bug chưa đúng quy tắc: " + " | ".join(x.strip() for x in r4.stdout.strip().splitlines() if "đạt" not in x)[:600])
    # Truy vết và test plan (chỉ đọc, không ghi file): requirement đổi mà test case/smoke/regression chưa cập nhật,
    # hoặc test plan lệch số liệu, thì báo lỗi ngay thay vì chờ có người nhớ chạy lệnh (rà soát 2026-11-19, A1, A2)
    py = [sys.executable, "-X", "utf8"]
    for slug in sorted(d for d in os.listdir(os.path.join(ROOT, "testing")) if os.path.isdir(os.path.join(ROOT, "testing", d))):
        tdir = os.path.join(ROOT, "testing", slug)
        for feat in sorted(os.listdir(tdir)):
            if (os.path.exists(os.path.join(tdir, feat, "truy-vet-cau-hinh.json"))
                    and os.path.exists(os.path.join(tdir, feat, "test-case.md"))):   # chưa có test case thì chưa có gì để truy vết
                rt = subprocess.run(py + [os.path.join(ROOT, "scripts", "truy-vet.py"), "kiem", slug, feat, "--chi-doc"],
                                    capture_output=True, text=True, encoding="utf-8")
                m = re.search(r"TÓM TẮT: ma_doi=(\d+) can_xem_lai=(\d+) tc_bo=(\d+)", rt.stdout or "")
                if m and any(int(x) for x in m.groups()):
                    loi.append(f"truy vết {slug}/{feat}: {m.group(1)} mã requirement đổi, {m.group(2)} test case cần xem lại, "
                               f"{m.group(3)} test case đã bỏ. Xem: python -X utf8 scripts/truy-vet.py kiem {slug} {feat}")
                elif not m:
                    loi.append(f"truy vết {slug}/{feat} chạy lỗi: " + (rt.stdout + rt.stderr).strip()[-300:])
        for name, script in (("smoke-test.md", "truy-vet-smoke.py"), ("regression-test.md", "truy-vet-regression.py")):
            if os.path.exists(os.path.join(tdir, name)):
                rs = subprocess.run(py + [os.path.join(ROOT, "scripts", script), "kiem", slug], capture_output=True, text=True, encoding="utf-8")
                if rs.returncode != 0:
                    viec = [x.strip() for x in rs.stdout.splitlines() if x.strip().startswith(("-", "!"))][:4]
                    loi.append(f"{name} của {slug} cần cập nhật theo test case/requirement: " + " | ".join(viec)[:400]
                               + f". Xem: python -X utf8 scripts/{script} kiem {slug}")
        if os.path.exists(os.path.join(tdir, "test-plan-nguon.txt")):
            tp = os.path.join(ROOT, ".claude", "skills", "tao-test-plan", "scripts", "sinh-test-plan.py")
            rp = subprocess.run(py + [tp, "kiem", slug], capture_output=True, text=True, encoding="utf-8")
            if rp.returncode != 0:
                loi.append(f"test plan của {slug} lệch số liệu hoặc nguồn (nói 'Cập nhật test plan'): " + rp.stdout.strip()[:300])
    print(f"Tổng memories: {tong:.1f} KB · phần luôn đọc (CLAUDE.md + bản đồ + 2 file ★): {luon_kb:.1f} KB")
    if loi:
        print(f"\n{len(loi)} LỖI:")
        for l in loi:
            print("  -", l)
        return 1
    print("0 lỗi.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
