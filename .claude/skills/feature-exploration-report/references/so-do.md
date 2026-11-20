# Sơ đồ và giao diện chuẩn (dùng chung cho mọi dự án)

Người dùng đã chốt **một** giao diện cho báo cáo khám phá: font, màu, bố cục và ba kiểu sơ đồ. Cách giữ cho giống nhau trên mọi máy và mọi dự án:

| Phần | Nằm ở đâu | Ai lo |
|---|---|---|
| Font thương hiệu Be Vietnam Pro (SIL OFL) | `docs/thuong-hieu/fonts/` (tải bằng `scripts/tai-font.py`); `scripts/giao_dien.py` cắt theo chữ thật của báo cáo | `build-embed.py` nhúng vào file |
| Bảng độ rộng chữ để vẽ hộp sơ đồ | `assets/fonts/do-rong-chu.json` (Be Vietnam Pro), tạo lại bằng `scripts/tao-bang-do-rong.py` khi đổi font | `ve-so-do.py` đo chữ |
| Logo | `docs/thuong-hieu/brand.json` | `build-embed.py` chèn vào hero |
| Màu, cỡ chữ, bố cục (CSS) | `assets/giao-dien-chuan.css` | `build-embed.py` chèn vào `<style id="giao-dien-chuan">` |
| Ba kiểu sơ đồ | `scripts/ve-so-do.py` + nội dung trong file JSON | `build-embed.py` vẽ khi gặp `data-so-do` |

**Không được:** chép CSS vào file nguồn, đổi màu/font trong từng báo cáo, vẽ SVG sơ đồ bằng tay. Vì sao: trước đây sơ đồ vẽ tay và font `Segoe UI` (chỉ có trên Windows) làm báo cáo tạo trên Mac khác hẳn bản đã chốt (người dùng báo 2026-11-18). Cần kiểu sơ đồ mới thì hỏi người dùng trước, rồi thêm vào `ve-so-do.py` chứ không vẽ tay.

## Cách dùng trong báo cáo
1. Chép `assets/so-do-mau/*.json` sang `evidence/<slug>/features/<feature>/_src/so-do/`, sửa nội dung theo **điều đã thấy**.
2. Trong file nguồn: `<div class="diag" data-so-do="so-do/tong-quan.json"></div>` (đường dẫn tính từ thư mục file nguồn). Khuôn đã có sẵn ba dòng này.
3. Xem thử riêng sơ đồ: `python -X utf8 scripts/ve-so-do.py <a.json> <b.json> -o xem-thu.html`, rồi mở qua `http://` (xem `evidence-and-build.md`).
4. Build như thường. Build in **Cảnh báo** nếu còn sơ đồ vẽ tay, có khối `<style>` riêng đổi font/màu, hoặc dòng ghi chú dài quá khung.

Mọi khóa không nằm trong bảng dưới (vd `_huong-dan`) được bỏ qua. Chữ `**đậm**` dùng được trong nhãn và ghi chú.

## 1. `tong-quan` — ai nói chuyện với ai
Vai trò bên trái, hệ thống ở giữa, hệ thống bên thứ ba bên phải, vòng số ở đầu mũi tên, hộp ghi chú nhánh phụ ở dưới.

| Khóa | Ý nghĩa |
|---|---|
| `he-thong` | `ten`, `phu`, `tieu-de-muc` + `muc` (danh sách bước/phần), `tieu-de-trang-thai` + `trang-thai` (các dòng) |
| `vai-tro[]` | `id`, `mau` (`p1`…`p5`), `ten` (mã tài khoản), `vai` (chuỗi hoặc danh sách dòng), `mo-ta` (danh sách dòng) |
| `ben-ngoai[]` | `id`, `ten`, `mo-ta` |
| `buoc[]` | `so`, `nhan` và **một** trong hai: |
| | `tu` = id vai trò: mũi tên vai trò → hệ thống. `"chieu": "ve"` = hệ thống → vai trò (vòng số đặt phía hệ thống, màu xám; đổi bằng `mau`). `"tra-ve": true` = nét đứt (kết quả trả về) |
| | `den` = id bên thứ ba: hệ thống gọi ra. `tra-ve` = nhãn của mũi tên nét đứt trả về; `so-tra-ve` = số trên mũi tên trả về nếu nó là một bước riêng; hoặc `ghi-chu-nho` (dòng nhỏ dưới mũi tên) |
| `ghi-chu` | `dong` (danh sách đoạn; dòng dài quá khung tự xuống dòng); `so` + `mau` nếu là một bước có số, bỏ `so` nếu chỉ là chú thích |

