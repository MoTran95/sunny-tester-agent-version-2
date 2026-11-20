#!/usr/bin/env python3
"""Tạo `.env` (nếu chưa có) và ghi tài khoản test của dự án hiện tại vào đó.

Claude chạy lệnh này khi vào dự án lần đầu trên máy (CLAUDE.md bước 0): hỏi người dùng địa chỉ, mã tài khoản,
tên đăng nhập, mật khẩu trong chat rồi ghi (mật khẩu qua stdin); người dùng muốn thì gõ ẩn trong terminal (getpass).

  python -X utf8 scripts/nhap-tai-khoan.py --trang-thai                 # khóa nào có/trống (không in giá trị)
  python -X utf8 scripts/nhap-tai-khoan.py --url https://staging...      # tạo .env + ghi địa chỉ
  python -X utf8 scripts/nhap-tai-khoan.py --ma NV01 --user nv01@vd.com  # ghi tên đăng nhập (mật khẩu để trống)
  python -X utf8 scripts/nhap-tai-khoan.py --ma NV01 --go-mat-khau       # NGƯỜI DÙNG chạy trong terminal: gõ ẩn mật khẩu
  ... --mat-khau-tu-stdin   # chỉ khi người dùng chọn gửi mật khẩu qua chat: đọc một dòng từ stdin

Khóa: `<TIỀN_TỐ>_URL`, `<TIỀN_TỐ>_<MÃ>_USER`, `<TIỀN_TỐ>_<MÃ>_PASSWORD` (tiền tố lấy từ `testing/<dự-án>/auto-config.json`,
chưa có thì từ slug). Giữ nguyên các dòng khác của `.env`. Không bao giờ in mật khẩu hay tên đăng nhập.
"""
import argparse
import getpass
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV = os.path.join(ROOT, ".env")
HEADER = ("# Tài khoản test trên máy này (không commit, đã có trong .gitignore). Mẫu khóa: .env.example.\n"
          "# Sửa bằng: python -X utf8 scripts/nhap-tai-khoan.py --ma <MÃ> --user <tên đăng nhập>\n")


def project_slug(arg):
    if arg:
        return arg
    f = os.path.join(ROOT, ".du-an-hien-tai")
    if not os.path.exists(f):
        sys.exit("Chưa có .du-an-hien-tai; truyền --project <slug>.")
    return io.open(f, encoding="utf-8").read().strip()


def env_prefix(slug):
    cfg = os.path.join(ROOT, "testing", slug, "auto-config.json")
    if os.path.exists(cfg):
        try:
            p = json.load(io.open(cfg, encoding="utf-8")).get("env_prefix", "")
            if p and "<" not in p:
                return p.rstrip("_")
        except ValueError:
            pass
    return slug.upper().replace("-", "_")


def read_lines():
    if not os.path.exists(ENV):
        return None
    return io.open(ENV, encoding="utf-8").read().replace("\r\n", "\n").split("\n")


def parse(lines):
    out = {}
    for line in lines or []:
        s = line.strip()
        if s and not s.startswith("#") and "=" in s:
            k, v = s.split("=", 1)
            out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def set_key(lines, slug, prefix, key, value):
    """Đổi dòng `key=` nếu có; chưa có thì thêm vào khối của dự án (tạo khối ở cuối nếu chưa có)."""
    for i, line in enumerate(lines):
        if line.strip().split("=", 1)[0].strip() == key and "=" in line and not line.strip().startswith("#"):
            lines[i] = f"{key}={value}"
            return
    last = None
    for i, line in enumerate(lines):
        if line.strip().startswith(prefix + "_") or line.strip() == f"# Dự án {slug}":
            last = i
    if last is None:
        while lines and lines[-1] == "":
            lines.pop()
        lines += ["", f"# Dự án {slug}", f"{key}={value}"]
    else:
        lines.insert(last + 1, f"{key}={value}")


def ask_password():
    for _ in range(3):
        p1 = getpass.getpass("Mật khẩu (gõ không hiện chữ, Enter để xong): ")
        if not p1:
            print("Mật khẩu trống, gõ lại.")
            continue
        if getpass.getpass("Gõ lại mật khẩu để chắc chắn: ") == p1:
            return p1
        print("Hai lần gõ không khớp, gõ lại.")
    sys.exit("Không ghi mật khẩu (gõ sai 3 lần).")


