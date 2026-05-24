"""
Fix the broken {select} perPage label in all admin templates.
simple-datatables renders the perPage label via innerText so the {select} placeholder
literally appears as text. The fix is to remove the perPage label entirely (the library
will still render the dropdown, without the extra translated label).
"""
import glob, re

files = glob.glob('templates/admin/*.html')

# Match the perPage line
perpage_pattern = re.compile(r"\s*perPage: \"[^\"]*\",\n")

for f in files:
    with open(f, encoding='utf-8') as fh:
        content = fh.read()
    
    if 'perPage' not in content:
        continue
        
    new_content = perpage_pattern.sub('\n', content)
    
    with open(f, 'w', encoding='utf-8') as fh:
        fh.write(new_content)
    
    print(f"Fixed: {f}")

print("Done.")
