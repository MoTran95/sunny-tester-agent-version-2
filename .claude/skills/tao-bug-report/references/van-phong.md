# Văn phong bug report (người dùng đã chỉnh, 2026-11-18)

Cũng đọc `memories/user/document-preferences.md` mục Bug report khi cần nhắc lại.

- **Tiêu đề** `[Module] Mô tả lỗi`: module là tên màn hình/chức năng người dùng thấy; mô tả **chỉ nói cái gì đang sai**, ngắn gọn (ví dụ `[Đơn hàng] Nút Thanh toán vẫn bật khi giỏ hàng trống`). Không "lỗi ở màn hình X"; **không lý do, ngữ cảnh hay hậu quả** ("dù BA đã chốt bỏ", "theo BA…"; hậu quả để ở mục Ảnh hưởng nghiệp vụ).
- **Tên thành phần giao diện** đúng tên người dùng quen: "thanh điều hướng" (không "thanh trên"), "khung lỗi", "ô Mật khẩu"…
- **Môi trường:** dòng Trình duyệt chỉ ghi tên + số bản + hệ điều hành (ví dụ `Chrome 157.0.8103.78 trên Windows 11`), không công cụ chạy hay chế độ (Playwright, ẩn cửa sổ), không nhãn Giả định ở dòng này.
- **Kết quả mong đợi:** chép câu chữ của requirement hoặc test case; **không** chèn ngoặc nguồn "(theo TC-014, bước 4; theo BA…)". Nguồn nằm ở mục Test case liên quan.
- **Mức độ nghiêm trọng/ưu tiên:** tiếng Việt (xem `thang-muc-do.md`).
- **Câu hỏi cho Dev:** viết đủ nghĩa để đọc một mình cũng hiểu: nêu điều đã thấy, điều chưa biết, vì sao hỏi, mình sẽ làm gì tùy câu trả lời; không viết cụt kiểu "A có chung nguyên nhân với B không?". Đánh số khi nhiều ý.
- **Câu hỏi cho BA:** khuôn ở `memories/conventions/ba-question-wording.md`.

## Danh sách tự kiểm văn phong
- [ ] Tiêu đề không có "dù…", "vì…", "theo BA…", hậu quả; đúng tên thành phần.
- [ ] Dòng Trình duyệt chỉ có tên + số bản (+ hệ điều hành).
- [ ] Kết quả mong đợi không có ngoặc nguồn.
- [ ] Mức độ nghiêm trọng/ưu tiên bằng tiếng Việt, không Severity/Priority/Trivial.
- [ ] Câu hỏi cho Dev đọc một mình cũng hiểu.
- [ ] Ảnh lỗi có bản tô đỏ (đã `Read` kiểm khung đúng chỗ), mỗi dòng ghi lỗi ở bước nào.
