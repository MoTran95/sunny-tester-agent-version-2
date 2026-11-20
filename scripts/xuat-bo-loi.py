#!/usr/bin/env python3
"""Xuất BỘ LÕI dùng chung (quy trình, quy tắc, skill, script, khuôn, hướng dẫn) ra một thư mục riêng, KHÔNG kèm dữ liệu
của dự án nào và thông tin cá nhân, để đem dùng cho dự án khác hoặc đưa người khác.

    python -X utf8 scripts/xuat-bo-loi.py <thư-mục-đích>            # xuất lần đầu (thư mục trống/chưa có) hoặc cập nhật bộ lõi đã xuất
    python -X utf8 scripts/xuat-bo-loi.py <thư-mục-đích> --khong-git # không `git init`

Ranh giới chung/riêng: `scripts/bo-loi.json` (khong_xuat, chi_muc_du_an, thay_khi_xuat) + thư mục từng dự án
(memories/modules/<slug>, srs/<slug>, testing/<slug>, evidence/<slug>) luôn bị bỏ.
Biến đổi khi xuất: cắt phần dự án trong file chỉ mục (.env.example, MEMORY.md, bảng dự án trong overview.md); thay nội dung
các file cá nhân bằng bản trống; thay địa chỉ remote git bằng chỗ trống và tên thư mục repo nguồn bằng tên thư mục đích;
sinh lại mọi trang HTML (`build_docs.py --all`).
Soát sau khi xuất (lỗi thì thoát mã 1, bộ lõi vẫn để lại để xem): dấu hiệu của mọi dự án nguồn (kể cả trong HTML), thông tin
cá nhân (tên/email git, chủ và tên repo remote, tên người test), chỗ còn nhắc file không xuất.
An toàn: chỉ ghi vào thư mục trống hoặc thư mục có `.bo-loi-xuat` (bộ lõi đã xuất trước). Khi cập nhật, chỉ xóa/ghi đè file
do lần xuất trước tạo ra (danh sách trong `.bo-loi-xuat`); dự án người dùng tự tạo trong bộ lõi được giữ nguyên.
Không commit: người dùng tự commit/push khi muốn.
"""
import argparse
import datetime
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = ".bo-loi-xuat"
TEXT_EXT = (".md", ".json", ".py", ".txt", ".csv", ".css", ".js", ".html", ".sh", ".yml", ".yaml", ".toml", ".cfg", ".ini")
TEXT_NAMES = {".gitignore", ".gitattributes", ".env.example", "pre-commit", "CLAUDE.md", "README.md"}
REMOTE_TRONG = "<địa-chỉ-repo-của-bạn>"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

_spec = importlib.util.spec_from_file_location("kiem_tra_lan_du_an", os.path.join(ROOT, "scripts", "kiem-tra-lan-du-an.py"))
lan = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lan)


def is_text(path):
    name = os.path.basename(path)
    return name in TEXT_NAMES or name.lower().endswith(TEXT_EXT)


def git(*args, cwd=ROOT):
    try:
        r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8")
        return r.returncode, r.stdout.strip()
    except OSError:
        return 1, ""


def files_to_export(cfg, slugs):
    """Đường dẫn tương đối (dấu /) của mọi file thuộc bộ lõi, mọi định dạng."""
    proj = {f"{d}/{s}" for d in lan.PROJECT_DIRS for s in slugs}
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        rel_dir = os.path.relpath(dirpath, ROOT).replace(os.sep, "/")
        rel_dir = "" if rel_dir == "." else rel_dir
        keep = []
        for d in dirnames:
            r = f"{rel_dir}/{d}" if rel_dir else d
            if d in lan.SKIP_DIRS or r in proj or lan._match_rel(r, cfg["khong_xuat"]):
                continue
            keep.append(d)
        dirnames[:] = sorted(keep)
        for name in sorted(filenames):
            r = f"{rel_dir}/{name}" if rel_dir else name
            if not lan._match_rel(r, cfg["khong_xuat"]) and not name.endswith((".pyc", ".pyo")):
                out.append(r)
    return out


