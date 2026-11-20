---
name: feature-exploration-report
description: Lập báo cáo khám phá dạng HTML cho người mới từ lượt khám phá thật (vai trò, ảnh khoanh nút đánh số, sơ đồ luồng, điểm mơ hồ kèm bằng chứng). Dùng khi nghe "báo cáo khám phá", "làm báo cáo HTML cho feature X", "mô tả vai trò, luồng của hệ thống". Không dùng cho SRS (srs-from-website), bug hay test case.
---

# Báo cáo khám phá feature (HTML)

Biến một lượt khám phá thật trên hệ thống thành **một file HTML tự chứa**, mở được ngay trong khung xem trước của app. Khuôn: `assets/report-template.src.html`; sơ đồ mẫu: `assets/so-do-mau/`.

Ngôn ngữ: **tiếng Việt**, dùng đúng thuật ngữ IT, dễ hiểu (xem `references/report-structure.md` mục "Thuật ngữ").

## Quy tắc không được phá

1. **Chỉ ghi điều đã nhìn thấy trên màn hình.** Điều chưa kiểm chứng ghi `❓ chưa xác nhận`. Không suy đoán công thức, quyền, ý nghĩa thiết kế. Không kết luận “lỗi” hay “đúng thiết kế” khi chưa có tài liệu — viết “đã thấy / vì sao chưa rõ / cần làm rõ”.
2. **Trung thực về bằng chứng.** Chỗ nào không có ảnh thì nói “không có ảnh, chỉ ghi nhận trong báo cáo”. Không dựng lại ảnh, không gán ảnh cho khoảnh khắc khác.
3. **Mật khẩu:** không tự gõ mật khẩu; người dùng tự đăng nhập từng tài khoản trong cửa sổ trình duyệt. Không ghi mật khẩu vào báo cáo, bộ nhớ hay chat.
4. **Hỏi trước khi tạo/sửa dữ liệu thật, tải file, gửi thứ có thể ra ngoài** (SMS, email…). Dữ liệu test do mình tạo thì ghi rõ mã để người dùng nhận ra.
5. **Hỏi người dùng khi chưa rõ**, đừng tự quyết (xem mục 7 của báo cáo).
6. **Giữ đúng giao diện đã chốt, ở mọi dự án:** không viết CSS, không đổi màu/font trong báo cáo, không vẽ SVG sơ đồ bằng tay. Font (Be Vietnam Pro), màu, CSS, logo do `build-embed.py` chèn (từ `assets/` và `docs/thuong-hieu/`), cùng giao diện thương hiệu với mọi trang HTML khác của repo. Sơ đồ viết bằng JSON (`data-so-do`), `ve-so-do.py` vẽ. Cần kiểu sơ đồ mới thì hỏi người dùng trước. Chi tiết: `references/so-do.md`.
7. **Đã khám phá rồi thì KHÔNG khám phá lại.** Nếu đã có `evidence/<hệ thống>/features/<feature>/bao-cao.md` (hoặc báo cáo tổng) và ảnh, và mục 0 "Bảng phủ" của nhật ký không còn ô trống (khuôn ở `srs-from-website/assets/exploration-log-template.md`), dựng/sửa báo cáo HTML **từ đó**, không mở trình duyệt, không chụp lại. Chỉ khám phá lại khi **người dùng nói rõ** "khám phá lại" hoặc "feature đã đổi" (và phần nào đổi → chỉ làm phần đó). Thiếu bằng chứng → ghi "không có ảnh" và hỏi người dùng, không tự chụp bù. *Người dùng hết token để chạy lại.*

## Đọc gì cho từng việc
Luôn đọc: `memories/user/working-preferences.md`, `memories/project/overview.md`, và `memories/modules/<slug>/overview.md` của **dự án hiện tại** (slug trong `.du-an-hien-tai`; chưa có thì hỏi người dùng trước, xem `CLAUDE.md` bước 0). `<hệ thống>` trong các đường dẫn dưới đây chính là slug đó. **Không mở file của dự án khác, kể cả để làm mẫu**: dùng khuôn trong `assets/` (và `srs/_template.md`). Thêm theo việc:

| Việc | Đọc | Không cần đọc |
|---|---|---|
| Khám phá + làm báo cáo mới | `references/report-structure.md`, `references/evidence-and-build.md`, `references/so-do.md`, `assets/report-template.src.html`, `assets/so-do-mau/*.json`, `memories/user/document-preferences.md`, `memories/pitfalls/dont-trigger-lockouts.md`. Thêm các file khám phá của dự án hiện tại trong `memories/modules/<slug>/` (xem bảng của `memories/MEMORY.md`) và bộ nhớ của feature nếu có | File HTML đã build (~500 KB, đọc vô ích); ảnh cũ trong `evidence/` trừ khi dùng lại; `scripts/*.py`, `assets/giao-dien-chuan.css`, `assets/fonts/` (chỉ chạy/được chèn tự động) |
| Sửa báo cáo có sẵn | Phần cần sửa trong file `*.src.html` (tìm bằng Grep) hoặc file JSON sơ đồ trong `_src/so-do/`, `references/evidence-and-build.md` (mục build, soát), `references/so-do.md` nếu sửa sơ đồ. Nếu dự án đã có ghi chú về báo cáo: thêm file đó trong `memories/modules/<slug>/` (xem bảng của `memories/MEMORY.md`) | File HTML đã build; cả file nguồn nếu chỉ sửa một mục |
| Sửa chính skill này | `memories/project/skills.md`, file cần sửa | Báo cáo và ảnh |

Ảnh: chỉ mở những ảnh cần khoanh nút hoặc cần kiểm, không mở hàng loạt (một phiên trước mở 41 ảnh trước khi viết dòng đầu tiên).

