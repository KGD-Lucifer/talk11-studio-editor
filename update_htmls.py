import re

# 12 Wall Screens definition
new_wall_screens_code = '''    // ----------------------------------------------------
    // 12 GALLERY SCREENS — KHỚP CHUẨN 100% VỊ TRÍ ẢNH CÓ SẴN TRÊN 2 BÊN TƯỜNG
    // studio_cyber_neon.jpg có sẵn các khung ảnh quân đội/lịch sử ở cả 2 bên tường.
    // 12 wallScreens này overlay chuẩn xác từng pixel theo đúng góc nghiêng 3D phối cảnh.
    // BTV có thể thay ảnh/video mới vào bất kỳ khung nào qua sidebar bên trái.
    // Canvas: 1920 × 1080px
    // ----------------------------------------------------
    let wallScreens = [
      // ============================================================
      // TƯỜNG TRÁI — 6 KHUNG (Khớp chuẩn 100% vị trí ảnh có sẵn trên tường trái)
      // ============================================================
      {
        id: 'wall_1',
        name: '#1 Trái-Trên-Vòm (CỜ TỔ QUỐC)',
        label: 'VIỆT NAM',
        mediaType: 'image',
        mediaElement: imgHistoryGold,
        thumbUrl: '03_ASSETS/Studio_Backgrounds/studio_history_gold.jpg',
        p0: { x: 95, y: 120 },
        p1: { x: 395, y: 220 },
        p2: { x: 355, y: 345 },
        p3: { x: 80, y: 260 }
      },
      {
        id: 'wall_2',
        name: '#2 Trái-Giữa-Ngoài (HISTORIC PARADES)',
        label: 'HISTORIC PARADES',
        mediaType: 'image',
        mediaElement: imgTopicHistory,
        thumbUrl: '03_ASSETS/Studio_Backgrounds/topic_vietnam_history.jpg',
        p0: { x: 255, y: 365 },
        p1: { x: 520, y: 425 },
        p2: { x: 512, y: 535 },
        p3: { x: 255, y: 525 }
      },
      {
        id: 'wall_3',
        name: '#3 Trái-Dưới-Ngoài (ĐOÀN QUÂN)',
        label: 'QUÂN ĐỘI NHÂN DÂN',
        mediaType: 'image',
        mediaElement: imgHistoryBlue,
        thumbUrl: '03_ASSETS/Studio_Backgrounds/studio_history_blue.jpg',
        p0: { x: 330, y: 595 },
        p1: { x: 488, y: 600 },
        p2: { x: 485, y: 720 },
        p3: { x: 330, y: 708 }
      },
      {
        id: 'wall_4',
        name: '#4 Trái-Trên-Trong (VIETNAM NEWS)',
        label: 'VIETNAM NEWS',
        mediaType: 'image',
        mediaElement: imgTopicBreaking,
        thumbUrl: '03_ASSETS/Studio_Backgrounds/intro_breaking_news.jpg',
        p0: { x: 480, y: 275 },
        p1: { x: 625, y: 335 },
        p2: { x: 595, y: 410 },
        p3: { x: 460, y: 360 }
      },
      {
        id: 'wall_5',
        name: '#5 Trái-Giữa-Trong (NATION S JOURNEY)',
        label: "NATION'S JOURNEY",
        mediaType: 'image',
        mediaElement: imgDocReport,
        thumbUrl: '03_ASSETS/Studio_Backgrounds/studio_documentary_report.jpg',
        p0: { x: 555, y: 430 },
        p1: { x: 698, y: 445 },
        p2: { x: 690, y: 535 },
        p3: { x: 555, y: 528 }
      },
      {
        id: 'wall_6',
        name: '#6 Trái-Dưới-Trong (3RD REGIMENT)',
        label: '3RD REGIMENT',
        mediaType: 'image',
        mediaElement: imgHistoryGold,
        thumbUrl: '03_ASSETS/Studio_Backgrounds/studio_history_gold.jpg',
        p0: { x: 518, y: 580 },
        p1: { x: 620, y: 580 },
        p2: { x: 615, y: 668 },
        p3: { x: 518, y: 662 }
      },

      // ============================================================
      // TƯỜNG PHẢI — 6 KHUNG (Khớp chuẩn 100% vị trí ảnh có sẵn trên tường phải)
      // ============================================================
      {
        id: 'wall_7',
        name: '#7 Phải-Trên-Ngoài (DOCUMENTARY)',
        label: 'DOCUMENTARY',
        mediaType: 'image',
        mediaElement: imgTopicHistory,
        thumbUrl: '03_ASSETS/Studio_Backgrounds/topic_vietnam_history.jpg',
        p0: { x: 1565, y: 110 },
        p1: { x: 1735, y: 35 },
        p2: { x: 1795, y: 190 },
        p3: { x: 1630, y: 265 }
      },
      {
        id: 'wall_8',
        name: '#8 Phải-Giữa-Ngoài (LIVE BROADCAST)',
        label: 'LIVE BROADCAST',
        mediaType: 'image',
        mediaElement: imgDocReport,
        thumbUrl: '03_ASSETS/Studio_Backgrounds/studio_documentary_report.jpg',
        p0: { x: 1555, y: 335 },
        p1: { x: 1800, y: 275 },
        p2: { x: 1812, y: 520 },
        p3: { x: 1560, y: 560 }
      },
      {
        id: 'wall_9',
        name: '#9 Phải-Dưới-Ngoài (TƯ LIỆU LỊCH SỬ)',
        label: 'TƯ LIỆU',
        mediaType: 'image',
        mediaElement: imgHistoryBlue,
        thumbUrl: '03_ASSETS/Studio_Backgrounds/studio_history_blue.jpg',
        p0: { x: 1535, y: 605 },
        p1: { x: 1690, y: 590 },
        p2: { x: 1685, y: 755 },
        p3: { x: 1535, y: 760 }
      },
      {
        id: 'wall_10',
        name: '#10 Phải-Trên-Trong (NATION S JOURNEY)',
        label: "NATION'S JOURNEY",
        mediaType: 'image',
        mediaElement: imgTalk11Full,
        thumbUrl: '01_TALK11_Broadcast_16x9_Full.png',
        p0: { x: 1405, y: 185 },
        p1: { x: 1540, y: 130 },
        p2: { x: 1595, y: 280 },
        p3: { x: 1458, y: 338 }
      },
      {
        id: 'wall_11',
        name: '#11 Phải-Giữa-Trong (CỜ SAO VÀNG)',
        label: 'QUỐC KỲ',
        mediaType: 'image',
        mediaElement: imgTopicBreaking,
        thumbUrl: '03_ASSETS/Studio_Backgrounds/intro_breaking_news.jpg',
        p0: { x: 1412, y: 395 },
        p1: { x: 1520, y: 365 },
        p2: { x: 1525, y: 515 },
        p3: { x: 1414, y: 535 }
      },
      {
        id: 'wall_12',
        name: '#12 Phải-Dưới-Trong (DIỄU HÀNH XE TĂNG)',
        label: 'DIỄU BINH',
        mediaType: 'image',
        mediaElement: imgTopicScience,
        thumbUrl: '03_ASSETS/Studio_Backgrounds/topic_science_space.jpg',
        p0: { x: 1415, y: 565 },
        p1: { x: 1500, y: 548 },
        p2: { x: 1498, y: 668 },
        p3: { x: 1415, y: 678 }
      }
    ];'''

