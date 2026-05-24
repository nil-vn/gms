import sys

def process(filepath):
    lines = open(filepath, 'r', encoding='utf-8').read().splitlines()
    seen_msgid = {}
    current_msgid = None
    msgids_to_fix = []
    
    with open('check_po_result.txt', 'a', encoding='utf-8') as f:
        f.write(f"--- Parsing {filepath} ---\n")
        for i, line in enumerate(lines):
            if line.startswith('msgid '):
                current_msgid = line[6:]
                if current_msgid not in seen_msgid:
                    seen_msgid[current_msgid] = []
                seen_msgid[current_msgid].append(i + 1)
            elif line.startswith('msgstr ""') and len(line) == 9:
                if current_msgid and current_msgid != '""':
                    msgids_to_fix.append((current_msgid, i + 1))
                    
        for msgid, occur in seen_msgid.items():
            if len(occur) > 1 and msgid != '""':
                f.write(f"DUPLICATE FOUND: {msgid} at lines {occur}\n")
                
        for msgid, lineno in msgids_to_fix:
            f.write(f"EMPTY MSGSTR: {msgid} at line {lineno}\n")

with open('check_po_result.txt', 'w', encoding='utf-8') as f:
    f.write("")
process('lang/translations/vi/LC_MESSAGES/messages.po')
process('lang/translations/ja/LC_MESSAGES/messages.po')