def cat_env_example(text):
    """Giữ phần đầu giải thích, bỏ từ khối '# Dự án ...' đầu tiên trở đi."""
    lines = text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if line.startswith("# Dự án "):
            return "".join(lines[:i]).rstrip() + "\n"
    return text


def cat_memory_index(text, kit):
    """Bỏ các mục '## Dự án ...' và dòng bảng trỏ tới file memory không có trong bộ lõi."""
    out, skip, removed = [], False, []
    for line in text.splitlines(keepends=True):
        if line.startswith("## "):
            skip = line.startswith("## Dự án ")
        if skip:
            continue
        m = re.match(r"\|\s*★?\s*`([^`]+\.md)`", line)
        if m and not os.path.exists(os.path.join(kit, "memories", m.group(1))):
            removed.append(m.group(1))
            continue
        out.append(line)
    return "".join(out).rstrip() + "\n", removed


def cat_overview(text, slugs):
    lines = [l for l in text.splitlines(keepends=True) if not any(l.startswith(f"| `{s}` |") for s in slugs)]
    return "".join(lines)


def kit_project_parts(kit):
    """Phần dự án RIÊNG của bộ lõi (người dùng bộ lõi tự tạo) trong 3 file chỉ mục, để giữ lại khi cập nhật."""
    slugs = lan.projects(kit)
    keep = {"overview": [], "memory": [], "env": []}
    if not slugs:
        return keep
    ov = lan.read(os.path.join(kit, "memories", "project", "overview.md")).replace("\r\n", "\n")
    keep["overview"] = [l for l in ov.split("\n") if any(l.startswith(f"| `{s}` |") for s in slugs)]
    mm = lan.read(os.path.join(kit, "memories", "MEMORY.md")).replace("\r\n", "\n")
    for sec in re.split(r"\n(?=## )", mm):
        m = re.match(r"## Dự án `([^`]+)`", sec)
        if m and m.group(1) in slugs:
            keep["memory"].append(sec.rstrip())
    env = lan.read(os.path.join(kit, ".env.example")).replace("\r\n", "\n")
    for blk in re.split(r"\n(?=# Dự án )", env):
        m = re.match(r"# Dự án (\S+)", blk)
        if m and m.group(1) in slugs:
            keep["env"].append(blk.rstrip())
    return keep


def put_back(kit, keep):
    """Ghép lại phần dự án riêng của bộ lõi vào 3 file chỉ mục vừa xuất."""
    if keep["overview"]:
        p = os.path.join(kit, "memories", "project", "overview.md")
        lines = io.open(p, encoding="utf-8", newline="").read().split("\n")
        head = next((i for i, l in enumerate(lines) if l.startswith("| Slug |")), None)
        if head is not None:
            nl_r = "\r" if lines[head].endswith("\r") else ""
            lines[head + 2:head + 2] = [l + nl_r for l in keep["overview"]]
            io.open(p, "w", encoding="utf-8", newline="").write("\n".join(lines))
    if keep["memory"]:
        p = os.path.join(kit, "memories", "MEMORY.md")
        s = io.open(p, encoding="utf-8").read().rstrip("\n")
        io.open(p, "w", encoding="utf-8", newline="\n").write(s + "\n\n" + "\n\n".join(keep["memory"]) + "\n")
    if keep["env"]:
        p = os.path.join(kit, ".env.example")
        s = io.open(p, encoding="utf-8").read().rstrip("\n")
        io.open(p, "w", encoding="utf-8", newline="\n").write(s + "\n\n" + "\n\n".join(keep["env"]) + "\n")
    n = sum(len(v) for v in keep.values())
    if n:
        print(f"giữ phần dự án riêng của bộ lõi trong file chỉ mục: {', '.join(lan.projects(kit))}")


