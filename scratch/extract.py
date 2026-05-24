import re
import json

lines = open('lang/translations/vi/LC_MESSAGES/messages.po', encoding='utf-8').read().split('\n')
missing = []
for i in range(len(lines) - 1):
    if lines[i].startswith('msgid "') and lines[i+1].startswith('msgstr ""'):
        msgid = re.search(r'^msgid "(.*)"', lines[i])
        if msgid and msgid.group(1):
            missing.append(msgid.group(1))

print(json.dumps(missing, ensure_ascii=False, indent=2))
