<!--
KHUÔN TEST PLAN (kế hoạch kiểm thử) — bản đầy đủ, dùng chung mọi dự án (2026-11-19).
- Khuôn này để NGƯỜI ĐỌC hiểu cấu trúc. Khi dùng thật, theo skill tao-test-plan: viết `testing/<dự-án>/test-plan-nguon.txt` từ `.claude/skills/tao-test-plan/assets/mau-test-plan-nguon.txt`, rồi `sinh-test-plan.py sinh` ra test-plan.md (số liệu tự đọc từ tài liệu dự án, câu trả lời người test lưu ở test-plan-thong-tin.json).
- Mỗi dự án/mỗi đợt test một file: testing/<dự-án>/test-plan.md (đợt mới → sao khuôn này, đặt tên test-plan-<bản-build>.md nếu cần giữ nhiều bản).
- Viết TRƯỚC khi test (kế hoạch). **Test plan KHÔNG ghi kết quả test** (số case đã chạy/đạt/không đạt, bug đã thấy, trạng thái lượt chạy): người dùng dặn 2026-11-19 "test plan là phần chưa test". Kết quả chỉ nằm ở test-summary-report.md và các file kết quả. Rủi ro viết dạng "có thể", dựa trên requirement/khám phá, không dựa trên lượt chạy. Kết quả sau khi test nằm ở test-summary-report.md; hai file dùng cùng khung nên đọc cạnh nhau là khớp.
- Chỉ ghi điều có nguồn: tài liệu của dự án, lời sếp/BA, hoặc điều đã thấy trên hệ thống. Chưa biết → ghi "Chưa rõ" và đưa vào mục 9 hoặc hỏi người test, KHÔNG đoán.
- KHÔNG tự đặt con số cho tiêu chí (số bug còn mở, tỉ lệ đạt, số lần nhập sai, thời gian chờ…): lấy từ sếp, requirement của dự án hoặc hỏi người test rồi ghi nguồn bên cạnh số.
- Viết tiếng Việt thường, câu đủ ý, đọc là hiểu. Không dùng mã nội bộ làm nội dung chính; mã (TC, bug, requirement) phải là link bấm được tới đúng dòng.
- Chỉ test chức năng (functional). Bảo mật, hiệu năng chỉ xuất hiện ở mục "Ngoài phạm vi" trừ khi sếp yêu cầu.
- Phần trong dấu <...> là chỗ điền. Phần chữ nghiêng là hướng dẫn: xóa đi khi điền xong. Xóa luôn khối chú thích này trong file thật.
-->

# Kế hoạch kiểm thử (Test plan) — <Tên hệ thống / đợt test>

| | |
|---|---|
| Hệ thống | <tên hệ thống>, <địa chỉ môi trường test> |
| Bản build / phiên bản | <số phiên bản đang test> |
| Mã kế hoạch | <ví dụ TP-<dự án>-001> |
| Ngày lập | YYYY-MM-DD |
| Cập nhật lần cuối | YYYY-MM-DD |
| Người lập | <tên> |
| Người yêu cầu | <sếp / bên yêu cầu> |
| Người duyệt kế hoạch | <tên> |
| Tình trạng | nháp / đã gửi duyệt / đã duyệt |

## 1. Mục tiêu và bối cảnh
- **Vì sao có đợt test này:** <1–2 câu: build mới, feature mới, chuẩn bị phát hành…>
- **Câu hỏi đợt test cần trả lời:** <ví dụ "Bản build này đủ điều kiện để phát hành chưa?">
- **Kết quả bàn giao cuối cùng:** <ví dụ báo cáo tổng kết kiểm thử và quyết định nhận / không nhận build>
- **Tài liệu đầu vào:** <requirement/SRS, release note, câu trả lời của BA — mỗi mục một link; mục nào chưa có thì ghi "Chưa có">

## 2. Phạm vi
*Phần sếp đọc kỹ nhất: ghi rõ cả điều không test.*

**2.1. Trong phạm vi**

| Feature / chức năng | Vai trò (tài khoản) liên quan | Căn cứ (requirement) | Đã có test case chưa |
|---|---|---|---|
| <feature 1> | <vai trò> | <link requirement> | Có (<số> case) / Chưa |

