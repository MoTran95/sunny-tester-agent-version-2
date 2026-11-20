#!/usr/bin/env python3
"""Soát một file SRS theo khuôn Story + AC của repo (srs/_template.md).

Kiểm tra:
  - ID định nghĩa trùng nhau
  - Tham chiếu tới ID chưa được định nghĩa
  - AC thiếu story cha, thiếu nhãn (đã thấy / theo tài liệu / đã xác nhận / chưa rõ / đã bỏ) hoặc thiếu bằng chứng
  - Dải ID (`MÃ-R01–R04`, `MÃ-S01-AC03–AC05`) được mở thành từng ID rồi kiểm như tham chiếu thường
  - Liên kết bằng chứng #eNN không có mỏ neo <a id="eNN">
  - Liên kết tệp tương đối (ảnh, nhật ký) không tồn tại
  - Dòng bằng chứng không có liên kết tệp
  - Từ/ký hiệu bị cấm làm tên cột hoặc nhãn (cảnh báo)
  - Dòng AC/quy tắc/thông báo/câu hỏi thiếu thẻ neo <a id="<mã chữ thường>"> ở ô đầu (cảnh báo):
    test case link tới đúng dòng SRS nhờ thẻ này. `--them-neo` tự chèn thẻ còn thiếu (ghi vào file).
In số liệu để đối chiếu với mục "Lịch sử thay đổi".

Dùng:  python -X utf8 check-srs.py srs/<hệ thống>/<feature>.md [--them-neo]
Thoát mã 1 nếu có lỗi (cảnh báo không làm thoát mã 1).
"""
import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote

LABELS = ("đã thấy", "theo tài liệu", "đã xác nhận", "chưa rõ", "đã bỏ")
# (mẫu, gợi ý). Chỉ cảnh báo: có thể nằm trong đoạn giải thích hợp lệ.
FORBIDDEN = [
    (r"\bCho trước\b", "không dùng 'Cho trước/Khi/Thì' làm tên cột"),
    (r"\bGiven\b", "chỉ nhắc Given-When-Then một lần trong đoạn 'Cách đọc'"),
    (r"NK#\d+", "ký hiệu nguồn viết tắt 'NK#' khó hiểu — dùng 'Nhật ký, hàng N'"),
    (r"\bDN-\d+", "ký hiệu 'DN-NN' khó hiểu — dùng 'Ảnh NN'"),
    (r"\bBC-\d+", "ký hiệu 'BC-NN' khó hiểu — dùng 'Ảnh cũ NN'"),
    (r"\b(FR|BR)-[A-Z]+-\d+", "ID kiểu cũ FR-/BR- — dùng S/AC/R/M/Q/E"),
    (r"giải phẫu|dây chuyền|\btick\b", "từ người dùng đã chê — dùng từ thông dụng khác"),
]

ROW_ID = re.compile(r'^\|\s*(?:<a id="[^"]+"></a>)?`([A-Z][A-Z0-9]*-[A-Z0-9-]+)`\s*\|')
HEAD_ID = re.compile(r"^#{2,4}\s+`([A-Z][A-Z0-9]*-S\d+)`")
LINK = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")
ANCHOR = re.compile(r'<a id="([^"]+)"></a>')


def file_exists(base, rel):
    """Tệp tương đối có tồn tại không. Chuẩn hóa `..` trước (đường dẫn thô `srs/x/../../evidence/...` dễ vượt
    giới hạn 260 ký tự của Windows khi repo nằm sâu), và dùng tiền tố đường dẫn dài của Windows khi cần."""
    import os
    full = os.path.normpath(os.path.abspath(os.path.join(str(base), rel)))
    if os.name == "nt" and len(full) >= 240 and not full.startswith("\\\\?\\"):
        full = "\\\\?\\" + full
    return os.path.exists(full)


def kind(i):
    """Phân loại ID theo phần cuối: S, AC, R, M, Q, E."""
    if re.search(r"-S\d+-AC\d+$", i):
        return "AC"
    m = re.search(r"-([A-Z])\d+$", i)
    return m.group(1) if m else "?"