Mũi tên của mỗi vai trò xếp theo thứ tự trong `buoc`; `so` là số hiển thị (không cần liên tục theo vị trí).

## 2. `tuan-tu` — luồng chính theo thời gian
| Khóa | Ý nghĩa |
|---|---|
| `lan[]` | các làn từ trái sang phải: `id`, `mau` (`p1`…`p5`, `sys` cho hệ thống chính, `ext` cho bên thứ ba), `ten`, `phu` (dòng nhỏ, không bắt buộc) |
| `buoc[]` | thông điệp: `tu`, `den`, `nhan` (`\n` để xuống 2 dòng), `tra-ve: true` = nét đứt. Số **tự đánh** theo thứ tự (ghi `so` nếu muốn khác) |
| | hộp ghi chú: `ghi-chu`, `tu`, `den` (hộp trải từ làn `tu` tới làn `den`), không đánh số |

Khoảng cách giữa các làn tự nới theo nhãn dài nhất.

## 3. `trang-thai` — vòng đời trạng thái
| Khóa | Ý nghĩa |
|---|---|
| `trang-thai[]` | `id`, `ten` (đúng nhãn trên màn hình), `kieu` (`xam` nháp, `xanh` đang xử lý, `ok` thành công, `loi` bị từ chối/lỗi, `cho` chờ/trả lại, `tim`, `ngoai` = ngoài phạm vi feature, viền nét đứt), `cot`, `hang` (vị trí lưới từ 0; được dùng số lẻ như `0.6` để ô nằm giữa hai hàng), `ghi-chu` (chữ nhỏ bên phải ô), `dong` (các dòng phụ trong ô, thường cho ô `ngoai`) |
| `chuyen[]` | `tu`, `den`, `nhan` (ngắn), `so` (bỏ = không vẽ vòng số), `net-dut: true` (mũi tên xám nét đứt, vd sang phần ngoài phạm vi). Sang cột phải = đường thẳng; cùng cột = thẳng đứng; về cột trái = đường cong phía dưới. Nhiều mũi tên toả ra từ một ô hoặc cùng đổ vào một ô: script tự giãn đầu mũi tên và đặt nhãn phía ngoài |
| `chu-thich` | các dòng chữ nhỏ dưới sơ đồ (vd điều kiện kèm số ảnh) |

Điều kiện chuyển trạng thái viết ở danh sách `ol.steplist` **bên dưới** sơ đồ, không nhồi lên mũi tên (từng bị chồng chữ).

## Bảng màu (khớp `giao-dien-chuan.css`)
Vai trò: `p1` xanh lá `#177a5c`, `p2` hổ phách `#b7791f`, `p3` xanh dương `#2b6cb0`, `p4` hồng `#b83280`, `p5` xanh ngọc `#2c7a7b`; `ext` tím `#6b46c1` (bên thứ ba), `sys` xám `#4a5568` (hệ thống chính); màu thương hiệu `#0b5d4e`. Một tài khoản giữ **cùng một màu** ở bảng vai trò, thẻ tag, cả ba sơ đồ.

## Sửa font (hiếm khi cần)
Font đã cắt sẵn, máy mới không cần tải gì. Muốn cắt lại (thêm ký tự): cài `fonttools brotli`, lấy `OpenSans[wdth,wght].ttf` từ kho Google Fonts, chạy `fontTools.varLib.instancer` (wdth=100, wght=400:700) rồi `fontTools.subset --flavor=woff2` với dải Latin + tiếng Việt; sau đó tạo lại `assets/fonts/do-rong-chu.json` (độ rộng ký tự cho `ve-so-do.py`). Font làm báo cáo nặng thêm ~40 KB; build tự giảm chất lượng ảnh thu nhỏ khi vượt 512 KiB.