## Quy trình

0. **Đọc đúng những file cần cho việc này** (bảng "Đọc gì cho từng việc" ngay dưới), sau `CLAUDE.md` và `memories/MEMORY.md`. Không đọc thêm cho chắc.
1. **Chốt phạm vi** (hỏi nếu thiếu): tên feature, URL hệ thống/phiên bản, danh sách tài khoản + vai trò đã biết, được phép tạo dữ liệu test không, tích hợp bên ngoài (SMS/email/…) là thật hay mô phỏng. **Ngữ cảnh hệ thống** (tài khoản, bản đồ feature, điều đã/chưa khám phá) đọc ở `memories/modules/<slug>/` của dự án hiện tại; chỉ khám phá thêm phần còn thiếu. **Không đọc ngữ cảnh của dự án khác**, mọi thông tin về hệ thống phải lấy từ khám phá thật của dự án này.
2. **Khám phá thật** — chỉ khi feature **chưa có** nhật ký/ảnh, hoặc người dùng nói rõ đã đổi/khám phá lại (quy tắc 7); đã có thì bỏ bước này và bước 5 chụp thêm, đi thẳng bước 3–4 từ nhật ký cũ. Cách làm, bằng trình duyệt (xem `references/evidence-and-build.md` mục "Chụp ảnh"). Với mỗi vai trò: màn hình đầu, từng nút, trường nhập, thông báo (chép **nguyên văn**), trạng thái chuyển. Chạy hết luồng chính rồi các nhánh (thành công, từ chối, trả lại/hoàn tác, nhập sai).
3. **Ghi nhật ký gốc bằng Markdown** (`evidence/<hệ thống>/features/<feature>/bao-cao.md`) ngay trong lúc khám phá: bảng thao tác → kết quả → số ảnh. Đây là nguồn sự thật để dựng HTML. Giữ mục “Chưa thử” và “Câu hỏi cho team”.
4. **Dựng nguồn HTML** từ `assets/report-template.src.html` → `evidence/<hệ thống>/features/<feature>/_src/<ten>.src.html`. Cấu trúc 7 mục và cách viết từng mục: `references/report-structure.md`. Giữ nguyên `<style id="giao-dien-chuan">` rỗng. **Sơ đồ:** chép `assets/so-do-mau/*.json` sang `_src/so-do/`, sửa nội dung (cách viết: `references/so-do.md`), xem thử bằng `scripts/ve-so-do.py`.
5. **Khoanh nút trên ảnh**: đo toạ độ thật từ ảnh gốc (mở ảnh, đọc vị trí), điền `<i class="mk" ...>`; vị trí số do script tự chọn. Chi tiết: `references/evidence-and-build.md`.
6. **Build**: `python -X utf8 scripts/build-embed.py --src <src.html> --out <report.html> --shots <thư_mục_ảnh>`. Phải ≤ 512 KiB (build tự giảm chất lượng ảnh thu nhỏ nếu vượt). Build in **Cảnh báo** (sơ đồ vẽ tay, CSS riêng đổi font/màu…) thì sửa cho hết rồi mới giao.
7. **Soát**: chạy thêm `--review <thư_mục>` và xem từng tranh ghép (khung có đúng ô? số có đè chữ/đè nhau?); mở file thật trong khung xem trước kiểm tra ảnh hiện, thanh tab cuộn đúng. Xong mới giao.
8. **Cập nhật bộ nhớ** (`memories/modules/<hệ thống>/feature-<tên>.md` + `MEMORY.md`): kết quả khám phá, bẫy mới, khoảng trống bằng chứng.
9. **Trả lời người dùng**: nêu file, điều đã kiểm tra, điều **chưa** kiểm tra, và các câu cần họ trả lời.

## Khi người dùng nhờ sửa báo cáo đã có

Sửa **file nguồn `*.src.html`**, chạy lại build — không sửa file đã build. Lỗi hay gặp: khung vẽ sai ô (không phải chỉ chồng số) → soát bằng `--review`. Đổi từ ngữ → áp cho toàn bộ báo cáo, rồi grep lại các từ cũ.


## Tệp trong skill

- `references/report-structure.md` — 7 mục báo cáo, văn phong, bảng thuật ngữ IT, quy tắc sơ đồ.
- Ngữ cảnh riêng của từng hệ thống (tài khoản, bản đồ feature, độ phủ khám phá) **không nằm trong skill**: ở `memories/modules/<slug>/` của dự án hiện tại.
- `references/evidence-and-build.md` — chụp ảnh, đặt tên, khoanh nút, build, soát, các bẫy đã gặp.
- `references/so-do.md` — giao diện chuẩn, cách viết JSON cho ba kiểu sơ đồ (tổng quan, tuần tự, trạng thái), bảng màu.
- `assets/report-template.src.html` — khung HTML nguồn (thanh tab, mẫu step/flow/điểm mơ hồ, chỗ đặt sơ đồ).
- `assets/giao-dien-chuan.css` — CSS chuẩn duy nhất (màu, cỡ chữ, bố cục); `assets/fonts/do-rong-chu.json` — bảng độ rộng chữ của Be Vietnam Pro; `scripts/giao_dien.py` — nạp font thương hiệu (cắt theo chữ thật), logo, CSS.
- `assets/so-do-mau/` — ba file JSON mẫu (nội dung trung lập) để chép sang dự án.
- `scripts/build-embed.py` — chèn CSS + font chuẩn, vẽ sơ đồ từ JSON, nhúng ảnh thu nhỏ, tự đặt số thứ tự, JS thanh tab, kiểm tra giới hạn 512 KiB.
- `scripts/ve-so-do.py` — vẽ sơ đồ theo mẫu đã chốt; chạy riêng để xem thử.
