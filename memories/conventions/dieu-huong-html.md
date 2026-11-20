# Điều hướng trang HTML của dự án (người dùng chốt 2026-11-20)

- Mọi trang HTML thuộc dự án (testing/, srs/, evidence/ của dự án) được chèn khối `<!--dh-->…<!--/dh-->` ngay sau `<body>` bởi `scripts/test_automation/dieu_huong.py`, gọi cuối `docs_pages.render_all`. Chạy lại vẫn một khối.
- Trang con: thanh cố định `← Trang tổng` (về đúng `#tn-<tính-năng>`), breadcrumb Dự án › Tính năng › Trang, menu nhảy Smoke/Regression/Test plan/Tổng kết/Hướng dẫn, dải tab các trang cùng tính năng (kèm BUG-xx). Trang cấp dự án (smoke, regression, tổng kết): tab nhóm bộ test.
- Trang tổng: thanh menu ngang cố định, ☰ khi hẹp; mọi trang có nút "↑ Lên đầu".
- Không chèn vào test plan (tài liệu gửi ngoài) và tài liệu dùng chung ngoài dự án. Dải `nav-doc` cũ đã bỏ.
- Báo cáo khám phá do skill dựng (không do build_docs sinh) vẫn được chèn khi chạy `build_docs.py --all`; dựng lại báo cáo xong phải chạy lại để có thanh. Thanh dùng biến `--dh-h` để thanh `nav.top` của báo cáo xếp ngay dưới.

## Dùng cho dự án khác và giữ chi phí thấp
- Không có gì riêng dự án trong `dieu_huong.py`/`theme.py`: dự án mới (`tao-du-an.py`) chạy `build_docs.py --all` là có đủ trang, thanh, font, logo (đổi thương hiệu: `brand.json`, xem `docs/thuong-hieu/README.md`). `xuat-bo-loi.py` chép cả thư viện này sang máy/bộ khác.
- Tiết kiệm token: toàn bộ HTML/điều hướng do script sinh (0 token AI); AI chỉ viết md/JSON nguồn. Không đọc lại HTML sinh ra; kiểm bằng `kiem-tra-bo-nho.py` (0 lỗi là đủ) và `selftest/run_selftest.py` (mục `nav:` giữ chất lượng: thanh có mặt, link về đúng thẻ, chỉ một khối). Cần xem bằng mắt: một ảnh chụp thu nhỏ (`scale` 0.5), không dựng thêm trang thử.
- Sửa thanh: chỉ `dieu_huong.py` (CSS/JS nằm trong một chuỗi); sau đó selftest + `build_docs.py --all`.
