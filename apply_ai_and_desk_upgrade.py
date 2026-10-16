import os

with open('Tao_Khung_Thoi_Su_Talk11.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. State variables
t1_old = '''    // Google MediaPipe AI Person Segmentation State
    let selfieSegmentation = null;
    let selfieSegmentationReady = false;
    let latestSegmentMask = null;
    let isSegmentingFrame = false;
    let lastSegmentTime = 0;
    let aiMaskCanvas = document.createElement('canvas');
    let aiMaskCtx = aiMaskCanvas.getContext('2d');'''

t1_new = '''    // Google MediaPipe AI Person Segmentation State
    let selfieSegmentation = null;
    let selfieSegmentationReady = false;
    let latestSegmentMask = null;
    let isSegmentingFrame = false;
    let lastSegmentTime = 0;
    let enableAiAntiFlicker = true; // Chống nhấp nháy AI 60FPS
    let enableDeskForegroundOverlay = true; // Tách layout bàn tiền cảnh & ghế hậu cảnh
    let aiTemporalAlphaBuffer = null;
    let aiTemporalBufferWidth = 0;
    let aiTemporalBufferHeight = 0;
    let smoothedAutoLumaFactor = 1.0;
    let aiMaskCanvas = document.createElement('canvas');
    let aiMaskCtx = aiMaskCanvas.getContext('2d', { willReadFrequently: true });
    let offscreenBeautyCanvas = document.createElement('canvas');
    let offscreenBeautyCtx = offscreenBeautyCanvas.getContext('2d');'''

assert t1_old in c, 't1_old not found'
c = c.replace(t1_old, t1_new, 1)

# 2. Image loader
t2_old = '''    const imgStudioTalkshow = createImageLoader(
      '03_ASSETS/Studio_Backgrounds/studio_talk11_talkshow_solo.jpg','''

t2_new = '''    const imgDeskOverlay = createImageLoader(
      '03_ASSETS/Studio_Backgrounds/studio_talk11_talkshow_solo_desk_foreground.png',
      '../03_ASSETS/Studio_Backgrounds/studio_talk11_talkshow_solo_desk_foreground.png',
      '../../03_ASSETS/Studio_Backgrounds/studio_talk11_talkshow_solo_desk_foreground.png',
      '../Studio_Backgrounds/studio_talk11_talkshow_solo_desk_foreground.png'
    );
    const imgStudioTalkshow = createImageLoader(
      '03_ASSETS/Studio_Backgrounds/studio_talk11_talkshow_solo.jpg','''

assert t2_old in c, 't2_old not found'
c = c.replace(t2_old, t2_new, 1)

# 3. Sidebar UI controls
t3_old = '''            <!-- Sliders: Tolerance / AI Confidence, Feather, Despill -->
            <div style="display: flex; align-items: center; justify-content: space-between; gap: 6px; font-size: 10px; color: #94A3B8;">
              <span style="min-width: 80px;" id="lblChromaTolerance">🎯 Ngưỡng nhạy AI:</span>
              <input type="range" class="range-slider" id="sliderChromaTolerance" min="10" max="85" value="45" step="1" style="accent-color: #10B981; flex: 1;">
              <span id="valChromaTolerance" style="font-family: monospace; font-size: 9.5px; color: #34D399; min-width: 28px; text-align: right;">45%</span>
            </div>

            <div style="display: flex; align-items: center; justify-content: space-between; gap: 6px; font-size: 10px; color: #94A3B8;">
              <span style="min-width: 80px;">✨ Mịn viền tóc & mép:</span>
              <input type="range" class="range-slider" id="sliderChromaFeather" min="0" max="10" value="4" step="1" style="accent-color: #38BDF8; flex: 1;">
              <span id="valChromaFeather" style="font-family: monospace; font-size: 9.5px; color: #38BDF8; min-width: 28px; text-align: right;">4px</span>
            </div>'''

t3_new = '''            <!-- Sliders: Tolerance / AI Confidence, Feather, Despill -->
            <div style="display: flex; align-items: center; justify-content: space-between; gap: 6px; font-size: 10px; color: #94A3B8;">
              <span style="min-width: 90px;" id="lblChromaTolerance" title="Kéo tăng để ôm sát dính người hơn, xóa sạch viền thừa">🎯 Độ ôm sát người:</span>
              <input type="range" class="range-slider" id="sliderChromaTolerance" min="15" max="85" value="52" step="1" style="accent-color: #10B981; flex: 1;">
              <span id="valChromaTolerance" style="font-family: monospace; font-size: 9.5px; color: #34D399; min-width: 28px; text-align: right;">52%</span>
            </div>

            <div style="display: flex; align-items: center; justify-content: space-between; gap: 6px; font-size: 10px; color: #94A3B8;">
              <span style="min-width: 90px;">✨ Mịn viền tóc & mép:</span>
              <input type="range" class="range-slider" id="sliderChromaFeather" min="1" max="10" value="4" step="1" style="accent-color: #38BDF8; flex: 1;">
              <span id="valChromaFeather" style="font-family: monospace; font-size: 9.5px; color: #38BDF8; min-width: 28px; text-align: right;">4px</span>
            </div>

            <!-- CHỐNG NHẤP NHÁY AI 60FPS -->
            <div style="display: flex; align-items: center; justify-content: space-between; background: rgba(16,185,129,0.08); padding: 4px 6px; border-radius: 4px; border: 1px solid rgba(16,185,129,0.25);">
              <label style="cursor: pointer; display: flex; align-items: center; gap: 4px; font-size: 9.5px; font-weight: 700; color: #34D399; margin-bottom: 0;">
                <input type="checkbox" id="chkAiAntiFlicker" checked style="accent-color: #10B981; width: 12px; height: 12px;">
                <span>🛡️ Lọc Khử Nhấp Nháy (Anti-Flicker 60FPS)</span>
              </label>
              <span style="font-size: 8px; color: #6EE7B7;">Mượt viền liên tục</span>
            </div>'''

assert t3_old in c, 't3_old not found'
c = c.replace(t3_old, t3_new, 1)

# Desk UI under chroma card
t3_desk_anchor = '''            <!-- Cắt xén viền ngoài (Crop) -->
            <div style="display: flex; align-items: center; justify-content: space-between; gap: 6px; font-size: 9.5px; color: #94A3B8; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 4px;">
              <span>✂️ Cắt lề ngoài thừa:</span>
              <div style="display: flex; gap: 3px; align-items: center;">
                <input type="number" id="inputCropLeft" min="0" max="40" value="0" style="width: 32px; font-size: 9px; text-align: center; background: #070D1E; border: 1px solid rgba(255,255,255,0.2); color: #FFF; border-radius: 3px;" title="Cắt lề trái (%)">%T
                <input type="number" id="inputCropRight" min="0" max="40" value="0" style="width: 32px; font-size: 9px; text-align: center; background: #070D1E; border: 1px solid rgba(255,255,255,0.2); color: #FFF; border-radius: 3px;" title="Cắt lề phải (%)">%P
                <input type="number" id="inputCropBottom" min="0" max="40" value="0" style="width: 32px; font-size: 9px; text-align: center; background: #070D1E; border: 1px solid rgba(255,255,255,0.2); color: #FFF; border-radius: 3px;" title="Cắt lề đáy (%)">%D
              </div>
            </div>
          </div>'''

t3_desk_insert = '''            <!-- Cắt xén viền ngoài (Crop) -->
            <div style="display: flex; align-items: center; justify-content: space-between; gap: 6px; font-size: 9.5px; color: #94A3B8; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 4px;">
              <span>✂️ Cắt lề ngoài thừa:</span>
              <div style="display: flex; gap: 3px; align-items: center;">
                <input type="number" id="inputCropLeft" min="0" max="40" value="0" style="width: 32px; font-size: 9px; text-align: center; background: #070D1E; border: 1px solid rgba(255,255,255,0.2); color: #FFF; border-radius: 3px;" title="Cắt lề trái (%)">%T
                <input type="number" id="inputCropRight" min="0" max="40" value="0" style="width: 32px; font-size: 9px; text-align: center; background: #070D1E; border: 1px solid rgba(255,255,255,0.2); color: #FFF; border-radius: 3px;" title="Cắt lề phải (%)">%P
                <input type="number" id="inputCropBottom" min="0" max="40" value="0" style="width: 32px; font-size: 9px; text-align: center; background: #070D1E; border: 1px solid rgba(255,255,255,0.2); color: #FFF; border-radius: 3px;" title="Cắt lề đáy (%)">%D
              </div>
            </div>
          </div>

          <!-- BỐ CỤC BÀN TIỀN CẢNH: BTV NHÍ NGỒI GIỮA BÀN VÀ GHẾ -->
          <div style="background: rgba(255, 107, 0, 0.08); border: 1.5px solid rgba(255, 107, 0, 0.4); border-radius: 7px; padding: 7px 9px; display: flex; flex-direction: column; gap: 4px; margin-top: 5px;">
            <div style="display: flex; align-items: center; justify-content: space-between;">
              <label style="cursor: pointer; display: flex; align-items: center; gap: 5px; font-size: 10.5px; font-weight: 800; color: #FFB703; margin-bottom: 0;">
                <input type="checkbox" id="chkEnableDeskOverlay" checked style="accent-color: #FF6B00; width: 13px; height: 13px;">
                <span>🎙️ Tách Bàn Tiền Cảnh (Bé Ngồi Sau Bàn & Trước Ghế)</span>
              </label>
              <span style="font-size: 8.5px; color: #FFB703; font-weight: 700; background: rgba(255,107,0,0.2); padding: 1px 5px; border-radius: 4px;">Studio 3 Lớp</span>
            </div>
            <div style="font-size: 8.5px; color: #94A3B8; line-height: 1.35;">
              ✨ Tự động đưa Bàn, Máy tính bảng & Mic lên trước BTV nhí, ghế ở sau lưng bé. Tạo cảm giác trường quay 3D chân thực!
            </div>
          </div>'''

assert t3_desk_anchor in c, 't3_desk_anchor not found'
c = c.replace(t3_desk_anchor, t3_desk_insert, 1)

# 4. processStudentChromaKey AI mask
t4_old = '''        if (latestSegmentMask) {
          // Composite person mask: keep ONLY the child's body and face!
          offscreenKeyCtx.globalCompositeOperation = 'destination-in';
          offscreenKeyCtx.drawImage(latestSegmentMask, 0, 0, procW, procH);
          offscreenKeyCtx.globalCompositeOperation = 'source-over';'''

t4_new = '''        if (latestSegmentMask) {
          if (aiMaskCanvas.width !== procW || aiMaskCanvas.height !== procH) {
            aiMaskCanvas.width = procW;
            aiMaskCanvas.height = procH;
            aiTemporalAlphaBuffer = new Float32Array(procW * procH);
            aiTemporalBufferWidth = procW;
            aiTemporalBufferHeight = procH;
          }

          // 1. Draw raw AI probability mask from MediaPipe onto aiMaskCanvas
          aiMaskCtx.globalCompositeOperation = 'source-over';
          aiMaskCtx.clearRect(0, 0, procW, procH);
          aiMaskCtx.drawImage(latestSegmentMask, 0, 0, procW, procH);

          // 2. High-Precision Mask Post-Processing: Tight Edge Hugging & Temporal Anti-Flicker
          const maskImgData = aiMaskCtx.getImageData(0, 0, procW, procH);
          const mData = maskImgData.data;
          const totalPix = procW * procH;

          // studentChromaTolerance (15% - 85%, default ~52%):
          // Kéo tăng để ôm sát dính người hơn nữa, loại bỏ triệt để viền thừa phòng gần người
          const tol = (typeof studentChromaTolerance === 'number') ? studentChromaTolerance : 0.52;
          const cutoff = 70 + tol * 135;
          const featherWidth = Math.max(10, (studentChromaFeather || 4) * 3.5);
          const blendAlpha = enableAiAntiFlicker ? 0.68 : 1.0;

          if (!aiTemporalAlphaBuffer || aiTemporalAlphaBuffer.length !== totalPix) {
            aiTemporalAlphaBuffer = new Float32Array(totalPix);
          }

          for (let p = 0; p < totalPix; p++) {
            const idx = p * 4;
            const rawProb = Math.max(mData[idx], mData[idx + 1], mData[idx + 2], mData[idx + 3]);

            let targetA = 0;
            if (rawProb <= cutoff) {
              targetA = 0; // Cắt dứt khoát 100% phần viền phòng thừa xung quanh!
            } else if (rawProb < cutoff + featherWidth) {
              const t = (rawProb - cutoff) / featherWidth;
              targetA = Math.round(255 * (t * t * (3 - 2 * t))); // Smoothstep S-curve chống răng cưa
            } else {
              targetA = 255;
            }

            // Lọc thời gian khử nhấp nháy liên tục (Temporal Exponential Moving Average)
            if (enableAiAntiFlicker) {
              const prevA = aiTemporalAlphaBuffer[p];
              const smoothA = prevA * (1 - blendAlpha) + targetA * blendAlpha;
              aiTemporalAlphaBuffer[p] = smoothA;
              const finalA = Math.round(smoothA);
              mData[idx + 3] = finalA;
              mData[idx] = mData[idx + 1] = mData[idx + 2] = finalA;
            } else {
              mData[idx + 3] = targetA;
              mData[idx] = mData[idx + 1] = mData[idx + 2] = targetA;
            }
          }

          aiMaskCtx.putImageData(maskImgData, 0, 0);

          // Áp dụng mặt nạ đã ôm sát và khử rung nhấp nháy vào video BTV nhí
          offscreenKeyCtx.globalCompositeOperation = 'destination-in';
          offscreenKeyCtx.drawImage(aiMaskCanvas, 0, 0, procW, procH);
          offscreenKeyCtx.globalCompositeOperation = 'source-over';'''

assert t4_old in c, 't4_old not found'
c = c.replace(t4_old, t4_new, 1)

# 5. drawStudentCharacter lighting & beauty filter
t5_light_old = '''      // 1. AUTO LIGHTING (DYNAMIC LUMA LIFT FOR DARK ROOM FOOTAGE)
      let autoLumaFactor = 1.0;
      if (enableAutoLighting) {
        const luma = getSampledLuma(processedCanvas);
        if (luma < 122) {
          // Smoothly boost exposure up to 1.45x
          autoLumaFactor = Math.min(1.45, Math.max(1.0, 126 / Math.max(35, luma)));
        }
      }

      // 2. BASE BEAUTY FILTER LAYER (Tích hợp độ sắc nét bằng GPU không gây giật lag)
      let filterList = [];
      const sharpnessBoost = (enableBeauty && beautySharpness > 0) ? (beautySharpness / 100) * 0.22 : 0;
      if (enableBeauty) {
        const finalBrightness = beautyBrightness * autoLumaFactor;
        const finalContrast = (beautyContrast * (1.0 + sharpnessBoost)).toFixed(2);
        filterList.push(`brightness(${finalBrightness.toFixed(2)})`);
        filterList.push(`contrast(${finalContrast})`);
        filterList.push(`saturate(${beautySaturation})`);
        if (beautyWarmth !== 0) {
          filterList.push(`hue-rotate(${beautyWarmth}deg)`);
        }
      } else if (autoLumaFactor > 1.0) {
        filterList.push(`brightness(${autoLumaFactor.toFixed(2)})`);
      }'''

t5_light_new = '''      // 1. AUTO LIGHTING (DYNAMIC LUMA LIFT WITH SMOOTH CONTINUOUS INTERPOLATION - ZERO STROBE)
      if (enableAutoLighting) {
        const luma = getSampledLuma(processedCanvas);
        let targetLuma = 1.0;
        if (luma < 122) {
          targetLuma = Math.min(1.40, Math.max(1.0, 126 / Math.max(35, luma)));
        }
        smoothedAutoLumaFactor = smoothedAutoLumaFactor * 0.90 + targetLuma * 0.10;
      } else {
        smoothedAutoLumaFactor = 1.0;
      }

      // 2. BASE BEAUTY FILTER LAYER (Tích hợp độ sắc nét bằng GPU không gây giật lag)
      let filterList = [];
      const sharpnessBoost = (enableBeauty && beautySharpness > 0) ? (beautySharpness / 100) * 0.22 : 0;
      if (enableBeauty) {
        const finalBrightness = (beautyBrightness * smoothedAutoLumaFactor).toFixed(2);
        const finalContrast = (beautyContrast * (1.0 + sharpnessBoost)).toFixed(2);
        filterList.push(`brightness(${finalBrightness})`);
        filterList.push(`contrast(${finalContrast})`);
        filterList.push(`saturate(${beautySaturation})`);
        if (beautyWarmth !== 0) {
          filterList.push(`hue-rotate(${beautyWarmth}deg)`);
        }
      } else if (smoothedAutoLumaFactor > 1.0) {
        filterList.push(`brightness(${smoothedAutoLumaFactor.toFixed(2)})`);
      }'''

assert t5_light_old in c, 't5_light_old not found'
c = c.replace(t5_light_old, t5_light_new, 1)

# Skin smoothing clamp
t5_smooth_old = '''        // Soft skin smoothing / glow overlay
        if (enableBeauty && beautySmoothness > 0) {
          ctx.save();
          ctx.globalAlpha = beautySmoothness * 0.38;
          ctx.filter = `blur(${Math.max(2, Math.round(beautySmoothness * 8))}px) brightness(1.12) saturate(1.15)`;
          ctx.drawImage(processedCanvas, x0, y0, charW, charH);
          ctx.restore();
        }'''

t5_smooth_new = '''        // Soft skin smoothing / glow overlay (Khóa chặt trong người, không loang ra ngoài nền, chống nhấp nháy 100%)
        if (enableBeauty && beautySmoothness > 0) {
          if (offscreenBeautyCanvas.width !== processedCanvas.width || offscreenBeautyCanvas.height !== processedCanvas.height) {
            offscreenBeautyCanvas.width = processedCanvas.width;
            offscreenBeautyCanvas.height = processedCanvas.height;
          }
          offscreenBeautyCtx.save();
          offscreenBeautyCtx.clearRect(0, 0, processedCanvas.width, processedCanvas.height);
          offscreenBeautyCtx.filter = `blur(${Math.max(2, Math.round(beautySmoothness * 6))}px) brightness(1.10) saturate(1.12)`;
          offscreenBeautyCtx.drawImage(processedCanvas, 0, 0);
          offscreenBeautyCtx.globalCompositeOperation = 'destination-in';
          offscreenBeautyCtx.filter = 'none';
          offscreenBeautyCtx.drawImage(processedCanvas, 0, 0);
          offscreenBeautyCtx.restore();

          ctx.save();
          ctx.globalAlpha = beautySmoothness * 0.35;
          ctx.drawImage(offscreenBeautyCanvas, x0, y0, charW, charH);
          ctx.restore();
        }'''

assert t5_smooth_old in c, 't5_smooth_old not found'
c = c.replace(t5_smooth_old, t5_smooth_new, 1)

# 6. Render loop desk overlay
t6_old = '''      // ============================================================
      // DRAW STUDENT CHARACTER HOST / ANCHOR (CHROMA KEY & BEAUTY)
      // ============================================================
      if (selectedExportMode !== 'greenscreen') {
        drawStudentCharacter(ctx, w, h, timeSec);
      }'''

t6_new = '''      // ============================================================
      // DRAW STUDENT CHARACTER HOST / ANCHOR (CHROMA KEY & BEAUTY)
      // ============================================================
      if (selectedExportMode !== 'greenscreen') {
        drawStudentCharacter(ctx, w, h, timeSec);
      }

      // ============================================================
      // DRAW STUDIO DESK FOREGROUND OVERLAY (BÀN TIỀN CẢNH & CÁC VẬT TRÊN BÀN)
      // Tách riêng cụm bàn, máy tính bảng & mic ra trước mặt bé; ghế ở sau lưng bé!
      // ============================================================
      if (enableDeskForegroundOverlay && selectedStudioTheme === 'talk11_talkshow') {
        if (imgDeskOverlay && (imgDeskOverlay._loaded || (imgDeskOverlay.complete && imgDeskOverlay.naturalWidth > 0))) {
          ctx.save();
          if (selectedAspectRatio === '9:16') {
            ctx.drawImage(imgDeskOverlay, (w - 1920) / 2, (h - 1080) / 2, 1920, 1080);
          } else {
            ctx.drawImage(imgDeskOverlay, 0, 0, w, h);
          }
          ctx.restore();
        }
      }'''

assert t6_old in c, 't6_old not found'
c = c.replace(t6_old, t6_new, 1)

# 7. Event listeners
t7_old = '''    document.getElementById('sliderChromaTolerance')?.addEventListener('input', (e) => {
      const val = parseInt(e.target.value) || 38;
      studentChromaTolerance = val / 100;
      const lbl = document.getElementById('valChromaTolerance');
      if (lbl) lbl.textContent = `${val}%`;
      try { render(previewCurrentSec); } catch(err) {}
    });'''

t7_new = '''    document.getElementById('sliderChromaTolerance')?.addEventListener('input', (e) => {
      const val = parseInt(e.target.value) || 52;
      studentChromaTolerance = val / 100;
      const lbl = document.getElementById('valChromaTolerance');
      if (lbl) lbl.textContent = `${val}%`;
      try { render(previewCurrentSec); } catch(err) {}
    });

    document.getElementById('chkAiAntiFlicker')?.addEventListener('change', (e) => {
      enableAiAntiFlicker = e.target.checked;
      try { render(previewCurrentSec); } catch(err) {}
    });

    document.getElementById('chkEnableDeskOverlay')?.addEventListener('change', (e) => {
      enableDeskForegroundOverlay = e.target.checked;
      try { render(previewCurrentSec); } catch(err) {}
    });'''

assert t7_old in c, 't7_old not found'
c = c.replace(t7_old, t7_new, 1)

with open('Tao_Khung_Thoi_Su_Talk11.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('Successfully applied all AI & Desk upgrades to Tao_Khung_Thoi_Su_Talk11.html!')
