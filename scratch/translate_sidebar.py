import re, base64, json

vi_b64 = "ewogICJEYXNoYm9hcmQiOiAiQuG6o25nIMSRaeG7gXUga2hp4buDbiIsCiAgIk5hdmlnYXRpb24iOiAixJBp4buBdSBoxrDhu5tuZyIsCiAgIkNhciBNYW5hZ2VtZW50IjogIlF14bqnbiBsw70geGUiLAogICJDYXIgTGlzdCI6ICJEYW5oIHPDoWNoIHhlIiwKICAiQ3VzdG9tZXIgTWFuYWdlbWVudCI6ICJRdeG6o24gbMO9IGtow6FjaIGow6BuZyIsCiAgIkN1c3RvbWVycyI6ICJLaMOhY2ggaMOgbmciLAogICJTYWxlIE1hbmFnZW1lbnQiOiAiUXXhuqNuIGzDvSBiw6FuIGjDoG5nIiwKICAiVHJhbnNhY3Rpb25zIjogIkdpYW8gZOG7i2NoIiwKICAiQWRkIFRyYW5zYWN0aW9uIjogIlRow6ptIGdpYW8gZOG7i2NoIiwKICAiU2V0dGluZyI6ICJDw6BpIMSR4bqjdCIsCiAgIlVzZXIgTWFuYWdlbWVudCI6ICJRdeG6o24gbMO9IG5nxrDhu51pIGTDuW5nIiwKICAiVXNlcnMiOiAiTmfGsOG7nWkgZMO5bmciLAogICJTeXN0ZW0iOiAiSOG7hyB0aOG7kW5nIgp9"
ja_b64 = "ewogICJEYXNoYm9hcmQiOiAi44OA44OD44K344Ol44Oc44O844OJIiwKICAiTmF2aWdhdGlvbiI6ICLjg4rjg5Pjggrjg7zjgrfjg6fjg7MiLAogICJDYXIgTWFuYWdlbWVudCI6ICLoi4HkuKHnrqHnkIYiLAogICJDYXIgTGlzdCI6ICLoi4HkuKHkuIDopqciLAogICJDdXN0b21lciBNYW5hZ2VtZW50IjogIuWupuaIkeeuoeeQhiIsCiAgIkN1c3RvbWVycyI6ICLlrqbmiIEiLAogICJTYWxlIE1hbmFnZW1lbnQiOiAi6Lca5LiK566h55CGIiwKICAiVHJhbnNhY3Rpb25zIjogIuWPluW8lSIsCiAgIkFkZCBUcmFuc2FjdGlvbiI6ICLlI5blvJXjgpLoj73liqAiLAogICJTZXR0aW5nIjogIuioreWumuIsCiAgIlVzZXIgTWFuYWdlbWVudCI6ICLjg6bjg7zjgrbmnKznrqHnkIYiLAogICJVc2VycyI6ICLjg6bjg7zjgrbmiIEiLAogICJTeXN0ZW0iOiAi44K344K544OG44OgIgp9"

vi_dict = json.loads(base64.b64decode(vi_b64).decode('utf-8'))
ja_dict = json.loads(base64.b64decode(ja_b64).decode('utf-8'))

def translate_po(file_path, translation_dict):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for i in range(len(lines) - 1):
        if lines[i].startswith('msgid "'):
            msgid_match = re.search(r'^msgid "(.*)"', lines[i])
            if msgid_match:
                msgid = msgid_match.group(1)
                # Thay thế các msgstr đã có hoặc rỗng
                if lines[i+1].startswith('msgstr "'):
                    translated = translation_dict.get(msgid)
                    if translated:
                        lines[i+1] = f'msgstr "{translated}"\n'

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

translate_po('lang/translations/vi/LC_MESSAGES/messages.po', vi_dict)
translate_po('lang/translations/ja/LC_MESSAGES/messages.po', ja_dict)
print("Updated sidebar translations.")
