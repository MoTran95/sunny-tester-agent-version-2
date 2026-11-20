# Tốc độ phiên: số đo và cách giữ nhanh
Đọc khi: người dùng than chậm/tốn token, hoặc sửa skill/khuôn/bộ nhớ.

## Số đo (nhật ký `~/.claude/projects/D--AI-sunny-tester-kit/*.jsonl`)
- Ngữ cảnh ở lượt trả lời đầu: **~73–76 nghìn token** (đo 2026-11-18 bằng `scripts/do-toc-do-phien.py`). Phân tích phiên đo: ~55 nghìn là phần đệm cố định (prompt hệ thống + schema công cụ của Claude Code); skill listing 30 nghìn ký tự (~7,5 nghìn token: repo+built-in 10,9K, `anthropic-skills` 10K, plugin tài khoản 9,1K ký tự); danh sách công cụ hoãn ~9K ký tự; `CLAUDE.md` ~4 KB. **Plugin/skill tài khoản chỉ ~2–5 nghìn token (3–6%)**, không phải "gần hết" như từng ghi. Repo chỉ góp `CLAUDE.md` + 4 skill (~1,5 nghìn token).
- Công cụ chỉ ~0,3–6 phút/phiên; phần lớn thời gian là mô hình **sinh chữ** (phiên ghi TL-01…05: 11,6 phút, một bước 52 nghìn token).
- Phiên kéo tới 300–700 nghìn token ngữ cảnh → mỗi bước sau chậm hơn.
- Nguyên nhân từng có: bảng soát 84 KB chép lặp câu hỏi; lớp "luôn đọc" dày; phiên dài nhiều việc; máy mới thiếu allowlist/Python/`.env`.

## Đã làm (2026-11-18)
| Việc | Kết quả |
|---|---|
| Bảng soát không chép lại câu hỏi | hai bảng soát thật giảm 25–28% dung lượng |
| Gọn phần luôn đọc | 17,4→8,9 KB, sau đó thu gọn bộ nhớ AI (xem dưới) |
| Bảng "Đọc gì cho từng việc" trong mỗi `SKILL.md` | |
| Máy mới | `.claude/settings.json` (13 quyền), `.env.example`, `kiem-tra-may-moi.py`, `docs/cai-dat-may-moi.md` (chưa thử máy mới thật) |
| Bộ nhớ chỉ cho AI đọc, viết ngắn, bản đồ dạng bảng | xem `memory-writing-rules.md` |
| Script tắt plugin qua `.claude/settings.local.json` (`syncClaudeAiPlugins=false`, `disableClaudeAiConnectors=true`) | **Đã đo, vô tác dụng → đã xóa script**: phiên mới vẫn 74,4 nghìn token, đủ 57 skill. Thử thêm 23 deny `Skill(...)`: vẫn 74,5 nghìn. Chi tiết `user/connectors-and-plugins.md` |

## Giảm đọc/viết lặp (2026-11-18, nhật ký 21 phiên)
- **Số đo đã loại trùng** (nhật ký ghi mỗi khối nội dung một dòng kèm cùng `usage`; gộp theo mã tin nhắn, `do-toc-do-phien.py` nay in sẵn): phiên skill = 90–200 lượt gọi mô hình, 110–500 nghìn token sinh ra (chữ nhìn thấy chỉ 23–37%, còn lại là suy nghĩ ẩn), **12–75 triệu token đọc lại từ cache** (ngữ cảnh TB 150–440 nghìn/lượt). Phần nạp sẵn ~70 nghìn × số lượt ≈ 7–14M; đọc skill ~15–20 nghìn × số lượt chỉ ~5–8%. Đòn bẩy thật: ít lượt hơn, ngữ cảnh nhỏ hơn, bớt suy nghĩ ở bước máy móc. Các số "300–700 nghìn token sinh ra" ghi trước đây bị đếm đôi.
- Kết quả lệnh Bash phiên nặng 190–240 KB, phần lớn là `cat` bộ nhớ/file và `grep` dòng bảng soát 700 ký tự; script soát chỉ in 160–800 byte. → quy tắc "Giữ ngữ cảnh gọn khi soát" trong cả 4 `SKILL.md`.
- Không chạy `truy-vet.py kiem` để "thử": nó **ghi** `truy-vet.md` và lịch sử vào checklist/test case (chỉ `tra` là chỉ đọc).
- Mô hình sinh ra 100–500 nghìn token/phiên nặng (xem số đo loại trùng ở trên); phần nhìn thấy được chủ yếu là **script Python viết một lần rồi bỏ** (30–46 KB: `build_analysis.py`, `cap-nhat-tl.py`, `gen_tc.py`) và đọc lại file lớn (bảng soát 73 KB đọc 8 lần/phiên).
- Đã làm: `truy-vet.py tra` (xem `project/truy-vet-requirement.md`) và `phan-tich-requirement/scripts/ghi-tl.py` (xem `project/skills.md`). **Chưa đo trên phiên thật**: mốc cũ phiên ghi 5 TL = 31 phút, 142 nghìn token sinh ra, 4 script viết mới (~86 KB).
- Đã làm (2026-11-18, chưa đo trên phiên thật): **cổng khám phá** (đã có nhật ký thì không khám phá lại; xem `project/srs-process.md`) + **mục 0 "Bảng phủ"** trong nhật ký khám phá + `srs-from-website/scripts/kiem-tra-bang-phu.py` (ĐỦ / CÒN THIẾU / KHÔNG CÓ); dựng bảng phủ cho các feature đã khám phá (trạng thái từng dự án ở `modules/<slug>/`). Quy tắc "Giữ ngữ cảnh gọn" ở 4 skill. `do-toc-do-phien.py` in lượt gọi/token sinh ra/token đọc lại đã loại trùng.
- Chưa làm (đề xuất): đoạn JS dò trang + ngân sách ảnh khi khám phá feature mới; đặt `effort` thấp cho skill máy móc (tách skill nhỏ; `context: fork` chỉ cho việc thuần file, không cho khám phá vì cần thao tác trên trình duyệt); nguồn JSON cho bảng soát + câu hỏi (cần round-trip).

## Rủi ro khi sửa
- Bảng soát: đừng thay câu hỏi bằng mã trần (người dùng chê mã nội bộ); `kiem-tra.py` phải theo.
- Gọn bộ nhớ: chuyển chỗ, không xóa quy tắc; sau sửa kiểm từng quy tắc còn đúng một nơi (`scripts/kiem-tra-bo-nho.py`).
- Hạ effort chỉ cho việc đơn giản (push git, ghi TL, sửa chữ); phân tích requirement/khám phá giữ mức cao.
- Thói quen người dùng: mỗi việc một phiên mới; nói rõ việc + feature ngay câu đầu.
