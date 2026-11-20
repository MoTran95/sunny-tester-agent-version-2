# Chọn kỹ thuật thiết kế test case

Chọn **theo dấu hiệu trong requirement**. Mỗi dòng checklist ghi đúng **một** kỹ thuật trong: `EP`, `BVA`, `Bảng quyết định`, `Chuyển trạng thái`, `Use case`, `Đoán lỗi`. Ví dụ dưới đây là ví dụ trung lập, không phải của feature nào.

## Bảng dấu hiệu

| Dấu hiệu trong requirement | Kỹ thuật | Ra bao nhiêu dòng |
|---|---|---|
| Khoảng giá trị, độ dài, ngưỡng, số lần ("từ 1 đến 10", "tối đa 5 lần") | **EP** rồi **BVA ba giá trị** | EP: mỗi lớp (hợp lệ, mỗi kiểu không hợp lệ) một dòng. BVA: dưới biên, đúng biên, trên biên |
| Nhiều điều kiện cùng quyết định một kết quả ("nếu A và B thì C, còn A mà không B thì D") | **Bảng quyết định** | Mỗi tổ hợp có kết quả khác nhau một dòng; tổ hợp cùng kết quả thì gộp thành lớp |
| Một thứ đi qua nhiều trạng thái ("nháp → đã gửi → đã duyệt", "bình thường → bị chặn → hết chặn") | **Chuyển trạng thái** | Mỗi chuyển hợp lệ một dòng; chuyển không được phép (nếu requirement nói) một dòng |
| Hành trình nhiều bước của người dùng, có luồng chính và luồng thay thế | **Use case** | Luồng chính một dòng; mỗi luồng thay thế quan trọng một dòng |
| Chỗ requirement nói "không được", "không có", hoặc lỗi hay gặp liên quan trực tiếp tới một AC | **Đoán lỗi** | Ít, chỉ khi có lý do ghi được bằng một câu từ requirement |

## Cách làm từng kỹ thuật
- **EP (lớp tương đương):** chia giá trị nhập thành lớp mà hệ thống xử lý giống nhau; mỗi lớp thử **một** giá trị đại diện. Lớp không hợp lệ: mỗi dòng **một** kiểu không hợp lệ (đừng gộp "trống hoặc quá dài hoặc sai dạng"), để khi lỗi biết ngay do kiểu nào.
- **BVA ba giá trị:** với biên *b*, thử *b−1* (ngay dưới), *b*, *b+1*. Khoảng [1, 10] cho 0, 1, 2 và 9, 10, 11. Ngưỡng đếm ("N lần sai thì chặn") thử N−1, N, N+1 lần. Biên thời gian ("sau T phút"): thử ngay trước và ngay sau; giây đúng ở biên chỉ làm khi requirement nói rõ tính bên nào, không thì ghi vào câu hỏi.
- **Bảng quyết định:** liệt kê điều kiện và hành động, gộp các tổ hợp cho cùng kết quả (nếu nhiều tổ hợp đều ra cùng một câu báo lỗi thì một lớp là đủ, đừng sinh 2ⁿ dòng).
- **Chuyển trạng thái:** vẽ (trong đầu hoặc nháp) các trạng thái và sự kiện làm đổi; test cả việc **đếm/đặt lại** (ví dụ thao tác đúng đưa bộ đếm về 0). Chỉ có chuyển trái phép khi requirement nêu.
- **Use case:** viết thành hành trình ("mở link → bị hỏi đăng nhập → đăng nhập → vào đúng trang"), cùng một dòng cho cả hành trình, không tách từng bước.
- **Đoán lỗi:** ghi **vì sao** nghĩ lỗi có ở đây dựa vào requirement; không đoán bằng kinh nghiệm chung rồi thêm quy tắc không có trong nguồn (đó là Giả định → hỏi BA).

## Bốn góc gợi ý (chỉ dùng góc liên quan tới requirement)
1. **Người dùng mới và người dùng đã có dữ liệu** (lần đầu vào, đã có hồ sơ).
2. **Gián đoạn giữa chừng** (tải lại, đổi ngôn ngữ giữa chừng, đăng xuất ở tab khác, mất phiên).
3. **Thao tác lặp lại nhiều lần** (sai liên tiếp, bấm hai lần, gửi lại).
4. **Phân quyền** (mỗi vai trò làm được gì; vai trò không đủ quyền).
Góc không liên quan thì bỏ, đừng thêm cho đủ.

## Ưu tiên
- **Cao:** luồng chính; chỗ liên quan tiền, bảo mật, tài khoản; hành vi chặn/khóa; thông báo lỗi chính. Dòng Cao **xếp trước** trong bảng.
- **Trung bình:** biến thể hợp lệ của luồng chính, hiển thị, ngôn ngữ, điều hướng phụ.
- **Thấp:** ca hiếm, trình bày, chỗ requirement nói không quy định.

## Không làm
Không thêm ca bảo mật, hiệu năng, tương thích trình duyệt khi requirement không nói. Không test điều requirement nói thuộc phần khác. Không thêm tình huống chỉ để "đủ bộ".
