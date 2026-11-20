# Bằng chứng (ảnh), khoanh nút, build, soát

## Chụp ảnh khi khám phá

- Dùng trình duyệt tích hợp của app. Trang tải chậm: **chờ xong rồi mới chụp** (thường 3–5 giây).
- Phần tử ngoài màn hình không hiện trong cây trang: cuộn xuống rồi chụp/đọc. Bấm link trong danh sách có thể chỉ cuộn trang → dùng URL trực tiếp của bước nếu biết.
- Với mỗi nút quan trọng: chụp **trước khi bấm** (thấy nút) và **sau khi bấm** (thấy kết quả). Báo cáo đầu tiên thiếu ảnh nút hành động chính vì chỉ chụp sau — đừng lặp lại.
- Chụp cả trường hợp lỗi/chặn (thông báo nguyên văn). Chụp cả “không có nút” khi đổi tài khoản (so sánh vai trò).
- Ảnh trình duyệt tự lưu ở thư mục kết quả công cụ của phiên → **copy sang** `evidence/<feature>/screenshots/` để giữ lâu dài.
- Đặt tên: `NN-<tài-khoản>-<mã-bản-ghi>-<mô-tả-ngắn>.jpg`, `NN` hai chữ số tăng dần (số này = “Ảnh NN” trong báo cáo; script dùng tiền tố này).
- Giữ danh sách “ảnh còn thiếu” để ghi vào mục 6.

## Khoanh nút trên ảnh

Trong `<figure class="shot" style="--W:<rộng gốc>;--H:<cao gốc>">` (px của ảnh gốc, đọc bằng Pillow hoặc xem thuộc tính ảnh):

```html
<i class="mk" data-n="1" style="--x:446;--y:109;--w:126;--h:39"></i>      <!-- đỏ: có -->
<i class="mk neg" data-n="2" style="--x:19;--y:158;--w:235;--h:35"></i>   <!-- cam đứt: không có -->
```

- Toạ độ `x,y` = góc trên trái, `w,h` = kích thước, **đơn vị px ảnh gốc**. Đo bằng cách mở ảnh và đọc vị trí phần tử; đừng đoán.
- Đặt khung **ôm sát đúng ô được nói tới**, không phủ sang ô bên cạnh (lỗi từng gặp: khung ghi nhãn của ô này nằm đè lên ô bên cạnh). Mỗi số trong legend phải khớp một khung.
- Script tự: nới khung vài px (viền vẽ bằng `outline`, không che chữ), **chọn vị trí số thứ tự** ít đè chữ nhất (đo độ “rối” của ảnh gốc), tránh đè khung/số khác, thu nhỏ độ nới khi hai khung chạm nhau. Không cần (và không nên) tự đặt vị trí số.
- Nhiều khung cùng một số được (vd thanh trên + menu); số đánh theo thứ tự đọc.

## Build

```bash
python -X utf8 .claude/skills/feature-exploration-report/scripts/build-embed.py \
  --src evidence/<feature>/_src/<ten>.src.html \
  --out evidence/<feature>/<ten>.html \
  --shots evidence/<feature>/screenshots
```

