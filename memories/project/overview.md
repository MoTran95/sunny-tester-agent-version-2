# Tổng quan repo (LUÔN ĐỌC)

- Repo này (thư mục gốc chứa `CLAUDE.md`; chạy Windows và Mac), remote ở `git-remote.md`. Chỗ làm việc của **tester** cho **nhiều dự án** (mỗi dự án = một hệ thống đang test).
- Dùng chung: 11 skill `.claude/skills/` (`skills.md`), khuôn `srs/_template.md` + `srs/id-and-source-rules.md`, memory chung (trừ `memories/modules/`).
- Riêng mỗi dự án: `memories/modules/<slug>/`, `srs/<slug>/`, `testing/<slug>/`, `evidence/<slug>/`. **Không dùng kiến thức dự án này cho dự án khác** (`conventions/nhieu-du-an.md`).
- Tài liệu cho **người đọc** (srs/, testing/, evidence/, docs/, báo cáo HTML) viết đầy đủ; `memories/` chỉ cho AI, viết ngắn (`conventions/memory-writing-rules.md`).

| Slug | Tên | Tổng quan |
|---|---|---|
| `ecommerce-lite` | Ecommerce Lite | [../modules/ecommerce-lite/overview.md](../modules/ecommerce-lite/overview.md) |

Dự án mới: `scripts/tao-du-an.py` tự thêm dòng.
