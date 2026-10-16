# -*- coding: utf-8 -*-
import sys
import re

print("Reading Tao_Intro_Va_Studio_Thoi_Su_Talk11.html...")
with open('Tao_Intro_Va_Studio_Thoi_Su_Talk11.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Read fix-webm-duration.js
with open('03_ASSETS/fix-webm-duration.js', 'r', encoding='utf-8') as f:
    fix_webm_code = f.read()

# 2. Add CSS styles for Persistent Media Vault
css_to_add = """
    /* PERSISTENT MEDIA VAULT STYLING */
    .vault-card {
      border: 1.5px solid #10B981;
      background: linear-gradient(180deg, rgba(16, 185, 129, 0.12) 0%, rgba(10, 17, 36, 0.95) 100%);
      box-shadow: 0 4px 18px rgba(16, 185, 129, 0.18);
      border-radius: 9px;
      padding: 10px;
      margin-bottom: 8px;
    }
    .vault-item-card {
      background: rgba(15, 23, 42, 0.92);
      border: 1px solid rgba(16, 185, 129, 0.35);
      border-radius: 6px;
      padding: 5px;
      display: flex;
      flex-direction: column;
      gap: 3px;
      position: relative;
      transition: all 0.2s ease;
    }
    .vault-item-card:hover {
      border-color: #10B981;
      box-shadow: 0 0 10px rgba(16, 185, 129, 0.4);
      transform: translateY(-1px);
    }
    .vault-thumb {
      width: 100%;
      height: 52px;
      object-fit: cover;
      border-radius: 4px;
      background: #000;
    }
    .vault-item-name {
      font-size: 9.5px;
      font-weight: 700;
      color: #F8FAFC;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .vault-item-meta {
      font-size: 8.5px;
      color: #94A3B8;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .vault-btn-use {
      background: rgba(16, 185, 129, 0.25);
      border: 1px solid #10B981;
      color: #A7F3D0;
      font-size: 9px;
      font-weight: 700;
      padding: 2px 5px;
      border-radius: 4px;
      cursor: pointer;
      text-align: center;
      transition: background 0.15s;
    }
    .vault-btn-use:hover {
      background: #10B981;
      color: #FFFFFF;
    }
    .vault-btn-del {
      background: rgba(239, 68, 68, 0.2);
      border: 1px solid rgba(239, 68, 68, 0.4);
      color: #FCA5A5;
      font-size: 9px;
      padding: 1px 4px;
      border-radius: 3px;
      cursor: pointer;
    }
    .vault-btn-del:hover {
      background: #EF4444;
      color: #FFFFFF;
    }
"""

if '.vault-card {' not in content:
    content = content.replace('  </style>', css_to_add + '\n  </style>')
    print("Added CSS styles.")

# 3. Add Media Vault HTML component right before <!-- BỘ CHỌN TRƯỜNG QUAY ẢO (VIRTUAL STUDIO THEME) -->
vault_html = """      <!-- ======================================================== -->
      <!-- 0. KHO MEDIA TỔNG & BỘ NHỚ LƯU TRỮ TỰ ĐỘNG (PERSISTENT VAULT) -->
      <!-- ======================================================== -->
      <div class="card-box vault-card" id="mediaVaultCard">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 5px;">
          <div style="display: flex; align-items: center; gap: 6px;">
            <span style="font-size: 14px;">🗄️</span>
            <span style="font-size: 11px; font-weight: 900; color: #34D399; letter-spacing: 0.3px;">KHO MEDIA ĐÃ TẢI LÊN (BỘ NHỚ TỰ ĐỘNG)</span>
          </div>
          <span id="vaultBadgeCount" style="font-size: 9.5px; font-weight: 800; background: rgba(16,185,129,0.25); color: #A7F3D0; border: 1px solid #10B981; padding: 1px 7px; border-radius: 10px;">0 Media</span>
        </div>

        <div style="font-size: 9.5px; color: #94A3B8; line-height: 1.35; margin-bottom: 7px;">
          💾 Mọi ảnh & video bạn tải lên được lưu <b>vĩnh viễn trong trình duyệt</b>. Lần sau hoặc khi có lỗi, chỉ cần bấm <b>"Khôi Phục Vào TV"</b> là nạp lại ngay lập tức mà không phải up lại từ đầu!
        </div>

        <!-- Master Action Buttons -->
        <div style="display: flex; gap: 4px; margin-bottom: 7px;">
          <button type="button" class="btn" id="btnRestoreVaultToTv" style="flex: 1.3; justify-content: center; background: linear-gradient(135deg, #10B981 0%, #059669 100%); color: white; padding: 4px 6px; font-size: 10px; box-shadow: 0 2px 8px rgba(16,185,129,0.3);" title="Tự động nạp toàn bộ ảnh & video trong kho vào màn hình TV trường quay">
            🔄 Khôi Phục Vào TV
          </button>
          <button type="button" class="btn" id="btnUploadToVault" style="flex: 1; justify-content: center; background: rgba(255,107,0,0.2); border: 1px solid #FF6B00; color: #FFB703; padding: 4px 6px; font-size: 10px;" title="Tải thêm ảnh/video từ máy tính vào kho lưu trữ">
            ➕ Tải Vào Kho
          </button>
          <button type="button" class="btn" id="btnClearVault" style="background: rgba(239,68,68,0.15); border: 1px solid rgba(239,68,68,0.4); color: #FCA5A5; padding: 4px 6px; font-size: 10px;" title="Xóa toàn bộ kho dữ liệu đã lưu">
            🗑️
          </button>
          <input type="file" id="inputVaultMultiFile" accept="image/*,video/*" multiple style="display: none;">
        </div>

        <!-- Media Vault Grid -->
        <div id="mediaVaultEmptyState" style="text-align: center; padding: 8px 4px; border: 1px dashed rgba(16,185,129,0.3); border-radius: 6px; background: rgba(6,10,20,0.5); font-size: 10px; color: #64748B;">
          Chưa có media nào. Tải ảnh/video ở dưới hoặc bấm "➕ Tải Vào Kho".
        </div>
        <div id="mediaVaultGrid" style="display: none; grid-template-columns: repeat(2, 1fr); gap: 5px; max-height: 160px; overflow-y: auto; padding-right: 2px;">
          <!-- Dynamically populated cards -->
        </div>
      </div>

"""

target_str = "<!-- BỘ CHỌN TRƯỜNG QUAY ẢO (VIRTUAL STUDIO THEME) -->"
if 'id="mediaVaultCard"' not in content:
    content = content.replace(target_str, vault_html + target_str)
    print("Added Media Vault HTML component before studio theme selector.")

# 4. Enhance exportModal with metrics for long video export
old_modal_progress = """      <div style="display: flex; justify-content: space-between; font-size: 12px; color: var(--gold); font-family: 'JetBrains Mono';">
        <span id="modalPercent">0%</span>
        <span><span id="modalTimeElapsed">00:00</span> / <span id="modalTimeTotal">01:00</span></span>
      </div>"""

new_modal_progress = """      <div style="display: flex; justify-content: space-between; font-size: 12px; color: var(--gold); font-family: 'JetBrains Mono';">
        <span id="modalPercent">0%</span>
        <span><span id="modalTimeElapsed">00:00</span> / <span id="modalTimeTotal">01:00</span></span>
      </div>

      <!-- Real-time metrics for long video export -->
      <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px; padding: 6px 10px; background: rgba(10,17,36,0.75); border: 1px solid rgba(255,107,0,0.3); border-radius: 6px; font-size: 11px; color: #94A3B8; font-family: 'JetBrains Mono';">
        <span>💾 Đã ghi: <b id="modalDataSize" style="color: #38BDF8;">0.0 MB</b></span>
        <span>⏳ Còn lại: <b id="modalEstimatedRemaining" style="color: #FBBF24;">--:--</b></span>
      </div>

      <div style="font-size: 10px; color: #10B981; margin-top: 6px; line-height: 1.4; display: flex; align-items: center; gap: 5px;">
        <span>🛡️</span> <span>Đã bật <b>WakeLock</b> (chống tắt màn hình) & <b>Bộ đệm nền</b> mượt mà cho video dài.</span>
      </div>"""

if 'id="modalDataSize"' not in content:
    content = content.replace(old_modal_progress, new_modal_progress)
    print("Enhanced exportModal HTML.")

# 5. Insert fix-webm-duration and IndexedDB Vault Script right after <script>
vault_js = """
    // ====================================================
    // 0. FIX WEBM DURATION (EBML DURATION INJECTOR)
    // ====================================================
""" + fix_webm_code + """

    // ====================================================
    // PERSISTENT MEDIA VAULT (INDEXEDDB STORAGE SYSTEM)
    // ====================================================
    const VAULT_DB_NAME = 'TALK11_STUDIO_VAULT_DB';
    const VAULT_DB_VERSION = 1;
    const VAULT_STORE = 'media_vault';

    let vaultDbInstance = null;

    function getVaultDB() {
      return new Promise((resolve, reject) => {
        if (vaultDbInstance) return resolve(vaultDbInstance);
        const req = indexedDB.open(VAULT_DB_NAME, VAULT_DB_VERSION);
        req.onupgradeneeded = (e) => {
          const db = e.target.result;
          if (!db.objectStoreNames.contains(VAULT_STORE)) {
            db.createObjectStore(VAULT_STORE, { keyPath: 'id' });
          }
        };
        req.onsuccess = (e) => {
          vaultDbInstance = e.target.result;
          resolve(vaultDbInstance);
        };
        req.onerror = (e) => reject(e.target.error);
      });
    }

    async function saveMediaToVault(file, source = 'user_upload') {
      if (!file) return;
      try {
        const db = await getVaultDB();
        const id = 'vault_' + Date.now() + '_' + Math.random().toString(36).substr(2, 6);
        const isVid = file.type.startsWith('video/');
        
        // Tạo ảnh thu nhỏ (thumbnail) nhẹ và nhanh
        let thumbUrl = '';
        if (!isVid) {
          thumbUrl = await new Promise((resolve) => {
            const reader = new FileReader();
            reader.onload = (e) => {
              const img = new Image();
              img.onload = () => {
                const c = document.createElement('canvas');
                c.width = 160; c.height = 90;
                const ctx = c.getContext('2d');
                ctx.drawImage(img, 0, 0, 160, 90);
                resolve(c.toDataURL('image/jpeg', 0.8));
              };
              img.onerror = () => resolve('');
              img.src = e.target.result;
            };
            reader.readAsDataURL(file);
          });
        }

        const item = {
          id,
          name: file.name,
          type: isVid ? 'video' : 'image',
          mimeType: file.type,
          size: file.size,
          blob: file,
          thumbUrl,
          source,
          createdAt: Date.now()
        };

        const tx = db.transaction(VAULT_STORE, 'readwrite');
        tx.objectStore(VAULT_STORE).put(item);
        tx.oncomplete = () => {
          renderVaultUI();
        };
      } catch (err) {
        console.warn('Lỗi lưu vào kho media:', err);
      }
    }

    async function getAllVaultItems() {
      try {
        const db = await getVaultDB();
        return new Promise((resolve, reject) => {
          const tx = db.transaction(VAULT_STORE, 'readonly');
          const req = tx.objectStore(VAULT_STORE).getAll();
          req.onsuccess = () => resolve(req.result || []);
          req.onerror = () => reject(req.error);
        });
      } catch (e) {
        return [];
      }
    }

    async function deleteVaultItem(id) {
      try {
        const db = await getVaultDB();
        const tx = db.transaction(VAULT_STORE, 'readwrite');
        tx.objectStore(VAULT_STORE).delete(id);
        tx.oncomplete = () => {
          renderVaultUI();
          showToast('Đã xóa media khỏi kho lưu trữ');
        };
      } catch (e) {
        console.error(e);
      }
    }

    async function clearAllVault() {
      if (!confirm('Bạn có chắc muốn xóa sạch toàn bộ hình ảnh và video trong kho lưu trữ không?')) return;
      try {
        const db = await getVaultDB();
        const tx = db.transaction(VAULT_STORE, 'readwrite');
        tx.objectStore(VAULT_STORE).clear();
        tx.oncomplete = () => {
          renderVaultUI();
          showToast('Đã dọn sạch kho lưu trữ');
        };
      } catch (e) {
        console.error(e);
      }
    }

    async function renderVaultUI() {
      const badge = document.getElementById('vaultBadgeCount');
      const emptyState = document.getElementById('mediaVaultEmptyState');
      const grid = document.getElementById('mediaVaultGrid');
      if (!grid) return;

      const items = await getAllVaultItems();
      items.sort((a, b) => b.createdAt - a.createdAt);

      if (badge) badge.textContent = `${items.length} Media`;

      if (items.length === 0) {
        if (emptyState) emptyState.style.display = 'block';
        grid.style.display = 'none';
        grid.innerHTML = '';
        return;
      }

      if (emptyState) emptyState.style.display = 'none';
      grid.style.display = 'grid';
      grid.innerHTML = '';

      items.forEach(it => {
        const card = document.createElement('div');
        card.className = 'vault-item-card';

        const sizeMb = (it.size / (1024 * 1024)).toFixed(1);
        const typeIcon = it.type === 'video' ? '🎬' : '🖼️';

        let thumbHtml = '';
        if (it.thumbUrl) {
          thumbHtml = `<img src="${it.thumbUrl}" class="vault-thumb" alt="${it.name}">`;
        } else {
          thumbHtml = `<div class="vault-thumb" style="display: flex; align-items: center; justify-content: center; background: #0A1124; color: #10B981; font-size: 20px;">${typeIcon}</div>`;
        }

        card.innerHTML = `
          ${thumbHtml}
          <div class="vault-item-name" title="${it.name}">${it.name}</div>
          <div class="vault-item-meta">
            <span>${typeIcon} ${sizeMb} MB</span>
            <button type="button" class="vault-btn-del" data-id="${it.id}" title="Xóa khỏi kho">🗑️</button>
          </div>
          <button type="button" class="vault-btn-use" data-id="${it.id}" title="Nạp vào màn hình TV trường quay">➕ Nạp Vào TV</button>
        `;

        card.querySelector('.vault-btn-del').addEventListener('click', (e) => {
          e.stopPropagation();
          deleteVaultItem(it.id);
        });

        card.querySelector('.vault-btn-use').addEventListener('click', (e) => {
          e.stopPropagation();
          addVaultItemToTvSlot(it);
        });

        grid.appendChild(card);
      });
    }

    function addVaultItemToTvSlot(item) {
      const clipDur = getNewSlotDuration();
      let currentEnd = 0;
      if (mediaSlots.length > 0) {
        currentEnd = Math.max(...mediaSlots.map(s => s.endSec));
      }

      let elem = null;
      if (item.type === 'video') {
        const vid = document.createElement('video');
        vid.src = URL.createObjectURL(item.blob);
        vid.muted = true;
        vid.loop = true;
        vid.playsInline = true;
        vid.play().catch(() => {});
        elem = vid;
      } else {
        const img = new Image();
        img.src = item.thumbUrl || URL.createObjectURL(item.blob);
        elem = img;
      }

      const newSlot = {
        id: 'slot_' + Date.now(),
        title: (item.type === 'video' ? '🎬 ' : '🖼️ ') + item.name.substring(0, 24),
        mediaType: item.type,
        fileName: item.name,
        mediaElement: elem,
        startSec: currentEnd,
        endSec: currentEnd + clipDur,
        effect: selectedTvTransitionFx || 'tv_pop_bounce'
      };

      mediaSlots.push(newSlot);
      totalDurationSec = Math.max(totalDurationSec, newSlot.endSec);
      syncDurationUI();
      renderMediaSlotsUI();
      renderTimelineTrackBlocks();
      showToast(`✓ Đã nạp "${item.name}" vào TV (+${clipDur}s)!`);
    }

    async function restoreVaultToTimeline() {
      const items = await getAllVaultItems();
      if (items.length === 0) {
        showToast('⚠️ Kho chưa có media nào được lưu! Hãy tải ảnh hoặc video vào kho trước.');
        return;
      }

      items.sort((a, b) => a.createdAt - b.createdAt);

      const clipDur = getNewSlotDuration();
      let currentEnd = 0;
      mediaSlots = [];

      for (let i = 0; i < items.length; i++) {
        const item = items[i];
        let elem = null;
        if (item.type === 'video') {
          const vid = document.createElement('video');
          vid.src = URL.createObjectURL(item.blob);
          vid.muted = true;
          vid.loop = true;
          vid.playsInline = true;
          vid.play().catch(() => {});
          elem = vid;
        } else {
          const img = new Image();
          img.src = item.thumbUrl || URL.createObjectURL(item.blob);
          elem = img;
        }

        const slot = {
          id: 'slot_restored_' + item.id + '_' + i,
          title: (item.type === 'video' ? '🎬 ' : '🖼️ ') + item.name.substring(0, 24),
          mediaType: item.type,
          fileName: item.name,
          mediaElement: elem,
          startSec: currentEnd,
          endSec: currentEnd + clipDur,
          effect: selectedTvTransitionFx || 'tv_pop_bounce'
        };

        currentEnd = slot.endSec;
        mediaSlots.push(slot);
      }

      totalDurationSec = Math.max(currentEnd, 15);
      syncDurationUI();
      renderMediaSlotsUI();
      renderTimelineTrackBlocks();
      updatePlayheadPosition(0);
      try { render(0); } catch(e) {}
      showToast(`✓ Đã khôi phục thành công ${items.length} media vào TV (Tổng: ${totalDurationSec}s)!`);
    }

    // Screen WakeLock for Long Video Exports
    let screenWakeLock = null;
    async function requestWakeLock() {
      try {
        if ('wakeLock' in navigator) {
          screenWakeLock = await navigator.wakeLock.request('screen');
        }
      } catch (err) {
        console.warn('WakeLock:', err);
      }
    }
    function releaseWakeLock() {
      if (screenWakeLock) {
        screenWakeLock.release().catch(() => {});
        screenWakeLock = null;
      }
    }

    let recordingIntervalTimer = null;
"""

if 'VAULT_STORE =' not in content:
    content = content.replace('  <script>', '  <script>\n' + vault_js)
    print("Injected fix-webm-duration and Vault JS module.")

# 6. Hook saveMediaToVault into handleFileForSlot and handleMultipleFilesDrop
old_handle_file = """    function handleFileForSlot(slot, file) {
      slot.fileName = file.name;"""
new_handle_file = """    function handleFileForSlot(slot, file) {
      slot.fileName = file.name;
      try { saveMediaToVault(file, 'tv_slot'); } catch(e) {}"""
if 'try { saveMediaToVault(file' not in content:
    content = content.replace(old_handle_file, new_handle_file)
    print("Hooked saveMediaToVault into handleFileForSlot.")

old_multi_drop = """      for (let i = 0; i < files.length; i++) {
        const f = files[i];"""
new_multi_drop = """      for (let i = 0; i < files.length; i++) {
        const f = files[i];
        try { saveMediaToVault(f, 'tv_slot_batch'); } catch(e) {}"""
if "saveMediaToVault(f, 'tv_slot_batch')" not in content:
    content = content.replace(old_multi_drop, new_multi_drop)
    print("Hooked saveMediaToVault into handleMultipleFilesDrop.")

# 7. Wire up vault UI buttons
vault_buttons_init = """
    // WIRE UP MEDIA VAULT CONTROLS
    const btnRestoreVaultToTv = document.getElementById('btnRestoreVaultToTv');
    if (btnRestoreVaultToTv) {
      btnRestoreVaultToTv.addEventListener('click', () => {
        restoreVaultToTimeline();
      });
    }

    const btnUploadToVault = document.getElementById('btnUploadToVault');
    const inputVaultMultiFile = document.getElementById('inputVaultMultiFile');
    if (btnUploadToVault && inputVaultMultiFile) {
      btnUploadToVault.addEventListener('click', () => {
        inputVaultMultiFile.click();
      });
      inputVaultMultiFile.addEventListener('change', async (e) => {
        if (e.target.files && e.target.files.length > 0) {
          const fls = Array.from(e.target.files);
          for (const f of fls) {
            await saveMediaToVault(f, 'vault_direct');
          }
          showToast(`✓ Đã lưu ${fls.length} media vào kho!`);
        }
      });
    }

    const btnClearVault = document.getElementById('btnClearVault');
    if (btnClearVault) {
      btnClearVault.addEventListener('click', () => {
        clearAllVault();
      });
    }
"""

# 8. Update animate loop for long video progress
old_animate_rec = """      if (isRecording) {
        const elapsed = Math.max(0, (performance.now() - recStartTime) / 1000);
        previewCurrentSec = Math.min(targetExportSec, elapsed);

        const progress = Math.min(100, (elapsed / targetExportSec) * 100);
        if (modalProgressBar) modalProgressBar.style.width = `${progress}%`;
        if (modalPercent) modalPercent.textContent = `${Math.round(progress)}%`;
        if (modalTimeElapsed) modalTimeElapsed.textContent = formatTime(elapsed);

        updatePlayheadPosition(previewCurrentSec);"""

new_animate_rec = """      if (isRecording) {
        const elapsed = Math.max(0, (performance.now() - recStartTime) / 1000);
        previewCurrentSec = Math.min(targetExportSec, elapsed);

        const progress = Math.min(100, (elapsed / targetExportSec) * 100);
        if (modalProgressBar) modalProgressBar.style.width = `${progress}%`;
        if (modalPercent) modalPercent.textContent = `${Math.round(progress)}%`;
        if (modalTimeElapsed) modalTimeElapsed.textContent = formatTime(elapsed);

        const remainSec = Math.max(0, targetExportSec - elapsed);
        const modalEst = document.getElementById('modalEstimatedRemaining');
        if (modalEst) modalEst.textContent = `~${formatTime(remainSec)}`;

        updatePlayheadPosition(previewCurrentSec);"""

if 'id="modalEstimatedRemaining"' in content and 'modalEst' not in content:
    content = content.replace(old_animate_rec, new_animate_rec)
    print("Updated animate loop with remaining time estimate.")

# 9. Replace startExport and stopExport with upgraded long video export engine
old_start_export_block = """    function startExport(durationSec) {
      if (isRecording) {
        stopExport();
        return;
      }

      // Tự động kết xuất cho đến đoạn ảnh cuối cùng
      const finalDur = getFinalExportDuration();
      targetExportSec = Math.max(2, durationSec || finalDur);

      let videoStream = null;
      try {
        const captureFn = canvas.captureStream || canvas.mozCaptureStream;
        if (typeof captureFn === 'function') {
          videoStream = captureFn.call(canvas, 60);
        } else {
          throw new Error('NOT_SUPPORTED');
        }
      } catch (e) {
        console.error('CaptureStream error:', e);
        if (window.location.protocol === 'file:' || (e && e.name === 'SecurityError')) {
          const m = document.getElementById('protocolGuideModal');
          if (m) m.classList.add('show');
          return;
        }
        showToast('⚠️ Vui lòng mở trang web trên Chrome hoặc Microsoft Edge để xuất video!');
        return;
      }

      let combinedStream = videoStream;
      try {
        const actx = getAudioCtx();
        const dest = actx.createMediaStreamDestination();
        const now = actx.currentTime;

        // Schedule SFX timeline events only if enableSoundFX is active and not muted
        if (enableSoundFX) {
          soundFxTimeline.forEach(inst => {
            if (!inst.muted && inst.timeSec <= targetExportSec) {
              playSyntheticSFX(inst.sfxId, dest, now + inst.timeSec);
            }
          });
        }

        if (dest.stream) {
          combinedStream = new MediaStream([
            ...videoStream.getVideoTracks(),
            ...dest.stream.getAudioTracks()
          ]);
        }
      } catch (err) {
        combinedStream = videoStream;
      }

      const mimes = [
        'video/webm;codecs=vp9,opus',
        'video/webm;codecs=vp9',
        'video/webm;codecs=h264,opus',
        'video/webm;codecs=h264',
        'video/mp4;codecs=avc1',
        'video/webm',
        'video/mp4'
      ];
      let selectedMime = '';
      for (const m of mimes) {
        if (typeof MediaRecorder !== 'undefined' && MediaRecorder.isTypeSupported && MediaRecorder.isTypeSupported(m)) {
          selectedMime = m;
          break;
        }
      }

      recordedChunks = [];
      try {
        mediaRecorder = selectedMime ? new MediaRecorder(combinedStream, { mimeType: selectedMime, videoBitsPerSecond: 12000000 }) : new MediaRecorder(combinedStream);
      } catch (e1) {
        mediaRecorder = new MediaRecorder(videoStream);
      }

      mediaRecorder.ondataavailable = (e) => {
        if (e.data && e.data.size > 0) recordedChunks.push(e.data);
      };

      mediaRecorder.onstop = () => {
        isRecording = false;
        exportModal.classList.remove('show');

        if (recordedChunks.length === 0) {
          showToast('⚠️ Không có dữ liệu video để tải xuống!');
          return;
        }

        const blob = new Blob(recordedChunks, { type: selectedMime || 'video/webm' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        const rawTitle = (inputVideoTitle ? inputVideoTitle.value : '').trim() || 'BanTin';
        const cleanTitle = rawTitle.replace(/[^a-zA-Z0-9_\\-\\s\\u00C0-\\u024F\\u1EA0-\\u1EF9]/g, '').trim().replace(/\\s+/g, '_').substring(0, 30);
        a.download = `TALK11_${cleanTitle}_${targetExportSec}s_${Date.now()}.webm`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        setTimeout(() => URL.revokeObjectURL(url), 1000);
        showToast('✓ Đã xuất và tải video thành công!');
      };

      // Reset and play videos
      mediaSlots.forEach(s => {
        if (s.mediaType === 'video' && s.mediaElement) {
          try {
            s.mediaElement.currentTime = 0;
            s.mediaElement.muted = true;
            s.mediaElement.loop = true;
            s.mediaElement.play().catch(() => {});
          } catch(e) {}
        }
      });

      previewCurrentSec = 0;
      recStartTime = performance.now();
      lastAnimTimestamp = performance.now();

      mediaRecorder.start(1000);
      isRecording = true;

      modalProgressBar.style.width = '0%';
      modalPercent.textContent = '0%';
      modalTimeElapsed.textContent = '00:00';
      modalTimeTotal.textContent = formatTime(targetExportSec);
      exportModal.classList.add('show');
    }

    function stopExport() {
      if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
      }
      isRecording = false;
    }"""

new_start_export_block = """    let totalRecordedBytes = 0;

    function startExport(durationSec) {
      if (isRecording) {
        stopExport();
        return;
      }

      // Tự động kết xuất cho đến đoạn ảnh cuối cùng
      const finalDur = getFinalExportDuration();
      targetExportSec = Math.max(2, durationSec || finalDur);

      let videoStream = null;
      try {
        const captureFn = canvas.captureStream || canvas.mozCaptureStream;
        if (typeof captureFn === 'function') {
          videoStream = captureFn.call(canvas, 60);
        } else {
          throw new Error('NOT_SUPPORTED');
        }
      } catch (e) {
        console.error('CaptureStream error:', e);
        if (window.location.protocol === 'file:' || (e && e.name === 'SecurityError')) {
          const m = document.getElementById('protocolGuideModal');
          if (m) m.classList.add('show');
          return;
        }
        showToast('⚠️ Vui lòng mở trang web trên Chrome hoặc Microsoft Edge để xuất video!');
        return;
      }

      let combinedStream = videoStream;
      try {
        const actx = getAudioCtx();
        const dest = actx.createMediaStreamDestination();
        const now = actx.currentTime;

        // Schedule SFX timeline events only if enableSoundFX is active and not muted
        if (enableSoundFX) {
          soundFxTimeline.forEach(inst => {
            if (!inst.muted && inst.timeSec <= targetExportSec) {
              playSyntheticSFX(inst.sfxId, dest, now + inst.timeSec);
            }
          });
        }

        if (dest.stream) {
          // Audio keep-alive oscillator to guarantee continuous audio/video synchronization
          try {
            const silentOsc = actx.createOscillator();
            const silentGain = actx.createGain();
            silentGain.gain.setValueAtTime(0.00001, now);
            silentOsc.connect(silentGain);
            silentGain.connect(dest);
            silentOsc.start(now);
            silentOsc.stop(now + targetExportSec + 2);
          } catch(eSilent) {}

          combinedStream = new MediaStream([
            ...videoStream.getVideoTracks(),
            ...dest.stream.getAudioTracks()
          ]);
        }
      } catch (err) {
        combinedStream = videoStream;
      }

      const mimes = [
        'video/webm;codecs=vp9,opus',
        'video/webm;codecs=vp9',
        'video/webm;codecs=h264,opus',
        'video/webm;codecs=h264',
        'video/mp4;codecs=avc1',
        'video/webm',
        'video/mp4'
      ];
      let selectedMime = '';
      for (const m of mimes) {
        if (typeof MediaRecorder !== 'undefined' && MediaRecorder.isTypeSupported && MediaRecorder.isTypeSupported(m)) {
          selectedMime = m;
          break;
        }
      }

      // Tối ưu Bitrate thích ứng thông minh: Video dài dùng 5-6 Mbps để chống tràn RAM trình duyệt
      let exportBitrate = 9000000;
      if (targetExportSec > 300) {
        exportBitrate = 4800000; // 4.8 Mbps cho video > 5 phút (tiết kiệm RAM, hình vẫn Full HD sắc nét)
      } else if (targetExportSec > 60) {
        exportBitrate = 6500000; // 6.5 Mbps cho video 1 - 5 phút
      }

      recordedChunks = [];
      totalRecordedBytes = 0;
      try {
        mediaRecorder = selectedMime ? new MediaRecorder(combinedStream, { mimeType: selectedMime, videoBitsPerSecond: exportBitrate }) : new MediaRecorder(combinedStream);
      } catch (e1) {
        mediaRecorder = new MediaRecorder(videoStream);
      }

      mediaRecorder.ondataavailable = (e) => {
        if (e.data && e.data.size > 0) {
          recordedChunks.push(e.data);
          totalRecordedBytes += e.data.size;
          const mb = (totalRecordedBytes / (1024 * 1024)).toFixed(1);
          const modalDataSize = document.getElementById('modalDataSize');
          if (modalDataSize) modalDataSize.textContent = `${mb} MB`;
        }
      };

      mediaRecorder.onstop = () => {
        isRecording = false;
        releaseWakeLock();
        if (recordingIntervalTimer) {
          clearInterval(recordingIntervalTimer);
          recordingIntervalTimer = null;
        }
        exportModal.classList.remove('show');

        if (recordedChunks.length === 0) {
          showToast('⚠️ Không có dữ liệu video để tải xuống!');
          return;
        }

        const rawBlob = new Blob(recordedChunks, { type: selectedMime || 'video/webm' });
        const durationMs = Math.round(targetExportSec * 1000);

        function triggerDownload(finalBlob) {
          const url = URL.createObjectURL(finalBlob);
          const a = document.createElement('a');
          a.href = url;
          const rawTitle = (inputVideoTitle ? inputVideoTitle.value : '').trim() || 'BanTin';
          const cleanTitle = rawTitle.replace(/[^a-zA-Z0-9_\\-\\s\\u00C0-\\u024F\\u1EA0-\\u1EF9]/g, '').trim().replace(/\\s+/g, '_').substring(0, 30);
          const ext = (selectedMime && selectedMime.includes('mp4')) ? 'mp4' : 'webm';
          a.download = `TALK11_${cleanTitle}_${targetExportSec}s_${Date.now()}.${ext}`;
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);

          // Cực kỳ quan trọng: Cho trình duyệt 3 phút (180,000ms) để ghi file lớn vào ổ đĩa trước khi revoke!
          setTimeout(() => {
            try { URL.revokeObjectURL(url); } catch(e) {}
          }, 180000);

          const sizeMb = (finalBlob.size / (1024 * 1024)).toFixed(1);
          showToast(`✓ Đã xuất và tải video thành công (${sizeMb} MB)!`);
        }

        // Tự động vá Header Duration WebM để CapCut & trình phát tua được video dài
        if (typeof ysFixWebmDuration === 'function' && (!selectedMime || selectedMime.includes('webm'))) {
          try {
            ysFixWebmDuration(rawBlob, durationMs, (fixedBlob) => {
              triggerDownload(fixedBlob);
            });
          } catch(errFix) {
            console.warn('WebM duration fix fallback:', errFix);
            triggerDownload(rawBlob);
          }
        } else {
          triggerDownload(rawBlob);
        }
      };

      // Reset and play videos
      mediaSlots.forEach(s => {
        if (s.mediaType === 'video' && s.mediaElement) {
          try {
            s.mediaElement.currentTime = 0;
            s.mediaElement.muted = true;
            s.mediaElement.loop = true;
            s.mediaElement.play().catch(() => {});
          } catch(e) {}
        }
      });

      previewCurrentSec = 0;
      recStartTime = performance.now();
      lastAnimTimestamp = performance.now();

      mediaRecorder.start(1000);
      isRecording = true;
      requestWakeLock(); // Bật WakeLock chống tắt màn hình

      // Vòng lặp timer phụ: Bảo vệ tốc độ 60FPS khi người dùng ẩn tab hoặc chuyển cửa sổ
      if (recordingIntervalTimer) clearInterval(recordingIntervalTimer);
      recordingIntervalTimer = setInterval(() => {
        if (!isRecording) {
          clearInterval(recordingIntervalTimer);
          recordingIntervalTimer = null;
          return;
        }
        const now = performance.now();
        if (now - lastAnimTimestamp >= 20) {
          animate(now);
        }
      }, 16);

      modalProgressBar.style.width = '0%';
      modalPercent.textContent = '0%';
      modalTimeElapsed.textContent = '00:00';
      modalTimeTotal.textContent = formatTime(targetExportSec);
      const modalDataSize = document.getElementById('modalDataSize');
      if (modalDataSize) modalDataSize.textContent = '0.0 MB';
      const modalEst = document.getElementById('modalEstimatedRemaining');
      if (modalEst) modalEst.textContent = `~${formatTime(targetExportSec)}`;

      exportModal.classList.add('show');
    }

    function stopExport() {
      if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
      }
      isRecording = false;
      releaseWakeLock();
      if (recordingIntervalTimer) {
        clearInterval(recordingIntervalTimer);
        recordingIntervalTimer = null;
      }
    }"""

if 'exportBitrate = 9000000' not in content:
    content = content.replace(old_start_export_block, new_start_export_block)
    print("Replaced export engine with upgraded Long Video Engine.")

# 10. In btnCancelExport:
old_cancel = """    btnCancelExport.addEventListener('click', () => {
      recordedChunks = [];
      stopExport();
      exportModal.classList.remove('show');
      showToast('Đã hủy xuất video');
    });"""

new_cancel = """    btnCancelExport.addEventListener('click', () => {
      recordedChunks = [];
      stopExport();
      releaseWakeLock();
      if (recordingIntervalTimer) {
        clearInterval(recordingIntervalTimer);
        recordingIntervalTimer = null;
      }
      exportModal.classList.remove('show');
      showToast('Đã hủy xuất video');
    });"""

content = content.replace(old_cancel, new_cancel)

# 11. Add vault buttons initialization & renderVaultUI() in init
old_init = """    // Initialize All Components
    initCollapsibleSections();"""

new_init = vault_buttons_init + """
    // Initialize All Components
    initCollapsibleSections();
    try { renderVaultUI(); } catch(eVault) {}"""

if 'btnRestoreVaultToTv.addEventListener' not in content:
    content = content.replace(old_init, new_init)
    print("Wired up vault buttons and init call.")

# Write master file
with open('Tao_Intro_Va_Studio_Thoi_Su_Talk11.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Successfully updated Tao_Intro_Va_Studio_Thoi_Su_Talk11.html ({len(content)} bytes).")
