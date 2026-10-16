import os
import sys

src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Tao_Khung_Thoi_Su_Talk11.html')
if not os.path.exists(src_path):
    print(f"Error: {src_path} not found")
    sys.exit(1)

with open(src_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add tf.min.js in <head>
tfjs_tag = '''  <!-- TensorFlow.js for Robust Video Matting (RVM - CapCut Pro Core Model) -->
  <script src="03_ASSETS/tfjs/tf.min.js"></script>
  <script>
    if (typeof tf === 'undefined') {
      document.write('<script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@3.21.0/dist/tf.min.js" crossorigin="anonymous"><\\/script>');
    }
  </script>'''

old_head_marker = '  <!-- Google MediaPipe AI Person Segmentation (Local Offline Fast-Load + CDN Fallback) -->'
if tfjs_tag not in content:
    assert old_head_marker in content, "old_head_marker not found"
    content = content.replace(old_head_marker, tfjs_tag + '\n' + old_head_marker, 1)

# 2. Update Chroma Key UI Badge and Add RVM 4K Backend Button
old_ui_header = '''              <span id="badgeAiSegmentStatus" style="font-size: 8.5px; color: #34D399; font-weight: 700; background: rgba(16,185,129,0.15); padding: 1px 5px; border-radius: 4px; border: 1px solid rgba(16,185,129,0.3);">🤖 AI Tự Động</span>
            </div>'''

new_ui_header = '''              <span id="badgeAiSegmentStatus" style="font-size: 8.5px; color: #F59E0B; font-weight: 700; background: rgba(245,158,11,0.15); padding: 1px 5px; border-radius: 4px; border: 1px solid rgba(245,158,11,0.35);">👑 AI RVM CapCut Pro</span>
            </div>'''

assert old_ui_header in content, "old_ui_header not found"
content = content.replace(old_ui_header, new_ui_header, 1)

old_hint = '''            <div id="hintAiSegmentation" style="font-size: 8.5px; color: #34D399; line-height: 1.35; background: rgba(16,185,129,0.08); padding: 3px 6px; border-radius: 4px; border-left: 2px solid #10B981;">
              🤖 <b>AI Tách Người:</b> Tự động nhận diện & giữ trọn cơ thể, khuôn mặt bé; xóa sạch 100% nền phòng đằng sau không cần phông xanh!
            </div>'''

new_hint = '''            <div id="hintAiSegmentation" style="font-size: 8.5px; color: #F59E0B; line-height: 1.35; background: rgba(245,158,11,0.08); padding: 4px 6px; border-radius: 4px; border-left: 2px solid #F59E0B;">
              👑 <b>AI RVM (Robust Video Matting):</b> Thuật toán cốt lõi của CapCut PC — Bóc tách từng sợi tóc tơ & nếp áo, khử rung giật thời gian thực và khử 100% quầng sáng tường phòng!
            </div>

            <button type="button" id="btnRunRvm4kBackend" style="width: 100%; background: linear-gradient(135deg, #F59E0B, #D97706); color: #0F172A; font-weight: 800; font-size: 9.5px; border: none; border-radius: 4px; padding: 5px 8px; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 5px; box-shadow: 0 2px 6px rgba(245, 158, 11, 0.25); transition: all 0.15s ease;">
              <span>👑 Xuất Video Tách Nền RVM 4K Siêu Nét (AI Backend ONNX)</span>
            </button>'''

assert old_hint in content, "old_hint not found"
content = content.replace(old_hint, new_hint, 1)

# 3. Add RVM Engine State Variables
old_rvm_vars_marker = '    // Google MediaPipe AI Person Segmentation State'
new_rvm_vars = '''    // Robust Video Matting (RVM - CapCut Pro Core Neural Network) State
    let rvmModel = null;
    let rvmModelReady = false;
    let isRvmInferencing = false;
    let lastRvmInferTime = 0;
    let rvmRecurrentStates = null;
    let rvmDownsampleRatio = null;
    let rvmOutputCanvas = document.createElement('canvas');
    let rvmOutputCtx = rvmOutputCanvas.getContext('2d');
    let hasValidRvmMatte = false;

    // Google MediaPipe AI Person Segmentation State'''

assert old_rvm_vars_marker in content, "old_rvm_vars_marker not found"
content = content.replace(old_rvm_vars_marker, new_rvm_vars, 1)

# 4. Add initRvmWebModel and runRvmFrameInference functions
old_init_mediapipe = '    function initMediaPipeSelfie() {'
rvm_functions = '''    // ========================================================
    // ROBUST VIDEO MATTING (RVM - CAPCUT PRO CORE ENGINE)
    // ========================================================
    async function initRvmWebModel() {
      if (typeof tf === 'undefined' || rvmModel) return;
      try {
        console.log('🔄 Đang nạp Robust Video Matting (RVM - CapCut Pro)...');
        rvmModel = await tf.loadGraphModel('03_ASSETS/models/rvm/rvm_mobilenetv3_tfjs_int8/model.json');
        rvmRecurrentStates = [
          tf.tensor(0.),
          tf.tensor(0.),
          tf.tensor(0.),
          tf.tensor(0.)
        ];
        rvmDownsampleRatio = tf.tensor(0.25);
        rvmModelReady = true;
        console.log('✓ Robust Video Matting (RVM) loaded & ready!');
        const badge = document.getElementById('badgeAiSegmentStatus');
        if (badge) {
          badge.textContent = '👑 AI RVM CapCut Pro';
          badge.style.color = '#F59E0B';
        }
      } catch (err) {
        console.warn('RVM Web Model load fallback to MediaPipe:', err);
      }
    }

    async function runRvmFrameInference(vidElem, w, h) {
      if (!rvmModel || !rvmModelReady || isRvmInferencing) return;
      isRvmInferencing = true;
      try {
        const outputs = await tf.tidy(() => {
          const tfImg = tf.browser.fromPixels(vidElem);
          const src = tfImg.expandDims(0).div(255);
          return rvmModel.executeAsync(
            {
              src: src,
              r1i: rvmRecurrentStates[0],
              r2i: rvmRecurrentStates[1],
              r3i: rvmRecurrentStates[2],
              r4i: rvmRecurrentStates[3],
              downsample_ratio: rvmDownsampleRatio
            },
            ['fgr', 'pha', 'r1o', 'r2o', 'r3o', 'r4o']
          );
        });

        const [fgr, pha, r1o, r2o, r3o, r4o] = await outputs;

        // Dispose old recurrent states and save new ones
        tf.dispose(rvmRecurrentStates);
        rvmRecurrentStates = [r1o, r2o, r3o, r4o];

        // Combine decontaminated fgr (RGB) and continuous pha (Alpha) into RGBA
        const rgbaTensor = tf.tidy(() => {
          const rgb = fgr.squeeze(0).mul(255).cast('int32');
          const a = pha.squeeze(0).mul(255).cast('int32');
          return tf.concat([rgb, a], -1);
        });

        const [mH, mW] = rgbaTensor.shape.slice(0, 2);
        const pixelData = new Uint8ClampedArray(await rgbaTensor.data());
        const imgData = new ImageData(pixelData, mW, mH);

        if (rvmOutputCanvas.width !== mW || rvmOutputCanvas.height !== mH) {
          rvmOutputCanvas.width = mW;
          rvmOutputCanvas.height = mH;
        }
        rvmOutputCtx.putImageData(imgData, 0, 0);
        hasValidRvmMatte = true;

        tf.dispose([fgr, pha, rgbaTensor]);
      } catch (err) {
        console.warn('RVM inference error:', err);
      } finally {
        isRvmInferencing = false;
      }
    }

    function initMediaPipeSelfie() {'''

assert old_init_mediapipe in content, "old_init_mediapipe not found"
content = content.replace(old_init_mediapipe, rvm_functions, 1)

# 5. In processStudentChromaKey: trigger RVM inference and use rvmOutputCanvas if available
old_mode1_header = '''      // ----------------------------------------------------
      // MODE 1: AI PERSON SEGMENTATION (MỌI PHÒNG • KHÔNG CẦN PHÔNG XANH)
      // ----------------------------------------------------
      if (studentChromaMode === 'ai_auto') {
        if (typeof SelfieSegmentation !== 'undefined' && !selfieSegmentation) {
          initMediaPipeSelfie();
        }'''

new_mode1_header = '''      // ----------------------------------------------------
      // MODE 1: AI PERSON SEGMENTATION & RVM CAPCUT PRO MATTING
      // ----------------------------------------------------
      if (studentChromaMode === 'ai_auto') {
        if (!rvmModel && typeof tf !== 'undefined') {
          initRvmWebModel();
        }
        if (typeof SelfieSegmentation !== 'undefined' && !selfieSegmentation) {
          initMediaPipeSelfie();
        }

        // ƯU TIÊN 1: Chạy mô hình Robust Video Matting (RVM - CapCut Pro) nếu đã nạp
        if (rvmModelReady && !isRvmInferencing && studentVideoElem.readyState >= 2) {
          const rvmNow = performance.now();
          if (rvmNow - lastRvmInferTime > 32) {
            lastRvmInferTime = rvmNow;
            runRvmFrameInference(studentVideoElem, procW, procH);
          }
        }

        if (hasValidRvmMatte && rvmOutputCanvas.width > 0 && rvmOutputCanvas.height > 0) {
          offscreenKeyCtx.globalCompositeOperation = 'copy';
          offscreenKeyCtx.drawImage(rvmOutputCanvas, 0, 0, procW, procH);
          offscreenKeyCtx.globalCompositeOperation = 'source-over';
          return offscreenKeyCanvas;
        }'''

assert old_mode1_header in content, "old_mode1_header not found"
content = content.replace(old_mode1_header, new_mode1_header, 1)

# 6. Add event listener for btnRunRvm4kBackend
old_listener_marker = "    document.getElementById('sliderChromaTolerance')?.addEventListener('input',"
new_listener = '''    // 1-Click RVM 4K Backend Matting
    document.getElementById('btnRunRvm4kBackend')?.addEventListener('click', async () => {
      if (!studentVideoUrl && !currentStudentVideoBlob) {
        showToast('⚠️ Vui lòng tải video học viên lên trước khi chạy tách nền 4K!');
        return;
      }
      const btn = document.getElementById('btnRunRvm4kBackend');
      if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<span>⏳ Đang chạy AI RVM 4K... Vui lòng đợi</span>';
      }
      showToast('🚀 Đang gửi video đến máy chủ AI RVM (Robust Video Matting ONNX)...');

      try {
        const res = await fetch('/api/rvm-matte', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ input: studentVideoFileName || 'student_input_sample.mp4' })
        });
        const data = await res.json();
        if (data.success && data.outputUrl) {
          showToast('🎉 Tách nền AI RVM 4K hoàn tất! Đang nạp video vào timeline...');
          studentVideoUrl = data.outputUrl;
          if (studentVideoElem) {
            studentVideoElem.src = data.outputUrl;
            studentVideoElem.load();
          }
        } else {
          showToast('⚠️ Lỗi xử lý backend: ' + (data.error || 'Thử lại'));
        }
      } catch (err) {
        console.error('RVM backend request failed:', err);
        showToast('⚠️ Lỗi kết nối backend AI: ' + err.message);
      } finally {
        if (btn) {
          btn.disabled = false;
          btn.innerHTML = '<span>👑 Xuất Video Tách Nền RVM 4K Siêu Nét (AI Backend ONNX)</span>';
        }
      }
    });

    document.getElementById('sliderChromaTolerance')?.addEventListener('input','''

assert old_listener_marker in content, "old_listener_marker not found"
content = content.replace(old_listener_marker, new_listener, 1)

with open(src_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("[SUCCESS] Robust Video Matting (RVM - CapCut Pro) integrated successfully into Tao_Khung_Thoi_Su_Talk11.html!")
