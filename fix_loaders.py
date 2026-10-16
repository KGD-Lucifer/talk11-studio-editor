import re

def fix_image_loaders(content):
    # Fix createImageLoader and remove crossOrigin = 'anonymous' which breaks file:///
    old_loader_pattern = r'function createImageLoader\(primaryPath, fallbackPath\) \{[\s\S]*?const imgTalk11Full = createImageLoader\([^\)]+\);'
    
    new_loader_block = '''function createImageLoader(...candidatePaths) {
      const img = new Image();
      let pathIdx = 0;
      
      function tryLoad() {
        if (pathIdx < candidatePaths.length) {
          img.src = candidatePaths[pathIdx++];
        } else {
          img._failed = true;
        }
      }

      img.onload = () => {
        img._loaded = true;
      };

      img.onerror = () => {
        tryLoad();
      };

      tryLoad();
      if (img.complete && img.naturalWidth > 0) {
        img._loaded = true;
      }
      return img;
    }

    const imgStudioCyber = createImageLoader(
      '03_ASSETS/Studio_Backgrounds/studio_cyber_neon.jpg',
      '../03_ASSETS/Studio_Backgrounds/studio_cyber_neon.jpg',
      '../../03_ASSETS/Studio_Backgrounds/studio_cyber_neon.jpg',
      '../Studio_Backgrounds/studio_cyber_neon.jpg'
    );
    const imgTopicHistory = createImageLoader(
      '03_ASSETS/Studio_Backgrounds/topic_vietnam_history.jpg',
      '../03_ASSETS/Studio_Backgrounds/topic_vietnam_history.jpg',
      '../../03_ASSETS/Studio_Backgrounds/topic_vietnam_history.jpg',
      '../Studio_Backgrounds/topic_vietnam_history.jpg'
    );
    const imgTopicScience = createImageLoader(
      '03_ASSETS/Studio_Backgrounds/topic_science_space.jpg',
      '../03_ASSETS/Studio_Backgrounds/topic_science_space.jpg',
      '../../03_ASSETS/Studio_Backgrounds/topic_science_space.jpg',
      '../Studio_Backgrounds/topic_science_space.jpg'
    );
    const imgTopicBreaking = createImageLoader(
      '03_ASSETS/Studio_Backgrounds/intro_breaking_news.jpg',
      '../03_ASSETS/Studio_Backgrounds/intro_breaking_news.jpg',
      '../../03_ASSETS/Studio_Backgrounds/intro_breaking_news.jpg',
      '../Studio_Backgrounds/intro_breaking_news.jpg'
    );
    const imgHistoryGold = createImageLoader(
      '03_ASSETS/Studio_Backgrounds/studio_history_gold.jpg',
      '../03_ASSETS/Studio_Backgrounds/studio_history_gold.jpg',
      '../../03_ASSETS/Studio_Backgrounds/studio_history_gold.jpg',
      '../Studio_Backgrounds/studio_history_gold.jpg'
    );
    const imgHistoryBlue = createImageLoader(
      '03_ASSETS/Studio_Backgrounds/studio_history_blue.jpg',
      '../03_ASSETS/Studio_Backgrounds/studio_history_blue.jpg',
      '../../03_ASSETS/Studio_Backgrounds/studio_history_blue.jpg',
      '../Studio_Backgrounds/studio_history_blue.jpg'
    );
    const imgDocReport = createImageLoader(
      '03_ASSETS/Studio_Backgrounds/studio_documentary_report.jpg',
      '../03_ASSETS/Studio_Backgrounds/studio_documentary_report.jpg',
      '../../03_ASSETS/Studio_Backgrounds/studio_documentary_report.jpg',
      '../Studio_Backgrounds/studio_documentary_report.jpg'
    );
    const imgTalk11Full = createImageLoader(
      '01_TALK11_Broadcast_16x9_Full.png',
      '../01_TALK11_Broadcast_16x9_Full.png',
      '../../01_TALK11_Broadcast_16x9_Full.png'
    );'''

    content = re.sub(old_loader_pattern, new_loader_block, content)

    # In render function: ensure background image checks .complete && naturalWidth > 0
    content = re.sub(
        r'if \(imgStudioCyber && imgStudioCyber\._loaded\)',
        'if (imgStudioCyber && (imgStudioCyber._loaded || (imgStudioCyber.complete && imgStudioCyber.naturalWidth > 0)))',
        content
    )

    # In drawWallGalleryScreens: ensure hasDim checks .complete && naturalWidth > 0
    content = re.sub(
        r'const hasDim = isVid \? \(media\.videoWidth > 0 \|\| media\.readyState >= 2\) : \(media\.naturalWidth > 0 \|\| media\.width > 0\);',
        'const hasDim = isVid ? (media.videoWidth > 0 || media.readyState >= 2) : (media._loaded || (media.complete && media.naturalWidth > 0) || media.width > 0);',
        content
    )

    return content

files = [
    'Tao_Khung_Thoi_Su_Talk11.html',
    'Tao_Intro_Va_Studio_Thoi_Su_Talk11.html',
    'TALK11_Community_Antigravity/Tao_Khung_Thoi_Su_Talk11.html',
    'TALK11_Community_Antigravity/Tao_Intro_Va_Studio_Thoi_Su_Talk11.html',
    'TALK11_Community_Antigravity/03_ASSETS/VTV_TALK11_CAPCUT_FRAMES/Tao_Khung_Thoi_Su_Talk11.html',
    'TALK11_Community_Antigravity/03_ASSETS/VTV_TALK11_CAPCUT_FRAMES/Tao_Intro_Va_Studio_Thoi_Su_Talk11.html',
    'VIDEO_KHUNG_THOI_SU_CAPCUT/Tao_Khung_Thoi_Su_Talk11.html',
    'VIDEO_KHUNG_THOI_SU_CAPCUT/Tao_Intro_Va_Studio_Thoi_Su_Talk11.html',
]

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        orig = file.read()
    fixed = fix_image_loaders(orig)
    with open(f, 'w', encoding='utf-8') as file:
        file.write(fixed)
    print(f"Fixed image loader in {f} ({len(fixed)} bytes)")
