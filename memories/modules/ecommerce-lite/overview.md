# Ecommerce Lite — tổng quan
Đọc khi: đầu tiên khi làm Ecommerce Lite (`.du-an-hien-tai` = ecommerce-lite). Ngày tạo: 2026-11-20.

## Hệ thống
- URL: https://staging-ecommerce-lite.vercel.app/
- Tài khoản test: `SHOPPER` (vai Customer, người dùng đưa 2026-11-20; mật khẩu trong `.env`, khóa `ECOMMERCE_LITE_`). Chưa có tài khoản quản trị (Admin) — không dùng tài khoản lộ trong mã giao diện khi người dùng chưa đưa.
- Là sân luyện test ("Sunny Commerce · Training environment"), SPA đổi trang bằng `#hash`, API `/api/...`. Hai cổng: cửa hàng (Customer: Shop/My orders/Profile) và quản trị (Dashboard/Products/Orders/Customers/API Lab/Challenges).
- Trang đăng nhập hiện sẵn email + mật khẩu mẫu Customer và nút "Use customer" (tự điền): dùng nút này thay vì gõ mật khẩu; ảnh phải che mật khẩu mẫu.

## Bối cảnh
_Chưa có. Chỉ ghi điều người dùng nói hoặc đã thấy trên hệ thống này; không suy từ dự án khác._

## Thư mục của dự án
| Loại | Đường dẫn |
|---|---|
| Bộ nhớ | `memories/modules/ecommerce-lite/` |
| SRS | `srs/ecommerce-lite/` (`dang-nhap.md` = `LOGIN`, `quen-mat-khau.md` = `FORGOT`) |
| Phân tích requirement | `testing/ecommerce-lite/` |
| Bằng chứng, báo cáo HTML | `evidence/ecommerce-lite/` |

## Việc cần làm tiếp
- Đăng nhập: đã khám phá, có SRS (`LOGIN`) + bảng phân tích requirement (0 câu hỏi BA) 2026-11-20; đã có test case (19 TC, chưa chạy); xem `feature-dang-nhap.md`.
- Quên mật khẩu: có SRS (`FORGOT`) + bảng phân tích + câu hỏi BA (chưa gửi) + test case 14 TC (phần đã rõ, chưa chạy); xem `feature-quen-mat-khau.md`.
- Chốt với người dùng: số lần sai tối đa, thời gian chặn (chưa có), tài khoản Admin.
