import re

vi_dict = {
  "1 Year": "1 Năm",
  "File too large (max 2 MB)": "Tệp quá lớn (tối đa 2 MB)",
  "Remove logo and reset to default?": "Xóa logo và đặt về mặc định?",
  "Link copied to clipboard!": "Đã sao chép liên kết!",
  "Brand & Identity": "Thương hiệu & Giao diện",
  "Remove Logo": "Xóa Logo",
  "e.g. Gemini": "VD: Gemini",
  "Displayed next to the logo in the sidebar.": "Hiển thị kế logo trên thanh bên.",
  "Upload Logo": "Tải lên Logo",
  "Localhost": "Localhost (Máy chủ cục bộ)",
  "No files uploaded yet.": "Chưa có file nào được tải lên."
}

ja_dict = {
  "1 Year": "1年",
  "File too large (max 2 MB)": "ファイルが大きすぎます (最大 2 MB)",
  "Remove logo and reset to default?": "ロゴを削除してデフォルトにリセットしますか？",
  "Link copied to clipboard!": "リンクをクリップボードにコピーしました！",
  "Brand & Identity": "ブランドとアイデンティティ",
  "Remove Logo": "ロゴを削除",
  "e.g. Gemini": "例: Gemini",
  "Displayed next to the logo in the sidebar.": "サイドバーのロゴの横に表示されます。",
  "Upload Logo": "ロゴをアップロード",
  "Localhost": "ローカルホスト",
  "No files uploaded yet.": "ファイルはまだアップロードされていません。"
}

def translate_po(file_path, translation_dict):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for i in range(len(lines) - 1):
        if lines[i].startswith('msgid "'):
            msgid_match = re.search(r'^msgid "(.*)"', lines[i])
            if msgid_match:
                msgid = msgid_match.group(1)
                
                # Check for empty msgstr on the next line
                if lines[i+1].startswith('msgstr ""\n'):
                    # Match exact string or try to find a matching prefix (for special chars)
                    translated = translation_dict.get(msgid)
                    if not translated:
                        # Fallback for the em-dash string
                        if "Accepted: PNG, JPG, SVG, WEBP" in msgid:
                            if "vi" in file_path:
                                translated = "Hỗ trợ: PNG, JPG, SVG, WEBP tối đa 2 MB. Khuyến nghị: 250x60px."
                            else:
                                translated = "対応: PNG, JPG, SVG, WEBP 最大 2 MB。推奨: 250x60px."
                    
                    if translated:
                        lines[i+1] = f'msgstr "{translated}"\n'

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

translate_po('lang/translations/vi/LC_MESSAGES/messages.po', vi_dict)
translate_po('lang/translations/ja/LC_MESSAGES/messages.po', ja_dict)
print("Updated .po files.")
