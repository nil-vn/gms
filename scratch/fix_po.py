import os

file_path = "lang/translations/vi/LC_MESSAGES/messages.po"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find the index of line containing "Available (inc. Awaiting)"
idx = -1
for i, line in enumerate(lines):
    if 'msgid "Available (inc. Awaiting)"' in line:
        idx = i
        break

if idx != -1:
    # Keep lines up to and including the msgid
    new_lines = lines[:idx+1]
    
    # Append the rest
    appends = """msgstr "Có sẵn (Giao ngay + Đang chờ)"

msgid "Sold"
msgstr "Đã bán"

msgid "Deposited"
msgstr "Đã cọc"

msgid "Paid"
msgstr "Đã thanh toán"

msgid "Deposit"
msgstr "Tiền cọc"

msgid "Deposit Amount"
msgstr "Tiền cọc"

msgid "Other Transaction"
msgstr "Giao dịch khác"

msgid "Total Amount"
msgstr "Tổng cộng"

msgid "Other Transactions (Accessories/Services)"
msgstr "Giao dịch khác (Phụ kiện/Dịch vụ tùy chọn)"

msgid "Accessory/Service Name"
msgstr "Tên phụ kiện/Dịch vụ"

msgid "Price"
msgstr "Giá tiền"

msgid "Add Item"
msgstr "Thêm dịch vụ"

msgid "Situation"
msgstr "Tình trạng xe"

msgid "Revenue (Last 6 Months)"
msgstr "Doanh thu (6 tháng gần nhất)"

msgid "Car Status Distribution"
msgstr "Phân bố trạng thái xe"

msgid "Search..."
msgstr "Tìm kiếm..."

msgid "{select} entries per page"
msgstr "{select} dòng / trang"

msgid "No entries found"
msgstr "Không có dữ liệu"

msgid "Showing {start} to {end} of {rows} entries"
msgstr "Hiển thị {start} đến {end} của {rows} dòng"

msgid "Total Cars"
msgstr "Tổng số xe"

msgid "units"
msgstr "chiếc"

msgid "Available Cars"
msgstr "Xe sẵn sàng"

msgid "ready"
msgstr "sẵn sàng"

msgid "Sold Cars"
msgstr "Xe đã bán"

msgid "delivered"
msgstr "đã bán"

msgid "Total Customers"
msgstr "Tổng khách hàng"

msgid "profiles"
msgstr "hồ sơ"

msgid "Active Customers"
msgstr "Khách đã giao dịch"

msgid "with purchases"
msgstr "có giao dịch"

msgid "Potential Leads"
msgstr "Khách tiềm năng"

msgid "no purchases yet"
msgstr "chưa giao dịch"

msgid "Total Revenue"
msgstr "Tổng doanh thu"

msgid "estimated"
msgstr "ước tính"

msgid "Paid Revenue"
msgstr "Thực thu"

msgid "collected"
msgstr "đã thu"

msgid "holding"
msgstr "đang cọc"

msgid "Total Users"
msgstr "Tổng người dùng"

msgid "accounts"
msgstr "tài khoản"

msgid "Admin Users"
msgstr "Quản trị viên"

msgid "managers"
msgstr "quản lý"

msgid "Staff/Members"
msgstr "Nhân viên"

msgid "employees"
msgstr "nhân sự"
"""
    new_lines.append(appends)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print("Fixed vi messages.po")
else:
    print("Could not find the hook line.")
