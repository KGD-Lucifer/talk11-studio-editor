# -*- coding: utf-8 -*-
import re
import os

def update_file_content(content):
    # =========================================================================
    # 1. ADD CSS STYLES FOR TRACK MUTED, BLOCK DRAGGING, SUB/SFX MANAGERS
    # =========================================================================
    old_css_anchor = ".timeline-block.block-sfx {\n      background: linear-gradient(90deg, #D97706 0%, #F59E0B 100%);\n      border-color: #FDE68A;\n      width: auto;\n      min-width: 50px;\n    }"
    
    new_css = """.timeline-block.block-sfx {
      background: linear-gradient(90deg, #D97706 0%, #F59E0B 100%);
      border-color: #FDE68A;
      width: auto;
      min-width: 50px;
    }

    /* TRACK CONTROLS & MUTED STATES */
    .track-row.track-muted {
      opacity: 0.38;
      filter: grayscale(0.65);
    }
    .btn-track-tool {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: 4px;
      padding: 1px 5px;
      font-size: 10px;
      cursor: pointer;
      color: inherit;
      transition: all 0.15s;
      line-height: 1.2;
    }
    .btn-track-tool:hover {
      background: rgba(255, 255, 255, 0.25);
      transform: scale(1.08);
    }
    .timeline-block.block-muted {
      opacity: 0.42 !important;
      filter: grayscale(0.85) !important;
      background: #475569 !important;
      border-color: #64748B !important;
    }
    .timeline-block.is-dragging {
      z-index: 100 !important;
      box-shadow: 0 0 16px rgba(255, 107, 0, 0.9) !important;
      cursor: grabbing !important;
      transform: scaleY(1.08);
    }
    .sub-item-card.sub-hidden {
      opacity: 0.48;
      border-color: rgba(255, 255, 255, 0.05);
      background: rgba(15, 23, 42, 0.45);
    }
    .sfx-inst-card {
      background: rgba(18, 26, 44, 0.75);
      border: 1px solid rgba(245, 158, 11, 0.25);
      border-radius: 6px;
      padding: 4px 7px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 5px;
      transition: all 0.15s;
    }
    .sfx-inst-card:hover {
      border-color: #F59E0B;
      background: rgba(245, 158, 11, 0.1);
    }
    .sfx-inst-card.sfx-muted {
      opacity: 0.45;
      border-color: rgba(255, 255, 255, 0.1);
      background: rgba(15, 23, 42, 0.4);
    }"""

    if old_css_anchor in content:
        content = content.replace(old_css_anchor, new_css)
    else:
        print("Warning: old_css_anchor not found exactly, trying regex...")
        content = re.sub(
            r'\.timeline-block\.block-sfx\s*\{[^}]*\}',
            new_css,
            content
        )

    # =========================================================================
    # 2. UPGRADE SECTION 3: SUBTITLE HTML
    # =========================================================================
    old_section_3_regex = r'<!-- 3\. PHỤ ĐỀ VIDEO \(11 KHUNG ĐIỀN SUBTITLE\) -->.*?<!-- 4\. HIỆU ỨNG ÂM THANH'
    new_section_3 = '''<!-- 3. PHỤ ĐỀ VIDEO (DI CHUYỂN, ẨN/HIỆN & 11 CÂU SUBTITLE) -->
      <div class="section-container">
        <div class="section-header-row" data-target="bodySubtitles">
          <span class="section-header-title">
            <span class="collapse-icon">▼</span> 3. Phụ Đề Video (Di Chuyển & Ẩn/Hiện)
          </span>
          <div style="display: flex; gap: 4px; align-items: center;">
            <button type="button" class="btn btn-secondary" id="btnAutoDistributeSubs" style="padding: 2px 6px; font-size: 10px;" title="Chia đều 60s cho 11 câu" onclick="event.stopPropagation()">⚡ Chia Đều</button>
            <button type="button" class="btn-toggle-section" data-target="bodySubtitles">
              <span class="toggle-text">Thu gọn</span>
            </button>
          </div>
        </div>

        <div class="section-collapsible-body" id="bodySubtitles">
          <!-- Bật / Ẩn phụ đề -->
          <div style="display: flex; align-items: center; justify-content: space-between; font-size: 11px; background: rgba(56, 189, 248, 0.08); padding: 5px 8px; border-radius: 6px; border: 1px solid rgba(56, 189, 248, 0.2);">
            <label style="cursor: pointer; display: flex; align-items: center; gap: 6px; font-weight: 700; color: #38BDF8;">
              <input type="checkbox" id="chkShowSubtitles" checked style="accent-color: #38BDF8; width: 15px; height: 15px;">
              <span>Bật hiển thị phụ đề</span>
            </label>
            <span id="subVisibilityStatus" style="font-size: 10px; color: #34D399; font-weight: 700;">● Đang hiển thị</span>
          </div>

          <!-- Điều khiển vị trí phụ đề (Di chuyển) -->
          <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 6px; padding: 7px; display: flex; flex-direction: column; gap: 6px; margin-top: 6px;">
            <div style="display: flex; align-items: center; justify-content: space-between; font-size: 10.5px; font-weight: 700; color: #F1F5F9;">
              <span>📍 Vị trí hiển thị:</span>
              <div style="display: flex; gap: 3px;">
                <button type="button" class="btn btn-secondary btn-sub-preset" data-pos="bottom" style="padding: 2px 5px; font-size: 9.5px;" title="Đặt ở đáy màn hình">⬇️ Dưới</button>
                <button type="button" class="btn btn-secondary btn-sub-preset" data-pos="middle" style="padding: 2px 5px; font-size: 9.5px;" title="Đặt ở giữa màn hình">↔️ Giữa</button>
                <button type="button" class="btn btn-secondary btn-sub-preset" data-pos="top" style="padding: 2px 5px; font-size: 9.5px;" title="Đặt ở trên đầu">⬆️ Trên</button>
              </div>
            </div>

            <!-- Slider Y -->
            <div style="display: flex; align-items: center; justify-content: space-between; gap: 6px; font-size: 10.5px; color: #94A3B8;">
              <span style="min-width: 65px;">↕️ Độ cao Y:</span>
              <input type="range" class="range-slider" id="sliderSubPosY" min="60" max="1020" step="5" value="960">
              <span id="valSubPosY" style="font-family: monospace; font-size: 10px; min-width: 42px; text-align: right; color: #38BDF8;">960px</span>
            </div>

            <!-- Slider X Offset -->
            <div style="display: flex; align-items: center; justify-content: space-between; gap: 6px; font-size: 10.5px; color: #94A3B8;">
              <span style="min-width: 65px;">↔️ Lệch X:</span>
              <input type="range" class="range-slider" id="sliderSubPosX" min="-500" max="500" step="5" value="0">
              <span id="valSubPosX" style="font-family: monospace; font-size: 10px; min-width: 42px; text-align: right; color: #38BDF8;">0px</span>
            </div>

            <!-- Cỡ chữ Font size -->
            <div style="display: flex; align-items: center; justify-content: space-between; gap: 6px; font-size: 10.5px; color: #94A3B8;">
              <span style="min-width: 65px;">🔤 Cỡ chữ:</span>
              <input type="range" class="range-slider" id="sliderSubFontSize" min="16" max="36" step="2" value="24">
              <span id="valSubFontSize" style="font-family: monospace; font-size: 10px; min-width: 42px; text-align: right; color: #38BDF8;">24px</span>
            </div>

            <div style="font-size: 9.5px; color: #38BDF8; background: rgba(56, 189, 248, 0.08); padding: 4px 6px; border-radius: 4px; border: 1px dashed rgba(56, 189, 248, 0.3);">
              💡 <b>Mẹo:</b> Bạn có thể bấm chuột trực tiếp vào khung phụ đề trên màn hình để kéo thả tự do!
            </div>
          </div>

          <div style="display: flex; align-items: center; justify-content: space-between; font-size: 10.5px; color: #94A3B8; margin-top: 6px;">
            <span style="font-weight: 700;">Danh sách 11 câu phụ đề:</span>
            <span style="font-size: 9.5px; color: #64748B;">Chỉnh giây & ẩn từng câu</span>
          </div>

          <!-- 11 Subtitle Cards Container -->
          <div id="subtitlesListContainer" style="display: flex; flex-direction: column; gap: 5px; max-height: 220px; overflow-y: auto; padding-right: 2px;">
            <!-- 11 subtitle items generated via JS -->
          </div>
        </div>
      </div>

      <!-- 4. HIỆU ỨNG ÂM THANH'''

    content = re.sub(old_section_3_regex, new_section_3, content, flags=re.DOTALL)

    # =========================================================================
    # 3. UPGRADE SECTION 4: SOUND FX HTML
    # =========================================================================
    old_section_4_regex = r'<!-- 4\. HIỆU ỨNG ÂM THANH \(10 SOUND EFFECTS KÉO THẢ\) -->.*?<!-- 5\. TIÊU ĐỀ BẢN TIN'
    new_section_4 = '''<!-- 4. HIỆU ỨNG ÂM THANH (DI CHUYỂN, ẨN/TẮT & 10 SOUND FX) -->
      <div class="section-container">
        <div class="section-header-row" data-target="bodySoundFX">
          <span class="section-header-title">
            <span class="collapse-icon">▼</span> 4. Hiệu Ứng Âm Thanh (Di Chuyển & Ẩn/Tắt)
          </span>
          <div style="display: flex; gap: 4px; align-items: center;">
            <button type="button" class="btn btn-secondary" id="btnClearAllSFX" style="padding: 2px 6px; font-size: 10px; border-color: rgba(239, 68, 68, 0.4); color: #FCA5A5;" title="Xóa tất cả hiệu ứng âm thanh khỏi Timeline" onclick="event.stopPropagation()">🗑️ Xóa Hết</button>
            <button type="button" class="btn-toggle-section" data-target="bodySoundFX">
              <span class="toggle-text">Thu gọn</span>
            </button>
          </div>
        </div>

        <div class="section-collapsible-body" id="bodySoundFX">
          <!-- Bật / Tắt toàn bộ Sound FX -->
          <div style="display: flex; align-items: center; justify-content: space-between; font-size: 11px; background: rgba(245, 158, 11, 0.08); padding: 5px 8px; border-radius: 6px; border: 1px solid rgba(245, 158, 11, 0.2);">
            <label style="cursor: pointer; display: flex; align-items: center; gap: 6px; font-weight: 700; color: #FBBF24;">
              <input type="checkbox" id="chkEnableSoundFX" checked style="accent-color: #F59E0B; width: 15px; height: 15px;">
              <span>Bật hiệu ứng âm thanh (SFX)</span>
            </label>
            <span id="sfxStatusBadge" style="font-size: 10px; color: #34D399; font-weight: 700;">🔊 Đang bật</span>
          </div>

          <!-- Kho 10 âm thanh kéo thả -->
          <div style="margin-top: 6px; font-size: 10px; color: #94A3B8; display: flex; justify-content: space-between;">
            <span style="font-weight: 700;">Kho 10 Sound FX (Bấm + hoặc kéo vào Timeline):</span>
          </div>
          <div class="sfx-grid" id="sfxGrid" style="margin-top: 4px;">
            <!-- 10 SFX Items -->
          </div>

          <!-- Danh sách SFX đang nằm trên Timeline (cho phép di chuyển giây phát hoặc tắt/xóa) -->
          <div style="margin-top: 8px; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 6px;">
            <div style="display: flex; align-items: center; justify-content: space-between; font-size: 10.5px; font-weight: 700; color: #FBBF24; margin-bottom: 4px;">
              <span>⏱️ Quản lý thời điểm phát SFX:</span>
              <span id="sfxCountBadge" style="font-size: 9.5px; color: #94A3B8;">3 hiệu ứng</span>
            </div>
            <div style="font-size: 9.5px; color: #FBBF24; background: rgba(245, 158, 11, 0.08); padding: 3px 6px; border-radius: 4px; border: 1px dashed rgba(245, 158, 11, 0.25); margin-bottom: 5px;">
              💡 <b>Di chuyển:</b> Kéo trực tiếp khối màu cam trên Timeline hoặc chỉnh giây bên dưới.
            </div>
            <div id="sfxTimelineListContainer" style="display: flex; flex-direction: column; gap: 4px; max-height: 160px; overflow-y: auto; padding-right: 2px;">
              <!-- Rendered dynamically -->
            </div>
          </div>
        </div>
      </div>

      <!-- 5. TIÊU ĐỀ BẢN TIN'''

    content = re.sub(old_section_4_regex, new_section_4, content, flags=re.DOTALL)

    # =========================================================================
    # 4. UPGRADE TIMELINE TRACK HEADERS (Eye & Speaker buttons)
    # =========================================================================
    old_track_sub = '''            <!-- TRACK 2: SUBTITLES (11 SUBS) -->
            <div class="track-row" id="trackSubRow">
              <div class="track-header" style="color: #38BDF8;">📝 Phụ Đề</div>
              <div class="track-content" id="trackSubContent">
                <!-- Sub blocks -->
              </div>
            </div>

            <!-- TRACK 3: SOUND FX -->
            <div class="track-row" id="trackSfxRow">
              <div class="track-header" style="color: #FBBF24;">🎵 Sound FX</div>
              <div class="track-content" id="trackSfxContent">
                <!-- SFX blocks -->
              </div>
            </div>'''

    new_track_sub = '''            <!-- TRACK 2: SUBTITLES (11 SUBS) -->
            <div class="track-row" id="trackSubRow">
              <div class="track-header" style="color: #38BDF8; display: flex; align-items: center; justify-content: space-between; padding-right: 6px;">
                <span>📝 Phụ Đề</span>
                <button type="button" class="btn-track-tool" id="btnToggleSubTrack" title="Ẩn/Hiện toàn bộ phụ đề" style="color: #38BDF8; border-color: rgba(56,189,248,0.4); background: rgba(56,189,248,0.12);">👁️</button>
              </div>
              <div class="track-content" id="trackSubContent">
                <!-- Sub blocks -->
              </div>
            </div>

            <!-- TRACK 3: SOUND FX -->
            <div class="track-row" id="trackSfxRow">
              <div class="track-header" style="color: #FBBF24; display: flex; align-items: center; justify-content: space-between; padding-right: 6px;">
                <span>🎵 Sound FX</span>
                <button type="button" class="btn-track-tool" id="btnToggleSfxTrack" title="Bật/Tắt âm thanh SFX (Mute)" style="color: #FBBF24; border-color: rgba(245,158,11,0.4); background: rgba(245,158,11,0.12);">🔊</button>
              </div>
              <div class="track-content" id="trackSfxContent">
                <!-- SFX blocks -->
              </div>
            </div>'''

    if old_track_sub in content:
        content = content.replace(old_track_sub, new_track_sub)
    else:
        print("Warning: track header block not matched exactly, trying regex...")
        content = re.sub(
            r'<!-- TRACK 2: SUBTITLES \(11 SUBS\) -->.*?<!-- SFX blocks -->\s*</div>\s*</div>',
            new_track_sub,
            content,
            flags=re.DOTALL
        )

    # =========================================================================
    # 5. UPGRADE JS VARIABLES DEFINITIONS
    # =========================================================================
    old_vars = "let showSubtitles = true;\n\n    const canvas = document.getElementById('mainCanvas');"
    new_vars = """let showSubtitles = true;
    let subPosY = 960; // Default: above ticker (1080 - 120 = 960)
    let subPosX = 0;   // Centered
    let subFontSize = 24; // 24px
    let isDraggingSubtitle = false;
    let isHoveringSubtitle = false;
    let subDragStartX = 0;
    let subDragStartY = 0;
    let currentSubBox = null; // { x, y, w, h, subId }

    let enableSoundFX = true;
    let lastPlayedSfxTimeSec = -1;

    const canvas = document.getElementById('mainCanvas');"""

    content = content.replace(old_vars, new_vars)

    # Also add new UI element references
    old_ui_refs = "const chkShowSubtitles = document.getElementById('chkShowSubtitles');"
    new_ui_refs = """const chkShowSubtitles = document.getElementById('chkShowSubtitles');
    const sliderSubPosY = document.getElementById('sliderSubPosY');
    const sliderSubPosX = document.getElementById('sliderSubPosX');
    const sliderSubFontSize = document.getElementById('sliderSubFontSize');
    const valSubPosY = document.getElementById('valSubPosY');
    const valSubPosX = document.getElementById('valSubPosX');
    const valSubFontSize = document.getElementById('valSubFontSize');
    const subVisibilityStatus = document.getElementById('subVisibilityStatus');
    const btnToggleSubTrack = document.getElementById('btnToggleSubTrack');

    const chkEnableSoundFX = document.getElementById('chkEnableSoundFX');
    const sfxStatusBadge = document.getElementById('sfxStatusBadge');
    const btnClearAllSFX = document.getElementById('btnClearAllSFX');
    const btnToggleSfxTrack = document.getElementById('btnToggleSfxTrack');
    const sfxTimelineListContainer = document.getElementById('sfxTimelineListContainer');
    const sfxCountBadge = document.getElementById('sfxCountBadge');
    const trackSubRow = document.getElementById('trackSubRow');
    const trackSfxRow = document.getElementById('trackSfxRow');"""

    content = content.replace(old_ui_refs, new_ui_refs)

    # =========================================================================
    # 6. UPGRADE SUBTITLES UI & SOUND EFFECTS UI FUNCTIONS & TIMELINE DRAGGING
    # =========================================================================
    old_sub_and_sfx_code_regex = r'// 11 SUBTITLES UI & SYNCHRONIZATION.*?// DRAG & DROP FOR MEDIA FILES'

    new_sub_and_sfx_code = '''// 11 SUBTITLES UI & SYNCHRONIZATION (MOVABLE & HIDEABLE)
    // ----------------------------------------------------
    function toggleSubtitlesVisibility(visible) {
      showSubtitles = visible;
      if (chkShowSubtitles) chkShowSubtitles.checked = showSubtitles;
      if (btnToggleSubTrack) btnToggleSubTrack.textContent = showSubtitles ? '👁️' : '🚫';
      if (subVisibilityStatus) {
        subVisibilityStatus.textContent = showSubtitles ? '● Đang hiển thị' : '○ Đã ẩn';
        subVisibilityStatus.style.color = showSubtitles ? '#34D399' : '#EF4444';
      }
      if (trackSubRow) trackSubRow.classList.toggle('track-muted', !showSubtitles);
      renderSubtitlesUI();
      try { render(previewCurrentSec); } catch(e) {}
      showToast(showSubtitles ? '✓ Đã bật hiển thị phụ đề' : '✓ Đã ẩn phụ đề trên video');
    }

    if (chkShowSubtitles) {
      chkShowSubtitles.addEventListener('change', (e) => {
        toggleSubtitlesVisibility(e.target.checked);
      });
    }

    if (btnToggleSubTrack) {
      btnToggleSubTrack.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleSubtitlesVisibility(!showSubtitles);
      });
    }

    // Subtitle Position Presets
    document.querySelectorAll('.btn-sub-preset').forEach(btn => {
      btn.addEventListener('click', () => {
        const p = btn.getAttribute('data-pos');
        if (p === 'bottom') {
          subPosY = 960;
          subPosX = 0;
        } else if (p === 'middle') {
          subPosY = 540;
          subPosX = 0;
        } else if (p === 'top') {
          subPosY = 140;
          subPosX = 0;
        }
        if (sliderSubPosY) sliderSubPosY.value = subPosY;
        if (valSubPosY) valSubPosY.textContent = `${subPosY}px`;
        if (sliderSubPosX) sliderSubPosX.value = subPosX;
        if (valSubPosX) valSubPosX.textContent = `${subPosX}px`;
        try { render(previewCurrentSec); } catch(e) {}
        showToast(`✓ Đã đặt vị trí phụ đề: ${btn.textContent.trim()}`);
      });
    });

    if (sliderSubPosY) {
      sliderSubPosY.addEventListener('input', (e) => {
        subPosY = parseInt(e.target.value) || 960;
        if (valSubPosY) valSubPosY.textContent = `${subPosY}px`;
        try { render(previewCurrentSec); } catch(err) {}
      });
    }

    if (sliderSubPosX) {
      sliderSubPosX.addEventListener('input', (e) => {
        subPosX = parseInt(e.target.value) || 0;
        if (valSubPosX) valSubPosX.textContent = `${subPosX}px`;
        try { render(previewCurrentSec); } catch(err) {}
      });
    }

    if (sliderSubFontSize) {
      sliderSubFontSize.addEventListener('input', (e) => {
        subFontSize = parseInt(e.target.value) || 24;
        if (valSubFontSize) valSubFontSize.textContent = `${subFontSize}px`;
        try { render(previewCurrentSec); } catch(err) {}
      });
    }

    function renderSubtitlesUI() {
      subtitlesListContainer.innerHTML = '';
      trackSubContent.innerHTML = '';

      subtitlesList.forEach((sub, idx) => {
        // 1. Sidebar Card
        const card = document.createElement('div');
        card.className = `sub-item-card ${sub.hidden ? 'sub-hidden' : ''}`;
        card.id = `sub_card_${sub.id}`;

        card.innerHTML = `
          <div style="display: flex; align-items: center; justify-content: space-between; gap: 4px;">
            <div style="display: flex; align-items: center; gap: 5px;">
              <span style="font-size: 10.5px; font-weight: 800; color: ${sub.hidden ? '#64748B' : '#38BDF8'};">Sub #${idx + 1}</span>
              <button type="button" class="btn-toggle-sub-item" data-id="${sub.id}" style="padding: 1px 5px; font-size: 9.5px; cursor: pointer; border-radius: 3px; background: ${sub.hidden ? 'rgba(239, 68, 68, 0.15)' : 'rgba(56, 189, 248, 0.15)'}; border: 1px solid ${sub.hidden ? 'rgba(239, 68, 68, 0.4)' : 'rgba(56, 189, 248, 0.3)'}; color: ${sub.hidden ? '#FCA5A5' : '#38BDF8'};" title="${sub.hidden ? 'Bấm để hiển thị lại câu này' : 'Bấm để ẩn câu này khỏi video'}">
                ${sub.hidden ? '🚫 Ẩn' : '👁️ Hiện'}
              </button>
            </div>
            <div style="display: flex; align-items: center; gap: 3px; font-size: 10px; color: #94A3B8;">
              <input type="number" min="0" max="${totalDurationSec}" class="form-control input-sub-start" data-id="${sub.id}" value="${sub.startSec}" style="width: 38px; padding: 1px 3px; text-align: center; font-size: 10px;" title="Giây bắt đầu">s
              <span>➔</span>
              <input type="number" min="0" max="${totalDurationSec}" class="form-control input-sub-end" data-id="${sub.id}" value="${sub.endSec}" style="width: 38px; padding: 1px 3px; text-align: center; font-size: 10px;" title="Giây kết thúc">s
            </div>
          </div>
          <input type="text" class="form-control input-sub-text" data-id="${sub.id}" value="${sub.text}" placeholder="Nhập câu phụ đề #${idx + 1}..." style="font-size: 11px; padding: 3px 6px; ${sub.hidden ? 'opacity: 0.55;' : ''}">
        `;
        subtitlesListContainer.appendChild(card);

        // 2. Timeline Sub Block
        const block = document.createElement('div');
        block.className = `timeline-block block-sub ${sub.hidden ? 'block-muted' : ''}`;
        block.id = `sub_block_${sub.id}`;
        block.style.left = `${sub.startSec * timelineZoomPxPerSec}px`;
        block.style.width = `${Math.max(20, (sub.endSec - sub.startSec) * timelineZoomPxPerSec)}px`;
        block.textContent = `${sub.hidden ? '🚫 ' : ''}#${idx + 1}. ${sub.text}`;
        block.title = `Sub #${idx + 1} (${sub.startSec}s - ${sub.endSec}s): ${sub.text} [Kéo để dời thời gian]`;

        // Interactive Timeline Dragging for Subtitle Block
        block.addEventListener('mousedown', (ev) => {
          ev.stopPropagation();
          const startX = ev.clientX;
          const origStart = sub.startSec;
          const origEnd = sub.endSec;
          const dur = Math.max(1, origEnd - origStart);
          let didMove = false;

          const onMouseMove = (moveEv) => {
            const diffPx = moveEv.clientX - startX;
            if (Math.abs(diffPx) > 3) didMove = true;
            const diffSec = Math.round(diffPx / timelineZoomPxPerSec);
            const newStart = Math.max(0, Math.min(totalDurationSec - dur, origStart + diffSec));
            block.style.left = `${newStart * timelineZoomPxPerSec}px`;
            block.classList.add('is-dragging');
          };

          const onMouseUp = (upEv) => {
            window.removeEventListener('mousemove', onMouseMove);
            window.removeEventListener('mouseup', onMouseUp);
            block.classList.remove('is-dragging');
            if (didMove) {
              const diffPx = upEv.clientX - startX;
              const diffSec = Math.round(diffPx / timelineZoomPxPerSec);
              const newStart = Math.max(0, Math.min(totalDurationSec - dur, origStart + diffSec));
              sub.startSec = newStart;
              sub.endSec = newStart + dur;
              renderSubtitlesUI();
              try { render(previewCurrentSec); } catch(e) {}
              showToast(`✓ Đã dời Sub #${sub.id} đến ${sub.startSec}s ➔ ${sub.endSec}s`);
            }
          };

          window.addEventListener('mousemove', onMouseMove);
          window.addEventListener('mouseup', onMouseUp);
        });

        trackSubContent.appendChild(block);
      });

      // Events for Sub text
      subtitlesListContainer.querySelectorAll('.input-sub-text').forEach(inp => {
        inp.addEventListener('input', (e) => {
          const s = subtitlesList.find(x => x.id === parseInt(e.target.getAttribute('data-id')));
          if (s) {
            s.text = e.target.value;
            const b = document.getElementById(`sub_block_${s.id}`);
            if (b) b.textContent = `${s.hidden ? '🚫 ' : ''}#${s.id}. ${s.text}`;
            try { render(previewCurrentSec); } catch(err) {}
          }
        });
      });

      // Events for Toggle Sub item
      subtitlesListContainer.querySelectorAll('.btn-toggle-sub-item').forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.stopPropagation();
          const s = subtitlesList.find(x => x.id === parseInt(btn.getAttribute('data-id')));
          if (s) {
            s.hidden = !s.hidden;
            renderSubtitlesUI();
            try { render(previewCurrentSec); } catch(err) {}
            showToast(s.hidden ? `✓ Đã ẩn câu phụ đề #${s.id}` : `✓ Đã bật câu phụ đề #${s.id}`);
          }
        });
      });

      // Events for Sub Start and End times
      subtitlesListContainer.querySelectorAll('.input-sub-start').forEach(inp => {
        inp.addEventListener('change', (e) => {
          const s = subtitlesList.find(x => x.id === parseInt(e.target.getAttribute('data-id')));
          if (s) {
            s.startSec = Math.max(0, Math.min(s.endSec - 1, parseInt(e.target.value) || 0));
            renderSubtitlesUI();
            try { render(previewCurrentSec); } catch(err) {}
          }
        });
      });

      subtitlesListContainer.querySelectorAll('.input-sub-end').forEach(inp => {
        inp.addEventListener('change', (e) => {
          const s = subtitlesList.find(x => x.id === parseInt(e.target.getAttribute('data-id')));
          if (s) {
            s.endSec = Math.max(s.startSec + 1, Math.min(totalDurationSec, parseInt(e.target.value) || 1));
            renderSubtitlesUI();
            try { render(previewCurrentSec); } catch(err) {}
          }
        });
      });
    }

    if (btnAutoDistributeSubs) {
      btnAutoDistributeSubs.addEventListener('click', () => {
        const step = totalDurationSec / 11;
        subtitlesList.forEach((s, i) => {
          s.startSec = Math.round(i * step);
          s.endSec = Math.round((i + 1) * step);
        });
        renderSubtitlesUI();
        try { render(previewCurrentSec); } catch(e) {}
        showToast('✓ Đã chia đều 11 câu phụ đề theo 60s!');
      });
    }

    // ----------------------------------------------------
    // SOUND EFFECTS UI & TIMELINE (MOVABLE & HIDEABLE)
    // ----------------------------------------------------
    function toggleSfxVisibility(enabled) {
      enableSoundFX = enabled;
      if (chkEnableSoundFX) chkEnableSoundFX.checked = enableSoundFX;
      if (btnToggleSfxTrack) btnToggleSfxTrack.textContent = enableSoundFX ? '🔊' : '🔇';
      if (sfxStatusBadge) {
        sfxStatusBadge.textContent = enableSoundFX ? '🔊 Đang bật' : '🔇 Đã tắt';
        sfxStatusBadge.style.color = enableSoundFX ? '#34D399' : '#EF4444';
      }
      if (trackSfxRow) trackSfxRow.classList.toggle('track-muted', !enableSoundFX);
      renderSoundFXUI();
      showToast(enableSoundFX ? '🔊 Đã bật hiệu ứng âm thanh SFX' : '🔇 Đã tắt toàn bộ hiệu ứng âm thanh SFX');
    }

    if (chkEnableSoundFX) {
      chkEnableSoundFX.addEventListener('change', (e) => {
        toggleSfxVisibility(e.target.checked);
      });
    }

    if (btnToggleSfxTrack) {
      btnToggleSfxTrack.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleSfxVisibility(!enableSoundFX);
      });
    }

    if (btnClearAllSFX) {
      btnClearAllSFX.addEventListener('click', () => {
        if (soundFxTimeline.length === 0) {
          showToast('Timeline chưa có hiệu ứng âm thanh nào!');
          return;
        }
        soundFxTimeline = [];
        renderSoundFXUI();
        showToast('✓ Đã xóa tất cả hiệu ứng âm thanh khỏi Timeline!');
      });
    }

    function renderSoundFXUI() {
      sfxGrid.innerHTML = '';
      trackSfxContent.innerHTML = '';
      if (sfxTimelineListContainer) sfxTimelineListContainer.innerHTML = '';
      if (sfxCountBadge) sfxCountBadge.textContent = `${soundFxTimeline.length} hiệu ứng`;

      // 1. Sound Library buttons
      soundLibrary.forEach(sfx => {
        const card = document.createElement('div');
        card.className = 'sfx-btn-card';
        card.draggable = true;
        card.setAttribute('data-sfxid', sfx.id);

        card.innerHTML = `
          <div style="font-size: 10px; font-weight: 700; color: #F8FAFC; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
            ${sfx.name}
          </div>
          <div style="display: flex; gap: 3px;">
            <button type="button" class="btn btn-secondary btn-test-sfx" data-sfxid="${sfx.id}" style="padding: 1px 4px; font-size: 9.5px;" title="Nghe thử">▶️</button>
            <button type="button" class="btn btn-primary btn-add-sfx" data-sfxid="${sfx.id}" style="padding: 1px 4px; font-size: 9.5px;" title="Thêm vào thời gian hiện tại">+</button>
          </div>
        `;

        card.addEventListener('dragstart', (e) => {
          e.dataTransfer.setData('text/plain', sfx.id);
        });

        sfxGrid.appendChild(card);
      });

      // Events for Library buttons
      sfxGrid.querySelectorAll('.btn-test-sfx').forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.stopPropagation();
          playSyntheticSFX(btn.getAttribute('data-sfxid'));
        });
      });

      sfxGrid.querySelectorAll('.btn-add-sfx').forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.stopPropagation();
          const sfxId = btn.getAttribute('data-sfxid');
          soundFxTimeline.push({
            id: 'sfx_' + Date.now(),
            sfxId: sfxId,
            timeSec: Math.round(previewCurrentSec),
            muted: false
          });
          soundFxTimeline.sort((a, b) => a.timeSec - b.timeSec);
          renderSoundFXUI();
          showToast(`✓ Đã thêm ${sfxId} vào giây ${Math.round(previewCurrentSec)}s`);
        });
      });

      // 2. Timeline SFX Blocks (Interactive Draggable on Timeline)
      soundFxTimeline.forEach((inst) => {
        const libObj = soundLibrary.find(x => x.id === inst.sfxId) || { name: inst.sfxId };
        const block = document.createElement('div');
        block.className = `timeline-block block-sfx ${inst.muted || !enableSoundFX ? 'block-muted' : ''}`;
        block.id = `sfx_inst_${inst.id}`;
        block.style.left = `${inst.timeSec * timelineZoomPxPerSec}px`;

        block.innerHTML = `
          <span style="display: flex; align-items: center; gap: 3px;">
            <span>${inst.muted ? '🔇 ' : ''}${libObj.name} (${inst.timeSec}s)</span>
          </span>
          <span style="display: flex; align-items: center; gap: 4px; margin-left: 6px;">
            <span class="btn-sfx-toggle-mute" data-id="${inst.id}" style="cursor: pointer; opacity: 0.9;" title="${inst.muted ? 'Bật âm thanh' : 'Tắt tiếng'}">${inst.muted ? '🔇' : '🔊'}</span>
            <span class="del-sfx-inst" data-id="${inst.id}" style="cursor: pointer; font-size: 13px; font-weight: 800; color: #FCA5A5;" title="Xóa">×</span>
          </span>
        `;

        // Interactive Timeline Dragging for SFX Block
        block.addEventListener('mousedown', (ev) => {
          ev.stopPropagation();
          const startX = ev.clientX;
          const origSec = inst.timeSec;
          let didMove = false;

          const onMouseMove = (moveEv) => {
            const diffPx = moveEv.clientX - startX;
            if (Math.abs(diffPx) > 3) didMove = true;
            const diffSec = Math.round(diffPx / timelineZoomPxPerSec);
            const targetSec = Math.max(0, Math.min(totalDurationSec, origSec + diffSec));
            block.style.left = `${targetSec * timelineZoomPxPerSec}px`;
            block.classList.add('is-dragging');
          };

          const onMouseUp = (upEv) => {
            window.removeEventListener('mousemove', onMouseMove);
            window.removeEventListener('mouseup', onMouseUp);
            block.classList.remove('is-dragging');
            if (didMove) {
              const diffPx = upEv.clientX - startX;
              const diffSec = Math.round(diffPx / timelineZoomPxPerSec);
              inst.timeSec = Math.max(0, Math.min(totalDurationSec, origSec + diffSec));
              soundFxTimeline.sort((a, b) => a.timeSec - b.timeSec);
              renderSoundFXUI();
              showToast(`✓ Đã dời hiệu ứng "${libObj.name}" đến giây ${inst.timeSec}s`);
            }
          };

          window.addEventListener('mousemove', onMouseMove);
          window.addEventListener('mouseup', onMouseUp);
        });

        // Block Delete & Mute Events
        block.querySelector('.del-sfx-inst').addEventListener('click', (ev) => {
          ev.stopPropagation();
          soundFxTimeline = soundFxTimeline.filter(x => x.id !== inst.id);
          renderSoundFXUI();
          showToast(`✓ Đã xóa ${libObj.name}`);
        });

        block.querySelector('.btn-sfx-toggle-mute').addEventListener('click', (ev) => {
          ev.stopPropagation();
          inst.muted = !inst.muted;
          renderSoundFXUI();
          showToast(inst.muted ? `🔇 Đã tắt tiếng ${libObj.name}` : `🔊 Đã bật tiếng ${libObj.name}`);
        });

        trackSfxContent.appendChild(block);
      });

      // 3. Manager List in Sidebar Section 4 (Chỉnh giây, di chuyển, bật/tắt hoặc xóa)
      if (sfxTimelineListContainer) {
        if (soundFxTimeline.length === 0) {
          sfxTimelineListContainer.innerHTML = '<div style="font-size: 10px; color: #64748B; text-align: center; padding: 6px; background: rgba(0,0,0,0.2); border-radius: 4px;">Chưa có SFX nào trên Timeline (Bấm + ở trên để thêm)</div>';
        } else {
          soundFxTimeline.forEach((inst) => {
            const libObj = soundLibrary.find(x => x.id === inst.sfxId) || { name: inst.sfxId };
            const row = document.createElement('div');
            row.className = `sfx-inst-card ${inst.muted || !enableSoundFX ? 'sfx-muted' : ''}`;
            row.innerHTML = `
              <div style="font-size: 10px; font-weight: 700; color: #F1F5F9; display: flex; align-items: center; gap: 4px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 105px;" title="${libObj.name}">
                <span>${libObj.name}</span>
              </div>
              <div style="display: flex; align-items: center; gap: 2px;">
                <button type="button" class="btn btn-secondary btn-sfx-shift-down" data-id="${inst.id}" style="padding: 1px 3px; font-size: 9px;" title="-1 giây">-1s</button>
                <input type="number" min="0" max="${totalDurationSec}" class="form-control input-sfx-sec" data-id="${inst.id}" value="${inst.timeSec}" style="width: 36px; padding: 1px 2px; text-align: center; font-size: 10px;" title="Giây phát">
                <span style="font-size: 9.5px; color: #94A3B8;">s</span>
                <button type="button" class="btn btn-secondary btn-sfx-shift-up" data-id="${inst.id}" style="padding: 1px 3px; font-size: 9px;" title="+1 giây">+1s</button>
                <button type="button" class="btn btn-secondary btn-test-sfx-row" data-sfxid="${inst.sfxId}" style="padding: 1px 4px; font-size: 9px;" title="Nghe thử">▶️</button>
                <button type="button" class="btn btn-secondary btn-mute-sfx-row" data-id="${inst.id}" style="padding: 1px 4px; font-size: 9px; ${inst.muted ? 'background: rgba(239, 68, 68, 0.2); color: #FCA5A5;' : ''}" title="${inst.muted ? 'Bật tiếng' : 'Tắt tiếng'}">${inst.muted ? '🔇' : '🔊'}</button>
                <button type="button" class="btn btn-secondary btn-del-sfx-row" data-id="${inst.id}" style="padding: 1px 4px; font-size: 9.5px; color: #F87171;" title="Xóa">×</button>
              </div>
            `;

            // Row Event Listeners
            row.querySelector('.btn-sfx-shift-down').addEventListener('click', () => {
              inst.timeSec = Math.max(0, inst.timeSec - 1);
              soundFxTimeline.sort((a, b) => a.timeSec - b.timeSec);
              renderSoundFXUI();
            });

            row.querySelector('.btn-sfx-shift-up').addEventListener('click', () => {
              inst.timeSec = Math.min(totalDurationSec, inst.timeSec + 1);
              soundFxTimeline.sort((a, b) => a.timeSec - b.timeSec);
              renderSoundFXUI();
            });

            row.querySelector('.input-sfx-sec').addEventListener('change', (e) => {
              inst.timeSec = Math.max(0, Math.min(totalDurationSec, parseInt(e.target.value) || 0));
              soundFxTimeline.sort((a, b) => a.timeSec - b.timeSec);
              renderSoundFXUI();
            });

            row.querySelector('.btn-test-sfx-row').addEventListener('click', () => {
              playSyntheticSFX(inst.sfxId);
            });

            row.querySelector('.btn-mute-sfx-row').addEventListener('click', () => {
              inst.muted = !inst.muted;
              renderSoundFXUI();
              showToast(inst.muted ? `🔇 Đã tắt tiếng ${libObj.name}` : `🔊 Đã bật tiếng ${libObj.name}`);
            });

            row.querySelector('.btn-del-sfx-row').addEventListener('click', () => {
              soundFxTimeline = soundFxTimeline.filter(x => x.id !== inst.id);
              renderSoundFXUI();
              showToast(`✓ Đã xóa ${libObj.name}`);
            });

            sfxTimelineListContainer.appendChild(row);
          });
        }
      }
    }

    // Allow dropping SFX onto SFX Track Content
    trackSfxContent.addEventListener('dragover', (e) => { e.preventDefault(); });
    trackSfxContent.addEventListener('drop', (e) => {
      e.preventDefault();
      const sfxId = e.dataTransfer.getData('text/plain');
      if (sfxId) {
        const rect = trackSfxContent.getBoundingClientRect();
        const dropX = e.clientX - rect.left;
        const dropSec = Math.max(0, Math.min(totalDurationSec, Math.round(dropX / timelineZoomPxPerSec)));
        soundFxTimeline.push({
          id: 'sfx_' + Date.now(),
          sfxId: sfxId,
          timeSec: dropSec,
          muted: false
        });
        soundFxTimeline.sort((a, b) => a.timeSec - b.timeSec);
        renderSoundFXUI();
        showToast(`✓ Đã thả SFX vào giây ${dropSec}s`);
      }
    });

    // ----------------------------------------------------
    // DRAG & DROP FOR MEDIA FILES'''

    content = re.sub(old_sub_and_sfx_code_regex, new_sub_and_sfx_code, content, flags=re.DOTALL)

    # =========================================================================
    # 7. TIMELINE SCRUBBING EVENT FIX (Prevent scrub when clicking blocks)
    # =========================================================================
    old_scrub_listener = '''    timelineTracksContainer.addEventListener('mousedown', (e) => {
      isTimelineScrubbing = true;
      handleTimelineScrub(e);
    });'''

    new_scrub_listener = '''    timelineTracksContainer.addEventListener('mousedown', (e) => {
      if (e.target.closest('.timeline-block') || e.target.closest('.btn-track-tool') || e.target.closest('button')) {
        return;
      }
      isTimelineScrubbing = true;
      handleTimelineScrub(e);
    });'''

    content = content.replace(old_scrub_listener, new_scrub_listener)

    # =========================================================================
    # 8. CANVAS MOUSE LISTENERS FOR DIRECT DRAGGING OF SUBTITLE BOX
    # =========================================================================
    old_canvas_section = """    // ----------------------------------------------------
    // PROPORTIONAL COVER MEDIA DRAWING HELPER
    // ----------------------------------------------------"""

    new_canvas_listeners = """    // ----------------------------------------------------
    // INTERACTIVE DIRECT DRAGGING FOR SUBTITLE ON CANVAS
    // ----------------------------------------------------
    canvas.addEventListener('mousemove', (e) => {
      const rect = canvas.getBoundingClientRect();
      const scaleX = canvas.width / rect.width;
      const scaleY = canvas.height / rect.height;
      const mouseX = (e.clientX - rect.left) * scaleX;
      const mouseY = (e.clientY - rect.top) * scaleY;

      if (isDraggingSubtitle && currentSubBox) {
        const newBoxY = mouseY - subDragStartY;
        const newBoxX = mouseX - subDragStartX;
        subPosY = Math.max(40, Math.min(canvas.height - currentSubBox.h - 40, newBoxY));
        subPosX = Math.max(-600, Math.min(600, newBoxX - (canvas.width - currentSubBox.w) / 2));

        if (sliderSubPosY) sliderSubPosY.value = Math.round(subPosY);
        if (valSubPosY) valSubPosY.textContent = `${Math.round(subPosY)}px`;
        if (sliderSubPosX) sliderSubPosX.value = Math.round(subPosX);
        if (valSubPosX) valSubPosX.textContent = `${Math.round(subPosX)}px`;

        try { render(previewCurrentSec); } catch(err) {}
        return;
      }

      if (showSubtitles && currentSubBox) {
        if (mouseX >= currentSubBox.x && mouseX <= currentSubBox.x + currentSubBox.w &&
            mouseY >= currentSubBox.y && mouseY <= currentSubBox.y + currentSubBox.h) {
          if (!isHoveringSubtitle) {
            isHoveringSubtitle = true;
            canvas.style.cursor = 'grab';
            try { render(previewCurrentSec); } catch(err) {}
          }
          return;
        }
      }

      if (isHoveringSubtitle) {
        isHoveringSubtitle = false;
        canvas.style.cursor = 'default';
        try { render(previewCurrentSec); } catch(err) {}
      }
    });

    canvas.addEventListener('mousedown', (e) => {
      if (!showSubtitles || !currentSubBox) return;
      const rect = canvas.getBoundingClientRect();
      const scaleX = canvas.width / rect.width;
      const scaleY = canvas.height / rect.height;
      const mouseX = (e.clientX - rect.left) * scaleX;
      const mouseY = (e.clientY - rect.top) * scaleY;

      if (mouseX >= currentSubBox.x && mouseX <= currentSubBox.x + currentSubBox.w &&
          mouseY >= currentSubBox.y && mouseY <= currentSubBox.y + currentSubBox.h) {
        isDraggingSubtitle = true;
        canvas.style.cursor = 'grabbing';
        subDragStartX = mouseX - currentSubBox.x;
        subDragStartY = mouseY - currentSubBox.y;
        try { render(previewCurrentSec); } catch(err) {}
      }
    });

    window.addEventListener('mouseup', () => {
      if (isDraggingSubtitle) {
        isDraggingSubtitle = false;
        canvas.style.cursor = isHoveringSubtitle ? 'grab' : 'default';
        try { render(previewCurrentSec); } catch(err) {}
      }
    });

    // ----------------------------------------------------
    // PROPORTIONAL COVER MEDIA DRAWING HELPER
    // ----------------------------------------------------"""

    content = content.replace(old_canvas_section, new_canvas_listeners)

    # =========================================================================
    # 9. UPGRADE drawActiveSubtitles ON CANVAS (Position X & Y, Font size, Hover outline)
    # =========================================================================
    old_draw_subs_regex = r'// ----------------------------------------------------\s*// SUBTITLE DRAWING ON CANVAS\s*// ----------------------------------------------------\s*function drawActiveSubtitles\(w, h, timeSec\) \{.*?ctx\.restore\(\);\s*\}'

    new_draw_subs = '''// ----------------------------------------------------
    // SUBTITLE DRAWING ON CANVAS (MOVABLE & HIDEABLE)
    // ----------------------------------------------------
    function drawActiveSubtitles(w, h, timeSec) {
      if (!showSubtitles) {
        currentSubBox = null;
        return;
      }

      let currentSub = null;
      let activeSubIdx = -1;
      for (let i = 0; i < subtitlesList.length; i++) {
        const s = subtitlesList[i];
        if (!s.hidden && timeSec >= s.startSec && timeSec < s.endSec && s.text && s.text.trim()) {
          currentSub = s;
          activeSubIdx = i;
          break;
        }
      }

      // Highlight in sidebar
      subtitlesList.forEach((s, i) => {
        const c = document.getElementById(`sub_card_${s.id}`);
        if (c) {
          if (i === activeSubIdx) c.classList.add('active-now');
          else c.classList.remove('active-now');
        }
      });

      if (!currentSub) {
        currentSubBox = null;
        return;
      }

      ctx.save();
      const subText = currentSub.text;
      ctx.font = `800 ${subFontSize}px "Be Vietnam Pro"`;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';

      const textMetrics = ctx.measureText(subText);
      const boxW = Math.min(w - 80, textMetrics.width + 56);
      const boxH = Math.max(46, subFontSize + 22);

      // Customizable Position X & Y
      let boxX = (w - boxW) / 2 + subPosX;
      boxX = Math.max(40, Math.min(w - boxW - 40, boxX));
      let boxY = Math.max(40, Math.min(h - boxH - 40, subPosY));

      currentSubBox = { x: boxX, y: boxY, w: boxW, h: boxH, subId: currentSub.id };

      // Glassmorphism Capsule Box
      ctx.shadowColor = 'rgba(0, 0, 0, 0.85)';
      ctx.shadowBlur = 18;

      ctx.fillStyle = 'rgba(8, 14, 28, 0.92)';
      ctx.beginPath();
      ctx.roundRect(boxX, boxY, boxW, boxH, 10);
      ctx.fill();

      ctx.strokeStyle = isDraggingSubtitle || isHoveringSubtitle ? '#38BDF8' : 'rgba(255, 107, 0, 0.6)';
      ctx.lineWidth = isDraggingSubtitle || isHoveringSubtitle ? 2.5 : 1.5;
      ctx.stroke();

      // Orange Accent Pill
      ctx.fillStyle = '#FF6B00';
      ctx.fillRect(boxX + 12, boxY + (boxH - 14) / 2, 4, 14);

      // Subtitle Text
      ctx.fillStyle = '#FFFFFF';
      ctx.fillText(subText, boxX + boxW / 2 + 2, boxY + boxH / 2);

      // Interactive Drag Overlay indicator
      if (isHoveringSubtitle || isDraggingSubtitle) {
        ctx.strokeStyle = '#38BDF8';
        ctx.setLineDash([6, 4]);
        ctx.lineWidth = 1.5;
        ctx.strokeRect(boxX - 3, boxY - 3, boxW + 6, boxH + 6);
        ctx.setLineDash([]);

        ctx.fillStyle = 'rgba(56, 189, 248, 0.95)';
        ctx.beginPath();
        ctx.roundRect(boxX + (boxW - 130) / 2, boxY - 22, 130, 18, 4);
        ctx.fill();
        ctx.fillStyle = '#0F172A';
        ctx.font = '700 10.5px sans-serif';
        ctx.fillText('✋ Kéo để di chuyển', boxX + boxW / 2, boxY - 13);
      }

      ctx.restore();
    }'''

    content = re.sub(old_draw_subs_regex, new_draw_subs, content, flags=re.DOTALL)

    # =========================================================================
    # 10. LIVE AUDIO TRIGGERING IN animate LOOP
    # =========================================================================
    old_play_trigger = '''      } else if (isTimelinePlaying) {
        previewCurrentSec = Math.max(0, (previewCurrentSec + delta) % totalDurationSec);
        updatePlayheadPosition(previewCurrentSec);
        if (playbackTimeDisplay) {
          playbackTimeDisplay.textContent = `${formatTimePrecise(previewCurrentSec)} / ${formatTimePrecise(totalDurationSec)}`;
        }
      }'''

    new_play_trigger = '''      } else if (isTimelinePlaying) {
        const prevSec = previewCurrentSec;
        previewCurrentSec = Math.max(0, (previewCurrentSec + delta) % totalDurationSec);
        updatePlayheadPosition(previewCurrentSec);
        if (playbackTimeDisplay) {
          playbackTimeDisplay.textContent = `${formatTimePrecise(previewCurrentSec)} / ${formatTimePrecise(totalDurationSec)}`;
        }

        // Live Audio Playback for enabled SFX
        if (enableSoundFX) {
          soundFxTimeline.forEach(inst => {
            if (!inst.muted) {
              if (prevSec <= inst.timeSec && previewCurrentSec >= inst.timeSec && Math.abs(previewCurrentSec - inst.timeSec) < 0.25) {
                playSyntheticSFX(inst.sfxId);
              }
            }
          });
        }
      }'''

    content = content.replace(old_play_trigger, new_play_trigger)

    # =========================================================================
    # 11. EXPORT STREAM CHECK FOR SFX (Only mix audio if enableSoundFX is true)
    # =========================================================================
    old_export_sfx = '''        // Schedule all SFX timeline events into the destination stream
        soundFxTimeline.forEach(inst => {
          if (inst.timeSec <= targetExportSec) {
            playSyntheticSFX(inst.sfxId, dest, now + inst.timeSec);
          }
        });'''

    new_export_sfx = '''        // Schedule SFX timeline events only if enableSoundFX is active and not muted
        if (enableSoundFX) {
          soundFxTimeline.forEach(inst => {
            if (!inst.muted && inst.timeSec <= targetExportSec) {
              playSyntheticSFX(inst.sfxId, dest, now + inst.timeSec);
            }
          });
        }'''

    content = content.replace(old_export_sfx, new_export_sfx)

    return content

if __name__ == '__main__':
    with open('Tao_Intro_Va_Studio_Thoi_Su_Talk11.html', 'r', encoding='utf-8') as f:
        src = f.read()
    
    updated = update_file_content(src)
    with open('Tao_Intro_Va_Studio_Thoi_Su_Talk11.html', 'w', encoding='utf-8') as f:
        f.write(updated)
    print("Done updating Tao_Intro_Va_Studio_Thoi_Su_Talk11.html, len =", len(updated))
