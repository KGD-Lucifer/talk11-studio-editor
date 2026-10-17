import os
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))
if not os.path.exists(os.path.join(base_dir, 'Tao_Khung_Thoi_Su_Talk11.html')):
    parent_dir = os.path.abspath(os.path.join(base_dir, '..'))
    if os.path.exists(os.path.join(parent_dir, 'Tao_Khung_Thoi_Su_Talk11.html')):
        base_dir = parent_dir

src_file = os.path.join(base_dir, 'Tao_Khung_Thoi_Su_Talk11.html')
if not os.path.exists(src_file):
    print(f"[X] Khong tim thay file goc: {src_file}")
    sys.exit(1)

with open(src_file, 'r', encoding='utf-8') as f:
    content = f.read()

targets = [
    os.path.join(base_dir, 'Tao_Intro_Va_Studio_Thoi_Su_Talk11.html'),
    os.path.join(base_dir, 'TALK11_Community_Antigravity', 'Tao_Khung_Thoi_Su_Talk11.html'),
    os.path.join(base_dir, 'TALK11_Community_Antigravity', 'Tao_Intro_Va_Studio_Thoi_Su_Talk11.html'),
    os.path.join(base_dir, 'TALK11_Community_Antigravity', '03_ASSETS', 'VTV_TALK11_CAPCUT_FRAMES', 'Tao_Khung_Thoi_Su_Talk11.html'),
    os.path.join(base_dir, 'TALK11_Community_Antigravity', '03_ASSETS', 'VTV_TALK11_CAPCUT_FRAMES', 'Tao_Intro_Va_Studio_Thoi_Su_Talk11.html'),
    os.path.join(base_dir, 'VIDEO_KHUNG_THOI_SU_CAPCUT', 'Tao_Khung_Thoi_Su_Talk11.html'),
    os.path.join(base_dir, 'VIDEO_KHUNG_THOI_SU_CAPCUT', 'Tao_Intro_Va_Studio_Thoi_Su_Talk11.html'),
    os.path.join(base_dir, 'TALK11_News_Studio_v2.1.0_Enhanced.html'),
]

synced = 0
for t in targets:
    if os.path.exists(os.path.dirname(t)):
        with open(t, 'w', encoding='utf-8') as out:
            out.write(content)
        print(f"[OK] Da dong bo: {t}")
        synced += 1

print(f"\n=> Hoan tat dong bo {synced} file HTML!")