def main():
    ap = argparse.ArgumentParser(description="Xuất bộ lõi dùng chung, không kèm dữ liệu dự án và thông tin cá nhân")
    ap.add_argument("dich", help="thư mục đích, ví dụ D:/AI/sunny-tester-kit")
    ap.add_argument("--khong-git", action="store_true", help="không chạy git init ở thư mục đích")
    a = ap.parse_args()

    kit = os.path.abspath(a.dich)
    try:
        nested = os.path.commonpath([kit, ROOT]) in (ROOT, kit)
    except ValueError:   # khác ổ đĩa (Windows): không thể lồng nhau
        nested = False
    if nested:
        sys.exit("Thư mục đích không được nằm trong repo nguồn hay chứa repo nguồn.")
    mark_p = os.path.join(kit, MARK)
    old_files = []
    if os.path.isdir(kit) and os.listdir(kit):
        if not os.path.exists(mark_p):
            sys.exit(f"{kit} không trống và không phải bộ lõi đã xuất (thiếu {MARK}). Chọn thư mục trống để không ghi đè dữ liệu lạ.")
        old_files = json.load(io.open(mark_p, encoding="utf-8")).get("files", [])

    cfg = lan.load_cfg(ROOT)
    slugs = lan.projects(ROOT)
    rieng = kit_project_parts(kit) if old_files else {"overview": [], "memory": [], "env": []}
    files = files_to_export(cfg, slugs)
    _, remote = git("remote", "get-url", "origin")
    src_name, kit_name = os.path.basename(ROOT), os.path.basename(kit)

    # 1. Xóa file do lần xuất trước tạo mà nay không còn trong bộ lõi (file người dùng tự tạo không đụng tới).
    removed_old = 0
    for r in old_files:
        if r not in files:
            p = os.path.join(kit, r)
            if os.path.isfile(p):
                os.remove(p)
                removed_old += 1

    # 2. Chép và biến đổi.
    for r in files:
        src, dst = os.path.join(ROOT, r), os.path.join(kit, r)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if r in cfg["thay_khi_xuat"]:
            io.open(dst, "w", encoding="utf-8", newline="\n").write(cfg["thay_khi_xuat"][r])
            continue
        if not is_text(src):
            shutil.copy2(src, dst)
            continue
        raw = io.open(src, encoding="utf-8", newline="").read()
        nl = "\r\n" if "\r\n" in raw else "\n"
        s = raw.replace("\r\n", "\n")
        if r == ".env.example":
            s = cat_env_example(s)
        elif r == "memories/project/overview.md":
            s = cat_overview(s, slugs)
        if remote:
            s = s.replace(remote, REMOTE_TRONG)
        if src_name != kit_name and len(src_name) >= 6:
            s = s.replace(src_name, kit_name)
        io.open(dst, "w", encoding="utf-8", newline="").write(s.replace("\n", nl))
    for r, content in cfg["thay_khi_xuat"].items():  # file thay thế mà nguồn không có
        if r not in files:
            os.makedirs(os.path.dirname(os.path.join(kit, r)), exist_ok=True)
            io.open(os.path.join(kit, r), "w", encoding="utf-8", newline="\n").write(content)
            files.append(r)
    mm = os.path.join(kit, "memories", "MEMORY.md")
    if os.path.exists(mm):
        s, dropped = cat_memory_index(io.open(mm, encoding="utf-8").read(), kit)
        io.open(mm, "w", encoding="utf-8", newline="\n").write(s)
        if dropped:
            print("MEMORY.md: bỏ dòng trỏ tới file không xuất:", ", ".join(dropped))
    # memory: dòng bảng/gạch đầu dòng chỉ mô tả file không xuất thì bỏ (memory viết mỗi dòng một ý)
    excluded = [os.path.basename(e) for e in cfg["khong_xuat"]
                if not e.startswith(".") and not e.endswith("/") and "." in os.path.basename(e)]
    for r in files:
        if r.startswith("memories/") and r.endswith(".md") and r not in cfg["thay_khi_xuat"]:
            p = os.path.join(kit, r)
            raw = io.open(p, encoding="utf-8", newline="").read()
            keep, drop = [], []
            for line in raw.splitlines(keepends=True):
                if line.lstrip().startswith(("|", "- ")) and any(e in line for e in excluded):
                    drop.append(line.strip()[:90])
                else:
                    keep.append(line)
            if drop:
                io.open(p, "w", encoding="utf-8", newline="").write("".join(keep))
                print(f"{r}: bỏ {len(drop)} dòng nhắc file không xuất:", *drop, sep="\n    ")
    put_back(kit, rieng)
    for d in ("srs", "testing", "evidence"):
        os.makedirs(os.path.join(kit, d), exist_ok=True)

    # 3. Sinh lại HTML trong bộ lõi (trang cũ có thể còn nội dung đã sửa ở md).
    r = subprocess.run([sys.executable, "-X", "utf8", "scripts/build_docs.py", "--all"], cwd=kit,
                       capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        print("build_docs.py trong bộ lõi lỗi:\n" + (r.stdout + r.stderr)[-1500:])

    # 4. Soát.
    problems = []
    kit_files = [os.path.join(dp, f) for dp, dn, fn in os.walk(kit) if ".git" not in dp.split(os.sep) for f in fn]
    kit_text = [p for p in kit_files if is_text(p)]
    markers = lan.all_markers(ROOT)
    markers["(cá nhân)"] = lan.personal_markers(ROOT)
    for f, line, label, slug in lan.scan(kit_text, markers, root=kit):
        problems.append(f"{'thông tin cá nhân' if slug == '(cá nhân)' else 'dự án `' + slug + '`'} ({label}): {f}:{line}")
    # file nội dung không xuất (bỏ file riêng của máy như .env, settings.local.json: nhắc tới chúng là bình thường)
    for p in kit_text:
        if os.path.relpath(p, kit).replace(os.sep, "/") in ("scripts/bo-loi.json", MARK):
            continue   # file cấu hình ranh giới vốn liệt kê file không xuất
        text = lan.read(p)
        for e in excluded:
            i = text.find(e)
            if i >= 0:
                problems.append(f"còn nhắc file không xuất `{e}`: {os.path.relpath(p, kit)}:{text.count(chr(10), 0, i) + 1}")
    for r in files:  # chốt chặn cuối: file riêng của máy không bao giờ được xuất
        if lan._match_rel(r, [".env", ".du-an-hien-tai", ".nguoi-test", ".phien-dang-nhap/", ".claude/settings.local.json"]):
            problems.append(f"file riêng của máy lọt vào bộ lõi: {r}")

    # 5. Ghi dấu bộ lõi (danh sách file do lần xuất này tạo: file chép + trang HTML sinh từ md chép) + git.
    built = sorted(set(files) | {r[:-3] + ".html" for r in files
                                 if r.endswith(".md") and os.path.exists(os.path.join(kit, r[:-3] + ".html"))})
    io.open(mark_p, "w", encoding="utf-8", newline="\n").write(json.dumps(
        {"ghi_chu": "Bộ lõi xuất bằng scripts/xuat-bo-loi.py. Đừng sửa tay danh sách files (dùng khi cập nhật).",
         "ngay_xuat": datetime.date.today().isoformat(), "files": built}, ensure_ascii=False, indent=1) + "\n")
    if not a.khong_git and not os.path.isdir(os.path.join(kit, ".git")):
        code, _ = git("init", "-b", "main", cwd=kit)
        if code == 0:
            git("config", "core.hooksPath", ".githooks", cwd=kit)
            print("đã git init (nhánh main, bật hook .githooks); chưa commit")

    print(f"Bộ lõi: {kit} — {len(files)} file chép" + (f", xóa {removed_old} file cũ" if removed_old else "") +
          f"; bỏ {len(slugs)} dự án nguồn")
    if problems:
        print(f"{len(problems)} chỗ cần sửa (sửa ở repo nguồn rồi xuất lại):")
        for x in problems[:40]:
            print("  -", x)
        return 1
    print("Soát: không có dữ liệu dự án, thông tin cá nhân hay chỗ nhắc file không xuất.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