def update_html_content(content):
    # 1. Update Section 2 Header
    content = re.sub(
        r'<!-- 2\. HÀNH LANG MÀN HÌNH PHỤ 3D.*?-->\s*<div class="section-container">\s*<div class="section-header-row" data-target="bodyWallScreens">\s*<span class="section-header-title">\s*<span class="collapse-icon">▼</span>\s*2\.[^<]+</span>\s*<div style="display: flex; gap: 4px; align-items: center;">\s*<label class="btn btn-secondary"[^>]*>\s*⚡ Nạp \d+ File\s*<input type="file" id="inputBatchWallFiles"[^>]*>\s*</label>',
        '''<!-- 2. HÀNH LANG MÀN HÌNH PHỤ 3D (12 KHUNG GALLERY 2 BÊN TƯỜNG) -->
      <div class="section-container">
        <div class="section-header-row" data-target="bodyWallScreens">
          <span class="section-header-title">
            <span class="collapse-icon">▼</span> 2. Khung Tranh 3D Hai Bên Tường (12 Khung Gallery)
          </span>
          <div style="display: flex; gap: 4px; align-items: center;">
            <label class="btn btn-secondary" style="padding: 2px 6px; font-size: 10px; cursor: pointer; border-color: rgba(255,107,0,0.4); color: #FFB703;" title="Nạp 12 file ảnh/video một lượt cho 2 bên tường" onclick="event.stopPropagation()">
              ⚡ Nạp 12 File
              <input type="file" id="inputBatchWallFiles" accept="image/*,video/*" multiple style="display: none;">
            </label>''',
        content,
        flags=re.DOTALL
    )

    # 2. Update wallScreens array definition
    content = re.sub(
        r'// -+\s*// \d+ GALLERY SCREENS.*?let wallScreens = \[.*?\];',
        new_wall_screens_code,
        content,
        flags=re.DOTALL
    )

    # 3. Update batch upload slice from 9 to 12
    content = re.sub(
        r'const files = Array\.from\(e\.target\.files\)\.slice\(0, \d+\);',
        'const files = Array.from(e.target.files).slice(0, 12);',
        content
    )
    content = re.sub(
        r'showToast\(`✓ Đã nạp \$\{files\.length\} file vào \d+ khung hành lang!`\);',
        'showToast(`✓ Đã nạp ${files.length} file vào 12 khung tranh 2 bên tường!`);',
        content
    )

    # 4. Update Presets for all 12 frames
    new_presets_code = '''        if (preset === 'reset') {
          wallScreens.forEach(sc => { sc.mediaElement = null; sc.thumbUrl = ''; });
          showToast('✓ Đã đặt lại toàn bộ 12 khung tranh trên tường!');
        } else if (preset === 'history') {
          // Tường Trái (6 khung)
          wallScreens[0].mediaElement = imgHistoryGold; wallScreens[0].thumbUrl = imgHistoryGold.src; wallScreens[0].label = 'VIỆT NAM';
          wallScreens[1].mediaElement = imgTopicHistory; wallScreens[1].thumbUrl = imgTopicHistory.src; wallScreens[1].label = 'HISTORIC PARADES';
          wallScreens[2].mediaElement = imgHistoryBlue; wallScreens[2].thumbUrl = imgHistoryBlue.src; wallScreens[2].label = 'QUÂN ĐỘI';
          wallScreens[3].mediaElement = imgTopicBreaking; wallScreens[3].thumbUrl = imgTopicBreaking.src; wallScreens[3].label = 'VIETNAM NEWS';
          wallScreens[4].mediaElement = imgDocReport; wallScreens[4].thumbUrl = imgDocReport.src; wallScreens[4].label = "NATION'S JOURNEY";
          wallScreens[5].mediaElement = imgHistoryGold; wallScreens[5].thumbUrl = imgHistoryGold.src; wallScreens[5].label = '3RD REGIMENT';
          // Tường Phải (6 khung)
          wallScreens[6].mediaElement = imgTopicHistory; wallScreens[6].thumbUrl = imgTopicHistory.src; wallScreens[6].label = 'DOCUMENTARY';
          wallScreens[7].mediaElement = imgDocReport; wallScreens[7].thumbUrl = imgDocReport.src; wallScreens[7].label = 'LIVE BROADCAST';
          wallScreens[8].mediaElement = imgHistoryBlue; wallScreens[8].thumbUrl = imgHistoryBlue.src; wallScreens[8].label = 'TƯ LIỆU';
          wallScreens[9].mediaElement = imgTalk11Full; wallScreens[9].thumbUrl = imgTalk11Full.src; wallScreens[9].label = "NATION'S JOURNEY";
          wallScreens[10].mediaElement = imgTopicBreaking; wallScreens[10].thumbUrl = imgTopicBreaking.src; wallScreens[10].label = 'QUỐC KỲ';
          wallScreens[11].mediaElement = imgTopicScience; wallScreens[11].thumbUrl = imgTopicScience.src; wallScreens[11].label = 'DIỄU BINH';
          showToast('✓ Đã áp dụng Bộ 12 Ảnh Lịch Sử VN');
        } else if (preset === 'talk11') {
          wallScreens[0].mediaElement = imgTalk11Full; wallScreens[0].thumbUrl = imgTalk11Full.src; wallScreens[0].label = 'TALK11 NEWS';
          wallScreens[1].mediaElement = imgTopicBreaking; wallScreens[1].thumbUrl = imgTopicBreaking.src; wallScreens[1].label = 'BẢN TIN NHÍ';
          wallScreens[2].mediaElement = imgTalk11Full; wallScreens[2].thumbUrl = imgTalk11Full.src; wallScreens[2].label = 'HỌC VIÊN';
          wallScreens[3].mediaElement = imgDocReport; wallScreens[3].thumbUrl = imgDocReport.src; wallScreens[3].label = 'PHÒNG THU 3D';
          wallScreens[4].mediaElement = imgTalk11Full; wallScreens[4].thumbUrl = imgTalk11Full.src; wallScreens[4].label = 'COMMUNITY';
          wallScreens[5].mediaElement = imgHistoryGold; wallScreens[5].thumbUrl = imgHistoryGold.src; wallScreens[5].label = 'MC NHÍ';
          wallScreens[6].mediaElement = imgTopicBreaking; wallScreens[6].thumbUrl = imgTopicBreaking.src; wallScreens[6].label = 'STUDENT NEWS';
          wallScreens[7].mediaElement = imgTalk11Full; wallScreens[7].thumbUrl = imgTalk11Full.src; wallScreens[7].label = 'TALK11 BROADCAST';
          wallScreens[8].mediaElement = imgDocReport; wallScreens[8].thumbUrl = imgDocReport.src; wallScreens[8].label = 'HOẠT ĐỘNG';
          wallScreens[9].mediaElement = imgTalk11Full; wallScreens[9].thumbUrl = imgTalk11Full.src; wallScreens[9].label = 'SỰ KIỆN NỔI BẬT';
          wallScreens[10].mediaElement = imgTopicBreaking; wallScreens[10].thumbUrl = imgTopicBreaking.src; wallScreens[10].label = 'KẾT NỐI';
          wallScreens[11].mediaElement = imgTalk11Full; wallScreens[11].thumbUrl = imgTalk11Full.src; wallScreens[11].label = 'TỎA SÁNG';
          showToast('✓ Đã áp dụng Bộ 12 Ảnh Talk11 Student');
        } else if (preset === 'science') {
          wallScreens[0].mediaElement = imgTopicScience; wallScreens[0].thumbUrl = imgTopicScience.src; wallScreens[0].label = 'SPACE & SCIENCE';
          wallScreens[1].mediaElement = imgTopicBreaking; wallScreens[1].thumbUrl = imgTopicBreaking.src; wallScreens[1].label = 'KHOA HỌC 4.0';
          wallScreens[2].mediaElement = imgTopicScience; wallScreens[2].thumbUrl = imgTopicScience.src; wallScreens[2].label = 'VŨ TRỤ';
          wallScreens[3].mediaElement = imgTopicScience; wallScreens[3].thumbUrl = imgTopicScience.src; wallScreens[3].label = 'AI & ROBOTICS';
          wallScreens[4].mediaElement = imgDocReport; wallScreens[4].thumbUrl = imgDocReport.src; wallScreens[4].label = 'CÔNG NGHỆ';
          wallScreens[5].mediaElement = imgTopicScience; wallScreens[5].thumbUrl = imgTopicScience.src; wallScreens[5].label = 'KHÁM PHÁ';
          wallScreens[6].mediaElement = imgTopicScience; wallScreens[6].thumbUrl = imgTopicScience.src; wallScreens[6].label = 'TƯƠNG LAI';
          wallScreens[7].mediaElement = imgTopicBreaking; wallScreens[7].thumbUrl = imgTopicBreaking.src; wallScreens[7].label = 'NGHIÊN CỨU';
          wallScreens[8].mediaElement = imgTopicScience; wallScreens[8].thumbUrl = imgTopicScience.src; wallScreens[8].label = 'ĐỔI MỚI';
          wallScreens[9].mediaElement = imgTopicScience; wallScreens[9].thumbUrl = imgTopicScience.src; wallScreens[9].label = 'GALAXY';
          wallScreens[10].mediaElement = imgTopicScience; wallScreens[10].thumbUrl = imgTopicScience.src; wallScreens[10].label = 'INNOVATION';
          wallScreens[11].mediaElement = imgTopicScience; wallScreens[11].thumbUrl = imgTopicScience.src; wallScreens[11].label = 'DISCOVERY';
          showToast('✓ Đã áp dụng Bộ 12 Ảnh Khoa Học Vũ Trụ');
        }'''
    
    content = re.sub(
        r'if \(preset === \'reset\'\) \{.*?showToast\(\'✓ Đã áp dụng Bộ \d+ Ảnh Khoa Học Vũ Trụ\'\);\s*\}',
        new_presets_code,
        content,
        flags=re.DOTALL
    )

    # 5. Update canvas draw sequence so TV frame on left wall does NOT block the 6 left photo frames:
    # If mediaSlots have media and user has active TV segment, center TV or draw cleanly:
    # Notice lines 2684:
    # // 2. Draw 12 Wall Gallery Screens (Customizable by user)
    # drawWallGalleryScreens(timeSec);
    content = re.sub(
        r'// 2\. Draw \d+ Right Wall Gallery Screens \(Customizable by user\)\s*drawWallGalleryScreens\(timeSec\);',
        '// 2. Draw 12 Wall Gallery Screens on Left & Right Walls (Customizable by user)\n      drawWallGalleryScreens(timeSec);',
        content
    )

    # Make the TV frame overlay optional or positioned cleanly (if mediaSlots exist and has loaded media)
    old_tv_block = '''      // 4. TV Frame & Content on Left Wall
      const tvX = 60;
      const tvY = 170;
      const tvW = 770;
      const tvH = 435;

      // Hologram Box Outer Border (Glowing Orange & Gold)
      ctx.save();
      ctx.strokeStyle = 'rgba(255, 107, 0, 0.9)';
      ctx.lineWidth = 2.5;
      ctx.shadowColor = '#FF6B00';
      ctx.shadowBlur = 20;
      ctx.strokeRect(tvX, tvY, tvW, tvH);
      ctx.restore();

      // Draw Dynamic TV Screen
      drawStudioTvScreen(tvX, tvY, tvW, tvH, timeSec, tvMotionIntensity);

      // Corner Brackets (Talk11 Gold)
      const brkLen = 28;
      ctx.save();
      ctx.strokeStyle = '#FBBF24';
      ctx.lineWidth = 3.5;

      ctx.beginPath();
      ctx.moveTo(tvX + 8, tvY + 8 + brkLen);
      ctx.lineTo(tvX + 8, tvY + 8);
      ctx.lineTo(tvX + 8 + brkLen, tvY + 8);
      ctx.stroke();

      ctx.beginPath();
      ctx.moveTo(tvX + tvW - 8 - brkLen, tvY + 8);
      ctx.lineTo(tvX + tvW - 8, tvY + 8);
      ctx.lineTo(tvX + tvW - 8, tvY + 8 + brkLen);
      ctx.stroke();

      ctx.beginPath();
      ctx.moveTo(tvX + 8, tvY + tvH - 8 - brkLen);
      ctx.lineTo(tvX + 8, tvY + tvH - 8);
      ctx.lineTo(tvX + 8 + brkLen, tvY + tvH - 8);
      ctx.stroke();

      ctx.beginPath();
      ctx.moveTo(tvX + tvW - 8 - brkLen, tvY + tvH - 8);
      ctx.lineTo(tvX + tvW - 8, tvY + tvH - 8);
      ctx.lineTo(tvX + tvW - 8, tvY + tvH - 8 - brkLen);
      ctx.stroke();
      ctx.restore();'''

    new_tv_block = '''      // 4. TV Screen Content: Draw into center stage screen when media slots are loaded
      if (mediaSlots && mediaSlots.length > 0) {
        // Center Stage Floating Screen (x: 695, y: 468, w: 530, h: 96)
        const tvX = 695;
        const tvY = 468;
        const tvW = 530;
        const tvH = 96;
        drawStudioTvScreen(tvX, tvY, tvW, tvH, timeSec, tvMotionIntensity * 0.3);
      }'''

    if old_tv_block in content:
        content = content.replace(old_tv_block, new_tv_block)

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
    updated = update_html_content(orig)
    with open(f, 'w', encoding='utf-8') as file:
        file.write(updated)
    print(f"Updated {f} ({len(updated)} bytes)")
