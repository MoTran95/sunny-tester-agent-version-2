# Chạy test cho tính năng MỚI (test case viết từ requirement, dev vừa làm xong)

Test case chưa từng gặp giao diện thật, nên **lượt đầu là lượt hiệu chuẩn**: Không đạt có thể do test case chứ chưa chắc do hệ thống.

## Thứ tự
1. **Chốt phạm vi** (bước 1 của `SKILL.md`): địa chỉ có nhãn môi trường thử, số bản build, tài khoản, dữ liệu cần. Thiếu thì hỏi; dữ liệu thật hỏi trước khi tạo.
2. **Cổng vào:** có bộ smoke của tính năng → chạy trước; **Trả build** thì dừng và báo. Chưa có smoke → ca luồng chính (đường vui) làm cổng; hỏng ngay thì dừng, báo, tạo bug.
3. **Giao diện thật:** `srs-from-website/scripts/kiem-tra-bang-phu.py`. Đã có nhật ký đủ cho các ca sắp chạy → dùng luôn, **không khám phá lại**; tính năng đã có mà đổi một phần → hỏi phần nào đổi. Chưa có → khám phá lần đầu **chỉ phạm vi các ca sắp chạy**, rồi tự dựng báo cáo khám phá (CLAUDE.md).
4. **Đối chiếu requirement với hệ thống TRƯỚC khi viết script**, mỗi chỗ khác thuộc một loại:
   | Loại | Xử lý |
   |---|---|
   | A. Test case sai/lạc hậu (tên nút, thứ tự bước, nhãn mà requirement không quy định) | Sửa test case, không bug |
   | B. Requirement rõ, hệ thống làm khác | Lỗi thật: Không đạt → bug |
   | C. Requirement mơ hồ/thiếu | Câu hỏi BA; ca `CẦN XÁC NHẬN`, nếu Không đạt thì bug "Nghi lỗi, chờ xác nhận" |
   | D. Hệ thống có hành vi requirement không nhắc | Hỏi BA "có phải yêu cầu không", không tự coi đúng/sai, không bug |
   Không phân được loại thì hỏi người dùng (tối đa 3 câu). Ngưỡng (số lần sai, thời gian chặn…) không tự đặt.
5. **Phân ca:** tự động được → script theo `assets/mau-ca-tu-dong.py`. Gây chặn hệ thống hoặc **cần bên ngoài** (captcha, email/SMS thật, cổng thanh toán thật) → `Bỏ qua`, Tự động hóa `Không tự động được: <lý do>`, liệt kê ở "chưa có kết quả" kèm rủi ro. Không ghi Đạt khi thiếu ảnh evidence (mục 9 `quy-tac-da-chot.md`); người test tự chạy và đưa ảnh thì ghi lượt với ảnh đó.
6. **Chạy, ghi lượt, bug, trang kết quả** như bước 3–8 của `SKILL.md`. Ghi nhãn lượt hiệu chuẩn; kết luận nói rõ "lượt đầu, một phần Không đạt có thể do test case". Loại A → sửa test case rồi chạy lại ca đó.
7. **Trả kết quả:** một link `testing/<slug>/index.html#tn-<tính-năng>`; nêu số ca đã / chưa có kết luận và vì sao, tóm tắt bảng khác biệt theo loại, câu hỏi đang chờ BA. Ca chưa chạy được không tính vào "đã chạy".

## Requirement đổi, hoặc team chốt một điểm còn mơ hồ
Cập nhật **cả chuỗi trong cùng lượt** để tài liệu không mâu thuẫn và truy vết được; làm xong mới chạy lại các ca bị ảnh hưởng.
1. **Chưa rõ ai chốt, chốt gì, áp dụng mã nào, thay hay thêm → hỏi trước, không tự quyết** (một lần, tối đa 3 câu). Tester tự quyết mà BA/team chưa xác nhận → ghi đúng như vậy, đưa vào câu hỏi BA, không sửa SRS tại chỗ.
2. Bảng phân tích + câu hỏi BA: ghi câu trả lời nguyên văn kèm nguồn bằng `phan-tich-requirement/scripts/ghi-tl.py`.
3. SRS: sửa tại chỗ giữ ID (đổi ý nghĩa → ID mới, mục cũ `đã bỏ`), thêm dòng "Lịch sử thay đổi"; số liệu lịch sử khớp file (`srs-writing-guide.md` mục 6, `check-srs.py`).
4. Test case: `scripts/truy-vet.py kiem <dự-án> <tính-năng>` → sửa các TC "Cần xem lại" (kết quả mong đợi `CẦN XÁC NHẬN` đổi theo câu trả lời; `kiem-tra-tc.py`) → `chot -m "<lý do>"` (người dùng quyết khi chốt).
5. Bộ phụ thuộc: `truy-vet-smoke.py kiem`, `truy-vet-regression.py kiem`; TC đã có script thì sửa script; bug đang mở dính mã này thì hỏi người dùng trước khi đóng/đổi.
6. Soát chéo: các script trên, `build_docs.py --all`, `kiem-tra-bo-nho.py` đều 0 lỗi; mã, ngày, trạng thái ở SRS, bảng phân tích, test case, truy vết, test plan khớp nhau. Nêu trong chat đã sửa file nào.

## Bẫy
- Viết script thẳng từ test case khi chưa nhìn giao diện thật → hàng loạt `Không kết luận` do không thấy phần tử.
- Coi mọi khác biệt là bug → bug rác; coi mọi khác biệt là test case sai → bỏ sót lỗi thật.
- Khám phá lại từ đầu "cho chắc" khi đã có nhật ký → tốn token người dùng đã dặn tránh.
