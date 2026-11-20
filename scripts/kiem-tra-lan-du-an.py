#!/usr/bin/env python3
"""Kiểm thông tin của dự án này không lẫn sang chỗ dùng chung hoặc sang dự án khác.

    python -X utf8 scripts/kiem-tra-lan-du-an.py

Mỗi dự án có "dấu hiệu nhận ra": tên thư mục (slug), tiền tố `.env`, tên miền của địa chỉ test, tên hiển thị
(bảng trong memories/project/overview.md), mã tài khoản test (khóa `<TIỀN_TỐ>_<MÃ>_PASSWORD` trong .env.example),
nhãn ô đăng nhập (`login.id_labels` trong auto-config.json), mã tính năng (khóa `tien_to` trong truy-vet-cau-hinh.json,
cả dạng `<MÃ>-S01` lẫn mã đứng riêng viết HOA), tên thư mục và tên hiển thị dài của tính năng (ten-tinh-nang.json).
Hai kiểm tra:
1. Chỗ dùng chung KHÔNG được chứa dấu hiệu của bất kỳ dự án nào. Chỗ dùng chung = mọi file văn bản trong repo, trừ
   thư mục từng dự án, các đường trong `khong_xuat` và `chi_muc_du_an` của `scripts/bo-loi.json`.
2. Thư mục riêng của dự án P (`memories/modules/P`, `srs/P`, `testing/P`, `evidence/P`) KHÔNG được chứa dấu hiệu của dự án Q khác.
Chỉ đọc file văn bản (md, json, py, txt, csv, css, js); bỏ qua HTML sinh tự động. Thoát mã 1 nếu có chỗ lẫn.
`scripts/xuat-bo-loi.py` dùng lại các hàm ở đây để soát bộ lõi đã xuất (kể cả HTML và thông tin cá nhân).
"""
import json
import os
import re
import subprocess
import sys
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXT_EXT = (".md", ".json", ".py", ".txt", ".csv", ".css", ".js")
SKIP_DIRS = {"__pycache__", ".git", "node_modules", ".venv"}
PROJECT_DIRS = ("memories/modules", "srs", "testing", "evidence")


def read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except (OSError, UnicodeDecodeError):
        return ""


def load_cfg(root=ROOT):
    """Cấu hình ranh giới bộ lõi (`scripts/bo-loi.json`); thiếu file thì coi như rỗng."""
    try:
        cfg = json.loads(read(os.path.join(root, "scripts", "bo-loi.json")) or "{}")
    except ValueError:
        cfg = {}
    cfg.setdefault("khong_xuat", [])
    cfg.setdefault("chi_muc_du_an", [])
    cfg.setdefault("thay_khi_xuat", {})
    return cfg


def projects(root=ROOT):
    base = os.path.join(root, "testing")
    if not os.path.isdir(base):
        return []
    return sorted(d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d)))


def display_names(root=ROOT):
    """slug → tên hiển thị, đọc bảng dự án trong memories/project/overview.md."""
    names = {}
    for line in read(os.path.join(root, "memories", "project", "overview.md")).splitlines():
        m = re.match(r"\|\s*`([a-z0-9-]+)`\s*\|\s*([^|]+?)\s*\|", line)
        if m:
            names[m.group(1)] = m.group(2)
    return names


def _word(text, flags=re.I):
    return re.compile(r"(?<![\w-])" + re.escape(text) + r"(?![\w-])", flags)


def markers(slug, names, env_example, root=ROOT):
    """Danh sách (nhãn, mẫu regex) nhận ra dự án `slug`."""
    found = [("tên thư mục", _word(slug))]
    proj = os.path.join(root, "testing", slug)
    cfg_path = os.path.join(proj, "auto-config.json")
    prefix = ""
    if os.path.exists(cfg_path):
        try:
            cfg = json.loads(read(cfg_path))
        except ValueError:
            cfg = {}
        prefix = str(cfg.get("env_prefix", ""))
        host = urlparse(str(cfg.get("default_url", ""))).hostname or ""
        if host and "<" not in host:
            found.append(("tên miền địa chỉ test", re.compile(re.escape(host), re.I)))
        for label in (cfg.get("login") or {}).get("id_labels", []):
            label = str(label).strip()
            if label and "<" not in label and len(label) >= 6:
                found.append((f"nhãn ô đăng nhập '{label}'", re.compile(r"(?<![\w])" + re.escape(label) + r"(?![\w])", re.I)))
    feats = sorted(d for d in os.listdir(proj) if os.path.isdir(os.path.join(proj, d))) if os.path.isdir(proj) else []
    for d in feats:
        tv = os.path.join(proj, d, "truy-vet-cau-hinh.json")
        if os.path.exists(tv):
            try:
                code = str(json.loads(read(tv)).get("tien_to", "")).strip()
            except ValueError:
                code = ""
            if code:
                found.append((f"mã tính năng {code}", re.compile(r"(?<![\w-])" + re.escape(code) + r"-(?:S\d\d|R\d\d|M\d\d|Q\d\d|E\d\d)")))
                if len(code) >= 4:  # mã đứng riêng, đúng chữ HOA (ví dụ `CART` trong câu)
                    found.append((f"mã tính năng {code}", re.compile(r"(?<![\w-])" + re.escape(code) + r"(?![\w])")))
        if len(d) >= 12:  # tên thư mục tính năng đủ dài để không trùng từ chung (bỏ qua kiểu `dang-nhap`)
            found.append((f"thư mục tính năng {d}", _word(d)))
    try:
        ten_tn = json.loads(read(os.path.join(proj, "ten-tinh-nang.json")) or "{}")
    except ValueError:
        ten_tn = {}
    for ten in ten_tn.values():
        ten = str(ten).strip()
        if len(ten) >= 12 and "<" not in ten:
            found.append((f"tên tính năng '{ten}'", _word(ten)))
    if not prefix:
        prefix = slug.upper().replace("-", "_")
    found.append(("tiền tố .env", re.compile(r"(?<![\w])" + re.escape(prefix) + r"_")))
    name = names.get(slug)
    if name and "<" not in name and len(name) >= 4:
        found.append(("tên hiển thị", re.compile(r"(?<![\w])" + re.escape(name) + r"(?![\w])", re.I)))
        short = re.split(r"\s+[—–-]\s+", name)[0].strip()  # "Tên — mô tả" → "Tên"
        if short != name and len(short) >= 6:
            found.append(("tên hiển thị", _word(short)))
    for m in re.finditer(r"^" + re.escape(prefix) + r"_([A-Za-z0-9]+)_PASSWORD", env_example, re.M):
        code = m.group(1)
        if len(code) >= 4:
            found.append((f"mã tài khoản {code}", re.compile(r"(?<![\w])" + re.escape(code) + r"(?![\w])")))
    return found


