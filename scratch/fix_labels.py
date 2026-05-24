"""
Fix the DataTable labels in all admin templates.
The issue is that {start}, {end}, {rows} inside _() Jinja calls
are interpreted as Jinja format variables and become empty strings.
We need to wrap them in {% raw %} blocks or use literal JS strings.
"""
import glob

files = glob.glob('templates/admin/*.html')

# The broken pattern (Jinja eats {start} etc)
old_labels = """            labels: {
                placeholder: "{{ _('Search...') }}",
                noRows: "{{ _('No entries found') }}",
                info: "{{ _('Showing {start} to {end} of {rows} entries') }}"
            }"""

# Fixed: use raw block for the info line to prevent Jinja from eating placeholders
new_labels = """            labels: {
                placeholder: "{{ _('Search...') }}",
                noRows: "{{ _('No entries found') }}",
                info: "{% raw %}Showing {start} to {end} of {rows} entries{% endraw %}"
            }"""

count = 0
for f in files:
    with open(f, encoding='utf-8') as fh:
        content = fh.read()
    
    if old_labels not in content:
        continue
    
    new_content = content.replace(old_labels, new_labels)
    with open(f, 'w', encoding='utf-8') as fh:
        fh.write(new_content)
    count += 1
    print(f"Fixed: {f}")

print(f"Done. Fixed {count} file(s).")
