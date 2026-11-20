# Nguồn điền từng mục và thông tin cần hỏi người test

Đọc ở bước 2 và 4 của `SKILL.md`. Tra nguồn trước, chỉ hỏi cái nguồn không có.

## Nguồn điền từng mục (đọc trong `<slug>` của dự án hiện tại)

| Mục test plan | Lấy từ | Lưu ý |
|---|---|---|
| Bảng đầu (hệ thống, build, địa chỉ) | `memories/modules/<slug>/overview.md`, `testing/<slug>/auto-config.json` (`default_url`, `health_api`) | Số build do người dùng nêu hoặc chân trang hệ thống; không suy từ lượt chạy |
| 1. Mục tiêu | Lời người dùng/sếp trong chat; `memories/modules/<slug>/overview.md` cho phần "hệ thống làm gì" | Lý do đợt test chưa rõ thì hỏi (nhóm A) |
| 1. Tài liệu đầu vào | `srs/<slug>/`, `testing/<slug>/<tính-năng>/bang-soat-requirement.md`, `cau-hoi-cho-ba.md` | Chỉ ghi có/chưa có, số câu BA đã trả lời, SRS nháp hay đã xác nhận |
| 2. Phạm vi | Tính năng có `testing/<slug>/<tính-năng>/test-case.md` = trong phạm vi; phần chỉ có khám phá (`evidence/<slug>/`) = ngoài phạm vi kèm lý do | Số test case đếm từ file test case |
| 2.2 Mã requirement chưa có case | `scripts/truy-vet.py kiem <slug> <tính-năng>` hoặc `truy-vet.md` | |
| 3. Cách kiểm thử | `smoke-test.md`, `regression-test.md` (số case, số tầng, thời gian ước tính), `docs/chay-test-tu-dong.md` | Chỉ nêu bộ case và cách làm, **không** kết quả |
| 4. Môi trường, tài khoản | `memories/modules/<slug>/overview.md`, `exploration-findings.md` (vai trò), `tu-dong-hoa.md` (địa chỉ, trần nhập sai, thời gian chặn: số riêng của dự án) | Không ghi mật khẩu |
| 4. Chỗ dễ khóa hệ thống | `memories/pitfalls/dont-trigger-lockouts.md`, `testing/<slug>/auto-config.json`, các ca có cờ SAI-N trong `liet-ke-tc.py` | Không nêu lỗi đã thấy khi chạy |
| 5.1 Điều kiện bắt đầu | Release note có hay chưa; smoke là cổng vào; tài khoản và dữ liệu | Ghi "Cách kiểm", không ghi "đã đạt chưa" |
| 5.2 Tiêu chí kết thúc | Tiêu chí trả build trong `smoke-test.md`; phần còn lại **hỏi người test** | Không tự đặt số |
| 5.3 Tạm dừng | Smoke Không đạt thì dừng (`smoke-test.md`); chặn đăng nhập; môi trường lỗi | |
| 6. Phân công, lịch | **Hỏi người test**; thời gian chạy lấy từ `smoke-test.md` và ước tính trong test case | |
| 7. Quản lý bug | Skill `tao-bug-report` (`references/thang-muc-do.md`) | Không liệt kê bug đã ghi |
| 8. Sản phẩm bàn giao | Danh sách file của dự án; file kết quả ghi tên không link nếu chưa có | |
| 9. Rủi ro | SRS nháp, câu hỏi BA chưa trả lời, tích hợp chưa thiết lập, dữ liệu dùng chung, chưa có release note, chỉ một trình duyệt | Dạng "có thể", dựa trên tài liệu |
| 10. Truy vết | `scripts/truy-vet.py`, `truy-vet.md` mỗi tính năng | Chỉ độ phủ requirement ↔ test case |

## Thông tin phải hỏi người test (khi nguồn không có)

Hỏi theo nhóm, mỗi nhóm một tin nhắn thường trong chat (xem bẫy ở bước 4 của `SKILL.md`). Mỗi câu nói rõ đang ở mục nào, vì sao cần, và chỗ nào chưa biết thì bỏ qua để để trống.

**A. Yêu cầu của đợt test (mục bảng đầu, 1, 2)**
- Ai yêu cầu test plan, ai duyệt kế hoạch?
- Đợt test để quyết định chuyện gì (nhận build, phát hành, nghiệm thu)?
- Phạm vi đúng là các tính năng đã có test case, hay cả hệ thống? (Cả hệ thống nghĩa là phải khám phá, viết requirement, test case thêm trước.)
- Có release note hoặc danh sách thay đổi của build không?

**B. Tiêu chí kết thúc (mục 5.2): số do sếp/công ty quyết**
- Tối đa bao nhiêu bug Nghiêm trọng và bao nhiêu bug Lớn còn mở thì vẫn xin nhận build?
- Tỉ lệ test case Đạt tối thiểu, tính trên số đã có kết luận? (Chưa có số thì ghi "người duyệt build quyết định dựa trên báo cáo, không có ngưỡng cứng".)
- Test case bắt buộc chạy và số tầng regression: công ty quy định hay người test tự quyết theo nguồn lực và thời gian?
- Ca làm tay chưa làm kịp (ca chặn đăng nhập…) có chặn việc kết thúc không, hay chỉ ghi vào rủi ro?

**C. Người và lịch (mục 6, bảng đầu)**
- Tên BA, Dev, người duyệt build, người duyệt kế hoạch.
- Ngày bắt đầu, hạn nộp, số giờ mỗi ngày dành cho test.
- Mã kế hoạch (công ty có quy ước không).

**D. Môi trường và công cụ (mục 4, 7)**
- Trình duyệt và thiết bị cần phủ ngoài Chrome? Số bản Chrome đang dùng.
- Môi trường có người khác dùng chung không? Được tạo thêm dữ liệu test và đặt lại bộ đếm nhập sai không, ai làm?
- Công cụ quản lý bug của công ty (Jira hay khác), trạng thái bug gồm những gì, thang mức nghiêm trọng có giống Nghiêm trọng / Lớn / Nhỏ / Rất nhỏ không?
- Sếp muốn nhận file dạng nào (HTML, PDF, Word)? (Chưa có lệnh sinh PDF/Word bằng script: PDF in từ nút trên trang.)

## Cách đặt câu hỏi
- Đủ ngữ cảnh: người đọc không phải lật lại chat cũ.
- Có thể kèm lựa chọn và hệ quả ngắn của từng lựa chọn khi có cách làm phổ biến; **không đưa con số làm lựa chọn cho ngưỡng** (ngưỡng do sếp/công ty quyết), chỉ hỏi con số đó là bao nhiêu hoặc "chưa có".
- Không hỏi lại điều đã có trong chat, `memories/`, tài liệu dự án.
- Tối đa 3 câu một lượt cho mỗi nhóm; nhóm B và C là quan trọng nhất.