def all_markers(root=ROOT):
    names = display_names(root)
    env_example = read(os.path.join(root, ".env.example"))
    return {s: markers(s, names, env_example, root) for s in projects(root)}


def personal_markers(root=ROOT):
    """Dấu hiệu cá nhân của người dùng repo này: tên/email git, chủ và tên repo trên remote, tên người test."""
    found = []

    def git(*args):
        try:
            return subprocess.run(["git", "-C", root, *args], capture_output=True, text=True, encoding="utf-8").stdout.strip()
        except OSError:
            return ""

    for key in ("user.name", "user.email"):
        v = git("config", key)
        if len(v) >= 4:
            found.append((f"git {key}", re.compile(re.escape(v), re.I)))
    url = git("remote", "get-url", "origin")
    m = re.search(r"[:/]([\w.-]+)/([\w.-]+?)(?:\.git)?$", url)
    if m:
        for part, label in ((m.group(1), "chủ repo trên remote"), (m.group(2), "tên repo trên remote")):
            if len(part) >= 4:
                found.append((label, _word(part)))
    for line in read(os.path.join(root, ".nguoi-test")).splitlines()[:1]:
        if len(line.strip()) >= 4:
            found.append(("tên người test (.nguoi-test)", _word(line.strip())))
    return found


def _match_rel(rel, entries):
    for e in entries:
        e = e.rstrip("/")
        if rel == e or rel.startswith(e + "/") or ("/" not in e and e in rel.split("/")):
            return True
    return False


def shared_files(root=ROOT, slugs=None, cfg=None, exts=TEXT_EXT, include_index=False):
    """File dùng chung: mọi file `exts` trong `root`, trừ thư mục dự án, `khong_xuat`, và `chi_muc_du_an` (trừ khi include_index)."""
    cfg = cfg or load_cfg(root)
    slugs = projects(root) if slugs is None else slugs
    proj = {f"{d}/{s}" for d in PROJECT_DIRS for s in slugs}
    skip = list(cfg["khong_xuat"]) + ([] if include_index else list(cfg["chi_muc_du_an"]))
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root).replace(os.sep, "/")
        rel_dir = "" if rel_dir == "." else rel_dir
        keep = []
        for d in dirnames:
            r = f"{rel_dir}/{d}" if rel_dir else d
            if d in SKIP_DIRS or r in proj or _match_rel(r, skip):
                continue
            keep.append(d)
        dirnames[:] = keep
        for name in filenames:
            r = f"{rel_dir}/{name}" if rel_dir else name
            if name.lower().endswith(exts) and not _match_rel(r, skip):
                out.append(os.path.join(dirpath, name))
    return sorted(out)


def text_files(folder):
    for dirpath, dirnames, filenames in os.walk(folder):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if name.lower().endswith(TEXT_EXT):
                yield os.path.join(dirpath, name)


def scan(files, other_markers, root=ROOT, all_hits=False):
    """[(file tương đối, số dòng, nhãn, dự án)] chỗ chứa dấu hiệu. Mặc định mỗi file mỗi dự án chỉ báo chỗ đầu tiên."""
    hits = []
    for path in files:
        text = read(path)
        for slug, marks in other_markers.items():
            for label, pattern in marks:
                for m in pattern.finditer(text):
                    line = text.count("\n", 0, m.start()) + 1
                    hits.append((os.path.relpath(path, root).replace(os.sep, "/"), line, label, slug))
                    if not all_hits:
                        break
                if hits and hits[-1][0] == os.path.relpath(path, root).replace(os.sep, "/") and hits[-1][3] == slug and not all_hits:
                    break
    return hits


def main():
    slugs = projects()
    markers_by = all_markers()
    problems = []
    for f, line, label, slug in scan(shared_files(slugs=slugs), markers_by):
        problems.append(f"chỗ dùng chung chứa thông tin dự án `{slug}` ({label}): {f}:{line}")
    for p in slugs:
        folders = [os.path.join(ROOT, d, p) for d in PROJECT_DIRS]
        files = [f for folder in folders if os.path.isdir(folder) for f in text_files(folder)]
        others = {s: m for s, m in markers_by.items() if s != p}
        for f, line, label, slug in scan(files, others):
            problems.append(f"thư mục dự án `{p}` chứa thông tin dự án `{slug}` ({label}): {f}:{line}")
    if problems:
        print(f"{len(problems)} chỗ thông tin dự án bị lẫn:")
        for x in problems[:30]:
            print("  -", x)
        if len(problems) > 30:
            print(f"  … và {len(problems) - 30} chỗ nữa")
        return 1
    print(f"Không lẫn thông tin giữa các dự án ({len(slugs)} dự án; mọi file dùng chung sạch).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
