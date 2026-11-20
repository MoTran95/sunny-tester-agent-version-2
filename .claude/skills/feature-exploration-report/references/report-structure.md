# Cấu trúc báo cáo và văn phong

Người đọc: **tester mới, chưa biết lĩnh vực**. Báo cáo phải giúp họ (1) hiểu hệ thống làm gì, (2) hiểu từng vai trò làm gì và làm thế nào, (3) thấy luồng đi từ đầu đến cuối, (4) biết chỗ nào chưa rõ để hỏi.

## 7 mục (đúng thứ tự, khớp thanh tab)

| Mục | Nội dung | Ghi chú |
|---|---|---|
| Cách đọc | Nguyên tắc “chỉ điều đã thấy”, ý nghĩa khung đỏ/cam trên ảnh | Có sẵn trong mẫu |
| 1 · Hệ thống là gì | 1–2 câu mô tả; khung “Ví dụ so sánh”; ảnh đăng nhập có khoanh nút; **bảng thuật ngữ**; **phân tích màn hình chính** (header/banner/stepper…) | Thuật ngữ lấy theo nhãn thật trên màn hình |
| 2 · Sơ đồ tổng quan | SVG: vai trò – hệ thống – hệ thống bên thứ ba, mũi tên **đánh số 1…N**, danh sách “Giải thích từng số” | Số trên hình = số trong danh sách |
| 3 · Vai trò | Bảng “ai làm được gì”; mỗi tài khoản một khối: tóm tắt 1 câu, ví dụ so sánh, làm được/không, rồi **từng thao tác một khối step có ảnh khoanh nút** | Chỉ ghi quyền đã thấy; ô chưa thử ghi ❓ |
| 4 · Luồng end-to-end | 4.1 sơ đồ tuần tự luồng chính (đánh số); 4.2 sơ đồ trạng thái; 4.3 các luồng A, B, C… (từng bước: ai – làm gì – kết quả – số ảnh); luồng cuối là bảng **ràng buộc chặn thao tác** | Chỉ luồng đã chạy thật |
| 5 · Điểm mơ hồ | Thẻ M-01…: Đã thấy / Vì sao chưa rõ / Cần làm rõ + ảnh khoanh; gom nhóm (bất thường, tích hợp, quy tắc nghiệp vụ, quyền); gắn mức “Nên hỏi trước / Hỏi sau” (chỉ là gợi ý thứ tự hỏi) | Xem quy tắc bên dưới |
| 6 · Chưa thử | Thẻ C-1…: nút/nhánh chưa bấm, ảnh còn thiếu, việc cần người dùng đồng ý | Nêu lý do chưa thử |
| 7 · Cần bạn trả lời | Danh sách việc người dùng phải quyết (đồng ý tải file, tích hợp thật hay mô phỏng, tài liệu…) + câu hỏi còn lại cho team | |

## Mỗi thao tác (khối `.step`) gồm

Tên thao tác → mục đích 1 câu → legend đánh số (tên nút **đúng như trên màn hình**) → “Kết quả đã thấy” (thông báo nguyên văn, trạng thái đổi) → nguồn ảnh. Ảnh kèm khung/số trùng legend. Chỗ **không có** nút/vùng thì dùng khung cam gạch đứt (`mk neg`, `li.neg`).

## Thẻ điểm mơ hồ

- **Đã thấy**: hiện tượng + trích nguyên văn + số ảnh. Nếu không có ảnh cho đúng khoảnh khắc: nói thẳng.
- **Vì sao chưa rõ**: thiếu tài liệu nào / chưa thử nhánh nào / hai giá trị bằng nhau nên không phân biệt được.
- **Cần làm rõ**: câu hỏi cụ thể, trả lời được bằng 1–2 câu.
- Tuyệt đối không viết “đây là lỗi”, “chắc là do…”. Cho phép viết “mâu thuẫn giữa A (bạn nói) và B (đã thấy)”.

