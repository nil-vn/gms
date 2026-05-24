# Currency Formatting Locations

Dưới đây là danh sách những vị trí trong template và codebase đang hardcode đơn vị tiền tệ là **"đ"**. Những vị trí này sẽ cần được refactor sau này (ví dụ: tạo và gọi hàm `format_currency()` trong tiện ích Jinja) để hỗ trợ đa ngôn ngữ (i18n).

## 1. Trong trang báo cáo/danh sách Giao dịch (`templates/admin/transactions.html`)
- **Dòng 136:** `{{ "{:,.0f}".format(total_revenue) }} đ` *(Tổng doanh thu)*
- **Dòng 157:** `{{ "{:,.0f}".format(paid_revenue) }} đ` *(Tiền đã thu)*
- **Dòng 178:** `{{ "{:,.0f}".format(deposited_amount) }} đ` *(Tiền đã cọc)*

## 2. Trong trang Chi tiết giao dịch (`templates/admin/transaction_detail.html`)
- **Dòng 165:** `{{ "{:,.0f}".format(transaction.total_other_amount) }} đ` *(Tổng phụ phí)*
- **Dòng 169:** `{{ "{:,.0f}".format(transaction.total_amount) }} đ` *(Tổng cộng)*

## 3. Trong trang Danh sách Xe (`templates/admin/cars.html`)
- **Dòng 65:** `{{ ("{:,.0f}".format(car.selling_price) ~ " đ") if car.selling_price else "-" }}` *(Giá bán của xe)*

## 4. Trong JavaScript file Dashboard (`templates/admin/dashboard.html`)
- **Dòng 137:** `return val.toLocaleString() + " đ";` *(Hiển thị tiền tệ trên biểu đồ trang chủ)*

> Ghi chú: Có thể rút logic format này vào `app/utils` hoặc viết một filter Jinja `format_currency` tuỳ biến theo locales đang áp dụng (VND, JPY, EUR, USD...).
