import os

file_path = 'Tao_Khung_Thoi_Su_Talk11.html'
with open(file_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update selectExportMode in header
old_select_export = '''      <!-- Export Mode Selector (Composite vs Green Screen) -->
      <select id="selectExportMode" class="form-control" style="width: auto; padding: 4px 7px; font-size: 10.5px; font-weight: 700; background: #0F172A; color: #34D399; border: 1px solid rgba(52,211,153,0.4); border-radius: 6px;" title="Chế độ xuất: Bản tin hoàn chỉnh hoặc Màn xanh để lồng CapCut">
        <option value="full" selected>🎬 Bản Tin Hoàn Chỉnh</option>
        <option value="greenscreen">🟩 Màn Xanh (Chroma Key CapCut)</option>
      </select>'''

new_select_export = '''      <!-- Export Mode Selector (Composite vs Green Screen vs WebM Alpha vs Alpha Matte) -->
      <select id="selectExportMode" class="form-control" style="width: auto; padding: 4px 7px; font-size: 10.5px; font-weight: 700; background: #0F172A; color: #34D399; border: 1px solid rgba(52,211,153,0.4); border-radius: 6px;" title="Chế độ xuất: Bản tin hoàn chỉnh, Tách nền trong suốt WebM VP9 hoặc Màn xanh CapCut">
        <option value="full" selected>🎬 Bản Tin Hoàn Chỉnh (3D Studio)</option>
        <option value="transparent_webm">✨ Tách Nền Trong Suốt (WebM VP9 Alpha)</option>
        <option value="alpha_matte">🏁 Mặt Nạ Alpha Trắng Đen (Luma Matte)</option>
        <option value="greenscreen">🟩 Màn Xanh (Chroma Key CapCut)</option>
      </select>'''

assert old_select_export in html, "Failed to find old_select_export"
html = html.replace(old_select_export, new_select_export, 1)

# 2. Update Section 2 UI (BTV Nhí Tách Nền)
old_sec2_start = '          <!-- 2. TÁCH NỀN BTV NHÍ (AI PERSON SEGMENTATION & CHROMA KEY) -->'
old_sec2_end = '''            <!-- Cắt xén viền ngoài (Crop) -->
            <div style="display: flex; align-items: center; justify-content: space-between; gap: 6px; font-size: 9.5px; color: #94A3B8; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 4px;">
              <span>✂️ Cắt lề ngoài thừa:</span>
              <div style="display: flex; gap: 3px; align-items: center;">
                <input type="number" id="inputCropLeft" min="0" max="40" value="0" style="width: 32px; font-size: 9px; text-align: center; background: #070D1E; border: 1px solid rgba(255,255,255,0.2); color: #FFF; border-radius: 3px;" title="Cắt lề trái (%)">%T
                <input type="number" id="inputCropRight" min="0" max="40" value="0" style="width: 32px; font-size: 9px; text-align: center; background: #070D1E; border: 1px solid rgba(255,255,255,0.2); color: #FFF; border-radius: 3px;" title="Cắt lề phải (%)">%P
                <input type="number" id="inputCropBottom" min="0" max="40" value="0" style="width: 32px; font-size: 9px; text-align: center; background: #070D1E; border: 1px solid rgba(255,255,255,0.2); color: #FFF; border-radius: 3px;" title="Cắt lề đáy (%)">%D
              </div>
            </div>
          </div>'''

new_sec2 = '''          <!-- 2. TÁCH NỀN BTV NHÍ (AI PERSON SEGMENTATION & CHROMA KEY) -->
          <div style="background: rgba(10, 16, 30, 0.85); border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 7px; padding: 7px 9px; display: flex; flex-direction: column; gap: 5px;">
            <div style="display: flex; align-items: center; justify-content: space-between;">
              <label class="talk11-help-title" id="lblProChromaTitle" data-tooltip="🤖 AI RVM & MediaPipe: Tự động nhận diện & giữ trọn cơ thể, khuôn mặt bé; xóa sạch 100% nền phòng đằng sau không cần phông xanh!" style="cursor: pointer; display: flex; align-items: center; gap: 5px; font-size: 10.5px; font-weight: 800; color: #10B981; margin-bottom: 0;">
                <input type="checkbox" id="chkChromaKeyEnable" checked style="accent-color: #10B981; width: 13px; height: 13px;">
                <span>🤖 Tách Nền BTV Nhí (AI / Chroma)</span>
              </label>
              <span id="badgeAiSegmentStatus" style="font-size: 8.5px; color: #F59E0B; font-weight: 700; background: rgba(245,158,11,0.15); padding: 1px 5px; border-radius: 4px; border: 1px solid rgba(245,158,11,0.35);">👑 AI RVM CapCut Pro</span>
            </div>

            <!-- Chế độ Tách: AI Tự Động vs Phông Xanh Lá vs Xanh Biển vs Giữ Phòng -->
            <div style="display: flex; gap: 3px; flex-wrap: wrap;" id="bgSegmentPills">
              <button type="button" class="btn-tint-pill active" id="btnKeyAi" data-keymode="ai_auto" style="flex: 1.4; padding: 2px 4px; font-size: 9px; font-weight: 800; color: #34D399; border-color: #10B981;">🤖 AI Tách Người</button>
              <button type="button" class="btn-tint-pill" id="btnKeyGreen" data-keymode="green" style="flex: 1; padding: 2px 4px; font-size: 9px;">🟢 Phông Xanh</button>
              <button type="button" class="btn-tint-pill" id="btnKeyBlue" data-keymode="blue" style="flex: 1; padding: 2px 4px; font-size: 9px;">🔵 Xanh Biển</button>
              <button type="button" class="btn-tint-pill" id="btnKeyRoom" data-keymode="room" style="flex: 1; padding: 2px 4px; font-size: 9px; color: #94A3B8;">🏠 Giữ Phòng</button>
              <input type="color" id="inputCustomKeyColor" value="#00FF00" style="width: 18px; height: 18px; border: none; border-radius: 3px; cursor: pointer; padding: 0;" title="Hút màu tùy chỉnh">
            </div>

            <!-- CÔNG CỤ TINH CHỈNH MẶT NẠ TRỰC TIẾP TRÊN CANVAS (CHỌN CHỦ THỂ / TÔ GIỮ / TÔ XÓA) -->
            <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 6px; padding: 5px 6px; display: flex; flex-direction: column; gap: 4px;">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 9px; font-weight: 800; color: #38BDF8;">🎯 Công Cụ Tinh Chỉnh Mặt Nạ (Interactive)</span>
                <button type="button" id="btnClearMatteStrokes" style="background: none; border: none; color: #94A3B8; font-size: 8.5px; cursor: pointer; padding: 0;" title="Xóa toàn bộ cọ vẽ và điểm chọn thủ công">↺ Đặt lại cọ</button>
              </div>
              <div style="display: flex; gap: 3px;" id="matteToolPills">
                <button type="button" class="btn-tint-pill active" id="btnMatteToolAuto" data-mtool="auto" style="flex: 1; padding: 2px 2px; font-size: 8.5px; font-weight: 700;" title="Chế độ bình thường: Di chuyển, thu phóng nhân vật">🤖 Tự Động</button>
                <button type="button" class="btn-tint-pill" id="btnMatteToolSelect" data-mtool="select" style="flex: 1.1; padding: 2px 2px; font-size: 8.5px; font-weight: 700;" title="Click vào người để chọn chủ thể chính (Shift+Click để loại trừ người/vật cạnh bên)">🎯 Chọn Người</button>
                <button type="button" class="btn-tint-pill" id="btnMatteToolBrushKeep" data-mtool="brush_keep" style="flex: 1; padding: 2px 2px; font-size: 8.5px; font-weight: 700; color: #34D399;" title="Tô màu xanh để giữ lại vùng bị cắt lẹm">🖌️ Tô Giữ</button>
                <button type="button" class="btn-tint-pill" id="btnMatteToolBrushRemove" data-mtool="brush_remove" style="flex: 1; padding: 2px 2px; font-size: 8.5px; font-weight: 700; color: #F87171;" title="Tô màu đỏ để xóa vùng tường thừa hoặc viền lem">🧹 Tô Xóa</button>
              </div>
              <div style="display: flex; align-items: center; justify-content: space-between; gap: 5px; font-size: 9px; color: #94A3B8;">
                <span style="min-width: 65px;">Cỡ cọ vẽ:</span>
                <input type="range" class="range-slider" id="sliderMatteBrushSize" min="6" max="80" value="24" step="2" style="accent-color: #38BDF8; flex: 1; height: 3px;">
                <span id="valMatteBrushSize" style="font-family: monospace; font-size: 8.5px; color: #38BDF8; min-width: 22px; text-align: right;">24px</span>
              </div>
            </div>

            <!-- CHẾ ĐỘ XEM TRƯỚC (PREVIEW MODES): STUDIO / VFX CHECKERBOARD / ALPHA MATTE / GREEN SCREEN -->
            <div style="display: flex; align-items: center; justify-content: space-between; gap: 3px; font-size: 9px; color: #94A3B8;">
              <span style="font-weight: 700; color: #CBD5E1;">👁️ Xem trước:</span>
              <div style="display: flex; gap: 2px; flex: 1; justify-content: flex-end;" id="aiMattingPreviewPills">
                <button type="button" class="btn-tint-pill active" id="btnPrevModeStudio" data-pmode="studio" style="padding: 1px 4px; font-size: 8.5px;">🏛️ Studio</button>
                <button type="button" class="btn-tint-pill" id="btnPrevModeCheckerboard" data-pmode="checkerboard" style="padding: 1px 4px; font-size: 8.5px;">🏁 Trong Suốt</button>
                <button type="button" class="btn-tint-pill" id="btnPrevModeAlpha" data-pmode="alpha_matte" style="padding: 1px 4px; font-size: 8.5px;">⬛ Alpha</button>
                <button type="button" class="btn-tint-pill" id="btnPrevModeGreen" data-pmode="greenscreen" style="padding: 1px 4px; font-size: 8.5px;">🟢 Phông</button>
              </div>
            </div>

            <!-- CHẤT LƯỢNG TÁCH NỀN (QUALITY MODES) -->
            <div style="display: flex; gap: 4px; align-items: center;">
              <button type="button" id="btnQualityFast" style="flex: 1; background: rgba(56, 189, 248, 0.15); border: 1px solid rgba(56, 189, 248, 0.4); color: #38BDF8; font-weight: 800; font-size: 9px; border-radius: 4px; padding: 4px 6px; cursor: pointer; text-align: center;">
                ⚡ Nhanh 60FPS (Client AI)
              </button>
              <button type="button" id="btnRunRvm4kBackend" style="flex: 1.3; background: linear-gradient(135deg, #F59E0B, #D97706); color: #0F172A; font-weight: 800; font-size: 9px; border: none; border-radius: 4px; padding: 4px 6px; cursor: pointer; text-align: center; box-shadow: 0 2px 6px rgba(245, 158, 11, 0.25);">
                👑 RVM 4K ONNX (CapCut Pro)
              </button>
            </div>

            <!-- Sliders: Tolerance / AI Confidence, Feather, Despill -->
            <div style="display: flex; align-items: center; justify-content: space-between; gap: 6px; font-size: 10px; color: #94A3B8;">
              <span style="min-width: 90px;" id="lblChromaTolerance" title="Kéo tăng để ôm sát dính người hơn nữa, triệt tiêu toàn bộ viền lem nền">🎯 Độ ôm sát người:</span>
              <input type="range" class="range-slider" id="sliderChromaTolerance" min="30" max="99" value="82" step="1" style="accent-color: #10B981; flex: 1;">
              <span id="valChromaTolerance" style="font-family: monospace; font-size: 9.5px; color: #34D399; min-width: 28px; text-align: right;">82%</span>
            </div>

            <div style="display: flex; align-items: center; justify-content: space-between; gap: 6px; font-size: 10px; color: #94A3B8;">
              <span style="min-width: 90px;" title="Tự động gọt ôm sát mép người, triệt tiêu 100% viền trắng tường phòng (Chuẩn CapCut Pro)">✂️ Gọt viền mép CapCut:</span>
              <input type="range" class="range-slider" id="sliderAiErode" min="0" max="8" value="4" step="1" style="accent-color: #F59E0B; flex: 1;">
              <span id="valAiErode" style="font-family: monospace; font-size: 9.5px; color: #F59E0B; min-width: 28px; text-align: right;">4px</span>
            </div>

            <div style="display: flex; align-items: center; justify-content: space-between; gap: 6px; font-size: 10px; color: #94A3B8;">
              <span style="min-width: 90px;">✨ Mịn viền tóc & mép:</span>
              <input type="range" class="range-slider" id="sliderChromaFeather" min="1" max="8" value="2" step="1" style="accent-color: #38BDF8; flex: 1;">
              <span id="valChromaFeather" style="font-family: monospace; font-size: 9.5px; color: #38BDF8; min-width: 28px; text-align: right;">2px</span>
            </div>

            <!-- CHỐNG NHẤP NHÁY AI 60FPS -->
            <div style="display: flex; align-items: center; justify-content: space-between; background: rgba(56,189,248,0.08); padding: 4px 6px; border-radius: 4px; border: 1px solid rgba(56,189,248,0.25);">
              <label style="cursor: pointer; display: flex; align-items: center; gap: 4px; font-size: 9.5px; font-weight: 700; color: #38BDF8; margin-bottom: 0;">
                <input type="checkbox" id="chkAiAntiFlicker" checked style="accent-color: #38BDF8; width: 12px; height: 12px;">
                <span>🛡️ Lọc Khử Nhấp Nháy (Anti-Flicker 60FPS)</span>
              </label>
              <span style="font-size: 8px; color: #7DD3FC;">Mượt viền chuyển động</span>
            </div>

            <div style="display: flex; align-items: center; justify-content: space-between; gap: 6px; font-size: 10px; color: #94A3B8;">
              <span style="min-width: 80px;">🌿 Khử ám màu viền:</span>
              <input type="range" class="range-slider" id="sliderChromaDespill" min="0" max="100" value="50" step="5" style="accent-color: #FBBF24; flex: 1;">
              <span id="valChromaDespill" style="font-family: monospace; font-size: 9.5px; color: #FBBF24; min-width: 28px; text-align: right;">50%</span>
            </div>

            <!-- Cắt xén viền ngoài (Crop) -->
            <div style="display: flex; align-items: center; justify-content: space-between; gap: 6px; font-size: 9.5px; color: #94A3B8; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 4px;">
              <span>✂️ Cắt lề ngoài thừa:</span>
              <div style="display: flex; gap: 3px; align-items: center;">
                <input type="number" id="inputCropLeft" min="0" max="40" value="0" style="width: 32px; font-size: 9px; text-align: center; background: #070D1E; border: 1px solid rgba(255,255,255,0.2); color: #FFF; border-radius: 3px;" title="Cắt lề trái (%)">%T
                <input type="number" id="inputCropRight" min="0" max="40" value="0" style="width: 32px; font-size: 9px; text-align: center; background: #070D1E; border: 1px solid rgba(255,255,255,0.2); color: #FFF; border-radius: 3px;" title="Cắt lề phải (%)">%P
                <input type="number" id="inputCropBottom" min="0" max="40" value="0" style="width: 32px; font-size: 9px; text-align: center; background: #070D1E; border: 1px solid rgba(255,255,255,0.2); color: #FFF; border-radius: 3px;" title="Cắt lề đáy (%)">%D
              </div>
            </div>
          </div>'''

pos_start = html.find(old_sec2_start)
pos_end = html.find(old_sec2_end, pos_start)
assert pos_start != -1 and pos_end != -1, "Failed to find Section 2 bounds"
html = html[:pos_start] + new_sec2 + html[pos_end + len(old_sec2_end):]

# 3. Add State Variables
old_state_target = '''    let offscreenBeautyCanvas = document.createElement('canvas');
    let offscreenBeautyCtx = offscreenBeautyCanvas.getContext('2d');

    // Undo / Redo History State Manager'''

new_state_target = '''    let offscreenBeautyCanvas = document.createElement('canvas');
    let offscreenBeautyCtx = offscreenBeautyCanvas.getContext('2d');

    // Interactive Matte Toolkit & Preview Mode State (SAM / Magic Mask / Roto Brush workflow)
    let aiMattingTool = 'auto'; // 'auto' | 'select' | 'brush_keep' | 'brush_remove'
    let aiMattingBrushSize = 24;
    let aiMattingPromptPoints = []; // [{ xNorm, yNorm, isPositive: true }]
    let aiMattingPreviewMode = 'studio'; // 'studio' | 'checkerboard' | 'alpha_matte' | 'greenscreen'
    let userMatteCorrectionCanvas = document.createElement('canvas');
    let userMatteCorrectionCtx = userMatteCorrectionCanvas.getContext('2d', { willReadFrequently: true });
    let hasUserMatteCorrections = false;
    let isPaintingMatteBrush = false;
    let lastBrushNormX = 0, lastBrushNormY = 0;
    let canvasHoverScreenX = -1, canvasHoverScreenY = -1;

    // Undo / Redo History State Manager'''

assert old_state_target in html, "Failed to find state variables target"
html = html.replace(old_state_target, new_state_target, 1)

# 4. Update Pointer Handlers
old_pointer_move_head = '''    function handleCanvasPointerMove(clientX, clientY) {
      const rect = canvas.getBoundingClientRect();
      const scaleX = canvas.width / rect.width;
      const scaleY = canvas.height / rect.height;
      const mouseX = (clientX - rect.left) * scaleX;
      const mouseY = (clientY - rect.top) * scaleY;'''

new_pointer_move_head = '''    function handleCanvasPointerMove(clientX, clientY) {
      const rect = canvas.getBoundingClientRect();
      const scaleX = canvas.width / rect.width;
      const scaleY = canvas.height / rect.height;
      const mouseX = (clientX - rect.left) * scaleX;
      const mouseY = (clientY - rect.top) * scaleY;

      canvasHoverScreenX = mouseX;
      canvasHoverScreenY = mouseY;

      // Handle Interactive Matte Brush Painting
      if (isPaintingMatteBrush && (aiMattingTool === 'brush_keep' || aiMattingTool === 'brush_remove')) {
        const studentBox = getStudentCharacterScreenBounds();
        if (studentBox && userMatteCorrectionCanvas.width > 0 && userMatteCorrectionCanvas.height > 0) {
          const normX = (mouseX - studentBox.x) / studentBox.w;
          const normY = (mouseY - studentBox.y) / studentBox.h;
          const px = normX * userMatteCorrectionCanvas.width;
          const py = normY * userMatteCorrectionCanvas.height;
          const lastPx = lastBrushNormX * userMatteCorrectionCanvas.width;
          const lastPy = lastBrushNormY * userMatteCorrectionCanvas.height;

          userMatteCorrectionCtx.beginPath();
          userMatteCorrectionCtx.strokeStyle = (aiMattingTool === 'brush_keep') ? '#00FF00' : '#FF0000';
          userMatteCorrectionCtx.lineWidth = Math.max(3, (aiMattingBrushSize / studentBox.w) * userMatteCorrectionCanvas.width);
          userMatteCorrectionCtx.lineCap = 'round';
          userMatteCorrectionCtx.lineJoin = 'round';
          userMatteCorrectionCtx.moveTo(lastPx, lastPy);
          userMatteCorrectionCtx.lineTo(px, py);
          userMatteCorrectionCtx.stroke();

          lastBrushNormX = normX;
          lastBrushNormY = normY;
          hasUserMatteCorrections = true;
          try { render(previewCurrentSec); } catch(err) {}
        }
        return true;
      }'''

assert old_pointer_move_head in html, "Failed to find old_pointer_move_head"
html = html.replace(old_pointer_move_head, new_pointer_move_head, 1)

# Pointer down
old_pointer_down_check = '''        // Check Student Character Body
        if (mouseX >= studentBox.x && mouseX <= studentBox.x + studentBox.w &&
            mouseY >= studentBox.y && mouseY <= studentBox.y + studentBox.h) {
          isDraggingStudent = true;
          canvas.style.cursor = 'grabbing';
          studentDragStartX = mouseX;
          studentDragStartY = mouseY;
          studentDragOffsetX = mouseX - studentBox.centerX;
          studentDragOffsetY = mouseY - studentBox.centerY;
          studentHovered = true;
          try { render(previewCurrentSec); } catch(err) {}
          return true;
        }'''

new_pointer_down_check = '''        // Check Student Character Body
        if (mouseX >= studentBox.x && mouseX <= studentBox.x + studentBox.w &&
            mouseY >= studentBox.y && mouseY <= studentBox.y + studentBox.h) {
          
          // INTERACTIVE MATTE TOOL: SELECT SUBJECT (POINT PROMPT)
          if (aiMattingTool === 'select') {
            const normX = (mouseX - studentBox.x) / studentBox.w;
            const normY = (mouseY - studentBox.y) / studentBox.h;
            const isPos = !(window.event && (window.event.shiftKey || window.event.altKey));
            aiMattingPromptPoints.push({ xNorm: normX, yNorm: normY, isPositive: isPos });
            pushUndoState('Thêm điểm chọn chủ thể AI');
            showToast(isPos ? '🎯 Đã ghim điểm giữ chủ thể' : '❌ Đã ghim điểm loại trừ vùng thừa');
            try { render(previewCurrentSec); } catch(err) {}
            return true;
          }

          // INTERACTIVE MATTE TOOL: BRUSH KEEP / REMOVE
          if (aiMattingTool === 'brush_keep' || aiMattingTool === 'brush_remove') {
            isPaintingMatteBrush = true;
            const normX = (mouseX - studentBox.x) / studentBox.w;
            const normY = (mouseY - studentBox.y) / studentBox.h;
            lastBrushNormX = normX;
            lastBrushNormY = normY;
            if (userMatteCorrectionCanvas.width > 0 && userMatteCorrectionCanvas.height > 0) {
              const px = normX * userMatteCorrectionCanvas.width;
              const py = normY * userMatteCorrectionCanvas.height;
              userMatteCorrectionCtx.fillStyle = (aiMattingTool === 'brush_keep') ? '#00FF00' : '#FF0000';
              userMatteCorrectionCtx.beginPath();
              const r = Math.max(2, (aiMattingBrushSize / studentBox.w) * userMatteCorrectionCanvas.width * 0.5);
              userMatteCorrectionCtx.arc(px, py, r, 0, Math.PI * 2);
              userMatteCorrectionCtx.fill();
              hasUserMatteCorrections = true;
              try { render(previewCurrentSec); } catch(err) {}
            }
            return true;
          }

          isDraggingStudent = true;
          canvas.style.cursor = 'grabbing';
          studentDragStartX = mouseX;
          studentDragStartY = mouseY;
          studentDragOffsetX = mouseX - studentBox.centerX;
          studentDragOffsetY = mouseY - studentBox.centerY;
          studentHovered = true;
          try { render(previewCurrentSec); } catch(err) {}
          return true;
        }'''

assert old_pointer_down_check in html, "Failed to find old_pointer_down_check"
html = html.replace(old_pointer_down_check, new_pointer_down_check, 1)

# Pointer up
old_pointer_up_start = '''    function handleCanvasPointerUp() {
      let didAct = false;
      if (isDraggingStudent) {'''

new_pointer_up_start = '''    function handleCanvasPointerUp() {
      let didAct = false;
      if (isPaintingMatteBrush) {
        isPaintingMatteBrush = false;
        pushUndoState('Tô cọ viền mặt nạ BTV');
        didAct = true;
      }
      if (isDraggingStudent) {'''

assert old_pointer_up_start in html, "Failed to find old_pointer_up_start"
html = html.replace(old_pointer_up_start, new_pointer_up_start, 1)

# 5. Integrate prompt points & user corrections into processStudentChromaKey
old_process_start = '''        // Draw original video frame
        offscreenKeyCtx.globalCompositeOperation = 'source-over';
        offscreenKeyCtx.drawImage(studentVideoElem, 0, 0, procW, procH);'''

new_process_start = '''        // Ensure userMatteCorrectionCanvas matches character processing dimensions
        if (userMatteCorrectionCanvas.width !== procW || userMatteCorrectionCanvas.height !== procH) {
          const oldW = userMatteCorrectionCanvas.width;
          const oldH = userMatteCorrectionCanvas.height;
          const tempCorr = document.createElement('canvas');
          tempCorr.width = oldW; tempCorr.height = oldH;
          if (oldW > 0 && oldH > 0) {
            tempCorr.getContext('2d').drawImage(userMatteCorrectionCanvas, 0, 0);
          }
          userMatteCorrectionCanvas.width = procW;
          userMatteCorrectionCanvas.height = procH;
          if (oldW > 0 && oldH > 0) {
            userMatteCorrectionCtx.drawImage(tempCorr, 0, 0, procW, procH);
          }
        }

        // Draw original video frame
        offscreenKeyCtx.globalCompositeOperation = 'source-over';
        offscreenKeyCtx.drawImage(studentVideoElem, 0, 0, procW, procH);'''

assert old_process_start in html, "Failed to find old_process_start"
html = html.replace(old_process_start, new_process_start, 1)

# Apply prompt points after base temporal smoothing
old_temporal_apply = '''              // Bộ lọc thời gian thích ứng nhạy bén (Responsive Smooth Temporal Filter):
              if (enableAiAntiFlicker) {
                const prevA = aiTemporalAlphaBuffer[p];
                const diff = Math.abs(targetA - prevA);
                if (diff > 20) {
                  // Cử chỉ / chuyển động: Bám sát tức thì không trễ!
                  aiTemporalAlphaBuffer[p] = targetA;
                } else {
                  // Vùng ổn định: Lọc mượt chống nhấp nháy
                  const smoothA = prevA * 0.35 + targetA * 0.65;
                  aiTemporalAlphaBuffer[p] = smoothA;
                  targetA = Math.round(smoothA);
                }
              }

              fData[idx + 3] = targetA;
            }
          }'''

new_temporal_apply = '''              // Bộ lọc thời gian thích ứng nhạy bén (Responsive Smooth Temporal Filter):
              if (enableAiAntiFlicker) {
                const prevA = aiTemporalAlphaBuffer[p];
                const diff = Math.abs(targetA - prevA);
                if (diff > 20) {
                  // Cử chỉ / chuyển động: Bám sát tức thì không trễ!
                  aiTemporalAlphaBuffer[p] = targetA;
                } else {
                  // Vùng ổn định: Lọc mượt chống nhấp nháy
                  const smoothA = prevA * 0.35 + targetA * 0.65;
                  aiTemporalAlphaBuffer[p] = smoothA;
                  targetA = Math.round(smoothA);
                }
              }

              fData[idx + 3] = targetA;
            }
          }

          // 4A. ÁP DỤNG ĐIỂM CHỌN CHỦ THỂ (CLICK-TO-SELECT / PROMPT POINTS)
          if (aiMattingPromptPoints && aiMattingPromptPoints.length > 0) {
            for (let pt of aiMattingPromptPoints) {
              const ptPxX = pt.xNorm * procW;
              const ptPxY = pt.yNorm * procH;
              const ptRadius = pt.isPositive ? Math.max(24, procW * 0.18) : Math.max(18, procW * 0.14);
              const r2 = ptRadius * ptRadius;
              const minX = Math.max(0, Math.floor(ptPxX - ptRadius));
              const maxX = Math.min(procW - 1, Math.ceil(ptPxX + ptRadius));
              const minY = Math.max(0, Math.floor(ptPxY - ptRadius));
              const maxY = Math.min(procH - 1, Math.ceil(ptPxY + ptRadius));

              for (let py = minY; py <= maxY; py++) {
                const row = py * procW;
                for (let px = minX; px <= maxX; px++) {
                  const dx = px - ptPxX;
                  const dy = py - ptPxY;
                  const d2 = dx * dx + dy * dy;
                  if (d2 <= r2) {
                    const p = row + px;
                    const idx = p * 4;
                    if (pt.isPositive) {
                      const falloff = 1.0 - (d2 / r2);
                      const boostA = Math.round(255 * (falloff * 0.85 + 0.15));
                      if (boostA > fData[idx + 3]) {
                        fData[idx + 3] = boostA;
                        if (aiTemporalAlphaBuffer) aiTemporalAlphaBuffer[p] = boostA;
                      }
                    } else {
                      fData[idx + 3] = 0;
                      if (aiTemporalAlphaBuffer) aiTemporalAlphaBuffer[p] = 0;
                    }
                  }
                }
              }
            }
          }'''

assert old_temporal_apply in html, "Failed to find old_temporal_apply"
html = html.replace(old_temporal_apply, new_temporal_apply, 1)

# Apply user brush corrections before despill
old_before_despill = '''          // 7. Khử ám màu viền (Despill) an toàn'''
new_before_despill = '''          // 5C. ÁP DỤNG NÉT CỌ TÔ GIỮ / TÔ XÓA THỦ CÔNG CỦA NGƯỜI DÙNG (USER MATTE CORRECTIONS)
          if (hasUserMatteCorrections && userMatteCorrectionCanvas.width === procW && userMatteCorrectionCanvas.height === procH) {
            const corrData = userMatteCorrectionCtx.getImageData(0, 0, procW, procH).data;
            for (let p = 0; p < totalPix; p++) {
              const cIdx = p * 4;
              const ca = corrData[cIdx + 3];
              if (ca > 30) {
                const cr = corrData[cIdx], cg = corrData[cIdx + 1], cb = corrData[cIdx + 2];
                if (cg > 160 && cr < 90 && cb < 90) {
                  // CỌ XANH: Giữ trọn vẹn điểm ảnh (Alpha = 255)
                  fData[cIdx + 3] = 255;
                  if (aiTemporalAlphaBuffer) aiTemporalAlphaBuffer[p] = 255;
                } else if (cr > 160 && cg < 90 && cb < 90) {
                  // CỌ ĐỎ: Xóa sạch hoàn toàn (Alpha = 0)
                  fData[cIdx + 3] = 0;
                  if (aiTemporalAlphaBuffer) aiTemporalAlphaBuffer[p] = 0;
                }
              }
            }
          }

          // 7. Khử ám màu viền (Despill) an toàn'''

assert old_before_despill in html, "Failed to find old_before_despill"
html = html.replace(old_before_despill, new_before_despill, 1)

# 6. Update drawStudentCharacter for Alpha Matte and Overlays
old_draw_char_start = '''      // Base character size (approx 640 height at 100% scale)
      const baseH = 640;
      const charH = Math.round(baseH * studentScale);
      const charW = Math.round(charH * aspect);'''

new_draw_char_start = '''      // Base character size (approx 640 height at 100% scale)
      const baseH = 640;
      const charH = Math.round(baseH * studentScale);
      const charW = Math.round(charH * aspect);

      // ALPHA MATTE PREVIEW & EXPORT (LUMA MATTE)
      const isExportingNow = (typeof mediaRecorder !== 'undefined' && mediaRecorder && mediaRecorder.state === 'recording');
      const curPreviewMode = isExportingNow ? selectedExportMode : aiMattingPreviewMode;
      if (curPreviewMode === 'alpha_matte') {
        let alphaMatteCanvas = document.createElement('canvas');
        alphaMatteCanvas.width = processedCanvas.width;
        alphaMatteCanvas.height = processedCanvas.height;
        let aCtx = alphaMatteCanvas.getContext('2d');
        const pImg = processedCanvas.getContext('2d').getImageData(0, 0, processedCanvas.width, processedCanvas.height);
        const pD = pImg.data;
        for (let i = 0; i < pD.length; i += 4) {
          const a = pD[i + 3];
          pD[i] = a; pD[i + 1] = a; pD[i + 2] = a; pD[i + 3] = 255;
        }
        aCtx.putImageData(pImg, 0, 0);

        let targetX = studentPosX;
        let targetY = studentPosY;
        if (selectedAspectRatio === '9:16') {
          targetX = Math.round(targetX * (1080 / 1920));
          targetY = Math.round(targetY * (1920 / 1080));
        }
        ctx.save();
        ctx.translate(targetX, targetY);
        if (studentFlipH) ctx.scale(-1, 1);
        ctx.drawImage(alphaMatteCanvas, -charW / 2, -charH / 2, charW, charH);
        ctx.restore();
        return;
      }'''

assert old_draw_char_start in html, "Failed to find old_draw_char_start"
html = html.replace(old_draw_char_start, new_draw_char_start, 1)

# Draw brush overlay and prompt markers over character
old_draw_char_end = '''          ctx.drawImage(offscreenBeautyCanvas, x0, y0, charW, charH);
          ctx.restore();
        }
      }

      ctx.restore();

      // 4. INTERACTIVE ON-CANVAS TRANSFORM BOUNDING BOX (NEON DASHED FRAME & CORNER HANDLES)'''

new_draw_char_end = '''          ctx.drawImage(offscreenBeautyCanvas, x0, y0, charW, charH);
          ctx.restore();
        }
      }

      // Draw manual user brush strokes overlay
      if (hasUserMatteCorrections && userMatteCorrectionCanvas.width > 0) {
        ctx.save();
        ctx.globalAlpha = 0.45;
        ctx.drawImage(userMatteCorrectionCanvas, x0, y0, charW, charH);
        ctx.restore();
      }

      // Draw interactive prompt point pins (SAM / Magic Mask markers)
      if (aiMattingPromptPoints && aiMattingPromptPoints.length > 0) {
        ctx.save();
        for (let pt of aiMattingPromptPoints) {
          const px = x0 + pt.xNorm * charW;
          const py = y0 + pt.yNorm * charH;
          ctx.beginPath();
          ctx.arc(px, py, 11, 0, Math.PI * 2);
          ctx.fillStyle = pt.isPositive ? 'rgba(16, 185, 129, 0.85)' : 'rgba(239, 68, 68, 0.85)';
          ctx.fill();
          ctx.lineWidth = 2;
          ctx.strokeStyle = '#FFFFFF';
          ctx.stroke();
          ctx.font = 'bold 11px sans-serif';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillStyle = '#FFFFFF';
          ctx.fillText(pt.isPositive ? '🎯' : '✕', px, py);
        }
        ctx.restore();
      }

      ctx.restore();

      // 4. INTERACTIVE ON-CANVAS TRANSFORM BOUNDING BOX (NEON DASHED FRAME & CORNER HANDLES)'''

assert old_draw_char_end in html, "Failed to find old_draw_char_end"
html = html.replace(old_draw_char_end, new_draw_char_end, 1)

# 7. Update render function background handling
old_render_bg = '''      // CHROMA KEY GREEN SCREEN MODE (Xuất nền xanh lá cây cho CapCut)
      if (selectedExportMode === 'greenscreen') {
        ctx.fillStyle = '#00FF00';
        ctx.fillRect(0, 0, w, h);
      }
      const time = timeSec * 1.2;'''

new_render_bg = '''      // PREVIEW & EXPORT BACKGROUND HANDLING
      const isExportingRecording = (typeof mediaRecorder !== 'undefined' && mediaRecorder && mediaRecorder.state === 'recording');
      const effMode = isExportingRecording ? selectedExportMode : (aiMattingPreviewMode || 'studio');

      if (effMode === 'transparent_webm' || (!isExportingRecording && aiMattingPreviewMode === 'checkerboard')) {
        if (!isExportingRecording && aiMattingPreviewMode === 'checkerboard') {
          // VFX Checkerboard background
          const chkSize = 24;
          for (let cy = 0; cy < h; cy += chkSize) {
            for (let cx = 0; cx < w; cx += chkSize) {
              ctx.fillStyle = ((Math.floor(cx / chkSize) + Math.floor(cy / chkSize)) % 2 === 0) ? '#1E293B' : '#0F172A';
              ctx.fillRect(cx, cy, chkSize, chkSize);
            }
          }
        } else {
          ctx.clearRect(0, 0, w, h);
        }
      } else if (effMode === 'alpha_matte') {
        ctx.fillStyle = '#000000';
        ctx.fillRect(0, 0, w, h);
      } else if (effMode === 'greenscreen') {
        ctx.fillStyle = '#00FF00';
        ctx.fillRect(0, 0, w, h);
      }
      const time = timeSec * 1.2;'''

assert old_render_bg in html, "Failed to find old_render_bg"
html = html.replace(old_render_bg, new_render_bg, 1)

# Wrap studio background theme drawing
old_studio_bg = '''      // 1. Draw Studio Background according to selected theme
      if (selectedStudioTheme === 'talk11_talkshow') {'''

new_studio_bg = '''      // 1. Draw Studio Background according to selected theme (Only when in normal studio mode)
      if ((effMode === 'full' || effMode === 'studio') && selectedStudioTheme === 'talk11_talkshow') {'''

assert old_studio_bg in html, "Failed to find old_studio_bg"
html = html.replace(old_studio_bg, new_studio_bg, 1)

old_theme_anchor = '''      } else if (selectedStudioTheme === 'white_orange_anchor') {'''
new_theme_anchor = '''      } else if ((effMode === 'full' || effMode === 'studio') && selectedStudioTheme === 'white_orange_anchor') {'''
assert old_theme_anchor in html, "Failed to find old_theme_anchor"
html = html.replace(old_theme_anchor, new_theme_anchor, 1)

# Add brush cursor ring at end of render()
old_render_end = '''      // 8. Bottom Ticker
      drawScrollingTicker(h - 56, 56, inputTickerText.value, 3.2, timeSec);
    }'''

new_render_end = '''      // 8. Bottom Ticker (Only when in studio broadcast mode)
      if (effMode === 'full' || effMode === 'studio') {
        drawScrollingTicker(h - 56, 56, inputTickerText.value, 3.2, timeSec);
      }

      // Interactive Brush Cursor Ring on Canvas
      if (canvasHoverScreenX >= 0 && canvasHoverScreenY >= 0 && (aiMattingTool === 'brush_keep' || aiMattingTool === 'brush_remove')) {
        ctx.save();
        ctx.strokeStyle = (aiMattingTool === 'brush_keep') ? '#10B981' : '#EF4444';
        ctx.lineWidth = 2;
        ctx.setLineDash([4, 4]);
        ctx.beginPath();
        ctx.arc(canvasHoverScreenX, canvasHoverScreenY, aiMattingBrushSize * 0.5, 0, Math.PI * 2);
        ctx.stroke();
        ctx.restore();
      }
    }'''

assert old_render_end in html, "Failed to find old_render_end"
html = html.replace(old_render_end, new_render_end, 1)

# 8. Update startExport mimes & file naming for transparent WebM VP9
old_export_mimes = '''      // Ưu tiên phần cứng H.264 (MP4 / WebM) & VP8 trước để GPU tăng tốc, tránh nghẽn CPU do phần mềm VP9
      const mimes = [
        'video/mp4;codecs=avc1.42E01E,mp4a.40.2',
        'video/mp4;codecs=avc1',
        'video/mp4',
        'video/webm;codecs=h264,opus',
        'video/webm;codecs=h264',
        'video/webm;codecs=vp8,opus',
        'video/webm;codecs=vp8',
        'video/webm',
        'video/webm;codecs=vp9,opus',
        'video/webm;codecs=vp9'
      ];'''

new_export_mimes = '''      // Ưu tiên định dạng phù hợp theo chế độ xuất đã chọn
      let mimes = [];
      if (selectedExportMode === 'transparent_webm') {
        // Xuất video trong suốt: Bắt buộc dùng WebM với VP9 alpha codec
        mimes = [
          'video/webm;codecs=vp9,opus',
          'video/webm;codecs=vp9',
          'video/webm;codecs=vp8,opus',
          'video/webm'
        ];
      } else {
        mimes = [
          'video/mp4;codecs=avc1.42E01E,mp4a.40.2',
          'video/mp4;codecs=avc1',
          'video/mp4',
          'video/webm;codecs=h264,opus',
          'video/webm;codecs=h264',
          'video/webm;codecs=vp8,opus',
          'video/webm;codecs=vp8',
          'video/webm',
          'video/webm;codecs=vp9,opus',
          'video/webm;codecs=vp9'
        ];
      }'''

assert old_export_mimes in html, "Failed to find old_export_mimes"
html = html.replace(old_export_mimes, new_export_mimes, 1)

old_export_filename = '''          const ext = (selectedMime && selectedMime.includes('mp4')) ? 'mp4' : 'webm';
          const fileName = `TALK11_${cleanTitle}_${targetExportSec}s_${exportFps}fps_${Date.now()}.${ext}`;'''

new_export_filename = '''          const ext = (selectedExportMode === 'transparent_webm') ? 'webm' : ((selectedMime && selectedMime.includes('mp4')) ? 'mp4' : 'webm');
          let modeSuffix = '';
          if (selectedExportMode === 'transparent_webm') modeSuffix = '_TrongSuot_Alpha';
          else if (selectedExportMode === 'alpha_matte') modeSuffix = '_MatNa_AlphaMatte';
          else if (selectedExportMode === 'greenscreen') modeSuffix = '_PhongXanh';
          const fileName = `TALK11_${cleanTitle}${modeSuffix}_${targetExportSec}s_${exportFps}fps_${Date.now()}.${ext}`;'''

assert old_export_filename in html, "Failed to find old_export_filename"
html = html.replace(old_export_filename, new_export_filename, 1)

# 9. Add event listeners for interactive matte toolbar & preview pills
old_listeners_anchor = '''    document.getElementById('btnRunRvm4kBackend')?.addEventListener('click', triggerRvm4kBackendMatting);
    document.getElementById('btnWizRunRvm4k')?.addEventListener('click', triggerRvm4kBackendMatting);'''

new_listeners = '''    document.getElementById('btnRunRvm4kBackend')?.addEventListener('click', triggerRvm4kBackendMatting);
    document.getElementById('btnWizRunRvm4k')?.addEventListener('click', triggerRvm4kBackendMatting);

    // Interactive Matte Toolkit Event Handlers (SAM / Magic Mask / Roto Brush)
    const matteToolBtns = [
      { id: 'btnMatteToolAuto', tool: 'auto' },
      { id: 'btnMatteToolSelect', tool: 'select' },
      { id: 'btnMatteToolBrushKeep', tool: 'brush_keep' },
      { id: 'btnMatteToolBrushRemove', tool: 'brush_remove' }
    ];

    matteToolBtns.forEach(({ id, tool }) => {
      const btn = document.getElementById(id);
      if (btn) {
        btn.addEventListener('click', () => {
          aiMattingTool = tool;
          document.querySelectorAll('#matteToolPills button').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          if (tool === 'select') {
            showToast('🎯 Chế độ Chọn Người: Click chuột lên người để ghim giữ chủ thể (Shift+Click để loại trừ)');
          } else if (tool === 'brush_keep') {
            showToast('🖌️ Cọ Giữ: Quét chuột lên vùng tóc hoặc thân thể bị lẹm để lấy lại');
          } else if (tool === 'brush_remove') {
            showToast('🧹 Cọ Xóa: Quét chuột lên vùng tường thừa hoặc viền lem để xóa sạch');
          } else {
            showToast('🤖 Chế độ Tự Động: Kéo thả và điều chỉnh khung nhân vật bình thường');
          }
          try { render(previewCurrentSec); } catch(err) {}
        });
      }
    });

    const sliderMatteBrushSize = document.getElementById('sliderMatteBrushSize');
    if (sliderMatteBrushSize) {
      sliderMatteBrushSize.addEventListener('input', (e) => {
        aiMattingBrushSize = parseInt(e.target.value) || 24;
        const valLbl = document.getElementById('valMatteBrushSize');
        if (valLbl) valLbl.textContent = `${aiMattingBrushSize}px`;
        try { render(previewCurrentSec); } catch(err) {}
      });
    }

    const btnClearMatteStrokes = document.getElementById('btnClearMatteStrokes');
    if (btnClearMatteStrokes) {
      btnClearMatteStrokes.addEventListener('click', () => {
        aiMattingPromptPoints = [];
        hasUserMatteCorrections = false;
        if (userMatteCorrectionCanvas.width > 0 && userMatteCorrectionCanvas.height > 0) {
          userMatteCorrectionCtx.clearRect(0, 0, userMatteCorrectionCanvas.width, userMatteCorrectionCanvas.height);
        }
        pushUndoState('Đặt lại cọ vẽ và điểm chọn');
        showToast('↺ Đã đặt lại toàn bộ cọ vẽ và điểm chọn thủ công');
        try { render(previewCurrentSec); } catch(err) {}
      });
    }

    // Preview Mode Pills (Studio / Checkerboard / Alpha Matte / Green Screen)
    const prevModeBtns = [
      { id: 'btnPrevModeStudio', mode: 'studio' },
      { id: 'btnPrevModeCheckerboard', mode: 'checkerboard' },
      { id: 'btnPrevModeAlpha', mode: 'alpha_matte' },
      { id: 'btnPrevModeGreen', mode: 'greenscreen' }
    ];

    prevModeBtns.forEach(({ id, mode }) => {
      const btn = document.getElementById(id);
      if (btn) {
        btn.addEventListener('click', () => {
          aiMattingPreviewMode = mode;
          document.querySelectorAll('#aiMattingPreviewPills button').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          try { render(previewCurrentSec); } catch(err) {}
        });
      }
    });

    const btnQualityFast = document.getElementById('btnQualityFast');
    if (btnQualityFast) {
      btnQualityFast.addEventListener('click', () => {
        studentChromaMode = 'ai_auto';
        showToast('⚡ Đã chuyển sang chế độ Tách Nền Realtime 60FPS (Client AI)');
        try { render(previewCurrentSec); } catch(err) {}
      });
    }'''

assert old_listeners_anchor in html, "Failed to find old_listeners_anchor"
html = html.replace(old_listeners_anchor, new_listeners, 1)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("✓ Successfully updated Tao_Khung_Thoi_Su_Talk11.html!")
