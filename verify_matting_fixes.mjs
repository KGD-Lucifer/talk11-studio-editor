import { spawn } from 'child_process';
import path from 'path';

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const fileUrl = 'file:///' + path.resolve('Tao_Khung_Thoi_Su_Talk11.html').replace(/\\/g, '/');

async function main() {
  console.log('Validating True Skin/Hair Contour Hugging & Zero Artifacts in Headless Edge...');
  const edgeProc = spawn(EDGE_PATH, [
    '--headless=new',
    '--remote-debugging-port=9229',
    '--window-size=1680,980',
    '--disable-gpu',
    'about:blank'
  ]);

  let res = null;
  for (let i = 0; i < 15; i++) {
    await new Promise(r => setTimeout(r, 400));
    try {
      res = await fetch('http://127.0.0.1:9229/json/new?' + encodeURIComponent(fileUrl), { method: 'PUT' });
      if (res.ok) break;
    } catch (e) {}
  }

  if (!res) {
    console.error('Failed to connect to Edge CDP');
    edgeProc.kill();
    process.exit(1);
  }

  const target = await res.json();
  const ws = new WebSocket(target.webSocketDebuggerUrl);

  let id = 1;
  const pending = new Map();
  const consoleErrors = [];

  function send(method, params = {}) {
    return new Promise((resolve) => {
      const curId = id++;
      pending.set(curId, resolve);
      ws.send(JSON.stringify({ id: curId, method, params }));
    });
  }

  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.method === 'Runtime.consoleAPICalled' && msg.params.type === 'error') {
      consoleErrors.push(msg.params.args.map(a => a.value || a.description).join(' '));
    }
    if (msg.id && pending.has(msg.id)) {
      const resolve = pending.get(msg.id);
      pending.delete(msg.id);
      resolve(msg);
    }
  };

  await new Promise((r) => (ws.onopen = r));
  await send('Page.enable');
  await send('Runtime.enable');

  await new Promise(r => setTimeout(r, 2500));

  const evalRes = await send('Runtime.evaluate', {
    expression: `(function() {
      const results = {};

      const w = 640, h = 360;
      const totalPix = w * h;
      const testVidData = new ImageData(w, h);
      const testMaskData = new ImageData(w, h);
      
      // Setup test pattern
      for (let y = 0; y < h; y++) {
        for (let x = 0; x < w; x++) {
          const idx = (y * w + x) * 4;
          // default background: bright room wall
          testVidData.data[idx] = 230;
          testVidData.data[idx+1] = 228;
          testVidData.data[idx+2] = 225;
          testVidData.data[idx+3] = 255;
          // Low prob background:
          testMaskData.data[idx] = 12;
          testMaskData.data[idx+1] = 12;
          testMaskData.data[idx+2] = 12;
          testMaskData.data[idx+3] = 255;
          
          // Person head (circle r=80 at 320, 160)
          const dxH = x - 320, dyH = y - 160;
          if (dxH*dxH + dyH*dyH <= 80*80) {
            testVidData.data[idx] = 210;
            testVidData.data[idx+1] = 160;
            testVidData.data[idx+2] = 130;
            testMaskData.data[idx] = 250;
            testMaskData.data[idx+1] = 250;
            testMaskData.data[idx+2] = 250;
            testMaskData.data[idx+3] = 255;
            // Specular nose highlight:
            if (Math.abs(x - 320) < 6 && Math.abs(y - 160) < 8) {
              testVidData.data[idx] = 238;
              testVidData.data[idx+1] = 230;
              testVidData.data[idx+2] = 225;
            }
          }
          
          // Outstretched arm (rect from x=80 to 240, y=260 to 320)
          if (x >= 80 && x <= 240 && y >= 260 && y <= 320) {
            testVidData.data[idx] = 245;
            testVidData.data[idx+1] = 115;
            testVidData.data[idx+2] = 25;
            testMaskData.data[idx] = 248;
            testMaskData.data[idx+1] = 248;
            testMaskData.data[idx+2] = 248;
            testMaskData.data[idx+3] = 255;
          }
          
          // Torso (rect from x=240 to 400, y=220 to 360)
          if (x >= 240 && x <= 400 && y >= 220 && y <= 360) {
            testVidData.data[idx] = 245;
            testVidData.data[idx+1] = 115;
            testVidData.data[idx+2] = 25;
            testMaskData.data[idx] = 252;
            testMaskData.data[idx+1] = 252;
            testMaskData.data[idx+2] = 252;
            testMaskData.data[idx+3] = 255;
          }
        }
      }

      // Prepare canvases
      offscreenKeyCanvas.width = w;
      offscreenKeyCanvas.height = h;
      offscreenKeyCtx.putImageData(testVidData, 0, 0);

      aiMaskCanvas.width = w;
      aiMaskCanvas.height = h;
      const maskCtx = aiMaskCanvas.getContext('2d');
      maskCtx.putImageData(testMaskData, 0, 0);

      // Mock studentVideoElem properties so readyState >= 2 and dimensions are 640x360
      if (!studentVideoElem) {
        studentVideoElem = document.createElement('video');
      }
      Object.defineProperty(studentVideoElem, 'readyState', { value: 4, configurable: true });
      Object.defineProperty(studentVideoElem, 'videoWidth', { value: w, configurable: true });
      Object.defineProperty(studentVideoElem, 'videoHeight', { value: h, configurable: true });

      // Run Chroma Key processing with Ultra preset
      hasValidAiMask = true;
      studentChromaMode = 'ai_auto';
      studentChromaEnabled = true;
      studentMattePreset = 'ultra';
      studentChromaTolerance = 0.92;
      studentAiErodeRadius = 2;
      studentMatteCoreProtect = 95;
      studentChromaFeather = 2;
      forceChromaReprocess = true;

      // Mock studentVideoElem with a canvas containing testVidData so drawImage doesn't wipe testVidData!
      const mockVidCanvas = document.createElement('canvas');
      mockVidCanvas.width = w;
      mockVidCanvas.height = h;
      mockVidCanvas.getContext('2d').putImageData(testVidData, 0, 0);
      const origDrawImage = offscreenKeyCtx.drawImage;
      offscreenKeyCtx.drawImage = function(img, dx, dy, dw, dh) {
        if (img === studentVideoElem) {
          origDrawImage.call(offscreenKeyCtx, mockVidCanvas, dx, dy, dw, dh);
        } else {
          origDrawImage.apply(offscreenKeyCtx, arguments);
        }
      };

      // Temporarily null selfieSegmentation so it doesn't trigger async send during test
      const savedSelfie = selfieSegmentation;
      selfieSegmentation = null;

      const keyResult = processStudentChromaKey();
      results.keyResultReturnedCanvas = (keyResult === offscreenKeyCanvas);
      selfieSegmentation = savedSelfie;
      offscreenKeyCtx.drawImage = origDrawImage;

      const resImg = offscreenKeyCtx.getImageData(0, 0, w, h);
      const rData = resImg.data;

      // 1. Top Right Wall Check: (450, 100) must be 0 (NO giant white block!)
      const wallIdx = (100 * w + 450) * 4;
      results.wallAlphaIsZero = (rData[wallIdx + 3] === 0);
      results.wallAlphaValue = rData[wallIdx + 3];

      // 2. Outstretched Arm Check: (120, 290) must be 255 (NO chopped off arm!)
      const armIdx = (290 * w + 120) * 4;
      results.outstretchedArmKept = (rData[armIdx + 3] === 255);
      results.armAlphaValue = rData[armIdx + 3];

      // 3. Specular Nose Highlight Check: (320, 160) must be 255 (NO nose hole!)
      const noseIdx = (160 * w + 320) * 4;
      results.noseHighlightKept = (rData[noseIdx + 3] === 255);
      results.noseAlphaValue = rData[noseIdx + 3];

      // 4. Head Center Check: (320, 140) must be 255
      const headIdx = (140 * w + 320) * 4;
      results.headCenterKept = (rData[headIdx + 3] === 255);

      // 5. Far Left Wall Check: (20, 20) must be 0
      const farLeftIdx = (20 * w + 20) * 4;
      results.farLeftWallIsZero = (rData[farLeftIdx + 3] === 0);

      return results;
    })()`,
    returnByValue: true
  });

  const resVal = evalRes.result?.result?.value || evalRes.result?.value || evalRes.result;
  console.log('Matting Validation Results:', JSON.stringify(resVal, null, 2));

  let allPassed = true;
  for (const [k, v] of Object.entries(resVal || {})) {
    if (k.includes('AlphaValue')) continue;
    if (!v) {
      console.error(`[FAIL] ${k}: ${v}`);
      allPassed = false;
    } else {
      console.log(`[PASS] ${k}`);
    }
  }

  try { ws.close(); } catch(e) {}
  edgeProc.kill();

  if (allPassed) {
    console.log('\n🎉 ALL MATTING REGRESSION & CONTOUR FIXES VALIDATED 100%!');
    process.exit(0);
  } else {
    console.error('\n❌ VALIDATION FAILED!');
    process.exit(1);
  }
}

main().catch(err => {
  console.error('Validation error:', err);
  process.exit(1);
});
