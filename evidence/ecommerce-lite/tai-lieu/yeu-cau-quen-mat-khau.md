# Requirement: Chức năng Quên mật khẩu (bản gốc, người dùng dán trong chat 2026-11-20)

Mô tả: Người dùng có thể đặt lại mật khẩu khi quên mật khẩu đăng nhập.

* Người dùng nhập địa chỉ email đã đăng ký tài khoản để yêu cầu đặt lại mật khẩu.
* Hệ thống gửi mã OTP gồm 6 chữ số đến email đã đăng ký. OTP có hiệu lực trong 5 phút.
* Người dùng nhập đúng OTP còn hiệu lực thì được chuyển đến màn hình tạo mật khẩu mới.
* Mật khẩu mới phải có từ 8 đến 16 ký tự, bao gồm chữ hoa, chữ thường, số và ký tự đặc biệt.
* Mật khẩu mới không được trùng với 5 mật khẩu gần nhất.
* Sau khi đổi mật khẩu thành công, hệ thống hiển thị thông báo thành công và yêu cầu người dùng đăng nhập lại.
