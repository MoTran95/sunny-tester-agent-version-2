# Checklist khám phá để viết SRS

Mục tiêu: **khám phá đủ để SRS không phải "bỏ ngõ"**. Chỉ bỏ ca khi có lý do thật (xem cuối file). Mỗi ca làm xong ghi ngay vào nhật ký gốc (hàng đánh số), chụp ảnh nếu có gì để nhìn.

## 1. Ba loại bằng chứng (ghi rõ loại trong SRS)
| Loại | Lấy bằng cách | Lưu ý |
|---|---|---|
| **Ảnh** | `computer screenshot` rồi copy từ thư mục kết quả công cụ sang `evidence/<hệ thống>/features/<feature>/screenshots/` | Đặt tên `NN-<tài-khoản>-<mô-tả-ngắn>.jpg` (NN hai chữ số tăng dần). Chụp **trước và sau** khi bấm nút quan trọng |
| **Quan sát bằng công cụ** | Mã trạng thái lệnh gọi mạng (`read_network_requests`), thuộc tính ô nhập/form (`javascript_tool` đọc DOM), **tên** khóa trong `localStorage` | Không có ảnh → SRS ghi "không có ảnh" và chỉ cách mở lại bằng F12 |
| **Tệp giao diện** | `fetch` tệp JavaScript công khai của trang rồi tìm chuỗi thông báo (ví dụ `auth.locked`, `invalidCredentials`) | Cho **toàn bộ câu thông báo hai ngôn ngữ** mà không phải kích hoạt lỗi. Nhưng là suy ra từ mã, **chưa phải hành vi thấy trên màn hình** — ghi rõ như vậy; tên tệp có hash đổi theo bản |
| Báo cáo cũ | Tham chiếu lượt khám phá trước | Ghi tệp nguồn |

## 2. Kỹ thuật đã dùng được
- **Trước mỗi lần bấm có rủi ro**: ghi số lệnh gọi mạng hiện tại; **sau** bấm đọc lại. Nếu số không tăng thì lần bấm **không gửi đi** (từng gặp: khung lỗi biến mất làm nút lệch chỗ, click trượt). Chờ ≥3–4 giây giữa các lần.
- `read_network_requests` với `urlPattern` (ví dụ `/api/auth`) và `limit` nhỏ để chỉ xem lệnh gọi mới. Thân phản hồi **GET** đọc được bằng `requestId`; thân phản hồi lỗi của POST thường không đọc được.
- **Đọc `GET /api/<…>` trực tiếp bằng `fetch` trong `javascript_tool`** (ví dụ `await fetch('/api/applications/<id>').then(r => r.json())`) để lấy **đủ mã lý do và chỉ số** mà màn hình không hiện hoặc hiện rút gọn. Nhanh hơn đọc màn hình và lộ cả lỗi hiển thị (từng gặp: API trả lý do `ageAtMaturity` nhưng màn hình không hiện lý do nào). Ba lưu ý: (a) chỉ **GET** (chỉ đọc) — không dùng `fetch` để gửi POST/PUT/DELETE; (b) chỉ in các trường cần ghi nhật ký, không in cookie/token; (c) bằng chứng ghi là "quan sát bằng công cụ, không có ảnh", kèm đường dẫn API và tên trường, để người khác kiểm lại bằng F12 → Network.
- **Không đọc thân yêu cầu POST đăng nhập** (chứa mật khẩu). Không in/ghi giá trị cookie, token.
- Điền ô bằng `form_input` theo `ref` (ổn định hơn gõ từng phím). Phần tử ngoài màn hình: cuộn rồi mới đọc, hoặc `find`.
- Trang tải chậm ("Đang tải…" 3–5 giây): luôn chờ rồi mới đọc/chụp.
- **Sau khi bấm `Lưu`, chờ cho tới khi giá trị phụ thuộc đã cập nhật (đo thời gian lưu ở lần đầu) rồi mới đọc kết quả.** Phần phụ thuộc kết quả lưu (ví dụ ô tổng kết ở đầu trang) cập nhật chậm; đọc sớm sẽ thấy giá trị cũ và ghi nhầm vào nhật ký. Không có số giây mặc định: đo thời gian lưu thật trên hệ thống đang test lần đầu rồi ghi vào bộ nhớ module của dự án đó.
- Hai tab: `preview_start` với `url` mở tab thứ hai dùng chung phiên; nhớ `tabs_close` khi xong.
- Nút **Back**: `navigate` với `url: "back"`.
- Khung xem trước bị ẩn → dùng `mcp__ccd_view__show_pane` (`preview`) để bật lại; người dùng không thấy gì nếu ẩn.
- Giữ khung nhìn cố định (ví dụ 606×845) để ảnh cùng kích thước; nhớ `resize_window preset desktop` khi xong.