def check_value(name, value):
    if "\n" in value or "\r" in value:
        sys.exit(f"{name} không được có xuống dòng.")
    if value != value.strip():
        sys.exit(f"{name} có khoảng trắng ở đầu/cuối: .env sẽ cắt mất, nên không ghi. Kiểm tra lại giá trị.")
    if value[:1] in ("'", '"') or value[-1:] in ("'", '"'):
        # bộ đọc .env (test_automation/config.read_env) bỏ dấu nháy ở hai đầu: ghi vào sẽ thành giá trị khác
        sys.exit(f"{name} bắt đầu hoặc kết thúc bằng dấu nháy (' hoặc \"): .env sẽ cắt mất dấu này, nên không ghi. "
                 "Sửa tay .env cũng bị cắt như vậy: đổi mật khẩu trên hệ thống thử sang giá trị không có nháy ở hai đầu.")


def status(env, prefix):
    keys = sorted(k for k in env if k.startswith(prefix + "_"))
    if not keys:
        print(f"Chưa có tài khoản nào của dự án (tiền tố {prefix}_).")
        return
    for k in keys:
        print(f"  {k}: {'có giá trị' if env[k] else 'TRỐNG'}")
    codes = sorted({m.group(1) for k in keys for m in [re.match(rf"{re.escape(prefix)}_([A-Za-z0-9]+)_PASSWORD$", k)] if m and env[k]})
    print("Tài khoản dùng được: " + (", ".join(codes) if codes else "(chưa có)"))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project")
    ap.add_argument("--url", help="địa chỉ môi trường thử")
    ap.add_argument("--ma", help="mã tài khoản, chữ và số, ví dụ NV01, ADMIN")
    ap.add_argument("--user", help="tên đăng nhập / email")
    ap.add_argument("--go-mat-khau", action="store_true", help="hỏi mật khẩu gõ ẩn (chỉ chạy trong cửa sổ terminal có người gõ)")
    ap.add_argument("--mat-khau-tu-stdin", action="store_true", help="đọc mật khẩu từ một dòng stdin (khi người dùng chọn gửi qua chat)")
    ap.add_argument("--trang-thai", action="store_true")
    a = ap.parse_args()

    slug = project_slug(a.project)
    prefix = env_prefix(slug)
    lines = read_lines()
    created = lines is None
    if a.trang_thai:
        print(f"Dự án: {slug} · .env: {'chưa có' if created else 'có'}")
        status(parse(lines), prefix)
        return 0
    if created:
        lines = HEADER.rstrip("\n").split("\n")

    if a.url:
        check_value("Địa chỉ", a.url)
        set_key(lines, slug, prefix, f"{prefix}_URL", a.url.rstrip("/"))
    if a.ma:
        code = a.ma.upper()
        if not re.fullmatch(r"[A-Z0-9]+", code):
            sys.exit("Mã tài khoản chỉ gồm chữ và số (không dấu, không gạch), ví dụ NV01.")
        if a.user:
            check_value("Tên đăng nhập", a.user)
            set_key(lines, slug, prefix, f"{prefix}_{code}_USER", a.user)
        pw = None
        if a.mat_khau_tu_stdin:
            pw = sys.stdin.readline().rstrip("\r\n")
        elif a.go_mat_khau:
            pw = ask_password()
        if pw:
            check_value("Mật khẩu", pw)
            set_key(lines, slug, prefix, f"{prefix}_{code}_PASSWORD", pw)
        elif not parse(lines).get(f"{prefix}_{code}_PASSWORD"):
            set_key(lines, slug, prefix, f"{prefix}_{code}_PASSWORD", "")
            print(f"Chưa có mật khẩu {code}: người dùng chạy trong terminal: python -X utf8 scripts/nhap-tai-khoan.py --ma {code} --go-mat-khau")
    elif a.user:
        sys.exit("Thiếu --ma (mã tài khoản) cho tên đăng nhập.")

    text = "\n".join(lines).rstrip("\n") + "\n"
    io.open(ENV, "w", encoding="utf-8", newline="\n").write(text)
    print(("Đã tạo" if created else "Đã cập nhật") + f" .env (dự án {slug}, không in giá trị):")
    status(parse(lines), prefix)
    return 0


if __name__ == "__main__":
    sys.exit(main())
