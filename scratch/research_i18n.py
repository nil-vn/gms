import os, re, json, glob

def get_html_i18n_keys():
    keys = set()
    # Tìm tất cả file html trong thư mục templates
    for filepath in glob.glob('templates/**/*.html', recursive=True):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                # Match {{ _('Text') }}, {{ _("Text") }}
                matches = re.findall(r"_\(\s*['\"](.*?)['\"]\s*\)", content)
                for m in matches:
                    keys.add(m)
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
    return keys

def get_pot_keys():
    keys = set()
    try:
        with open('messages.pot', 'r', encoding='utf-8') as f:
            content = f.read()
            matches = re.findall(r'^msgid "(.*)"', content, re.MULTILINE)
            for m in matches:
                if m != "":
                    keys.add(m)
    except:
        pass
    return keys

def get_po_keys(lang):
    keys = set()
    po_path = f'lang/translations/{lang}/LC_MESSAGES/messages.po'
    if not os.path.exists(po_path): return keys
    try:
        with open(po_path, 'r', encoding='utf-8') as f:
            content = f.read()
            matches = re.findall(r'^msgid "(.*)"', content, re.MULTILINE)
            for m in matches:
                if m != "":
                    keys.add(m)
    except:
        pass
    return keys

html_keys = get_html_i18n_keys()
pot_keys = get_pot_keys()
vi_keys = get_po_keys('vi')
ja_keys = get_po_keys('ja')

print(f"Total HTML Keys: {len(html_keys)}")
print(f"Total POT Keys: {len(pot_keys)}")
print(f"Total VI PO Keys: {len(vi_keys)}")
print(f"Total JA PO Keys: {len(ja_keys)}")

missing_in_pot = html_keys - pot_keys
print(f"Missing in POT: {len(missing_in_pot)}")
if len(missing_in_pot) > 0:
    print(list(missing_in_pot)[:10])

missing_in_vi = html_keys - vi_keys
print(f"Missing in VI PO: {len(missing_in_vi)}")

missing_in_ja = html_keys - ja_keys
print(f"Missing in JA PO: {len(missing_in_ja)}")

# Luu file missing de reference
with open('scratch/missing_i18n.json', 'w', encoding='utf-8') as f:
    json.dump({
        "html_keys": list(html_keys),
        "missing_in_pot": list(missing_in_pot),
        "missing_in_vi": list(missing_in_vi)
    }, f, ensure_ascii=False, indent=2)
