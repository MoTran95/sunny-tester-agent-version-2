#!/usr/bin/env python3
"""Tạo thư mục cho một dự án mới (hệ thống đang test) theo cấu trúc chung của repo.

Chạy từ gốc repo:
    python -X utf8 scripts/tao-du-an.py <slug> "<Tên dự án>" [<URL>]

Tạo:  memories/modules/<slug>/overview.md, srs/<slug>/, testing/<slug>/, evidence/<slug>/ (kèm .gitkeep),
      testing/<slug>/auto-config.json, auto-data.json, ten-tinh-nang.json (khuôn cho bộ chạy test tự động, còn chỗ `<…>` phải điền),
      khối khóa mẫu trong .env.example, thêm dòng vào bảng dự án trong memories/project/overview.md và mục trong memories/MEMORY.md,
      ghi slug vào .du-an-hien-tai.
Không ghi đè file đã có. Không đụng tới thư mục của dự án khác.
"""
import datetime
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    slug, ten = sys.argv[1].strip(), sys.argv[2].strip()
    url = sys.argv[3].strip() if len(sys.argv) > 3 else ""
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        print("LỖI: slug phải là kebab-case, chữ thường không dấu, ví dụ shop-online")
        return 2
    today = datetime.date.today().isoformat()
    env_prefix = slug.upper().replace("-", "_") + "_"

    for d in ("srs", "testing", "evidence"):
        p = os.path.join(ROOT, d, slug)
        os.makedirs(p, exist_ok=True)
        keep = os.path.join(p, ".gitkeep")
        if not os.listdir(p):
            io.open(keep, "w", encoding="utf-8").close()
        print("thư mục:", os.path.relpath(p, ROOT))

    test_dir = os.path.join(ROOT, "testing", slug)
    prefix = env_prefix.rstrip("_")
    auto_files = {
        "auto-config.json": {
            "env_prefix": prefix,
            "default_url": url or "<địa chỉ hệ thống đang test, phải có nhãn môi trường thử như staging, dev, test>",
            "login": {
                "id_labels": ["<nhãn ô tên đăng nhập, ví dụ Tên đăng nhập>"],
                "button_labels": ["<nhãn nút đăng nhập, ví dụ Đăng nhập>"],
                "login_api": "</đường dẫn API đăng nhập, lấy bằng scripts/inspect_page.py>",
                "session_check_api": "</đường dẫn API kiểm phiên, ví dụ /api/me>",
                "session_minutes": "<số phút phiên sống, điền số>",
                "max_consecutive_failures": None,
                "block_minutes": None,
            },
        },
        "auto-data.json": {"version": "", "ghi_chu": "version: số bản ở chân trang cần test, đổi khi có build mới. Thêm id dữ liệu test của dự án vào đây."},
        "ten-tinh-nang.json": {},
    }
    for name, content in auto_files.items():
        target = os.path.join(test_dir, name)
        if os.path.exists(target):
            print("đã có, giữ nguyên:", os.path.relpath(target, ROOT))
            continue
        io.open(target, "w", encoding="utf-8", newline="\n").write(json.dumps(content, ensure_ascii=False, indent=2) + "\n")
        print("tạo:", os.path.relpath(target, ROOT))

    env_example = os.path.join(ROOT, ".env.example")
    if os.path.exists(env_example):
        mau = io.open(env_example, encoding="utf-8").read()
        if f"{prefix}_URL" not in mau:
            khoi = f"# Dự án {slug}\n{prefix}_URL=\n{prefix}_<MÃ TÀI KHOẢN>_USER=\n{prefix}_<MÃ TÀI KHOẢN>_PASSWORD=\n"
            mau = mau.rstrip("\n") + "\n\n" + khoi
            io.open(env_example, "w", encoding="utf-8", newline="\n").write(mau)
            print("thêm khối khóa mẫu vào .env.example")

    mem_dir = os.path.join(ROOT, "memories", "modules", slug)
    os.makedirs(mem_dir, exist_ok=True)
    ov = os.path.join(mem_dir, "overview.md")
    if os.path.exists(ov):
        print("đã có, giữ nguyên:", os.path.relpath(ov, ROOT))
    else:
        io.open(ov, "w", encoding="utf-8", newline="\n").write(f"""# {ten} — tổng quan
Đọc khi: đầu tiên khi làm {ten} (`.du-an-hien-tai` = {slug}). Ngày tạo: {today}.

## Hệ thống
- URL: {url or "_chưa có, hỏi người dùng_"}
- Tài khoản test: _chưa biết_ (mật khẩu trong `.env`, khóa bắt đầu bằng `{env_prefix}`).

## Bối cảnh
_Chưa có. Chỉ ghi điều người dùng nói hoặc đã thấy trên hệ thống này; không suy từ dự án khác._

## Thư mục của dự án
| Loại | Đường dẫn |
|---|---|
| Bộ nhớ | `memories/modules/{slug}/` |
| SRS | `srs/{slug}/` |
| Phân tích requirement | `testing/{slug}/` |
| Bằng chứng, báo cáo HTML | `evidence/{slug}/` |

## Việc cần làm tiếp
_Điền khi có._
""")
        print("tạo:", os.path.relpath(ov, ROOT))

    tn = os.path.join(mem_dir, "tu-ngu-cau-hoi-ba.md")
    if not os.path.exists(tn):
        noi_dung = (
            f"# {ten} — từ đã chốt cho câu hỏi BA\n"
            f"Đọc khi: viết câu hỏi BA cho {ten} (quy ước chung: `conventions/ba-question-wording.md`). "
            "**Bảng trống**: chỉ ghi từ người dùng hoặc BA của dự án này đã chốt; KHÔNG lấy từ dự án khác.\n\n"
            "| Khái niệm | Dùng | Tránh |\n|---|---|---|\n")
        io.open(tn, "w", encoding="utf-8", newline="\n").write(noi_dung)
        print("tạo:", os.path.relpath(tn, ROOT))

    pov = os.path.join(ROOT, "memories", "project", "overview.md")
    text = io.open(pov, encoding="utf-8").read()
    if f"| `{slug}` |" not in text:
        row = f"| `{slug}` | {ten} | [../modules/{slug}/overview.md](../modules/{slug}/overview.md) |"
        lines = text.split("\n")
        rows = [i for i, l in enumerate(lines) if l.startswith("| `")]
        if rows:
            idx = rows[-1]
        else:   # bảng chưa có dự án nào (bộ lõi mới xuất): chèn ngay dưới dòng `|---|` của bảng có cột Slug
            head = [i for i, l in enumerate(lines) if l.startswith("| Slug |")]
            if not head or head[0] + 1 >= len(lines) or not lines[head[0] + 1].startswith("|---"):
                sys.exit(f"Không thấy bảng dự án (dòng '| Slug |' và '|---|') trong {os.path.relpath(pov, ROOT)}; thêm dòng tay: {row}")
            idx = head[0] + 1
        if lines[idx].endswith("\r"):
            row += "\r"
        lines.insert(idx + 1, row)
        io.open(pov, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
        print("thêm dòng vào bảng dự án:", os.path.relpath(pov, ROOT))

    mmp = os.path.join(ROOT, "memories", "MEMORY.md")
    mm = io.open(mmp, encoding="utf-8").read()
    if f"modules/{slug}/overview.md" not in mm:
        mm = mm.rstrip("\n") + (
            f"\n\n## Dự án `{slug}` (chỉ khi `.du-an-hien-tai` = {slug})\n"
            "| File | Khi | Chứa |\n|---|---|---|\n"
            f"| `modules/{slug}/overview.md` | đầu tiên | hệ thống, tài khoản, thư mục |\n"
            f"| `modules/{slug}/tu-ngu-cau-hoi-ba.md` | viết câu hỏi BA | từ đã chốt với BA của dự án này |\n"
        )
        io.open(mmp, "w", encoding="utf-8", newline="\n").write(mm)
        print("thêm mục dự án vào memories/MEMORY.md")

    io.open(os.path.join(ROOT, ".du-an-hien-tai"), "w", encoding="utf-8", newline="\n").write(slug + "\n")
    print("dự án hiện tại trên máy này:", slug)
    # Sinh trang tổng ngay (có sẵn mục Hướng dẫn) để gửi người dùng một link duy nhất
    import subprocess
    r = subprocess.run([sys.executable, "-X", "utf8", os.path.join(ROOT, "scripts", "build_docs.py"), "--project", slug],
                       capture_output=True, text=True, encoding="utf-8", cwd=ROOT)
    index = os.path.join(ROOT, "testing", slug, "index.html")
    if os.path.exists(index):
        print("trang tổng:", os.path.relpath(index, ROOT).replace(os.sep, "/"), "(gửi người dùng link này, kèm #huong-dan)")
    else:
        print("CHƯA sinh được trang tổng:", (r.stdout + r.stderr).strip()[-300:])

    print("\nViệc còn lại:")
    print(f"- Mỗi tính năng có SRS: python -X utf8 scripts/truy-vet.py khoi-tao {slug} <tính-năng> --tien-to <MÃ> --ten \"<Tên tính năng>\" "
          "(tạo cấu hình truy vết, ghi tên tính năng cho trang HTML và test plan).")
    print(f"- Chỉ khi chạy test tự động: thêm tài khoản vào .env (tiền tố {env_prefix}) và điền các chỗ <…> trong "
          f"testing/{slug}/auto-config.json (nhãn ô, API: dùng scripts/inspect_page.py). Viết tài liệu, bug, test plan không cần hai việc này.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
