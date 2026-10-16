import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('Tao_Khung_Thoi_Su_Talk11.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Extract all IDs in HTML
html_ids = set(re.findall(r'id=["\']([a-zA-Z0-9_\-]+)["\']', content))
print(f'Total unique IDs found in HTML: {len(html_ids)}')

# 2. Extract getElementById calls
js_ids = set(re.findall(r'getElementById\(["\']([a-zA-Z0-9_\-]+)["\']\)', content))
print(f'Total getElementById calls: {len(js_ids)}')

missing_in_html = js_ids - html_ids
print(f'IDs queried in JS but MISSING in HTML: {len(missing_in_html)}')
for mid in sorted(missing_in_html):
    for line_idx, line in enumerate(content.splitlines()):
        if f"getElementById('{mid}')" in line or f'getElementById("{mid}")' in line:
            print(f'   MISSING ID: {mid} at line {line_idx+1}: {line.strip()[:100]}')
