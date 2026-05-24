"""Add 'entries per page' translations to vi and ja locales."""

# Vietnamese
content = open('lang/translations/vi/LC_MESSAGES/messages.po', encoding='utf-8').read()
if 'entries per page' not in content:
    content = content.rstrip() + '\n\nmsgid "entries per page"\nmsgstr "d\u00f2ng / trang"\n'
    open('lang/translations/vi/LC_MESSAGES/messages.po', 'w', encoding='utf-8').write(content)
    print('vi: added')
else:
    print('vi: already present')

# Japanese
content = open('lang/translations/ja/LC_MESSAGES/messages.po', encoding='utf-8').read()
if 'entries per page' not in content:
    content = content.rstrip() + '\n\nmsgid "entries per page"\nmsgstr "\u4ef6\uff0f\u30da\u30fc\u30b8"\n'
    open('lang/translations/ja/LC_MESSAGES/messages.po', 'w', encoding='utf-8').write(content)
    print('ja: added')
else:
    print('ja: already present')
