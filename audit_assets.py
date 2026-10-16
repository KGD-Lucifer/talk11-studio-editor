import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('Tao_Khung_Thoi_Su_Talk11.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all relative file paths ending in .mp4, .png, .jpg, .jpeg, .mp3, .wav, .svg, .js, .wasm
potential_paths = set(re.findall(r'[\'"]([a-zA-Z0-9_\-\.\/]+\.(?:mp4|webm|png|jpg|jpeg|gif|mp3|wav|svg|wasm|tflite|binarypb))[\'"]', content))

print(f'Total asset paths referenced: {len(potential_paths)}')
missing_paths = []
existing_paths = []

for p in sorted(potential_paths):
    # ignore http/https
    if p.startswith('http://') or p.startswith('https://'):
        continue
    # resolve relative path
    full_path = os.path.normpath(os.path.join(os.getcwd(), p))
    if not os.path.exists(full_path):
        missing_paths.append(p)
    else:
        existing_paths.append(p)

print(f'\nExisting assets ({len(existing_paths)}):')
for p in existing_paths[:10]:
    print(f'  ✓ {p}')
if len(existing_paths) > 10:
    print(f'  ... and {len(existing_paths)-10} more')

print(f'\nMISSING assets referenced in code ({len(missing_paths)}):')
for p in missing_paths:
    print(f'  ✗ {p}')
