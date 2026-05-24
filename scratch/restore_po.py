import os
import io

po_file = "lang/translations/vi/LC_MESSAGES/messages.po"
with open(po_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith("#~ "):
        new_lines.append(line[3:]) # Remove '#~ '
    else:
        new_lines.append(line)

new_strings = """
msgid "Awaiting Delivery"
msgstr "Đang chờ giao"

msgid "Refurbished"
msgstr "Sơn sửa rồi"

msgid "Not Refurbished"
msgstr "Chưa sơn sửa"

msgid "Refurbished/Pending Cleaning"
msgstr "Sơn sửa rồi - chờ vệ sinh"

msgid "Available (inc. Awaiting)"
msgstr "Có sẵn (Giao ngay + Đang chờ)"

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

"""

new_lines.append(new_strings)

with open(po_file, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Restored and appended new strings to messages.po")
