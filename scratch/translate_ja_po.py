import os, time, re
from deep_translator import GoogleTranslator

file_path = r'lang\translations\ja\LC_MESSAGES\messages.po'

if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    exit(1)

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

translator = GoogleTranslator(source='en', target='ja')

print("Translating msgid to Japanese...")
translated_count = 0

for i in range(len(lines) - 1):
    if lines[i].startswith('msgid "'):
        msgid_match = re.search(r'^msgid "(.*)"', lines[i])
        if msgid_match:
            msgid = msgid_match.group(1)
            # if msgid is empty (header), skip
            if not msgid:
                continue
            
            # Find the next line which should be msgstr
            if lines[i+1].startswith('msgstr "'):
                try:
                    translated_text = translator.translate(msgid)
                    # Escape quotes just in case
                    safe_trans = translated_text.replace('"', '\\"')
                    lines[i+1] = f'msgstr "{safe_trans}"\n'
                    translated_count += 1
                    
                    # Sleep slightly to avoid rate limit
                    if translated_count % 20 == 0:
                        print(f"Translated {translated_count} terms...")
                        time.sleep(1)
                except Exception as e:
                    print(f"Error translating '{msgid}': {e}")

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"Done! Successfully translated {translated_count} terms.")
