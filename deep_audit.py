import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('Tao_Khung_Thoi_Su_Talk11.html', 'r', encoding='utf-8') as f:
    text = f.read()

print("=== STUDENT VIDEO UPLOAD & PROCESSING ===")
matches = list(re.finditer(r'inputStudentVideo|handleStudentVideo|saveStudentVideoToStorage', text))
for m in matches:
    line_no = text[:m.start()].count('\n') + 1
    print(f'Line {line_no}: {text[max(0, m.start()-20):min(len(text), m.end()+80)].strip()}')
