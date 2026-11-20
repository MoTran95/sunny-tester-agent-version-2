# Chạy test case tự động bằng Playwright

Dành cho người kiểm thử muốn chạy lại test case mà không cần nhờ AI mỗi lần. Dùng chung cho mọi dự án trong repo.

## Cách hoạt động trong một câu

Bạn đăng nhập một lần bằng lệnh đăng nhập (lưu phiên ra file), rồi lệnh chạy test mở trang bằng phiên đó, kiểm kết quả từng test case và in ra bảng Đạt / Không đạt kèm ảnh bằng chứng.

Mật khẩu chỉ nằm trong file `.env` trên máy bạn. Script test case **không thấy mật khẩu**: dùng phiên đã lưu, hoặc gọi `ctx.sign_in("<mã tài khoản>")` để thư viện đọc `.env` và điền form đăng nhập (bấm đúng một lần).

## Cài một lần

Cần Python 3.10 trở lên và Chrome hoặc Edge trên máy (không phải tải thêm trình duyệt). Cài thư viện bằng một lệnh, từ thư mục repo (tạo `.venv` trong repo, cần mạng; Mac gõ `python3`):

```powershell
python scripts/cai-dat-may-moi.py
```

Không cần nhớ đường dẫn venv: lệnh `python -X utf8 scripts/run_tests.py …` bên dưới tự chạy lại bằng `.venv` khi Python hệ thống chưa có Playwright. Chi tiết máy mới: `docs/cai-dat-may-moi.md`.

Tài khoản test để trong `.env` ở gốc repo (file này không commit), theo mẫu:

```
<TIỀN_TỐ>_URL=https://...
<TIỀN_TỐ>_<MÃ>_USER=<tên đăng nhập>
<TIỀN_TỐ>_<MÃ>_PASSWORD=<mật khẩu>
```

`<TIỀN_TỐ>` do file cấu hình của dự án quy định. Ví dụ dự án `cua-hang-mau` dùng `CUA_HANG_MAU`, tài khoản `NV01` thì khóa là `CUA_HANG_MAU_NV01_PASSWORD`.

## Chạy hằng ngày

Các lệnh dưới đây gõ `python` (Python hệ thống); phần cần Playwright tự dùng `.venv` như đã nói ở trên.

**Bước 1. Đăng nhập, lưu phiên** (phiên có thể chỉ sống vài phút tùy hệ thống, nên chạy bước 2 ngay sau đó):

```powershell
python -X utf8 scripts/auto_login.py NV01 NV02 NV03 --headless
```

**Bước 2. Chạy test:**

```powershell
python -X utf8 scripts/run_tests.py --smoke
```
```powershell
python -X utf8 scripts/run_tests.py --case-id dang-nhap/tc-001
```
```powershell
python -X utf8 scripts/run_tests.py --feature dang-nhap
```

Thêm `--project <slug>` nếu không muốn dùng dự án trong `.du-an-hien-tai`. Thêm `--headed` để xem cửa sổ trình duyệt khi gỡ lỗi.

## Bảng kết quả smoke và trang web

Chạy cả bộ smoke và ghi luôn thành một lượt. Lượt nào cũng phải có file kết luận và rủi ro (`--conclusion-file`); chưa có thì lệnh chỉ chạy, in ra lệnh `build_report.py add-run` để ghi lượt sau khi viết kết luận (số bản lấy ở chân trang, đổi `version` trong `auto-data.json` khi build mới):

```powershell
python -X utf8 scripts/run_tests.py --smoke --record-run --build 1.3.0 --conclusion-file <kết-luận.json>
```

Lệnh này ghi thêm một lượt vào `testing/<dự-án>/run-results/smoke.json`, rồi tự sinh lại hai file:
- `testing/<dự-án>/smoke-ket-qua.md`: bảng 6 cột (ID, Smoke case, Status, Evidence, Bug, Số lần chạy) của lượt mới nhất kèm Build, lịch sử các lượt, và bảng từng case qua các lượt.
- `testing/<dự-án>/smoke-ket-qua.html`: cùng nội dung dạng trang web, mở bằng trình duyệt hoặc gửi file cho người khác (ảnh Evidence là đường dẫn tương đối, nên gửi cả thư mục repo hoặc đưa lên cùng chỗ).

Hai file này **tự sinh, không sửa tay**. Muốn ghi kết quả từ các lần chạy riêng lẻ (ví dụ chạy nhiều đợt) hoặc gắn mã bug:

