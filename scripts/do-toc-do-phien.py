#!/usr/bin/env python3
"""Đo tốc độ các phiên Claude gần nhất của repo, từ nhật ký phiên trên máy này.

Chạy từ gốc repo (hoặc từ bản sao repo):
    python -X utf8 scripts/do-toc-do-phien.py            # 5 phiên gần nhất
    python -X utf8 scripts/do-toc-do-phien.py --so 10

Với mỗi phiên in: câu đầu của người dùng, số file đã đọc trước khi bắt tay làm (lần ghi/sửa file
hoặc mở trình duyệt đầu tiên), số phút tới lúc đó, tổng phút mô hình suy nghĩ/viết, bước suy nghĩ
dài nhất, số lượt gọi mô hình, token sinh ra (và phần chữ nhìn thấy được), token đọc lại từ cache
(đã gộp theo mã tin nhắn nên không đếm đôi), và các file của dự án KHÁC dự án hiện tại đã bị mở
(để kiểm "không lẫn dự án").
Chỉ đọc nhật ký, không gửi gì ra ngoài.
"""
import argparse
import datetime
import glob
import io
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACTION = ("Write", "Edit", "NotebookEdit")


def ts(t):
    return datetime.datetime.fromisoformat(t.replace("Z", "+00:00"))


def project_log_dir():
    name = re.sub(r"[^A-Za-z0-9]", "-", ROOT)
    return os.path.join(os.path.expanduser("~"), ".claude", "projects", name)


def user_text(c):
    if isinstance(c, str):
        return c
    for b in c or []:
        if b.get("type") == "text" and not b["text"].lstrip().startswith("<"):
            return b["text"]
    return None


