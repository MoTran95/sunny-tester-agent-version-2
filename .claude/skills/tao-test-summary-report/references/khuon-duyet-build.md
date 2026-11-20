# Khuôn `duyet-build.json`

File ở `testing/<slug>/duyet-build.json` (không đặt trong `run-results/`: thư mục đó chỉ chứa lượt chạy của các bộ test). Trang HTML tạo file này khi bấm **Tải file duyệt**; chỉ ghi tay khi người dùng đọc nội dung trong chat.

```json
{
  "approvals": [
    {
      "build": "<số build>",
      "based_on": {"<bộ test>": <số lượt>, "...": 0},
      "tester": {"name": "", "decision": "", "reason": "", "date": "YYYY-MM-DD"},
      "approver": {"name": "", "title": "", "decision": "", "conditions": "", "note": "", "date": "YYYY-MM-DD"}
    }
  ]
}
```

| Trường | Ý nghĩa |
|---|---|
| `build` | Build được duyệt. Mỗi build một phần tử; duyệt lại thì thay phần tử cũ cùng build. |
| `based_on` | Số lượt chạy mới nhất của từng bộ test lúc duyệt (tên bộ: `smoke`, `regression-tang-1`, tên thư mục tính năng…). Lấy từ báo cáo đang hiển thị, **không điền tay cho khác thực tế**: khác số lượt hiện tại thì trang báo "Đã lỗi thời". |
| `tester` | Đề xuất của người test (mục 2). Cả khối có thể bỏ trống. |
| `approver` | Quyết định của người duyệt (mục 9). |
| `decision` | Đúng một trong ba: `Nhận build`, `Không nhận build`, `Nhận có điều kiện`. |
| `conditions` | Bắt buộc khi `Nhận có điều kiện`. |
| `date` | Ngày duyệt (ISO). Trang tự điền ngày khi tải file nếu để trống. |

Cách lấy `based_on` khi ghi tay: chạy `build_report.py summary`, đọc số lượt ở mục 4 của báo cáo (cột "Lượt") cho từng bộ.
