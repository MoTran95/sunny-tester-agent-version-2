# Giao diện thương hiệu của mọi trang HTML

Mọi trang HTML do script sinh ra (bảng kết quả chạy, trang bug, trang tài liệu SRS/test case/bảng soát…, trang tổng) dùng **một** bộ giao diện duy nhất: `scripts/test_automation/theme.py`. Máy khác hay dự án khác chỉ cần clone repo là ra trang giống hệt; không có cấu hình riêng theo máy.

## Màu (lấy mẫu từ ảnh thương hiệu, hạ độ sáng cho đỡ chói)

| Vai trò | Sáng | Tối |
|---|---|---|
| Nền trang | `#E8DFD0` | `#251F1A` |
| Thẻ, bảng | `#F2EDE5` | `#2E2721` |
| Chữ chính | `#3A2E26` | `#F1E6D4` |
| Nhấn đỏ san hô (link, nút chính, lỗi) | `#C24E3A` | `#EE8F7C` |
| Vàng hổ phách (cảnh báo, ô được chọn) | `#D9902A` | `#E8A53C` |
| Xanh lá (đạt) | `#2E7D32` | `#86D08F` |
| Khung đỏ chỗ lỗi trên ảnh | `#E5252A` | |
| Khung xanh chỗ đạt trên ảnh | `#1B8F3A` | |

Chế độ sáng/tối theo hệ điều hành, có nút đổi tay (nhớ trong trình duyệt). Giá trị thật nằm ở đầu `CSS_BASE` trong `theme.py`.

## Font

- **Be Vietnam Pro** cho cả tiêu đề và chữ thường (đổi từ Fraunces + Hanken Grotesk ngày 2026-11-19 vì dấu tiếng Việt hiển thị lỗi). Font thiết kế cho tiếng Việt, giấy phép SIL OFL (dùng tự do, được đưa vào repo).
- Font nằm sẵn trong repo ở `docs/thuong-hieu/fonts/` (15 file `.woff2`: độ đậm 400, 500, 600, 700 và nghiêng 400, mỗi độ đậm ba tập ký tự gồm tiếng Việt, khoảng 230 KB, kèm `fonts.json`), nên trang giống hệt trên mọi máy kể cả khi không có mạng. `theme.py` tự dùng chúng.
- Tải lại hoặc cập nhật: `python -X utf8 scripts/tai-font.py` (tải từ Google Fonts), rồi `python -X utf8 scripts/build_docs.py --all`. Chưa có `fonts.json` thì trang tạm lấy font từ Google Fonts (cần mạng).

## Logo

- Logo gốc: `docs/thuong-hieu/logo-sunny-nhan-ra.png` (nền trong suốt). Bản nhúng vào trang: `logo-sunny-nhan-ra-nen-trong.png` (420 px, khoảng 55 KB), tạo bằng `python -X utf8 scripts/process_logo.py` (dọn chấm nhiễu li ti, cắt phần trống; cần Pillow). Logo gốc nền trắng cũng dùng được: script đổi nền trắng thành trong suốt.
- Logo nằm ở **góc trái đầu trang** (cao 60 px, nút đổi sáng/tối ở góc phải), nhúng thẳng vào mọi trang (không phụ thuộc đường dẫn). Đổi logo: thay file gốc, chạy `process_logo.py`, rồi `build_docs.py --all`.
- Màu logo: cam khoảng `#E8832A`, nâu đậm, xanh lá rêu. Cam logo hơi khác vàng hổ phách `#D9902A` của giao diện; muốn khớp hơn thì chỉnh `--amber` trong `theme.py`.

## Cấu hình thương hiệu (dùng cho thương hiệu khác hoặc tắt logo)

Logo không cố định trong code. Cấu hình ở `docs/thuong-hieu/brand.json` (mặc định là logo Sunny, ai dùng repo của Sunny không cần làm gì):

```
{
  "name": "Sunny Nhận Ra",
  "logo": "docs/thuong-hieu/logo-sunny-nhan-ra-nen-trong.png",
  "logo_source": "docs/thuong-hieu/logo-sunny-nhan-ra.png",
  "logo_enabled": true
}
```

- **Dùng thương hiệu khác:** đổi `name` và `logo` (đường dẫn tính từ gốc repo; nhận png, jpg, svg, webp). Có logo gốc nền trắng thì đặt vào `logo_source` rồi chạy `python -X utf8 scripts/process_logo.py` để tạo bản nhúng.
- **Không muốn logo:** đặt `"logo_enabled": false`.
- **Riêng một dự án:** tạo `testing/<dự-án>/brand.json` chỉ gồm các khóa muốn đổi (ví dụ `{"logo_enabled": false}`); chỉ trang của dự án đó đổi. Tài liệu dùng chung (`docs/`, `srs/*.md`, `testing/*.md`) luôn theo cấu hình chung của repo.
- File cấu hình hỏng hoặc thiếu file logo thì trang vẫn sinh bình thường, chỉ không có logo.
- Sửa xong chạy `python -X utf8 scripts/build_docs.py --all` để mọi trang cập nhật cùng lúc. Bảng màu và font vẫn là giao diện chung (`theme.py`).

## Đổi giao diện

Sửa `theme.py` (hoặc `_CSS_DOC` trong `docs_pages.py` cho riêng trang tài liệu) rồi chạy `python -X utf8 scripts/build_docs.py --all`. Mọi trang được sinh lại cùng lúc nên không bao giờ lệch nhau.