## Sơ đồ (không vẽ tay — viết JSON, `scripts/ve-so-do.py` vẽ theo mẫu đã chốt; cách viết: `so-do.md`)
Các quy tắc dưới đây đã nằm trong script; giữ ở đây để hiểu vì sao sơ đồ trông như vậy.

- **Sơ đồ tổng quan**: vai trò bên trái (mỗi vai trò một màu), hệ thống ở giữa (liệt kê các bước/trạng thái), hệ thống bên thứ ba bên phải; mũi tên liền = yêu cầu, nét đứt = kết quả trả về; vòng tròn số ở đầu mũi tên; ghi chú nhánh phụ (vd “trả lại → quay về bước 7”) ở hộp riêng phía dưới.
- **Sơ đồ tuần tự**: các “làn” = tài khoản + hệ thống + bên thứ ba; mỗi thông điệp một dòng, cách nhau ~44px; nhãn ngắn đặt phía trên mũi tên; nhãn 2 dòng thì chừa thêm khoảng trống; hộp ghi chú (vd nút bị vô hiệu hóa) cách thông điệp kế ≥ 68px để không đè.
- **Sơ đồ trạng thái**: ô trạng thái + mũi tên đánh số; **mô tả điều kiện chuyển ở danh sách bên dưới**, không nhồi chữ dài lên mũi tên (từng bị chồng chữ).
- Kiểm tra bằng mắt sau khi build: chữ không đè mũi tên/lifeline, số không che nhau. Nếu đè: sửa nội dung JSON (nhãn ngắn hơn, xuống dòng bằng `
`), hoặc sửa `ve-so-do.py` cho mọi báo cáo — không sửa tay SVG.

## Thuật ngữ — dùng đúng, dễ hiểu

| Dùng | Không dùng |
|---|---|
| luồng (flow), luồng chính (happy path), luồng end-to-end (E2E) | “đường đi”, “đường chính” |
| quy trình xử lý (workflow) | “dây chuyền” |
| nút bị vô hiệu hóa (disabled) | “nút bị khóa” |
| hồ sơ/bản ghi bị khóa (không còn sửa được) | dùng lẫn với disabled |
| banner / thông báo trạng thái | “dòng vàng/xanh” |
| nhãn trạng thái (badge) | “huy hiệu” |
| trường nhập (field), ô đánh dấu (checkbox), “đánh dấu chọn” | “ô”, “tick” |
| phần / vùng (section/panel) | “khối” |
| mô phỏng (mock) / hệ thống thật | “giả lập” (mơ hồ) |
| thanh điều hướng các bước (stepper) | “thanh bước” |
| phân tích màn hình / thành phần giao diện | “giải phẫu” |
| ví dụ so sánh | “cách hình dung” |
| ghi nhận trong báo cáo (không có ảnh) | “ghi chép” |
| mã lỗi gốc (chưa chuyển thành thông báo tiếng Việt) | “mã lỗi thô” |

Quy tắc chung: gặp từ lóng/ẩn dụ → thay bằng thuật ngữ IT hoặc từ đời thường chính xác; lần đầu dùng từ chuyên ngành của lĩnh vực (nghiệp vụ) thì giải nghĩa **theo nhãn và số liệu thật trên màn hình**, công thức chưa biết thì ghi ❓. Tên nút/nhãn giữ **nguyên văn** như giao diện, đặt trong ngoặc kép hoặc in đậm.

## Màu vai trò

`p1` xanh lá, `p2` hổ phách, `p3` xanh dương, `p4` hồng, `p5` xanh ngọc, `ext` tím (hệ thống bên thứ ba), `sys` xám (hệ thống chính). Giữ nhất quán giữa bảng, thẻ tag, sơ đồ. Mã màu nằm duy nhất ở `assets/giao-dien-chuan.css` và `scripts/ve-so-do.py`; không tự đặt màu khác.