```powershell
python -X utf8 scripts/build_report.py add-run --build 1.3.0 --results-files evidence/<dự-án>/chay-test/result-A.json evidence/<dự-án>/chay-test/result-B.json --status "2=Đạt kèm lỗi đã biết" --bug "2=BUG-001"
```

Chỉ sinh lại md và HTML từ dữ liệu đã có: `python -X utf8 scripts/build_report.py build`.

"Số lần chạy" của mỗi case là số lượt có kết luận Đạt hoặc Không đạt (đếm từ lịch sử). Lượt "Không kết luận" hoặc "Chưa chạy" không tính. Kết luận của lượt: **Nhận build** khi mọi case có kết luận Đạt (kể cả kèm lỗi đã biết), **Trả build** khi có ca Không đạt, **Chưa đủ kết luận** khi còn ca chưa chạy được.

### Cột Các bước và Kết quả mong đợi

Bảng kết quả (md và HTML) có hai cột này cho từng smoke case, lấy từ dòng test case gốc (`test-case.md`), nên sửa test case thì lần sinh sau tự đổi theo. Kết luận của từng case nằm ở cột **Status**, nên bảng không có cột "Kết quả thực tế" riêng (chi tiết từng ý đúng/sai vẫn lưu trong `smoke.json` và trong file kết quả của mỗi lần chạy).

### Xem bảng rộng trên trang HTML

Bảng kết quả có nhiều cột nên rộng hơn màn hình. Có một **thanh kéo ngang luôn nằm ở cuối màn hình** khi bạn đang xem bảng, không cần cuộn xuống cuối bảng mới kéo được. Ngoài ra có thể giữ chuột trái rồi kéo trên bảng, hoặc giữ Shift và lăn chuột. Hai cột ID và Smoke case được giữ cố định bên trái để luôn biết đang xem case nào.

### Ảnh evidence tô đỏ chỗ lỗi

Ca có ý kiểm tra sai mà đã khai `mark_text` sẽ có thêm một ảnh tên có `-loi` với khung đỏ và nhãn "LỖI" đúng chỗ chữ sai. Khai thêm `error_note="Lỗi ở bước 5: ..."` thì câu đó hiện **ngay trên ảnh trong cột Evidence** để người đọc biết lỗi gì, ở bước nào. Ảnh này cũng hiện trong trang bug. Ảnh gốc luôn được giữ nguyên.

Ảnh đã chụp từ trước, tô thủ công theo tọa độ (điểm ảnh, góc trên-trái rồi dưới-phải của chữ):

```powershell
python -X utf8 scripts/mark_error.py evidence/<dự-án>/chay-test/ten-anh.png --box 1067,14,1122,30
```