Cần Pillow (`pip install pillow`). Script:
- Thay `<style id="giao-dien-chuan">` bằng `assets/giao-dien-chuan.css` + font thương hiệu nhúng (Be Vietnam Pro) → chữ giống nhau trên mọi máy, cùng bảng màu và font với mọi trang HTML khác của repo (`docs/thuong-hieu/README.md`). Chèn logo góc trái đầu báo cáo theo `docs/thuong-hieu/brand.json` (thu nhỏ ~6 KB; `logo_enabled: false` thì không có). Trước đây dùng `Segoe UI` rồi Open Sans (2026-11-18); đổi sang font thương hiệu 2026-11-19.
- Vẽ mọi `<div class="diag" data-so-do="…json">` bằng `ve-so-do.py`. In **Cảnh báo** khi còn SVG vẽ tay hoặc có `<style>` riêng đổi font/màu.
- Nhúng mỗi ảnh **một lần** dưới dạng WebP thu nhỏ (mặc định 360px, q45) trong CSS (`.fNN`) → hiện được cả khi xem trước tĩnh. Nếu thư mục ảnh nằm cạnh file (mở bằng trình duyệt thường) thì JS tự thay bằng ảnh gốc nét.
- Viết lại JS: phóng to ảnh khi bấm, liên kết “ảnh NN” mở ảnh, **thanh tab cuộn tới mục** (liên kết `#anchor` thuần không chạy trong khung xem trước dạng `data:`) + tô sáng tab đang xem.
- Xoá chú thích HTML, bỏ thụt đầu dòng. In % so với giới hạn **512 KiB**.
- Vượt 512 KiB thì **tự build lại** với `--thumb-q` giảm 4 mỗi lần (45 → 41 → 37 …, thấp nhất 30). Ghi `--thumb-q` cụ thể thì không tự giảm. `--thumb-w` để giảm thêm; `--review <thư_mục>` để xuất tranh ghép soát khung/số.

### Giới hạn 512 KiB — vì sao
Khung xem trước của app hiển thị file HTML như ảnh chụp tĩnh (`data:`): ảnh đường dẫn tương đối **không tải được**, và file > 512 KiB bị từ chối (đã đo: ~500 KB mở được, ~540 KB không). Font nhúng chiếm ~40 KB của giới hạn này. Nhiều ảnh/chữ quá thì giảm `--thumb-w`, hoặc chia báo cáo theo feature.

## Soát trước khi giao (bắt buộc)

1. `--review <thư_mục>` → mở từng `sheet-XX.png`: khung có đúng ô được nói tới? số có đè chữ/đè số khác? Sửa toạ độ ở nguồn rồi build lại.
2. Mở file thật trong khung xem trước (`file:///…`). Kiểm tra: ảnh hiện hết; số/khung không che chữ; thanh tab bấm cuộn đúng (8 tab); sơ đồ SVG không chồng chữ; chữ thường và tiêu đề đều là Be Vietnam Pro (dấu tiếng Việt hiện đúng), logo ở góc trái hero; kiểm cả khi tắt mạng. Build không còn dòng **Cảnh báo**.
3. Đối chiếu nội dung với nhật ký MD: mọi nguyên văn thông báo, con số, mã bản ghi khớp. Không có điều nào không có trong nhật ký/ảnh.
4. Grep các từ cấm trong bảng thuật ngữ (`đường đi`, `dây chuyền`, `tick`, `giả lập`, `khối`, `huy hiệu`, `giải phẫu`…).
5. Kiểm tra dung lượng ≤ 512 KiB.

Mẹo xem thử bằng HTTP (nếu cần ảnh gốc nét): `python -m http.server` trong thư mục báo cáo rồi mở `http://127.0.0.1:<cổng>/…`; nhớ tắt server sau khi xong.

## Bẫy đã gặp

- Khung xem trước chụp màn hình có thể timeout khi pane ẩn hoặc trang nặng → chụp lại. Trên Windows, chụp không cần pane: `msedge --headless=new --user-data-dir=<thư_mục_tạm> --window-size=1100,2000 --screenshot=<file.png> http://127.0.0.1:<cổng>/<trang>` (chạy qua `Start-Process -Wait`).
- `scroll-behavior:smooth` làm đo vị trí ngay sau khi cuộn sai; chờ ~1.5s.
- Sửa chữ hàng loạt bằng regex: không thay trong tên file ảnh (vd `tick` trong `…-tick-danh-muc.jpg`) — dùng lookbehind loại ký tự `-`/chữ.
- Hai khung nhỏ sát nhau trong bảng đặc chữ → gộp thành một khung bao cả cột để có chỗ trống đặt số.
- Trong script/heredoc có `'''` hoặc nhiều dấu nháy, ghi file bằng công cụ ghi file thay vì heredoc shell.
- Không ghi mật khẩu/token vào báo cáo; số điện thoại/CCCD che như hệ thống hiển thị.