## 3. Ca phải phủ cho từng loại màn hình
Mỗi nhóm dưới đây là một dòng trong **mục 0 "Bảng phủ"** của nhật ký (khuôn `assets/exploration-log-template.md`); khám phá xong phải không còn dòng trống.

**Mọi feature:** luồng chính thành công; từng nhánh lỗi; từng vai trò/tài khoản (ai thấy gì, ai không có nút); đổi ngôn ngữ (nhãn, số, ngày, thông báo, mã lỗi chưa dịch); tải lại trang; nút Back; mở link sâu khi chưa đăng nhập / khi không đủ quyền; địa chỉ không tồn tại; hai tab; phản hồi mạng (mã trạng thái).

**Form nhập liệu:** để trống từng ô và tất cả; một ô trống, ô khác có giá trị; sai định dạng; thiếu/thừa độ dài; rất dài (tìm giới hạn tối đa); khoảng trắng đầu/cuối; chữ hoa/thường; ký tự đặc biệt; biên trên/dưới của số; nhấn Enter; bấm hai lần; mã lỗi thô chưa dịch; ô giữ lại giá trị sau lỗi không; thuộc tính HTML (`required`, `novalidate`, `maxlength`, `autocomplete`).

**Đăng nhập/phiên:** đăng nhập đúng; sai mật khẩu; mã không tồn tại (có cùng thông báo không); mã chữ thường; quay lại link đã mở; đăng xuất; Back sau đăng xuất; đăng xuất ở tab khác; địa chỉ không tồn tại khi đã/chưa đăng nhập; giới hạn đăng nhập sai (**chỉ theo quy tắc an toàn**); hết hạn phiên.

**Danh sách/bảng:** tab/bộ lọc; sắp xếp; rỗng; nhiều dòng; cột nào hiện theo vai trò.

**Luồng nhiều bước/trạng thái:** điều kiện mở từng bước; bước bị khóa và thông báo; trạng thái sau khi gửi; hoàn tác/trả lại/từ chối; ai làm được bước nào; lịch sử/nhật ký ghi gì.

## 4. Khi nào được ghi vào mục "Chưa khám phá"
Chỉ khi có **lý do thật**, ghi kèm lý do:
- cần **người dùng gõ mật khẩu** mà họ chưa làm / chưa đồng ý;
- cần **chờ thời gian** dài (hết hạn phiên) hoặc **trình duyệt/máy thứ hai**;
- thiếu **tài khoản/dữ liệu** (ví dụ chưa có mật khẩu của một vai trò);
- **có thể khóa hệ thống / đổi dữ liệu của người khác** → làm tối đa 3 lần rồi hỏi (xem `safety-and-collaboration.md`);
- **bị công cụ chặn** (ví dụ bấm một nút gửi yêu cầu bằng JS bị chặn vì "Destructive or Unwanted Actions") → **không đi đường vòng**; ghi ngay vào "Chưa khám phá" kèm lý do "bị công cụ chặn" và thao tác đã thử (xem `safety-and-collaboration.md` mục 6).

"Ngại rủi ro nhỏ", "hơi lâu", "giá trị thấp" **không phải** lý do — làm luôn, hoặc hỏi người dùng. Mục này không phải chỗ cất việc mình chưa làm.