Rồi đưa ảnh tô đỏ vào bảng kết quả khi ghi lượt: `--error-images "2=evidence/.../ten-anh-loi.png"` và câu mô tả lỗi `--error-captions "2=Lỗi ở bước 5: ..."` (số là cột # của bảng smoke).

## Trang HTML cho file bug

Mỗi `BUG-nnn.md` có trang `BUG-nnn.html` cạnh nó (tự sinh khi chạy `build_report.py build`, hoặc riêng: `build_report.py bug-pages`):

```powershell
python -X utf8 scripts/build_report.py bug-pages
```

Trang chia mỗi mục thành một thẻ có nút **Sao chép** (chép chữ thường của mục đó để dán vào Jira, chat...). Ở đầu trang có "Sao chép tiêu đề" và "Sao chép cả bug (md)". Ảnh bằng chứng hiện thành ảnh nhỏ, ảnh tô đỏ có viền đỏ; chữ `[Giả định: …]` được tô vàng. Cột Bug trong bảng kết quả smoke link thẳng tới trang này. Nút Sao chép cần trang mở bằng trình duyệt thường (Chrome, Edge); nếu trình duyệt chặn clipboard thì trang tự dùng cách dự phòng.

## Báo cáo tổng kết kiểm thử và duyệt build

Một trang cho cả dự án, tổng hợp mọi lượt chạy của build mới nhất (smoke, regression, test case từng tính năng):

```powershell
python -X utf8 scripts/build_report.py summary
```

Ra `testing/<dự-án>/test-summary-report.md` và `.html` (`build_docs.py` cũng tự sinh lại). Trang có 9 mục: thông tin chung (người viết báo cáo, người test), kết luận, kết quả theo tính năng, theo bộ test, bug, độ phủ requirement, rủi ro còn lại, đề xuất tiếp theo, duyệt build. Số liệu đọc từ file có sẵn, không tự quyết nhận hay trả build.

**Điền quyết định ngay trên trang HTML:**
1. Mục 2 (người test đề xuất) và mục 9 (người duyệt build): chọn **Nhận build / Không nhận build / Nhận có điều kiện**, điền tên, chức danh, điều kiện (bắt buộc khi chọn "có điều kiện"), ghi chú. Trình duyệt tự lưu bản nháp.
2. Bấm **Tải file duyệt** để tải `duyet-build.json`.
3. Đặt file vào `testing/<dự-án>/duyet-build.json` (ghi đè), rồi chạy `python -X utf8 scripts/build_docs.py`: quyết định vào cả bản md lẫn HTML. Nếu trình duyệt đặt tên `duyet-build (1).json` thì đổi lại cho đúng tên.
4. Quyết định gắn với số lượt của từng bộ test lúc duyệt. Có lượt chạy mới sau đó thì trang báo **đã lỗi thời**: cần xem lại và duyệt lại.

**Gửi người khác xem:** bấm **In / Lưu PDF** (hộp thoại in của trình duyệt, chọn "Lưu dưới dạng PDF"). Bản in tự dùng nền sáng, ẩn các nút, giữ nội dung đã điền.

## Đọc kết quả

| Kết luận | Nghĩa |
|---|---|
| Đạt | Mọi ý chính và ý phụ đúng |
| Đạt kèm ý phụ sai | Ý chính đúng, ý phụ sai (ghi rõ ý nào). Smoke vẫn cho qua nếu đó là lỗi đã biết |
| Không đạt | Sai ít nhất một ý chính |
| Không kết luận | Chưa kết luận được vì script lỗi, trang chờ quá hạn hoặc phiên hết hạn. **Không phải lỗi của hệ thống**, xem ảnh `...-loi-...png` rồi sửa script hoặc đăng nhập lại |
| Chưa có script | Test case chưa có script trong thư mục `auto/` |

Mã thoát của lệnh: 0 đạt hết, 1 có ca Không đạt, 2 sai cấu hình, 3 phiên hết hạn (chưa chạy ca nào), 4 có ca không kết luận được.

Mỗi lần chạy ghi một file `result-<giờ>.json` và các ảnh vào `evidence/<dự-án>/chay-test/`.

## An toàn

- Mỗi tài khoản chỉ đăng nhập **một lần** mỗi lượt chạy. Sai mật khẩu hay bị chặn thì dừng, không tự thử lại, để không kích hoạt khóa tài khoản.
- Không dùng thư viện này để cố ý nhập sai nhiều lần. Ca kiểu đó ghi "Không tự động được" trong test case.
- Thư mục `.phien-dang-nhap/` chứa cookie đăng nhập, đã nằm trong `.gitignore`. Không gửi cho ai.
- Ca làm mất phiên (ví dụ bấm Đăng xuất) cần khai `invalidates_sessions` trong script để lần chạy sau không dùng nhầm phiên đã mất; xếp ca đó cuối bộ.

## Viết script cho một test case

Một test case một file: `testing/<dự-án>/<tính-năng>/auto/<mã-ca>.py`, mã ca viết thường (ví dụ `tc-001.py`). Mẫu:

```python
CASE_INFO = {
    "code": "TC-001",
    "title": "Đăng nhập đúng NV01 vào trang chủ",
    "accounts": ["NV01"],      # để [] nếu ca không cần đăng nhập
    # "invalidates_sessions": ["NV01"] # nếu ca làm mất phiên
}

def run(ctx):
    ctx.goto("/")                           # mở trang
    ctx.wait_text("Danh sách việc")         # chờ chữ hiện (trang hay "Đang tải…" vài giây)
    ctx.check_main("Vào Danh sách việc", "Danh sách việc" in ctx.page_text())
    ctx.check_minor("Không có chữ DEFAULT", "DEFAULT" not in ctx.page_text())
    ctx.screenshot("danh-sach-viec")            # ảnh bằng chứng
```

Công cụ có sẵn trong `ctx`:

| Hàm | Dùng để |
|---|---|
| `goto`, `wait_text`, `page_text`, `screenshot` | Mở trang, chờ chữ hiện, đọc chữ cả trang, chụp ảnh bằng chứng |
| `check_main`, `check_minor` | Ghi một ý kiểm tra (chính hoặc phụ). Thêm `mark_text="chữ lỗi"` thì khi ý này sai, script **tự chụp thêm ảnh có khung đỏ** quanh chữ đó; thêm `error_note="Lỗi ở bước 5: ..."` để ghi chú lỗi gì, ở bước nào dưới ảnh |
| `poll_until(fn, seconds)` | Chờ dữ liệu hiện sau vài giây (số phiên bản ở chân trang, khuyến nghị cập nhật sau khi lưu). Hết giờ không báo lỗi, script tự quyết định |
| `test_data("key")` | Lấy dữ liệu test từ `testing/<dự-án>/auto-data.json` (ví dụ id đơn hàng nháp). Thiếu thì ca ra "Không kết luận" |
| `precondition(title, passed)` | Kiểm điều kiện trước của test case. Sai thì ca ra "Không kết luận", **không** phải Không đạt |
| `page`, `page_for("<account>")` | Trang Playwright để làm mọi thứ khác; `trang` là trang của tài khoản khác khi ca dùng nhiều tài khoản (khai đủ trong `accounts`) |

Nhiều script cùng tính năng dùng chung hàm thì để một file `<tính-năng>_chung.py` cùng thư mục `auto/` (đặt tên riêng từng tính năng để không trùng), rồi `import` trong script.

**Viết selector cho trang chưa biết:** dùng `scripts/inspect_page.py`, in cây vai trò + tên của trang bằng phiên đã lưu (không cần mật khẩu):

```powershell
python -X utf8 scripts/inspect_page.py /orders/<id> --account NV01 --wait-text "Tổng tiền"
```

(Trong Git Bash, đường dẫn bắt đầu bằng `/` bị đổi thành đường dẫn Windows; chạy trong PowerShell hoặc đặt `MSYS_NO_PATHCONV=1`.)

Quy tắc viết:
- **Ý chính** là điều test case buộc phải đúng; **ý phụ** chỉ ghi nhận.
- Chờ theo chữ hoặc phần tử (`wait_text`), không chờ số giây cố định.
- Không ghi mật khẩu hay giá trị cookie trong script, không in chúng ra.
- Ghi đường dẫn script vào cột `Tự động hóa` của test case khi script đã chạy được.

## Chuẩn bị dữ liệu test

Ca cần dữ liệu có sẵn trạng thái (ví dụ đơn hàng nháp đúng số tiền) lấy id từ `auto-data.json`. Dự án có thể có script tạo sẵn dữ liệu đó (**tạo dữ liệu thật** trên hệ thống đang test, chỉ chạy khi bạn đồng ý):

```powershell
python -X utf8 testing/<dự-án>/auto/<script-tạo-dữ-liệu>.py --count 2
```

Ca bấm Lưu dùng hết hồ sơ (như TC-022). Muốn chạy lại thì tạo hồ sơ mới: thêm `--tc-022-only --overwrite`.

## Thêm dự án mới

Tạo dự án bằng `python -X utf8 scripts/tao-du-an.py <slug> "<Tên>" <địa chỉ>`: lệnh này đã tạo sẵn ba file khuôn trong `testing/<dự-án>/` và khối khóa mẫu trong `.env.example`. Việc còn lại là **điền các chỗ `<…>`** trong `auto-config.json` (chưa điền thì thư viện từ chối chạy và nói rõ khóa nào còn thiếu):

```json
{
  "env_prefix": "TEN_DU_AN",
  "default_url": "https://staging...",
  "login": {
    "id_labels": ["Tên đăng nhập", "Username"],
    "button_labels": ["Đăng nhập", "Sign in"],
    "login_api": "/api/auth/sign-in",
    "session_check_api": "/api/me",
    "session_minutes": 10,
    "max_consecutive_failures": "<số lần sai tối đa: lấy từ requirement hoặc hỏi người test, điền số>",
    "block_minutes": "<số phút bị chặn: lấy từ requirement hoặc hỏi người test, điền số>"
  }
}
```

- `id_labels`, `button_labels`: chữ trên ô mã đăng nhập và nút đăng nhập (liệt kê cả bản tiếng Anh nếu hệ thống đổi ngôn ngữ). Lấy từ hệ thống thật bằng `scripts/inspect_page.py`.
- `login_api`: đường dẫn yêu cầu đăng nhập, để script biết đăng nhập đã xong chưa.
- `session_check_api`: đường dẫn trả 200 khi còn đăng nhập, trả khác 200 khi hết phiên.
- `session_minutes`: thời hạn phiên (chỉ để nhắc). `max_consecutive_failures`: trần nhập sai của bộ đếm; `block_minutes`: thời gian bị chặn. **Hai số này không có mặc định**: lấy từ requirement hoặc hỏi người kiểm thử; chưa khai thì ca cố ý nhập sai bị từ chối (Không kết luận).
- Hệ thống đăng nhập bằng SSO, mã xác nhận hay captcha: đặt `"mode": "manual"` trong `login` (chỉ cần `session_check_api` và `session_minutes`, không cần nhãn ô, nút, API đăng nhập). Người test tự đăng nhập trong cửa sổ trình duyệt bằng `python -X utf8 scripts/auto_login.py <mã> --manual`; script chỉ chờ rồi lưu phiên, không gõ gì và không đọc mật khẩu. Ca tự động dùng phiên đã lưu.
- `auto-data.json`: số bản ở chân trang (`version`) và id dữ liệu test. `ten-tinh-nang.json`: tên hiển thị tiếng Việt của từng tính năng, ví dụ `{"dang-nhap": "Đăng nhập"}`; tính năng chưa khai thì trang hiện tên thư mục.

Hệ thống đăng nhập khác kiểu (đăng nhập qua trang ngoài, mã xác nhận, nhiều ô) thì cần mở rộng thư viện `scripts/test_automation/phien.py` trước.

## Thư viện nằm ở đâu

| Đường dẫn | Việc |
|---|---|
| `scripts/auto_login.py` | Lệnh đăng nhập, lưu phiên (người dùng tự chạy) |
| `scripts/run_tests.py` | Lệnh chạy test |
| `scripts/test_automation/` | Thư viện dùng chung (cấu hình, phiên, ngữ cảnh, kết quả, chạy) |
| `scripts/inspect_page.py` | In cấu trúc một trang để viết selector |
| `testing/<dự-án>/auto-config.json` | Cấu hình từng dự án |
| `testing/<dự-án>/auto-data.json` | Dữ liệu test của dự án (id hồ sơ nháp, số phiên bản cần test…), người kiểm thử điền |
| `testing/<dự-án>/<tính-năng>/auto/` | Script từng test case |
| `evidence/<dự-án>/chay-test/` | Kết quả và ảnh mỗi lần chạy |
| `.phien-dang-nhap/<dự-án>/` | Phiên đã lưu (không commit) |

## Ca có nhập sai (bộ đếm theo trần của dự án)
- Khai trong `CASE_INFO`: `"ready_account": "NV01"` (đăng nhập đúng một lần đầu ca để chắc tài khoản dùng được) và `"wrong_attempts": <số lần cố ý sai>`.
- Gửi form bằng `ctx.submit_login(mã, mật khẩu giả, expect_success=False)`; mật khẩu đúng lấy bằng `password_of="NV01"` (thư viện đọc `.env`), kèm `variant="swap_letter_case"` hoặc `"trailing_space"`.
- Thư viện đếm số lần sai trong `.phien-dang-nhap/<dự-án>/failure-counter.json`, **cộng dồn** (đăng nhập đúng không đưa về 0), từ chối vượt trần đã khai hoặc khi đang bị chặn (ca thành Không kết luận). Đã chờ hết chặn hoặc chắc hệ thống đã về 0: `python -X utf8 scripts/run_tests.py --reset-failure-counter`.

## Trang kết quả cho cả bộ test case của một tính năng
- Sinh lại: `python -X utf8 scripts/build_report.py build --suite dang-nhap`. Ghi lượt mới: `add-run --suite dang-nhap --build 1.3.0 --results-files <các file result-*.json theo thời gian> --status "14=Bị chặn" --blocked-by "14=BUG-008" --bug "4=BUG-002"` (số là số của mã test case).
- Trang ở `testing/<dự-án>/<tính-năng>/ket-qua-test-case.html` (cùng cách xem như trang smoke, thêm bảng Bug đã mở). Case chưa test được vì bug của case khác ghi `Bị chặn` kèm `--blocked-by`.

## Ảnh kiểm tra xanh/đỏ và video
- Khai `mark_text="chữ trên trang"` ở `ctx.check_main/check_minor` thì ảnh `-kiem.png` có khung **xanh** quanh chữ khi ý đạt, khung **đỏ** khi ý sai (ảnh `-loi.png` chỉ có khung đỏ, dùng cho bug).
- Video quay mọi ca, chỉ giữ ca Không đạt (thư mục `evidence/<dự-án>/chay-test/video/`). Cần cài một lần: `python -m playwright install ffmpeg`. Tắt: `run_tests.py ... --no-video`.
