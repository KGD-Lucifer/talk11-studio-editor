import os
import sys

src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Tao_Khung_Thoi_Su_Talk11.html')
if not os.path.exists(src_path):
    print(f"Error: {src_path} not found")
    sys.exit(1)

with open(src_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update sliderAiErode HTML
old_erode_html = '''            <div style="display: flex; align-items: center; justify-content: space-between; gap: 6px; font-size: 10px; color: #94A3B8;">
              <span style="min-width: 90px;" title="Gọt viền mép (mặc định 0px để giữ 100% ngón tay, tóc tơ và nếp áo)">✂️ Gọt viền mép (nếu cần):</span>
              <input type="range" class="range-slider" id="sliderAiErode" min="0" max="4" value="0" step="1" style="accent-color: #F59E0B; flex: 1;">
              <span id="valAiErode" style="font-family: monospace; font-size: 9.5px; color: #F59E0B; min-width: 28px; text-align: right;">0px</span>
            </div>'''

new_erode_html = '''            <div style="display: flex; align-items: center; justify-content: space-between; gap: 6px; font-size: 10px; color: #94A3B8;">
              <span style="min-width: 90px;" title="Tự động gọt ôm sát mép người, triệt tiêu 100% viền trắng tường phòng (Chuẩn CapCut)">✂️ Gọt viền mép CapCut:</span>
              <input type="range" class="range-slider" id="sliderAiErode" min="0" max="4" value="1" step="1" style="accent-color: #F59E0B; flex: 1;">
              <span id="valAiErode" style="font-family: monospace; font-size: 9.5px; color: #F59E0B; min-width: 28px; text-align: right;">1px</span>
            </div>'''

assert old_erode_html in content, "old_erode_html not found"
content = content.replace(old_erode_html, new_erode_html, 1)

# 2. Update Beauty Preset Pills & Sliders in HTML
old_beauty_html = '''            <!-- Preset làm đẹp 1 chạm (Tối ưu da Trắng Sáng, khử vàng, khử bóng dầu) -->
            <div style="display: flex; gap: 3px; overflow-x: auto; padding-bottom: 2px;" id="beautyPresetPills">
              <button type="button" class="btn-tint-pill active" data-beauty="rosy">🌸 Trắng Sáng</button>
              <button type="button" class="btn-tint-pill" data-beauty="smooth">✨ Trắng Mịn</button>
              <button type="button" class="btn-tint-pill" data-beauty="bright">🌟 Studio Sáng</button>
              <button type="button" class="btn-tint-pill" data-beauty="warm">🎥 Tự Nhiên</button>
              <button type="button" class="btn-tint-pill" data-beauty="none">🚫 Gốc</button>
            </div>

            <!-- Sliders: Smoothness, Brightness, Warmth, Contrast, Saturation -->
            <div style="display: flex; align-items: center; justify-content: space-between; gap: 6px; font-size: 10px; color: #94A3B8;">
              <span style="min-width: 80px;">🌸 Mịn da:</span>
              <input type="range" class="range-slider" id="sliderBeautySmooth" min="0" max="100" value="45" step="5" style="accent-color: #F472B6; flex: 1;">
              <span id="valBeautySmooth" style="font-family: monospace; font-size: 9.5px; color: #F472B6; min-width: 28px; text-align: right;">45%</span>
            </div>

            <div style="display: flex; align-items: center; justify-content: space-between; gap: 6px; font-size: 10px; color: #94A3B8;">
              <span style="min-width: 80px;" title="Nâng sáng trắng khuôn mặt tự nhiên">💡 Sáng mặt:</span>
              <input type="range" class="range-slider" id="sliderBeautyBright" min="80" max="150" value="114" step="2" style="accent-color: #FBBF24; flex: 1;">
              <span id="valBeautyBright" style="font-family: monospace; font-size: 9.5px; color: #FBBF24; min-width: 28px; text-align: right;">114%</span>
            </div>

            <div style="display: flex; align-items: center; justify-content: space-between; gap: 6px; font-size: 10px; color: #94A3B8;">
              <span style="min-width: 80px;" title="Kéo về bên trái để da Trắng Sáng, khử vàng sạm">🌸 Tone da:</span>
              <input type="range" class="range-slider" id="sliderBeautyWarmth" min="-20" max="20" value="-2" step="1" style="accent-color: #FB7185; flex: 1;">
              <span id="valBeautyWarmth" style="font-family: monospace; font-size: 9.5px; color: #FB7185; min-width: 28px; text-align: right;">-2° (Trắng Sáng)</span>
            </div>

            <div style="display: flex; align-items: center; justify-content: space-between; gap: 6px; font-size: 10px; color: #94A3B8;">
              <span style="min-width: 80px;" title="Giữ 100% để da mịn tự nhiên, khử triệt để bóng dầu và nhờn mặt">👁️ Tương phản:</span>
              <input type="range" class="range-slider" id="sliderBeautyContrast" min="90" max="140" value="100" step="2" style="accent-color: #38BDF8; flex: 1;">
              <span id="valBeautyContrast" style="font-family: monospace; font-size: 9.5px; color: #38BDF8; min-width: 28px; text-align: right;">100%</span>
            </div>

            <div style="display: flex; align-items: center; justify-content: space-between; gap: 6px; font-size: 10px; color: #94A3B8;">
              <span style="min-width: 80px;" title="Khử vàng rực, làm da trắng trong trẻo">🎨 Bão hòa:</span>
              <input type="range" class="range-slider" id="sliderBeautySat" min="80" max="150" value="98" step="2" style="accent-color: #34D399; flex: 1;">
              <span id="valBeautySat" style="font-family: monospace; font-size: 9.5px; color: #34D399; min-width: 28px; text-align: right;">98%</span>
            </div>'''

new_beauty_html = '''            <!-- Preset làm đẹp 1 chạm (Tối ưu da tự nhiên chuẩn CapCut, khử vàng, khử bóng dầu) -->
            <div style="display: flex; gap: 3px; overflow-x: auto; padding-bottom: 2px;" id="beautyPresetPills">
              <button type="button" class="btn-tint-pill active" data-beauty="warm">🎥 Tự Nhiên CapCut</button>
              <button type="button" class="btn-tint-pill" data-beauty="rosy">🌸 Trắng Sáng</button>
              <button type="button" class="btn-tint-pill" data-beauty="smooth">✨ Trắng Mịn</button>
              <button type="button" class="btn-tint-pill" data-beauty="bright">🌟 Studio Sáng</button>
              <button type="button" class="btn-tint-pill" data-beauty="none">🚫 Gốc</button>
            </div>

            <!-- Sliders: Smoothness, Brightness, Warmth, Contrast, Saturation -->
            <div style="display: flex; align-items: center; justify-content: space-between; gap: 6px; font-size: 10px; color: #94A3B8;">
              <span style="min-width: 80px;">🌸 Mịn da:</span>
              <input type="range" class="range-slider" id="sliderBeautySmooth" min="0" max="100" value="25" step="5" style="accent-color: #F472B6; flex: 1;">
              <span id="valBeautySmooth" style="font-family: monospace; font-size: 9.5px; color: #F472B6; min-width: 28px; text-align: right;">25%</span>
            </div>

            <div style="display: flex; align-items: center; justify-content: space-between; gap: 6px; font-size: 10px; color: #94A3B8;">
              <span style="min-width: 80px;" title="Nâng sáng khuôn mặt tự nhiên (102% giữ trọn độ nét)">💡 Sáng mặt:</span>
              <input type="range" class="range-slider" id="sliderBeautyBright" min="80" max="150" value="102" step="2" style="accent-color: #FBBF24; flex: 1;">
              <span id="valBeautyBright" style="font-family: monospace; font-size: 9.5px; color: #FBBF24; min-width: 28px; text-align: right;">102%</span>
            </div>

            <div style="display: flex; align-items: center; justify-content: space-between; gap: 6px; font-size: 10px; color: #94A3B8;">
              <span style="min-width: 80px;" title="Tông màu tự nhiên, giữ trọn sắc da hồng hào chuẩn CapCut">🌸 Tone da:</span>
              <input type="range" class="range-slider" id="sliderBeautyWarmth" min="-20" max="20" value="0" step="1" style="accent-color: #FB7185; flex: 1;">
              <span id="valBeautyWarmth" style="font-family: monospace; font-size: 9.5px; color: #FB7185; min-width: 28px; text-align: right;">0° (Chuẩn)</span>
            </div>

            <div style="display: flex; align-items: center; justify-content: space-between; gap: 6px; font-size: 10px; color: #94A3B8;">
              <span style="min-width: 80px;" title="Tương phản rõ nét (104%), tóc đen sâu, môi đỏ tươi như CapCut">👁️ Tương phản:</span>
              <input type="range" class="range-slider" id="sliderBeautyContrast" min="90" max="140" value="104" step="2" style="accent-color: #38BDF8; flex: 1;">
              <span id="valBeautyContrast" style="font-family: monospace; font-size: 9.5px; color: #38BDF8; min-width: 28px; text-align: right;">104%</span>
            </div>

            <div style="display: flex; align-items: center; justify-content: space-between; gap: 6px; font-size: 10px; color: #94A3B8;">
              <span style="min-width: 80px;" title="Màu sắc tươi tắn, không bị bợt hay nhạt nhòa">🎨 Bão hòa:</span>
              <input type="range" class="range-slider" id="sliderBeautySat" min="80" max="150" value="103" step="2" style="accent-color: #34D399; flex: 1;">
              <span id="valBeautySat" style="font-family: monospace; font-size: 9.5px; color: #34D399; min-width: 28px; text-align: right;">103%</span>
            </div>'''

assert old_beauty_html in content, "old_beauty_html not found"
content = content.replace(old_beauty_html, new_beauty_html, 1)

# 3. Update State Variable Defaults
old_state_vars = '''    let studentChromaTolerance = 0.50; // 0.15 to 0.85 (mặc định 50%)
    let studentChromaFeather = 4; // 1 to 10 (mặc định 4px)
    let studentChromaDespill = 0.5; // 0.0 to 1.0
    let studentCropLeft = 0;
    let studentCropRight = 0;
    let studentCropBottom = 0;
    let enableBeauty = true;
    let beautyPreset = 'rosy'; // 'rosy' | 'smooth' | 'bright' | 'warm' | 'none'
    let beautySmoothness = 0.45; // 0.0 to 1.0: Mịn da tự nhiên
    let beautyBrightness = 1.16; // 0.8 to 1.5: Kéo sáng trắng tự nhiên (114%)
    let beautyWarmth = -2.5; // -20 to +20 deg: Mặc định -2° khử vàng, nâng tone trắng sáng tự nhiên
    let beautyContrast = 0.98; // 0.9 to 1.4: 100% tự nhiên dịu nhẹ, triệt tiêu bóng dầu và nhờn mặt
    let beautySaturation = 0.96; // 0.8 to 1.5: 98% da trong trẻo không ám vàng
    let studentAiErodeRadius = 0; // Mặc định 0px: Giữ trọn 100% ngón tay, sợi tóc, áo trắng & đồ vật'''

new_state_vars = '''    let studentChromaTolerance = 0.50; // 0.15 to 0.85 (mặc định 50% chuẩn CapCut)
    let studentChromaFeather = 4; // 1 to 10 (mặc định 4px)
    let studentChromaDespill = 0.5; // 0.0 to 1.0
    let studentCropLeft = 0;
    let studentCropRight = 0;
    let studentCropBottom = 0;
    let enableBeauty = true;
    let beautyPreset = 'warm'; // Chuẩn CapCut tự nhiên: Màu da mộc, hồng hào, sắc nét
    let beautySmoothness = 0.25; // 0.0 to 1.0: Mịn da tự nhiên, giữ trọn chi tiết khuôn mặt
    let beautyBrightness = 1.02; // 0.8 to 1.5: 102% giữ sáng chuẩn mộc, không cháy sáng da & áo trắng
    let beautyWarmth = 0.0; // 0°: Tông màu tự nhiên, không làm bợt da bé
    let beautyContrast = 1.04; // 1.04: Tương phản rõ nét, tóc đen sâu, môi đỏ tươi như CapCut
    let beautySaturation = 1.03; // 1.03: Màu sắc tươi tắn tự nhiên
    let studentAiErodeRadius = 1; // Mặc định 1px: Tự động gọt ôm sát viền người chuẩn CapCut'''

assert old_state_vars in content, "old_state_vars not found"
content = content.replace(old_state_vars, new_state_vars, 1)

# 4. Update AI Cutout Processing Block inside processStudentChromaKey
old_ai_block = '''          // 3. Chuẩn hóa tham số từ giao diện:
          // studentChromaTolerance (0.15 - 0.85): Điều chỉnh độ ôm sát người
          const tol = (typeof studentChromaTolerance === 'number')
            ? (studentChromaTolerance > 1 ? studentChromaTolerance / 100 : studentChromaTolerance)
            : 0.50;

          // Ngưỡng phân tách xác suất AI (MediaPipe boundary trung tâm ~128)
          // tol 0.20 -> cutoff 65; tol 0.50 -> cutoff 95; tol 0.80 -> cutoff 125
          const cutoff = Math.max(50, Math.min(140, Math.round(45 + tol * 100)));

          // Dải chuyển tiếp mượt mà (Feathering width)
          const featherSteps = (typeof studentChromaFeather === 'number') ? studentChromaFeather : 4;
          const feather = Math.max(8, Math.min(32, Math.round(featherSteps * 4)));

          // Tùy chọn cắt lề ngoài nếu người dùng cài đặt
          const cropL = (studentCropLeft > 0) ? Math.floor((studentCropLeft / 100) * procW) : 0;
          const cropR = (studentCropRight > 0) ? Math.floor((1 - studentCropRight / 100) * procW) : procW;
          const cropB = (studentCropBottom > 0) ? Math.floor((1 - studentCropBottom / 100) * procH) : procH;

          if (!aiTemporalAlphaBuffer || aiTemporalAlphaBuffer.length !== totalPix) {
            aiTemporalAlphaBuffer = new Float32Array(totalPix);
          }

          // 4. Xử lý đường cong S-Curve tự nhiên & Lọc khử rung nhấp nháy thích ứng chuyển động
          for (let y = 0; y < procH; y++) {
            const row = y * procW;
            const isCropY = (y > cropB);

            for (let x = 0; x < procW; x++) {
              const p = row + x;
              const idx = p * 4;

              // Nếu nằm trong vùng cắt lề ngoài
              if (isCropY || x < cropL || x > cropR) {
                fData[idx + 3] = 0;
                aiTemporalAlphaBuffer[p] = 0;
                continue;
              }

              // Khử triệt để phông xanh lá hoặc cành lá cây nếu có (Green Screen Eradication)
              const vr = fData[idx], vg = fData[idx + 1], vb = fData[idx + 2];
              const maxRB = Math.max(vr, vb);
              if (vg > maxRB + 20 && vg > 40) {
                fData[idx + 3] = 0;
                aiTemporalAlphaBuffer[p] = 0;
                continue;
              }

              // Xác suất chủ thể người từ MediaPipe (0..255)
              const rawProb = Math.max(mData[idx], mData[idx + 1], mData[idx + 2], mData[idx + 3]);

              // Đường cong Hermite smoothstep S-curve tự nhiên, giữ trọn 100% áo, da, tóc và đồ cầm
              let targetA = 0;
              if (rawProb <= cutoff) {
                targetA = 0;
              } else if (rawProb >= cutoff + feather) {
                targetA = 255;
              } else {
                const t = (rawProb - cutoff) / feather;
                targetA = Math.round(255 * (t * t * (3 - 2 * t)));
              }

              // Bộ lọc thời gian thích ứng chuyển động (Motion-Adaptive Temporal Filter):
              if (enableAiAntiFlicker) {
                const prevA = aiTemporalAlphaBuffer[p];
                const diff = Math.abs(targetA - prevA);
                if (diff > 28) {
                  aiTemporalAlphaBuffer[p] = targetA;
                } else {
                  const smoothA = prevA * 0.70 + targetA * 0.30;
                  aiTemporalAlphaBuffer[p] = smoothA;
                  targetA = Math.round(smoothA);
                }
              }

              // Trực tiếp gán kênh Alpha: Bảo toàn 100% màu gốc của áo sơ mi trắng, đồ vật và da bé
              fData[idx + 3] = targetA;
            }
          }

          // 5. Tùy chọn gọt viền mép nếu người dùng chủ động tăng sliderAiErode (mặc định = 0)
          const erodeRadius = (typeof studentAiErodeRadius === 'number') ? Math.min(3, Math.max(0, studentAiErodeRadius)) : 0;
          if (erodeRadius > 0) {
            const rawMask = new Uint8ClampedArray(totalPix);
            for (let i = 0; i < totalPix; i++) rawMask[i] = fData[i * 4 + 3];
            
            const tempHoriz = new Uint8ClampedArray(totalPix);
            for (let y = 0; y < procH; y++) {
              const row = y * procW;
              for (let x = 0; x < procW; x++) {
                let minV = rawMask[row + x];
                if (minV > 0 && minV < 255) {
                  for (let dx = 1; dx <= erodeRadius; dx++) {
                    if (x - dx >= 0 && rawMask[row + x - dx] < minV) minV = rawMask[row + x - dx];
                    if (x + dx < procW && rawMask[row + x + dx] < minV) minV = rawMask[row + x + dx];
                  }
                }
                tempHoriz[row + x] = minV;
              }
            }
            for (let y = 0; y < procH; y++) {
              const row = y * procW;
              for (let x = 0; x < procW; x++) {
                let minV = tempHoriz[row + x];
                if (minV > 0 && minV < 255) {
                  for (let dy = 1; dy <= erodeRadius; dy++) {
                    if (y - dy >= 0 && tempHoriz[(y - dy) * procW + x] < minV) minV = tempHoriz[(y - dy) * procW + x];
                    if (y + dy < procH && tempHoriz[(y + dy) * procW + x] < minV) minV = tempHoriz[(y + dy) * procW + x];
                  }
                }
                fData[(row + x) * 4 + 3] = minV;
              }
            }
          }

          // 6. Khử ám màu viền (Despill) an toàn
          const despillStrength = (typeof studentChromaDespill === 'number') ? (studentChromaDespill > 1 ? studentChromaDespill / 100 : studentChromaDespill) : 0;
          if (despillStrength > 0) {
            for (let p = 0; p < totalPix; p++) {
              const idx = p * 4;
              const a = fData[idx + 3];
              if (a > 0 && a < 255) {
                const r = fData[idx], g = fData[idx + 1], b = fData[idx + 2];
                const maxRB = Math.max(r, b);
                if (g > maxRB) {
                  fData[idx + 1] = Math.round(g * (1 - despillStrength * 0.75) + maxRB * (despillStrength * 0.75));
                }
              }
            }
          }'''

new_ai_block = '''          // 3. Chuẩn hóa tham số từ giao diện (Tối ưu hóa chuẩn CapCut):
          // studentChromaTolerance (0.15 - 0.85): Điều chỉnh độ ôm sát người
          const tol = (typeof studentChromaTolerance === 'number')
            ? (studentChromaTolerance > 1 ? studentChromaTolerance / 100 : studentChromaTolerance)
            : 0.50;

          // Ngưỡng phân tách xác suất AI chuẩn xác (MediaPipe boundary trung tâm ~128)
          // tol 0.20 -> cutoff 98; tol 0.50 -> cutoff 124 (Chuẩn CapCut); tol 0.80 -> cutoff 150
          const cutoffCenter = Math.max(90, Math.min(160, Math.round(80 + tol * 88)));

          // Dải chuyển tiếp mượt mà chống răng cưa (Feathering width)
          const featherSteps = (typeof studentChromaFeather === 'number') ? studentChromaFeather : 4;
          const feather = Math.max(4, Math.min(18, Math.round(featherSteps * 2.0)));
          const halfF = feather * 0.5;
          const fLow = cutoffCenter - halfF;
          const fHigh = cutoffCenter + halfF;

          // Tùy chọn cắt lề ngoài nếu người dùng cài đặt
          const cropL = (studentCropLeft > 0) ? Math.floor((studentCropLeft / 100) * procW) : 0;
          const cropR = (studentCropRight > 0) ? Math.floor((1 - studentCropRight / 100) * procW) : procW;
          const cropB = (studentCropBottom > 0) ? Math.floor((1 - studentCropBottom / 100) * procH) : procH;

          if (!aiTemporalAlphaBuffer || aiTemporalAlphaBuffer.length !== totalPix) {
            aiTemporalAlphaBuffer = new Float32Array(totalPix);
          }

          // 4. Xử lý đường cong S-Curve tự nhiên & Lọc khử rung nhấp nháy thích ứng chuyển động
          for (let y = 0; y < procH; y++) {
            const row = y * procW;
            const isCropY = (y > cropB);

            for (let x = 0; x < procW; x++) {
              const p = row + x;
              const idx = p * 4;

              // Nếu nằm trong vùng cắt lề ngoài
              if (isCropY || x < cropL || x > cropR) {
                fData[idx + 3] = 0;
                aiTemporalAlphaBuffer[p] = 0;
                continue;
              }

              // Khử triệt để phông xanh lá hoặc cành lá cây nếu có (Green Screen Eradication)
              const vr = fData[idx], vg = fData[idx + 1], vb = fData[idx + 2];
              const maxRB = Math.max(vr, vb);
              if (vg > maxRB + 20 && vg > 40) {
                fData[idx + 3] = 0;
                aiTemporalAlphaBuffer[p] = 0;
                continue;
              }

              // Xác suất chủ thể người từ MediaPipe (0..255)
              const rawProb = Math.max(mData[idx], mData[idx + 1], mData[idx + 2], mData[idx + 3]);

              // Đường cong Hermite smoothstep đối xứng chuẩn xác, loại bỏ 100% nền phòng và gối/sofa phía sau
              let targetA = 0;
              if (rawProb <= fLow) {
                targetA = 0;
              } else if (rawProb >= fHigh) {
                targetA = 255;
              } else {
                const t = (rawProb - fLow) / feather;
                targetA = Math.round(255 * (t * t * (3 - 2 * t)));
              }

              // Bộ lọc thời gian thích ứng chuyển động (Motion-Adaptive Temporal Filter):
              if (enableAiAntiFlicker) {
                const prevA = aiTemporalAlphaBuffer[p];
                const diff = Math.abs(targetA - prevA);
                if (diff > 28) {
                  aiTemporalAlphaBuffer[p] = targetA;
                } else {
                  const smoothA = prevA * 0.70 + targetA * 0.30;
                  aiTemporalAlphaBuffer[p] = smoothA;
                  targetA = Math.round(smoothA);
                }
              }

              // Trực tiếp gán kênh Alpha ban đầu
              fData[idx + 3] = targetA;
            }
          }

          // 5. Tự động gọt ôm sát mép người (Morphological Edge Choke / Erosion - Mặc định 1px chuẩn CapCut)
          const erodeRadius = (typeof studentAiErodeRadius === 'number') ? Math.min(4, Math.max(0, studentAiErodeRadius)) : 1;
          if (erodeRadius > 0) {
            const rawMask = new Uint8ClampedArray(totalPix);
            for (let i = 0; i < totalPix; i++) rawMask[i] = fData[i * 4 + 3];
            
            const tempHoriz = new Uint8ClampedArray(totalPix);
            for (let y = 0; y < procH; y++) {
              const row = y * procW;
              for (let x = 0; x < procW; x++) {
                let minV = rawMask[row + x];
                if (minV > 0) {
                  for (let dx = 1; dx <= erodeRadius; dx++) {
                    if (x - dx >= 0 && rawMask[row + x - dx] < minV) minV = rawMask[row + x - dx];
                    if (x + dx < procW && rawMask[row + x + dx] < minV) minV = rawMask[row + x + dx];
                  }
                }
                tempHoriz[row + x] = minV;
              }
            }
            for (let y = 0; y < procH; y++) {
              const row = y * procW;
              for (let x = 0; x < procW; x++) {
                let minV = tempHoriz[row + x];
                if (minV > 0) {
                  for (let dy = 1; dy <= erodeRadius; dy++) {
                    if (y - dy >= 0 && tempHoriz[(y - dy) * procW + x] < minV) minV = tempHoriz[(y - dy) * procW + x];
                    if (y + dy < procH && tempHoriz[(y + dy) * procW + x] < minV) minV = tempHoriz[(y + dy) * procW + x];
                  }
                }
                fData[(row + x) * 4 + 3] = minV;
              }
            }
          }

          // 6. KHỬ VIỀN TRẮNG MẶT/TÓC/ÁO THÔNG MINH (SMART EDGE DEFRINGING & COLOR DECONTAMINATION - CHUẨN CAPCUT)
          // Xóa bỏ triệt để quầng sáng trắng/kem của tường phòng lem vào mép tóc, da và áo
          for (let y = 1; y < procH - 1; y++) {
            const row = y * procW;
            for (let x = 1; x < procW - 1; x++) {
              const p = row + x;
              const idx = p * 4;
              const a = fData[idx + 3];
              // Chỉ xử lý các điểm ảnh nằm trên dải mép chuyển tiếp (semi-transparent boundary 0 < a < 252)
              if (a > 0 && a < 252) {
                // Tìm điểm ảnh đặc bên trong người (alpha >= 252) gần nhất trong 4 hướng lân cận
                let inIdx = -1;
                if (fData[(p - 1) * 4 + 3] >= 252) inIdx = (p - 1) * 4;
                else if (fData[(p + 1) * 4 + 3] >= 252) inIdx = (p + 1) * 4;
                else if (fData[(p - procW) * 4 + 3] >= 252) inIdx = (p - procW) * 4;
                else if (fData[(p + procW) * 4 + 3] >= 252) inIdx = (p + procW) * 4;
                else {
                  // Mở rộng tìm kiếm bán kính 2px nếu mép dốc mềm
                  if (x > 1 && fData[(p - 2) * 4 + 3] >= 252) inIdx = (p - 2) * 4;
                  else if (x < procW - 2 && fData[(p + 2) * 4 + 3] >= 252) inIdx = (p + 2) * 4;
                  else if (y > 1 && fData[(p - procW * 2) * 4 + 3] >= 252) inIdx = (p - procW * 2) * 4;
                  else if (y < procH - 2 && fData[(p + procW * 2) * 4 + 3] >= 252) inIdx = (p + procW * 2) * 4;
                }

                if (inIdx >= 0) {
                  const inR = fData[inIdx];
                  const inG = fData[inIdx + 1];
                  const inB = fData[inIdx + 2];
                  const normA = a / 255;
                  // Điểm càng ra sát mép ngoài (alpha càng nhỏ) thì càng nhận nhiều màu đặc của chủ thể, triệt tiêu viền trắng
                  const blend = (1 - normA) * 0.90;
                  fData[idx] = Math.round(fData[idx] * (1 - blend) + inR * blend);
                  fData[idx + 1] = Math.round(fData[idx + 1] * (1 - blend) + inG * blend);
                  fData[idx + 2] = Math.round(fData[idx + 2] * (1 - blend) + inB * blend);
                }
              }
            }
          }

          // 7. Khử ám màu viền (Despill) an toàn
          const despillStrength = (typeof studentChromaDespill === 'number') ? (studentChromaDespill > 1 ? studentChromaDespill / 100 : studentChromaDespill) : 0;
          if (despillStrength > 0) {
            for (let p = 0; p < totalPix; p++) {
              const idx = p * 4;
              const a = fData[idx + 3];
              if (a > 0 && a < 255) {
                const r = fData[idx], g = fData[idx + 1], b = fData[idx + 2];
                const maxRB = Math.max(r, b);
                if (g > maxRB) {
                  fData[idx + 1] = Math.round(g * (1 - despillStrength * 0.75) + maxRB * (despillStrength * 0.75));
                }
              }
            }
          }'''

assert old_ai_block in content, "old_ai_block not found"
content = content.replace(old_ai_block, new_ai_block, 1)

# 5. Update drawStudentCharacter Auto-lighting and Beauty Overlay
old_lighting = '''      // 1. AUTO LIGHTING (DYNAMIC LUMA LIFT WITH SOFT CONTINUOUS INTERPOLATION - ZERO STROBE)
      if (enableAutoLighting) {
        const luma = getSampledLuma(processedCanvas);
        let targetLuma = 1.0;
        if (luma < 122) {
          targetLuma = Math.min(1.25, Math.max(1.0, 126 / Math.max(35, luma)));
        }
        smoothedAutoLumaFactor = smoothedAutoLumaFactor * 0.90 + targetLuma * 0.10;
      } else {
        smoothedAutoLumaFactor = 1.0;
      }'''

new_lighting = '''      // 1. AUTO LIGHTING (CHỈ NÂNG SÁNG NHẸ NẾU VIDEO QUÁ TỐI, TRÁNH CHÁY SÁNG 100%)
      if (enableAutoLighting) {
        const luma = getSampledLuma(processedCanvas);
        let targetLuma = 1.0;
        if (luma < 90) {
          targetLuma = Math.min(1.10, Math.max(1.0, 95 / Math.max(40, luma)));
        }
        smoothedAutoLumaFactor = smoothedAutoLumaFactor * 0.90 + targetLuma * 0.10;
      } else {
        smoothedAutoLumaFactor = 1.0;
      }'''

assert old_lighting in content, "old_lighting not found"
content = content.replace(old_lighting, new_lighting, 1)

# 6. Update drawStudentCharacter Beauty blur overlay
old_blur_overlay = '''        // Soft skin smoothing / glow overlay (Khóa chặt trong người, không loang ra ngoài nền, chống nhấp nháy 100%)
        if (enableBeauty && beautySmoothness > 0) {
          if (offscreenBeautyCanvas.width !== processedCanvas.width || offscreenBeautyCanvas.height !== processedCanvas.height) {
            offscreenBeautyCanvas.width = processedCanvas.width;
            offscreenBeautyCanvas.height = processedCanvas.height;
          }
          offscreenBeautyCtx.save();
          offscreenBeautyCtx.clearRect(0, 0, processedCanvas.width, processedCanvas.height);
          // brightness(1.10) saturate(0.92): Nâng sáng nhẹ và khử vàng, tạo da trắng sứ mềm mại không bóng nhờn
          offscreenBeautyCtx.filter = `blur(${Math.max(2, Math.round(beautySmoothness * 6))}px) brightness(1.10) saturate(0.92)`;
          offscreenBeautyCtx.drawImage(processedCanvas, 0, 0);
          offscreenBeautyCtx.globalCompositeOperation = 'destination-in';
          offscreenBeautyCtx.filter = 'none';
          offscreenBeautyCtx.drawImage(processedCanvas, 0, 0);
          offscreenBeautyCtx.restore();

          ctx.save();
          ctx.globalAlpha = beautySmoothness * 0.38;
          ctx.drawImage(offscreenBeautyCanvas, x0, y0, charW, charH);
          ctx.restore();
        }'''

new_blur_overlay = '''        // Soft skin smoothing / glow overlay (Khóa chặt trong người, không loang ra ngoài nền, chống nhấp nháy 100%)
        if (enableBeauty && beautySmoothness > 0) {
          if (offscreenBeautyCanvas.width !== processedCanvas.width || offscreenBeautyCanvas.height !== processedCanvas.height) {
            offscreenBeautyCanvas.width = processedCanvas.width;
            offscreenBeautyCanvas.height = processedCanvas.height;
          }
          offscreenBeautyCtx.save();
          offscreenBeautyCtx.clearRect(0, 0, processedCanvas.width, processedCanvas.height);
          // Giữ brightness(1.00) để không làm cháy sáng hay bợt da bé
          offscreenBeautyCtx.filter = `blur(${Math.max(2, Math.round(beautySmoothness * 4))}px) brightness(1.00) saturate(1.00)`;
          offscreenBeautyCtx.drawImage(processedCanvas, 0, 0);
          offscreenBeautyCtx.globalCompositeOperation = 'destination-in';
          offscreenBeautyCtx.filter = 'none';
          offscreenBeautyCtx.drawImage(processedCanvas, 0, 0);
          offscreenBeautyCtx.restore();

          ctx.save();
          ctx.globalAlpha = beautySmoothness * 0.25;
          ctx.drawImage(offscreenBeautyCanvas, x0, y0, charW, charH);
          ctx.restore();
        }'''

assert old_blur_overlay in content, "old_blur_overlay not found"
content = content.replace(old_blur_overlay, new_blur_overlay, 1)

# 7. Update Beauty Presets logic around line 14278
old_presets_code = '''        if (p === 'rosy') {
          // Trắng Sáng BTV: Da trắng sáng trong trẻo, khử vàng sạm, không bóng nhờn
          beautySmoothness = 0.45; beautyBrightness = 1.14; beautyWarmth = -2; beautyContrast = 1.00; beautySaturation = 0.98; beautySharpness = 30;
        } else if (p === 'smooth') {
          // Trắng Mịn Hàn Quốc: Da sứ mịn màng, làm mờ khuyết điểm
          beautySmoothness = 0.60; beautyBrightness = 1.15; beautyWarmth = -3; beautyContrast = 0.98; beautySaturation = 0.95; beautySharpness = 25;
        } else if (p === 'bright') {
          // Studio Sáng Trong: Sáng rực rỡ, da bật tone
          beautySmoothness = 0.35; beautyBrightness = 1.22; beautyWarmth = -1; beautyContrast = 1.02; beautySaturation = 1.00; beautySharpness = 35;
        } else if (p === 'warm') {
          // Tự Nhiên Nhẹ: Màu mộc chuẩn da bé
          beautySmoothness = 0.30; beautyBrightness = 1.08; beautyWarmth = 0; beautyContrast = 1.00; beautySaturation = 1.00; beautySharpness = 25;
        } else if (p === 'none') {
          beautySmoothness = 0.0; beautyBrightness = 1.0; beautyWarmth = 0; beautyContrast = 1.0; beautySaturation = 1.0; beautySharpness = 0;
        }'''

new_presets_code = '''        if (p === 'warm') {
          // Tự Nhiên CapCut: Màu da mộc chuẩn, hồng hào, sắc nét tự nhiên
          beautySmoothness = 0.25; beautyBrightness = 1.02; beautyWarmth = 0; beautyContrast = 1.04; beautySaturation = 1.03; beautySharpness = 30;
        } else if (p === 'rosy') {
          // Trắng Sáng BTV: Da sáng mịn trong trẻo, không cháy sáng da & áo
          beautySmoothness = 0.35; beautyBrightness = 1.04; beautyWarmth = -1; beautyContrast = 1.02; beautySaturation = 1.02; beautySharpness = 30;
        } else if (p === 'smooth') {
          // Trắng Mịn Hàn Quốc: Da sứ mịn màng
          beautySmoothness = 0.45; beautyBrightness = 1.04; beautyWarmth = -1.5; beautyContrast = 1.00; beautySaturation = 1.00; beautySharpness = 25;
        } else if (p === 'bright') {
          // Studio Sáng: Rực rỡ nhưng giữ trọn chi tiết vải
          beautySmoothness = 0.25; beautyBrightness = 1.08; beautyWarmth = 0; beautyContrast = 1.04; beautySaturation = 1.04; beautySharpness = 35;
        } else if (p === 'none') {
          beautySmoothness = 0.0; beautyBrightness = 1.0; beautyWarmth = 0; beautyContrast = 1.0; beautySaturation = 1.0; beautySharpness = 0;
        }'''

assert old_presets_code in content, "old_presets_code not found"
content = content.replace(old_presets_code, new_presets_code, 1)

with open(src_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("[SUCCESS] All 7 CapCut-grade AI background removal upgrades applied successfully!")
