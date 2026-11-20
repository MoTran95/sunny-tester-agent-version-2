# Quy tắc viết bộ nhớ (memory = chỉ cho AI đọc)
Đọc khi: trước khi ghi/sửa `memories/`. Kiểm sau khi sửa: `python -X utf8 scripts/kiem-tra-bo-nho.py`.

## Hai lớp tài liệu
- **Cho người đọc** (`srs/`, `testing/`, `evidence/`, `docs/`, báo cáo HTML): viết đầy đủ, đọc là hiểu, giữ nguyên kết quả output.
- **Memory (`memories/`)**: chỉ AI đọc → viết **ngắn, dạng bảng/gạch đầu dòng**, tiếng Việt, không văn xuôi giải thích, không lặp nội dung đã có trong code/SRS/SKILL/test case (chỉ trỏ đường dẫn).

## Khuôn
- Đầu file: `# Tiêu đề` + 1 dòng `Đọc khi: …`. **Không** ghi "Cập nhật:", không dòng "Liên quan:", không nhật ký thay đổi; ngày tuyệt đối chỉ khi chính ngày đó là thông tin (quyết định, mốc).
- Một file = một chủ đề, mục tiêu <150 dòng và vài KB. Quá dài/hai chủ đề → tách + sửa bản đồ.
- Ưu tiên bảng (Khi | Chứa; Quyết định | Lý do | Đã loại). "Why/How to apply" chỉ khi không hiển nhiên.
- Link bằng đường dẫn `memories/…` hoặc `đường/dẫn.md` trong backtick; không cần câu giới thiệu.

## Ghi gì
- Ghi: lý do thiết kế, ràng buộc, quyết định + phương án đã loại, quy ước, bẫy đã gặp, sở thích người dùng, dữ liệu test (id hồ sơ…), điều chưa thử.
- Không ghi: nội dung code, lịch sử commit, chi tiết một phiên, số liệu suy ra nhanh từ file.
- Sai/lỗi thời → sửa hoặc xóa ngay. Một sự thật một nơi; gọn bộ nhớ = chuyển chỗ, không xóa quy tắc người dùng dặn.

## Đặt tên và thư mục
kebab-case tiếng Anh/Việt không dấu, tên nói lên nội dung: `conventions/ user/ project/ decisions/ pitfalls/ modules/<slug>/`. Nội dung tiếng Việt.

## Bản đồ
`memories/MEMORY.md` = bảng `File | Khi | Chứa`, mỗi file đúng một dòng, 2 file ★ luôn đọc. Thêm/đổi tên/xóa file → sửa bản đồ cùng lượt.