**2.2. Ngoài phạm vi (không test đợt này)**

| Nội dung | Lý do không test | Rủi ro nếu bỏ qua |
|---|---|---|
| <ví dụ bảo mật, hiệu năng, feature chưa có test case> | <lý do: ngoài yêu cầu, chưa có tài liệu, chưa có thời gian…> | <hậu quả có thể xảy ra> |

## 3. Cách kiểm thử
*Mỗi lớp test trả lời một câu hỏi khác nhau. Chỉ ghi lớp nào đợt này dùng.*

| Lớp test | Để làm gì | Chạy khi nào | Cách làm (tay / tự động) | Tài liệu / bộ case |
|---|---|---|---|---|
| Smoke | Build có đủ ổn để bắt đầu test sâu không | Ngay khi nhận build | <tay / tự động> | <link smoke-test.md> |
| Test từng feature | Từng chức năng chạy đúng theo requirement | Sau khi smoke Đạt | <tay / tự động> | <link test-case.md của từng feature> |
| Regression | Chỗ đã chạy tốt trước đây còn chạy tốt không sau khi build đổi | Khi build có thay đổi | <tay / tự động> | <link regression-test.md> |
| Re-test | Bug Dev báo đã sửa thì thật sự hết chưa | Khi Dev giao bản sửa | <tay> | <link kế hoạch re-test> |

**Kỹ thuật thiết kế test case đã dùng:** <ví dụ phân vùng tương đương, giá trị biên, bảng quyết định… — ghi theo file test case của feature>

## 4. Môi trường và dữ liệu test
- **Môi trường:** <địa chỉ>, nhãn môi trường: <staging / dev / test>.
- **Trình duyệt / thiết bị:** <tên + số bản, hệ điều hành>.
- **Tài khoản test:**

| Tài khoản | Vai trò | Dùng cho feature | Ghi chú |
|---|---|---|---|
| <mã tài khoản> | <vai trò> | <feature> | *Mật khẩu không ghi ở đây; để trong kho lưu tài khoản test của dự án.* |

- **Dữ liệu cần chuẩn bị trước:** <hồ sơ mẫu, số liệu, trạng thái cần có; ai chuẩn bị; chuẩn bị bằng cách nào>
- **Chỗ dễ gây khóa hệ thống hoặc đổi dữ liệu người khác:** <ví dụ nhập sai mật khẩu quá số lần cho phép; cách tránh; ca nào để người test tự làm tay>

## 5. Tiêu chí bắt đầu, kết thúc, tạm dừng
*Các con số lấy từ sếp, requirement hoặc người test; ghi nguồn cạnh số. Chưa có số thì ghi "Chưa chốt — hỏi <ai>".*

**5.1. Điều kiện để bắt đầu test**

| Điều kiện | Đã đạt chưa | Nguồn |
|---|---|---|
| Build đã lên môi trường test | <Có / Chưa> | |
| Smoke test Đạt | <Có / Chưa> | |
| Có requirement / release note của build | <Có / Chưa> | |
| Tài khoản và dữ liệu test sẵn sàng | <Có / Chưa> | |

**5.2. Điều kiện để kết thúc test (đủ thì mới gửi báo cáo tổng kết)**

| Tiêu chí | Ngưỡng | Nguồn của con số |
|---|---|---|
| Test case bắt buộc đã chạy hết | <tỉ lệ hoặc danh sách> | <sếp / requirement / người test> |
| Bug mức Nghiêm trọng còn mở | <số> | |
| Bug mức Lớn còn mở | <số> | |
| Re-test mọi bug đã sửa xong | <Có> | |
| Regression tầng bắt buộc đã chạy | <tầng nào> | |

**5.3. Khi nào tạm dừng và khi nào chạy tiếp**

| Dừng khi | Chạy tiếp khi |
|---|---|
| Smoke test Không đạt | Dev giao build mới và smoke Đạt |
| Môi trường test không truy cập được | Môi trường hoạt động lại |
| <tình huống khác> | <điều kiện> |

## 6. Phân công và lịch