def analyse(path, slug, projects):
    rows = [json.loads(l) for l in io.open(path, encoding="utf-8") if l.strip()]
    rows = [r for r in rows if r.get("timestamp") and r.get("type") in ("user", "assistant")]
    first, t0, t_action, reads, other, bash = None, None, None, [], set(), 0
    gen, longest, prev = 0.0, 0.0, None
    ctx0 = None  # ngữ cảnh (nghìn token) ở lượt trả lời đầu tiên = phần nạp sẵn + câu đầu
    for r in rows:
        t, c = ts(r["timestamp"]), (r.get("message") or {}).get("content")
        if ctx0 is None and r["type"] == "assistant":
            u = (r.get("message") or {}).get("usage") or {}
            tot = sum(u.get(k) or 0 for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
            if tot:
                ctx0 = tot / 1000
        if r["type"] == "user":
            txt = user_text(c)
            if first is None and txt:
                first, t0 = txt.strip().replace("\n", " ")[:80], t
            prev = t
            continue
        if prev is not None:
            g = (t - prev).total_seconds()
            if g < 1800:
                gen += g
                longest = max(longest, g)
        prev = t
        for b in c if isinstance(c, list) else []:
            if b.get("type") != "tool_use":
                continue
            name, inp = b["name"], b.get("input") or {}
            fp = str(inp.get("file_path") or inp.get("path") or inp.get("command") or "").replace("\\", "/")
            for p in projects:
                if p != slug and re.search(r"(memories/modules|srs|testing|evidence)/" + re.escape(p) + r"(/|$)", fp):
                    other.add(os.path.basename(fp.split()[0]) if " " not in fp else fp[:70])
            if first and t_action is None:
                if name in ACTION or name.startswith("mcp__Claude_Browser"):
                    t_action = t
                elif name == "Read":
                    reads.append(os.path.basename(fp))
                elif name in ("Bash", "PowerShell", "Grep", "Glob"):
                    bash += 1
    # Tổng token theo từng lượt gọi mô hình. Nhật ký ghi mỗi khối nội dung (suy nghĩ, chữ, lệnh) thành
    # một dòng riêng kèm cùng `usage`, nên phải gộp theo mã tin nhắn, nếu không số bị đếm đôi/đếm ba.
    calls = {}
    for r in rows:
        if r["type"] != "assistant":
            continue
        m = r.get("message") or {}
        u = m.get("usage") or {}
        if not u:
            continue
        mid = m.get("id") or r.get("uuid")
        c = calls.setdefault(mid, {"out": 0, "cr": 0, "cn": 0, "vis": 0})
        c["out"] = max(c["out"], u.get("output_tokens") or 0)
        c["cr"] = max(c["cr"], u.get("cache_read_input_tokens") or 0)
        c["cn"] = max(c["cn"], u.get("cache_creation_input_tokens") or 0)
        for b in m.get("content") or []:
            if b.get("type") == "text":
                c["vis"] += len(b.get("text", ""))
            elif b.get("type") == "tool_use":
                c["vis"] += len(json.dumps(b.get("input") or {}, ensure_ascii=False))
    out = sum(c["out"] for c in calls.values())
    return {
        "api": len(calls), "out": out, "vis": sum(c["vis"] for c in calls.values()) / 3.2,
        "cr": sum(c["cr"] for c in calls.values()), "cn": sum(c["cn"] for c in calls.values()),
        "file": os.path.basename(path)[:8], "first": first or "?",
        "reads": reads, "bash": bash, "to_action": ((t_action - t0).total_seconds() / 60) if t_action and t0 else None,
        "gen": gen / 60, "longest": longest / 60, "other": sorted(other), "ctx0": ctx0,
        "start": t0.astimezone().strftime("%Y-%m-%d %H:%M") if t0 else "?",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--so", type=int, default=5, help="số phiên gần nhất cần đo")
    a = ap.parse_args()
    d = project_log_dir()
    def start(f):
        for line in io.open(f, encoding="utf-8"):
            r = json.loads(line) if line.strip() else {}
            if r.get("timestamp"):
                return r["timestamp"]
        return ""
    files = sorted(glob.glob(os.path.join(d, "*.jsonl")), key=start, reverse=True)[: a.so]
    if not files:
        print("Chưa có nhật ký phiên nào cho thư mục này:", d)
        return 1
    cur = os.path.join(ROOT, ".du-an-hien-tai")
    slug = io.open(cur, encoding="utf-8").read().strip() if os.path.exists(cur) else ""
    mods = os.path.join(ROOT, "memories", "modules")
    projects = [p for p in os.listdir(mods) if os.path.isdir(os.path.join(mods, p))]
    print(f"Dự án hiện tại: {slug or '(chưa chọn)'} · nhật ký: {d}\n")
    for f in reversed(files):
        s = analyse(f, slug, projects)
        to_a = f"{s['to_action']:.1f}" if s["to_action"] is not None else "chưa ghi file"
        print(f"[{s['start']}] {s['first']}")
        if s["ctx0"] is not None:
            print(f"   ngữ cảnh ở lượt trả lời đầu: {s['ctx0']:.0f} nghìn token (phần nạp sẵn: plugin, skill, công cụ + CLAUDE.md)")
        print(f"   trước khi làm: đọc {len(s['reads'])} file, {s['bash']} lệnh tìm/đọc khác · tới lúc bắt tay làm: {to_a} phút · "
              f"mô hình suy nghĩ/viết: {s['gen']:.1f} phút · bước dài nhất: {s['longest']:.1f} phút")
        if s["api"]:
            pct = 100 * s["vis"] / s["out"] if s["out"] else 0
            print(f"   lượt gọi mô hình: {s['api']} · token sinh ra: {s['out']/1000:.0f}k (chữ nhìn thấy ~{pct:.0f}%, còn lại là suy nghĩ ẩn) · "
                  f"token đọc lại từ cache: {s['cr']/1e6:.1f}M (ngữ cảnh TB {(s['cr'] + s['cn'])/s['api']/1000:.0f}k/lượt)")
        if s["reads"]:
            print("   file đã đọc:", ", ".join(s["reads"][:15]) + (" …" if len(s["reads"]) > 15 else ""))
        print("   mở file của dự án khác:", ", ".join(s["other"]) if s["other"] else "không",
              "(so với dự án hiện tại; nếu phiên đã đổi dự án giữa chừng thì các lượt trước khi đổi cũng bị tính)" if s["other"] else "")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
