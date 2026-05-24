import json, os, time
from deep_translator import GoogleTranslator
import re

print("Starting deep-translation sync process...")

# Load keys
with open('scratch/missing_i18n.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    keys = data['html_keys']

# Các key đã dịch cứng (hardcode map) để đảm bảo không bị lệch
hardcode_vi = {
  "Dashboard": "Bảng điều khiển", "Navigation": "Điều hướng",
  "Car Management": "Quản lý xe", "Car List": "Danh sách xe",
  "Customer Management": "Quản lý khách hàng", "Customers": "Khách hàng",
  "Sale Management": "Quản lý bán hàng", "Transactions": "Giao dịch", "Add Transaction": "Thêm giao dịch",
  "Setting": "Cài đặt", "User Management": "Quản lý người dùng", "Users": "Người dùng", "System": "Hệ thống",
  "System Settings": "Cài đặt Hệ thống", "Current Logo": "Logo hiện tại", "System Name": "Tên Hệ thống"
}

vi_translator = GoogleTranslator(source='en', target='vi')
ja_translator = GoogleTranslator(source='en', target='ja')

vi_dict = {}
ja_dict = {}
en_dict = {}

print(f"Translating {len(keys)} keys...")
for i, key in enumerate(keys):
    en_dict[key] = key
    # VI
    if key in hardcode_vi:
        vi_dict[key] = hardcode_vi[key]
    else:
        try:
            vi_dict[key] = vi_translator.translate(key)
        except Exception as e:
            vi_dict[key] = key
    
    # JA
    try:
        ja_dict[key] = ja_translator.translate(key)
    except Exception as e:
        ja_dict[key] = key

    if i % 20 == 0:
        print(f"Progress: {i}/{len(keys)}")
        time.sleep(1) # tránh rate limit

# Ghi ra Frontend locales JSON
os.makedirs('static/json/locales', exist_ok=True)
with open('static/json/locales/vi.json', 'w', encoding='utf-8') as f:
    json.dump(vi_dict, f, ensure_ascii=False, indent=2)
with open('static/json/locales/ja.json', 'w', encoding='utf-8') as f:
    json.dump(ja_dict, f, ensure_ascii=False, indent=2)
with open('static/json/locales/en.json', 'w', encoding='utf-8') as f:
    json.dump(en_dict, f, ensure_ascii=False, indent=2)

print("Generated frontend JSON locales.")

# Update messages.po
def translate_po(file_path, translation_dict):
    if not os.path.exists(file_path): return
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for i in range(len(lines) - 1):
        if lines[i].startswith('msgid "'):
            msgid_match = re.search(r'^msgid "(.*)"', lines[i])
            if msgid_match:
                msgid = msgid_match.group(1)
                # Thay thế các msgstr
                if lines[i+1].startswith('msgstr "'):
                    translated = translation_dict.get(msgid)
                    if translated:
                        # Tranh ngoac kep loi
                        safe_trans = translated.replace('"', '\\"')
                        lines[i+1] = f'msgstr "{safe_trans}"\n'

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

translate_po('lang/translations/vi/LC_MESSAGES/messages.po', vi_dict)
translate_po('lang/translations/ja/LC_MESSAGES/messages.po', ja_dict)

print("Updated .po files. Sync Complete!")
