import os

messages = {
    "vi": {
        "System Settings": "Cài đặt hệ thống",
        "Currency": "Tiền tệ",
        "Theme": "Giao diện",
        "Language": "Ngôn ngữ",
        "Save Changes": "Lưu thay đổi",
    },
    "ja": {
        "System Settings": "システム設定",
        "Currency": "通貨",
        "Theme": "テーマ",
        "Language": "言語",
        "Save Changes": "変更を保存",
    }
}

for lang, trans in messages.items():
    path = f"lang/translations/{lang}/LC_MESSAGES/messages.po"
    with open(path, "a", encoding="utf-8") as f:
        f.write("\n")
        for k, v in trans.items():
            f.write(f'msgid "{k}"\nmsgstr "{v}"\n\n')

print("Done appending messages.")
