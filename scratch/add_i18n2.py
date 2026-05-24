messages = {
    "vi": {"Settings saved successfully!": "Lưu cài đặt thành công!", "Light": "Sáng", "Dark": "Tối"},
    "ja": {"Settings saved successfully!": "設定が正常に保存されました！", "Light": "ライト", "Dark": "ダーク"},
}
for lang, trans in messages.items():
    path = f"lang/translations/{lang}/LC_MESSAGES/messages.po"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    additions = ""
    for k, v in trans.items():
        if f'msgid "{k}"' not in content:
            additions += f'\nmsgid "{k}"\nmsgstr "{v}"\n'
    if additions:
        with open(path, "a", encoding="utf-8") as f:
            f.write(additions)
print("Done")
