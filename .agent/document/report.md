# Báo Cáo Tổng Hợp Kiến Trúc & Tính Năng Dự Án

## 1. Tổng Quan Dự Án
Dự án là một hệ thống Web Application với chức năng chính là quản trị (Admin Dashboard) dành cho việc quản lý hoạt động kinh doanh mua bán ô tô. 
- **Framework & Công nghệ**: Python, Flask, Flask-SQLAlchemy (ORM), Flask-Login (Authentication), Flask-Bcrypt (Mã hóa mật khẩu), Flask-WTF (Form & CSRF), Flask-Babel (Đa ngôn ngữ/i18n).
- **Cấu trúc Thư mục**: Áp dụng mô hình **Blueprints** của Flask để chia thành các phần rõ rệt (Admin, Homepage, Utils).

## 2. Tính Năng Chính
Hệ thống cung cấp phần quản trị hoàn chỉnh (Admin Management) với các tính năng:
- **Xác thực và phân quyền (Authentication)**: Đăng nhập, quản lý phiên qua `flask_login`. Đăng ký và phân quyền quản trị viên.
- **Quản lý Ô tô (Car Inventory)**: Trạng thái kinh doanh ô tô, nhãn hiệu xe bán ra, lưu trữ thông tin kỹ thuật và tình trạng xe.
- **Quản lý Khách hàng (Customer Relationship)**: Thông tin liên lạc khách hàng, nguồn từ nền tảng mạng xã hội và ghi chú chăm sóc.
- **Quản lý Giao dịch (Transaction)**: Giao dịch mua bán giữa hệ thống và Khách hàng; trạng thái xử lý đơn hàng (Đặt cọc, Đã thanh toán, ...).
- **Báo cáo Thống kê (Dashboard)**: Thống kê số lượng theo tháng, analytics qua API và biểu diễn trên Admin Dashboard.
- **Đa ngôn ngữ (i18n)**: Ứng dụng tích hợp `Flask-Babel` giúp có thể dịch và thay đổi ngôn ngữ giao diện dựa trên Cookies.

## 3. Các Trang (Pages)
Ứng dụng bao gồm các Blueprint phục vụ Routing như sau:

### Homepage Blueprint (`/`)
- `/`: Trang chủ quảng bá thông tin chung (Public Landing Page).

### Admin Blueprint (`/admin`)
Đòi hỏi quyền truy cập `@login_required` cho toàn bộ các route dưới đây (ngoại trừ trang khởi tạo user lúc đầu nếu cho phép).
- **Dashboard**: `/` hoặc `/dashboard` (Bảng điều khiển và biểu đồ).
- **Cars (Ô tô)**: 
  - `/cars`: Danh sách ô tô (phân tách thẻ Available, Reserved, Unchecked).
  - `/car/new`: Thêm ô tô mới.
  - `/car/<id>`: Cập nhật chi tiết xe.
  - `/car/<id>/delete`: Xóa xe.
  - `/car/<id>/purchase/new`: Tạo nhanh Giao dịch liên kết xe.
- **Customers (Khách hàng)**: 
  - `/customers`: Danh sách khách hàng.
  - `/customer/new`: Thêm khách hàng mới.
  - `/customer/<id>`: Cập nhật thông tin khách hàng.
  - `/customer/<id>/delete`: Xóa khách hàng.
  - `/customer/<id>/purchase/new`: Tạo nhanh Giao dịch liên kết khách hàng.
- **Transactions (Giao dịch)**: 
  - `/transactions`: Danh sách giao dịch.
  - `/transaction/new`: Tạo mới giao dịch (có thể khởi tạo sẵn `customer_id` hoặc `car_id`).
  - `/transaction/<id>`: Xem/Cập nhật trạng thái giao dịch.
  - `/transaction/<id>/delete`: Xóa giao dịch.
- **Users (Tài khoản Quản trị)**:
  - `/users`: Xem tất cả nhân sự/tài khoản admin.
  - `/user/new`: Khởi tạo tài khoản (Register).
  - `/user/<id>`: Chỉnh sửa tài khoản.
  - `/user/<id>/delete`: Xóa tài khoản admin.

## 4. API Endpoints
Ngoài giao diện Server-side rendered (SSR), hệ thống cung cấp sẵn các prefix Blueprint API cho tương tác từ Client (hoặc các tích hợp khác).
- Phía Homepage: `/api/test_home` (GET) -> `{"status": "OK"}`.
- Phía Admin: `/api/test_admin` (GET)-> `{"status": "OK"}`.

## 5. Cấu trúc Hình thái Dữ liệu (Data Structure / Models)
Hệ thống sử dụng **SQLAlchemy** để định nghĩa mô hình Schema DB:

1. **`Configuration`**: Bảng dữ liệu chứa cấu hình dạng Key-Value (vd: cấu hình ngôn ngữ, site info, ...).
2. **`User`**: 
   - Trường dữ liệu: `id`, `username`, `email`, `role`, `password_hash`, `status`, `created_date`.
   - Tính năng: Tích hợp thư viện `UserMixin` phục vụ `login_manager`, mã hóa bằng bcrypt.
3. **`Car`**: 
   - Trường dữ liệu: `id`, `name`, `vin`, `model`, `branch`, `color`, `purchase_price`, `selling_price`, `status` (Sold/Available/Awaiting Delivery), `car_situation` (Refurbished/Not Refurbished...), `license_plate_no`,...
4. **`Customer`**: 
   - Trường dữ liệu: `id`, `name`, `phone`, `gender`, `birth_day`, `facebook`, `address`, `lead_source`, `status`, `note`. 
   - Quan hệ 1:N với bảng `Transaction`.
5. **`Transaction`**: 
   - Trường dữ liệu: `id`, `purchase_date`, `selling_price`, `status` (Deposited/Paid), `note`, `customer_id`.
   - Quan hệ **Nhiều-Nhiều (M:N)** với `Car` thông qua bảng trung gian `transaction_car`.
6. **`transaction_car`**: Bảng Table liên kết giữ `Transaction` và `Car` (Gồm 2 foreign key `transaction_id` và `car_id`).

## 6. Tiện Ích Trợ Trợ (Utilities / Services)
- **`app.utils.constants`**: Định nghĩa Enum trạng thái xe (`CarStatus`, `CarSituation`, `CarBranches`) và trạng thái giao dịch (`TransactionStatus`).
- **`app.admin.services.forms`**: Lớp xử lý validation của các màn CRUD bằng Flask-WTForm.
- **`app.admin.services.create_or_updating`**: Lớp Service bóc tách Logic khởi tạo giao dịch (Xử lý model form).
- **`app.admin.services.analytics`**: Xử lý logic query dữ liệu đưa ra Dashboard.