| Việc | Người làm | Bắt đầu | Hạn | Thời gian ước tính | Ghi chú |
|---|---|---|---|---|---|
| Soát requirement, hỏi BA | <tên> | <ngày> | <ngày> | <giờ/ngày> | |
| Viết / cập nhật test case | <tên> | | | | |
| Chạy smoke | <tên> | | | | |
| Chạy test từng feature | <tên> | | | | |
| Chạy regression | <tên> | | | | |
| Re-test bug đã sửa | <tên> | | | | |
| Lập báo cáo tổng kết, gửi duyệt build | <tên> | | | | |

**Người liên hệ:** BA: <tên>; Dev: <tên>; Người duyệt build: <tên>.

## 7. Quản lý bug
- **Ghi bug thế nào:** bug report đủ mục (bước tái hiện, kết quả thực tế / mong đợi, môi trường, ảnh hoặc video); mỗi lỗi một bug; link tới test case Không đạt.
- **Thang đo:** mức nghiêm trọng Nghiêm trọng / Lớn / Nhỏ / Rất nhỏ; mức ưu tiên Cao / Trung bình / Thấp. <ghi định nghĩa của dự án cho từng mức nếu sếp yêu cầu>
- **Trạng thái bug:** <Mới → Dev đã sửa → Đã re-test → Đóng / Mở lại>.
- **Nơi quản lý bug:** <file trong repo / công cụ của công ty>.
- **Bug lọt ra production:** nếu chưa có test case chặn đúng bug đó thì viết case mới và thêm vào bộ regression.

## 8. Sản phẩm bàn giao

| Sản phẩm | Khi nào có | Link |
|---|---|---|
| Bảng soát requirement và câu hỏi cho BA | Trước khi viết test case | <link> |
| Test case từng feature | Trước khi chạy | <link> |
| Bộ smoke test và kết quả | Khi nhận build | <link> |
| Bộ regression và kết quả | Khi build có thay đổi | <link> |
| Bug report | Trong lúc test | <link> |
| Báo cáo tổng kết kiểm thử (có quyết định nhận build) | Cuối đợt | <link> |

## 9. Rủi ro, giả định, phụ thuộc

*Rủi ro viết dạng "có thể", dựa trên requirement và khám phá, KHÔNG rút từ lượt chạy.*

**9.1. Rủi ro và phụ thuộc**

| Loại | Nội dung | Ảnh hưởng | Cách giảm / ai quyết |
|---|---|---|---|
| Rủi ro | <ví dụ requirement chưa BA xác nhận> | <test case có thể phải viết lại> | <hỏi BA trước khi chạy> |
| Rủi ro | <ví dụ môi trường dùng chung dữ liệu; chưa có release note; chỉ một trình duyệt> | <ảnh hưởng> | <cách giảm> |
| Phụ thuộc | <chờ Dev trả lời câu hỏi, chờ release note…> | <ảnh hưởng> | <ai quyết> |

**9.2. Giả định**
*Mỗi gạch một điều đang coi là đúng khi lập kế hoạch; điều nào sai thì kế hoạch phải sửa.*
- <ví dụ: chỉ test chức năng>
- <ví dụ: môi trường test phản ánh đúng bản build cần test>
- <ví dụ: tích hợp bên ngoài chưa thiết lập nên không thuộc đợt test này>

## 10. Truy vết requirement ↔ test case

*Mỗi requirement trong phạm vi phải có ít nhất một test case, hoặc ghi rõ vì sao chưa có. Mã requirement và mã test case đều là link bấm được tới đúng dòng; dùng `scripts/truy-vet.py` để sinh và kiểm.*

| Requirement | Test case | Smoke / Regression | Tình trạng |
|---|---|---|---|
| <link mã requirement> | <link mã test case> | <có / không> | <Đã có case / Chưa có case: lý do> |

**Độ phủ:** <số requirement có test case / tổng số requirement trong phạm vi>.

## 11. Phê duyệt kế hoạch

| Vai trò | Họ tên | Quyết định (Duyệt / Cần sửa) | Ngày | Ý kiến |
|---|---|---|---|---|
| Người lập | | | | |
| Người duyệt kế hoạch | | | | |

## 12. Lịch sử cập nhật

| Ngày | Người sửa | Nội dung sửa | Lý do |
|---|---|---|---|
| YYYY-MM-DD | <tên> | Tạo bản đầu | <lý do> |
