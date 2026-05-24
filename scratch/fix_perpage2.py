"""
Fix the perPage label in all admin templates.
simple-datatables puts the SELECT element BEFORE the perPage label text.
So perPage should just be the suffix text: "dòng / trang" (not "{select} dòng / trang").
"""
import glob, re

files = glob.glob('templates/admin/*.html')

# We need to look for the labels block and ADD perPage back correctly
# Current pattern (after removing it): labels block has placeholder, noRows, info
# We need to insert perPage: "{{ _('entries per page') }}" back in

old = '''            labels: {
                placeholder: "{{ _('Search...') }}",
                noRows: "{{ _('No entries found') }}",
                info: "{{ _('Showing {start} to {end} of {rows} entries') }}"
            }'''

new = '''            labels: {
                placeholder: "{{ _('Search...') }}",
                perPage: "{{ _('entries per page') }}",
                noRows: "{{ _('No entries found') }}",
                info: "{{ _('Showing {start} to {end} of {rows} entries') }}"
            }'''

for f in files:
    with open(f, encoding='utf-8') as fh:
        content = fh.read()
    
    if old not in content:
        print(f"SKIP (not found): {f}")
        continue
        
    new_content = content.replace(old, new)
    
    with open(f, 'w', encoding='utf-8') as fh:
        fh.write(new_content)
    
    print(f"Fixed: {f}")

print("Done.")
