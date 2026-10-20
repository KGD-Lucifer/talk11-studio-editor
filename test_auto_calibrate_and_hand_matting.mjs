import { spawn } from 'child_process';
import path from 'path';

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const fileUrl = 'file:///' + path.resolve('Tao_Khung_Thoi_Su_Talk11.html').replace(/\\/g, '/');

async function main() {
  console.log('Testing Auto-Calibrate, Hand/Finger Boundary Snapping & Fallback in Headless Edge...');
  const edgeProc = spawn(EDGE_PATH, [
    '--headless=new',
    '--remote-debugging-port=9227',
    '--window-size=1680,980',
    '--disable-gpu',
    'about:blank'
  ]);

  let res = null;
  for (let i = 0; i < 15; i++) {
    await new Promise(r => setTimeout(r, 400));
    try {
      res = await fetch('http://127.0.0.1:9227/json/new?' + encodeURIComponent(fileUrl), { method: 'PUT' });
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

      // 1. Check UI elements
      const btnWizCal = document.getElementById('btnWizAutoCalibrate');
      const btnProCal = document.getElementById('btnProAutoCalibrate');
      results.hasBtnWizAutoCalibrate = !!btnWizCal;
      results.hasBtnProAutoCalibrate = !!btnProCal;

      // 2. Mock student video element with a bright room wall pattern
      const w = 640, h = 360;
      const testCanvas = document.createElement('canvas');
      testCanvas.width = w;
      testCanvas.height = h;
      const tCtx = testCanvas.getContext('2d');
      const imgData = tCtx.createImageData(w, h);
      const d = imgData.data;

      // Fill with bright white/cream wall (235, 230, 225)
      for (let i = 0; i < w * h; i++) {
        d[i * 4] = 235;
        d[i * 4 + 1] = 230;
        d[i * 4 + 2] = 225;
        d[i * 4 + 3] = 255;
      }
      tCtx.putImageData(imgData, 0, 0);

      if (!studentVideoElem) studentVideoElem = document.createElement('video');
      Object.defineProperty(studentVideoElem, 'readyState', { value: 4, configurable: true });
      Object.defineProperty(studentVideoElem, 'videoWidth', { value: w, configurable: true });
      Object.defineProperty(studentVideoElem, 'videoHeight', { value: h, configurable: true });

      // Mock drawImage to draw testCanvas
      const origDraw = CanvasRenderingContext2D.prototype.drawImage;
      CanvasRenderingContext2D.prototype.drawImage = function(img) {
        if (img === studentVideoElem) {
          origDraw.call(this, testCanvas, 0, 0, this.canvas.width, this.canvas.height);
        } else {
          origDraw.apply(this, arguments);
        }
      };

      // Test Auto-Calibrate execution
      btnWizCal.click();
      results.autoCalibrateSetsTol92 = (studentChromaTolerance === 0.92);
      results.autoCalibrateSetsErode2 = (studentAiErodeRadius === 2);
      results.autoCalibrateSetsCore95 = (studentMatteCoreProtect === 95);
      results.autoCalibrateSetsHair85 = (studentMatteHairDetail === 85);

      // 3. Test Hand and Finger Separation in AI Mode
      // Create a test frame with two fingers (skin) separated by a white wall gap
      // Finger 1 at x=300..306, y=200..260
      // Wall gap at x=307..312, y=200..260
      // Finger 2 at x=313..319, y=200..260
      const testVidData = new ImageData(w, h);
      const testMaskData = new ImageData(w, h);

      for (let y = 0; y < h; y++) {
        for (let x = 0; x < w; x++) {
          const idx = (y * w + x) * 4;
          // default white wall
          testVidData.data[idx] = 232;
          testVidData.data[idx+1] = 228;
          testVidData.data[idx+2] = 224;
          testVidData.data[idx+3] = 255;
          // low prob background
          testMaskData.data[idx] = 10;
          testMaskData.data[idx+1] = 10;
          testMaskData.data[idx+2] = 10;
          testMaskData.data[idx+3] = 255;

          // Head (center at 320, 100)
          const dxH = x - 320, dyH = y - 100;
          if (dxH*dxH + dyH*dyH <= 45*45) {
            testVidData.data[idx] = 210;
            testVidData.data[idx+1] = 160;
            testVidData.data[idx+2] = 130;
            testMaskData.data[idx] = 252;
            testMaskData.data[idx+1] = 252;
            testMaskData.data[idx+2] = 252;
            testMaskData.data[idx+3] = 255;
          }

          // Finger 1 (x=300..306, y=200..260) - Asian skin tone
          if (x >= 300 && x <= 306 && y >= 200 && y <= 260) {
            testVidData.data[idx] = 215;
            testVidData.data[idx+1] = 155;
            testVidData.data[idx+2] = 125;
            testMaskData.data[idx] = 180; // moderate neural prob
            testMaskData.data[idx+1] = 180;
            testMaskData.data[idx+2] = 180;
            testMaskData.data[idx+3] = 255;
          }

          // Wall gap between fingers (x=307..312, y=200..260)
          // Notice neural network had soft blur prob 120 across gap!
          if (x >= 307 && x <= 312 && y >= 200 && y <= 260) {
            testVidData.data[idx] = 232; // pure white wall
            testVidData.data[idx+1] = 228;
            testVidData.data[idx+2] = 224;
            testMaskData.data[idx] = 110; // blurred neural mask into gap
            testMaskData.data[idx+1] = 110;
            testMaskData.data[idx+2] = 110;
            testMaskData.data[idx+3] = 255;
          }

          // Finger 2 (x=313..319, y=200..260) - Asian skin tone
          if (x >= 313 && x <= 319 && y >= 200 && y <= 260) {
            testVidData.data[idx] = 215;
            testVidData.data[idx+1] = 155;
            testVidData.data[idx+2] = 125;
            testMaskData.data[idx] = 180;
            testMaskData.data[idx+1] = 180;
            testMaskData.data[idx+2] = 180;
            testMaskData.data[idx+3] = 255;
          }
        }
      }

      offscreenKeyCanvas.width = w;
      offscreenKeyCanvas.height = h;
      offscreenKeyCtx.putImageData(testVidData, 0, 0);

      aiMaskCanvas.width = w;
      aiMaskCanvas.height = h;
      aiMaskCanvas.getContext('2d').putImageData(testMaskData, 0, 0);

      const mockCanvas = document.createElement('canvas');
      mockCanvas.width = w; mockCanvas.height = h;
      mockCanvas.getContext('2d').putImageData(testVidData, 0, 0);

      CanvasRenderingContext2D.prototype.drawImage = function(img) {
        if (img === studentVideoElem) {
          origDraw.call(this, mockCanvas, 0, 0, this.canvas.width, this.canvas.height);
        } else {
          origDraw.apply(this, arguments);
        }
      };

      hasValidAiMask = true;
      studentChromaMode = 'ai_auto';
      studentChromaEnabled = true;
      forceChromaReprocess = true;

      const savedSelfie = selfieSegmentation;
      selfieSegmentation = null;
      processStudentChromaKey();
      selfieSegmentation = savedSelfie;
      CanvasRenderingContext2D.prototype.drawImage = origDraw;

      const outData = offscreenKeyCtx.getImageData(0, 0, w, h).data;

      // Finger 1 test at (303, 230): Must be solid (255)
      const f1Idx = (230 * w + 303) * 4;
      results.finger1IsSolid = (outData[f1Idx + 3] === 255);
      results.finger1Alpha = outData[f1Idx + 3];

      // Wall gap test at (309, 230): Must be completely clear (0)
      const gapIdx = (230 * w + 309) * 4;
      results.wallGapBetweenFingersIsZero = (outData[gapIdx + 3] === 0);
      results.gapAlpha = outData[gapIdx + 3];

      // Finger 2 test at (316, 230): Must be solid (255)
      const f2Idx = (230 * w + 316) * 4;
      results.finger2IsSolid = (outData[f2Idx + 3] === 255);
      results.finger2Alpha = outData[f2Idx + 3];

      // 4. Test Fallback Mode Bookshelf Discard
      // Bookshelf at x=50, y=180 (brown wood: 110, 75, 45)
      // Head at x=320, y=100
      const fbData = new ImageData(w, h);
      for (let i = 0; i < w * h; i++) {
        fbData.data[i * 4] = 230;
        fbData.data[i * 4 + 1] = 228;
        fbData.data[i * 4 + 2] = 225;
        fbData.data[i * 4 + 3] = 255;
      }
      // Put bookshelf at x=0..120, y=0..360 (wooden brown)
      for (let y = 0; y < h; y++) {
        for (let x = 0; x < 120; x++) {
          const idx = (y * w + x) * 4;
          fbData.data[idx] = 110;
          fbData.data[idx+1] = 75;
          fbData.data[idx+2] = 45;
        }
      }
      // Put student face at x=320, y=100 (r=45)
      for (let y = 0; y < h; y++) {
        for (let x = 200; x < 440; x++) {
          const dx = x - 320, dy = y - 100;
          if (dx*dx + dy*dy <= 45*45) {
            const idx = (y * w + x) * 4;
            fbData.data[idx] = 210;
            fbData.data[idx+1] = 160;
            fbData.data[idx+2] = 130;
          }
        }
      }

      runPureJsSubjectMattingFallback(fbData, w, h, 0.92, 2);

      // Bookshelf at (50, 180) must be 0
      const bsIdx = (180 * w + 50) * 4;
      results.bookshelfDiscardedInFallback = (fbData.data[bsIdx + 3] === 0);
      results.bookshelfAlpha = fbData.data[bsIdx + 3];

      // Student face at (320, 100) must be 255
      const faceIdx = (100 * w + 320) * 4;
      results.studentFaceKeptInFallback = (fbData.data[faceIdx + 3] === 255);
      results.faceAlpha = fbData.data[faceIdx + 3];

      return results;
    })()`,
    returnByValue: true
  });

  const resVal = evalRes.result?.result?.value || evalRes.result?.value || evalRes.result;
  console.log('Test Results:', JSON.stringify(resVal, null, 2));

  let allPassed = true;
  for (const [k, v] of Object.entries(resVal)) {
    if (v === true) {
      console.log(`[PASS] ${k}`);
    } else if (typeof v === 'boolean') {
      console.error(`[FAIL] ${k}: ${v}`);
      allPassed = false;
    }
  }

  if (consoleErrors.length > 0) {
    console.error('Console Errors:', consoleErrors);
    allPassed = false;
  }

  if (allPassed) {
    console.log('\n🎉 ALL AUTO-CALIBRATE, HAND SEPARATION & BOOKSHELF TESTS PASSED 100%!');
  } else {
    console.error('\n❌ SOME TESTS FAILED!');
    process.exit(1);
  }

  edgeProc.kill();
  process.exit(0);
}

main().catch(err => {
  console.error('Test execution error:', err);
  process.exit(1);
});