def make_expander(code_re, errors):
    """Trả về hàm mở dải ID thành từng ID đầy đủ.

    Hiểu `MÃ-R01–R04` (hoặc `MÃ-R01–04`, `MÃ-R01 đến R04`) và dải AC
    `MÃ-S01-AC03–AC05`. Dấu nối: gạch dài – / —, hoặc chữ "đến". Không dùng
    gạch ngang '-' để khỏi lẫn với dấu gạch trong chính ID.
    """
    rng = re.compile(
        rf"\b((?:{code_re})-(?:S\d+-AC|[A-Z]))(\d+)\s*(?:[–—]|đến)\s*[A-Z]*(\d+)\b"
    )

    def expand(line, n):
        def repl(m):
            prefix, a, b = m.group(1), m.group(2), m.group(3)
            lo, hi = int(a), int(b)
            if hi < lo or hi - lo > 200:
                errors.append(f"dòng {n}: dải ID '{m.group(0)}' không hợp lệ (cuối nhỏ hơn đầu hoặc quá dài)")
                return m.group(0)
            return ", ".join(f"{prefix}{i:0{len(a)}d}" for i in range(lo, hi + 1))
        return rng.sub(repl, line)

    return expand


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("srs", help="đường dẫn file SRS (.md)")
    ap.add_argument("--them-neo", action="store_true",
                    help="chèn thẻ neo vào ô đầu các dòng AC/R/M/Q (<mã chữ thường>) và bằng chứng E (e01) còn thiếu, rồi soát")
    args = ap.parse_args()
    path = Path(args.srs)
    raw = path.read_bytes()
    text = raw.decode("utf-8")
    if args.them_neo:
        added = 0

        def add_anchor(m):
            nonlocal added
            i = m.group(1)
            k = kind(i)
            if k not in ("AC", "R", "M", "Q", "E"):
                return m.group(0)
            added += 1
            # dòng bằng chứng dùng neo ngắn `e01` (khuôn link [E01](#e01)); dòng khác dùng cả mã, chữ thường
            anchor = re.sub(r"^.*-E", "e", i) if k == "E" else i.lower()
            return f'| <a id="{anchor}"></a>`{i}`'
        text = re.sub(r"(?m)^\|\s*`([A-Z][A-Z0-9]*-[A-Z0-9-]+)`", add_anchor, text)
        if added:
            path.write_bytes(text.encode("utf-8"))
        print(f"Đã chèn {added} thẻ neo.")
    lines = text.split("\n")

    errors, warns = [], []
    defined = {}  # id -> số dòng đầu tiên
    ac_rows = {}  # id -> (số dòng, nội dung)
    ev_rows = {}

    for n, line in enumerate(lines, 1):
        ids = []
        m = HEAD_ID.match(line)
        if m:
            ids.append(m.group(1))
        m = ROW_ID.match(line)
        if m:
            ids.append(m.group(1))
        for i in ids:
            if i in defined:
                errors.append(f"dòng {n}: ID '{i}' định nghĩa trùng (đã có ở dòng {defined[i]})")
            else:
                defined[i] = n
            k = kind(i)
            if k == "AC":
                ac_rows[i] = (n, line)
            elif k == "E":
                ev_rows[i] = (n, line)

    codes = {i.split("-")[0] for i in defined}
    if not codes:
        errors.append("không tìm thấy ID nào theo dạng `MÃ-S01`, `MÃ-S01-AC01`… (file có đúng khuôn không?)")
    code_re = "|".join(re.escape(c) for c in sorted(codes)) or "ZZZ"

    # Tham chiếu tới ID chưa định nghĩa
    ref_re = re.compile(rf"`?\b((?:{code_re})-[A-Z]\d+(?:-AC\d+)?)\b`?")
    expand = make_expander(code_re, errors)
    # Dải ID (R01–R04) được mở thành từng ID trước khi tìm tham chiếu
    xlines = [expand(l, n) for n, l in enumerate(lines, 1)]
    referenced = set()
    for n, line in enumerate(xlines, 1):
        for m in ref_re.finditer(line):
            i = m.group(1)
            referenced.add(i)
            if i not in defined:
                errors.append(f"dòng {n}: tham chiếu '{i}' nhưng chưa được định nghĩa")

    # Mỏ neo bằng chứng
    anchors = set(ANCHOR.findall(text))
    for n, line in enumerate(lines, 1):
        for _, target in LINK.findall(line):
            if target.startswith("#") and target[1:] not in anchors:
                errors.append(f"dòng {n}: liên kết '{target}' không có mỏ neo <a id=\"{target[1:]}\"> tương ứng")

    # AC: story cha, nhãn, bằng chứng
    for i, (n, line) in ac_rows.items():
        story = re.sub(r"-AC\d+$", "", i)
        if story not in defined:
            errors.append(f"dòng {n}: {i} không có story cha '{story}'")
        lowered = line.lower()
        label = next((l for l in LABELS if l in lowered), None)
        if not label:
            errors.append(f"dòng {n}: {i} thiếu nhãn ({' / '.join(LABELS)})")
        if label != "đã bỏ" and not re.search(rf"\[E\d+\]\(#e\d+\)|(?:{code_re})-E\d+", line):
            errors.append(f"dòng {n}: {i} thiếu bằng chứng (liên kết [Exx](#exx) hoặc ID MÃ-Exx)")

    # Bằng chứng: phải có liên kết tệp
    for i, (n, line) in ev_rows.items():
        files = [t for _, t in LINK.findall(line) if not t.startswith("#")]
        if not files:
            warns.append(f"dòng {n}: bằng chứng {i} không có liên kết tệp (ảnh hoặc nhật ký)")

    # Liên kết tệp tương đối phải tồn tại
    base = path.parent
    checked = set()
    for n, line in enumerate(lines, 1):
        for _, target in LINK.findall(line):
            if target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            rel = unquote(target.split("#")[0])
            if not rel or (n, rel) in checked:
                continue
            checked.add((n, rel))
            if not file_exists(base, rel):
                errors.append(f"dòng {n}: liên kết tệp không tồn tại: {rel}")

    # ID đã định nghĩa nhưng không ai tham chiếu (cảnh báo nhẹ cho R, M, E)
    body_refs = {}
    for n, line in enumerate(xlines, 1):
        for m in ref_re.finditer(line):
            body_refs.setdefault(m.group(1), set()).add(n)
    for i, n in defined.items():
        if kind(i) in ("R", "M"):
            if not (body_refs.get(i, set()) - {n}):
                warns.append(f"dòng {n}: {i} chưa được AC hay mục nào tham chiếu")
    for i, (n, _) in ev_rows.items():
        short = re.sub(r"^.*-E", "E", i)  # E01
        used = re.search(rf"\[{short}\]\(#{short.lower()}\)", text) or (body_refs.get(i, set()) - {n})
        if not used:
            warns.append(f"dòng {n}: bằng chứng {i} chưa được AC/quy tắc/thông báo nào dùng")

    # Từ cấm (cảnh báo)
    for n, line in enumerate(lines, 1):
        if "Given – When – Then" in line or "Given - When - Then" in line:
            continue  # đoạn giải thích hợp lệ
        for pat, hint in FORBIDDEN:
            if re.search(pat, line):
                warns.append(f"dòng {n}: '{pat}' — {hint}")

    # Thẻ neo cho dòng AC/R/M/Q (để test case link tới đúng dòng)
    no_anchor = []
    for n, line in enumerate(lines, 1):
        m = ROW_ID.match(line)
        if m and kind(m.group(1)) in ("AC", "R", "M", "Q") and not line.lstrip("| ").startswith("<a id="):
            no_anchor.append(m.group(1))
    if no_anchor:
        warns.append(f"{len(no_anchor)} dòng thiếu thẻ neo (ví dụ {no_anchor[0]}); test case sẽ không link tới đúng dòng. "
                     f"Chạy lại với --them-neo để tự chèn")

    counts = {}
    for i in defined:
        counts[kind(i)] = counts.get(kind(i), 0) + 1

    print(f"File: {path}")
    print("Số liệu (đối chiếu với 'Lịch sử thay đổi'): "
          f"story={counts.get('S', 0)}, AC={counts.get('AC', 0)}, quy tắc R={counts.get('R', 0)}, "
          f"thông báo M={counts.get('M', 0)}, câu hỏi Q={counts.get('Q', 0)}, bằng chứng E={counts.get('E', 0)}")
    for w in warns:
        print("CẢNH BÁO:", w)
    for e in errors:
        print("LỖI:", e)
    print(f"Kết quả: {len(errors)} lỗi, {len(warns)} cảnh báo")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
