#!/usr/bin/env python3
"""Kiểm một hoặc nhiều file bug (BUG-nnn.md) theo quy tắc của skill tao-bug-report. Chỉ kiểm cấu trúc và chữ; không thay thế việc đọc lại.

    python -X utf8 .claude/skills/tao-bug-report/scripts/kiem-tra-bug.py <BUG-nnn.md> [...]
    python -X utf8 .claude/skills/tao-bug-report/scripts/kiem-tra-bug.py --du-an        # mọi bug của dự án hiện tại (.du-an-hien-tai)

Kiểm: tiêu đề dạng `# [Module] mô tả` không kèm lý do; đủ các mục theo khuôn `assets/mau-bug-report.md`;
mức độ nghiêm trọng bằng tiếng Việt (Nghiêm trọng, Lớn/Nặng, Nhỏ, Rất nhỏ) và ưu tiên (Cao, Trung bình, Thấp) có chữ "Đề xuất";
tần suất đúng một trong các dạng; có ít nhất hai bước tái hiện đánh số; Kết quả thực tế không có câu chung chung;
số nhãn `[Giả định: …]` trong thân bằng số mục ở cuối file; đường dẫn ảnh/video nêu trong file có thật (trừ video, vì video không vào git);
không chứa giá trị mật khẩu nào trong `.env` (chỉ báo tên khóa, không in giá trị).
Thang mức độ: mặc định như dưới; dự án có thang riêng của team thì khai ở `testing/<dự-án>/thang-muc-do-bug.json`
({"severity": [...], "priority": [...]}, tên mức bằng tiếng Việt), script dùng thang đó.
Thoát mã 1 nếu có lỗi.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(SKILL)))
OPTIONAL_SECTIONS = {"Test case liên quan"}
SEVERITY = ("Nghiêm trọng", "Lớn", "Nặng", "Nhỏ", "Rất nhỏ")
PRIORITY = ("Cao", "Trung bình", "Thấp")
STATUS = ("Mở", "Chờ re-test", "Mở lại", "Đóng")
FREQUENCY = re.compile(r"^(Luôn xảy ra|Thỉnh thoảng|Một lần|1/1|Chưa rõ)", re.I)
VAGUE_ACTUAL = ["không hoạt động", "bị lỗi", "lỗi hệ thống", "không như mong đợi", "hoạt động sai", "chạy sai", "hiển thị sai"]
ENGLISH_SEVERITY = re.compile(r"\b(Critical|Major|Minor|Trivial|Severity|Priority)\b")
REASON_IN_TITLE = re.compile(r"\b(dù|theo BA|vì|bởi vì|do BA)\b", re.I)


def project_scale(path):
    """(severity, priority) của dự án chứa file bug: thang riêng của team nếu có `testing/<dự-án>/thang-muc-do-bug.json`."""
    parts = os.path.abspath(path).replace("\\", "/").split("/")
    if "testing" in parts and parts.index("testing") + 1 < len(parts):
        f = os.path.join(ROOT, "testing", parts[parts.index("testing") + 1], "thang-muc-do-bug.json")
        if os.path.exists(f):
            import json
            data = json.loads(read(f))
            return tuple(data.get("severity") or SEVERITY), tuple(data.get("priority") or PRIORITY)
    return SEVERITY, PRIORITY


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def template_sections():
    found = []
    for line in read(os.path.join(SKILL, "assets", "mau-bug-report.md")).splitlines():
        if line.startswith("## "):
            found.append(line[3:].split("(")[0].strip())
    return found


def sections_of(text):
    """{tên mục: nội dung} theo `## `."""
    out, name, buf = {}, None, []
    for line in text.splitlines():
        if line.startswith("## "):
            if name is not None:
                out[name] = "\n".join(buf)
            name, buf = line[3:].split("(")[0].strip(), []
        elif name is not None:
            buf.append(line)
    if name is not None:
        out[name] = "\n".join(buf)
    return out


def env_password_keys():
    """{tên khóa: giá trị} của các mật khẩu trong .env (giá trị KHÔNG bao giờ được in)."""
    path = os.path.join(ROOT, ".env")
    keys = {}
    if os.path.exists(path):
        for line in read(path).splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                v = v.strip().strip('"').strip("'")
                if k.strip().endswith("PASSWORD") and len(v) >= 6:
                    keys[k.strip()] = v
    return keys


def check(path, passwords, required):
    problems = []
    text = read(path)
    name = os.path.basename(path)
    if not re.fullmatch(r"BUG-\d{3,}\.md", name):
        problems.append("tên file phải dạng BUG-nnn.md")
    first = text.splitlines()[0] if text.strip() else ""
    if not re.match(r"^# \[[^\]]+\] \S", first):
        problems.append("dòng đầu phải dạng `# [Module] Mô tả lỗi`")
    elif REASON_IN_TITLE.search(first):
        problems.append("tiêu đề chỉ nói cái gì sai, không kèm lý do hay ngữ cảnh (dù, theo BA, vì…)")
    secs = sections_of(text)
    for need in required:
        if need not in secs and need not in OPTIONAL_SECTIONS:
            problems.append(f"thiếu mục `## {need}`")
    severity, priority = project_scale(path)
    sev = secs.get("Mức độ nghiêm trọng", "").strip()
    if sev:
        m = re.match(r"\*\*([^*]+?)\.?\*\*", sev)
        if not m or m.group(1).strip().rstrip(".") not in severity:
            problems.append(f"`Mức độ nghiêm trọng` phải bắt đầu bằng **{'/'.join(severity)}** (in đậm, tiếng Việt)")
    if ENGLISH_SEVERITY.search(sev + secs.get("Mức độ ưu tiên đề xuất", "")):
        problems.append("mức độ phải viết tiếng Việt, không dùng Severity/Priority/Critical/Major/Minor")
    pri = secs.get("Mức độ ưu tiên đề xuất", "").strip()
    if pri:
        m = re.match(r"\*\*([^*]+?)\*\*", pri)
        if not m or m.group(1).strip() not in priority:
            problems.append(f"`Mức độ ưu tiên đề xuất` phải bắt đầu bằng **{'/'.join(priority)}**")
        if "đề xuất" not in pri.lower():
            problems.append("ưu tiên chỉ là đề xuất: ghi `(Đề xuất; team hoặc PO sẽ chốt.)`")
    state = secs.get("Trạng thái", "").strip()   # mục tùy chọn do skill lap-ke-hoach-retest ghi, không có trong khuôn
    if state:
        m = re.match(r"\*\*([^*]+?)\.?\*\*", state)
        if not m or m.group(1).strip() not in STATUS:
            problems.append("`Trạng thái` phải bắt đầu bằng **Mở / Chờ re-test / Mở lại / Đóng** (in đậm); ghi bằng script dat-trang-thai-bug.py của skill lap-ke-hoach-retest")
    freq = secs.get("Tần suất", "").strip()
    if freq and not FREQUENCY.match(freq):
        problems.append("`Tần suất` phải bắt đầu bằng Luôn xảy ra / Thỉnh thoảng / Một lần / 1/1 / Chưa rõ")
    steps = [l for l in secs.get("Các bước tái hiện", "").splitlines() if re.match(r"^\s*\d+[.)]\s+\S", l)]
    if secs.get("Các bước tái hiện") is not None and len(steps) < 2:
        problems.append("`Các bước tái hiện` cần ít nhất 2 bước đánh số")
    actual = secs.get("Kết quả thực tế", "")
    for phrase in VAGUE_ACTUAL:
        if phrase in actual.lower():
            problems.append(f"`Kết quả thực tế` có câu chung chung `{phrase}`: nói rõ màn hình nào, thấy chính xác gì")
            break
    if "Kết quả thực tế" in secs and len(actual.strip()) < 40:
        problems.append("`Kết quả thực tế` quá ngắn: nguyên văn thông báo, giá trị sai và đúng, ở bước nào")
    marker = "Thông tin đã gắn nhãn Giả định"
    if marker in secs:
        idx = text.index("## " + marker)
        inline = len(re.findall(r"\[Giả định:", text[:idx]))
        listed = len([l for l in secs[marker].splitlines() if re.match(r"^\s*(\d+[.)]|[-*])\s+\S", l)])
        if inline != listed:
            problems.append(f"có {inline} nhãn `[Giả định: …]` trong thân nhưng {listed} mục ở cuối file: hai số phải bằng nhau")
    for m in re.finditer(r"((?:evidence|docs)/[^\s`)\]]+?\.(?:png|jpg))", text):
        if not os.path.exists(os.path.join(ROOT, m.group(1))):
            problems.append(f"ảnh nêu trong file không có thật: {m.group(1)}")
    for m in re.finditer(r"(evidence/[^\s`)\]]+?/video/[^\s`)\]]+?\.webm)", text):
        problems.append(f"video nằm trong thư mục không vào git, máy khác sẽ không có: {m.group(1)}. "
                        "Chép vào thư mục của bug: python -X utf8 .claude/skills/tao-bug-report/scripts/luu-bang-chung.py <file bug> --ghi")
    for key, value in passwords.items():
        if value in text:
            problems.append(f"file chứa giá trị mật khẩu của khóa `{key}` trong .env: xóa ngay (không in giá trị ở đây)")
    return problems


def project_bugs():
    marker = os.path.join(ROOT, ".du-an-hien-tai")
    if not os.path.exists(marker):
        print("Chưa có .du-an-hien-tai: truyền đường dẫn file bug.")
        return []
    slug = read(marker).strip()
    found = []
    for dirpath, _dirs, files in os.walk(os.path.join(ROOT, "testing", slug)):
        found += [os.path.join(dirpath, f) for f in files if re.fullmatch(r"BUG-\d+\.md", f)]
    return sorted(found)


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 2
    paths = project_bugs() if args[0] == "--du-an" else args
    if not paths:
        print("Không có file bug nào để kiểm.")
        return 0
    required = template_sections()
    passwords = env_password_keys()
    total = 0
    for path in paths:
        problems = check(path, passwords, required)
        rel = os.path.relpath(path, ROOT) if os.path.abspath(path).startswith(ROOT) else path
        if problems:
            total += len(problems)
            print(f"{rel}: {len(problems)} lỗi")
            for p in problems:
                print("  -", p)
        else:
            print(f"{rel}: đạt")
    print(f"Kết quả: {total} lỗi trong {len(paths)} file bug.")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
