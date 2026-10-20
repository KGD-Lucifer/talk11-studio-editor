import { spawn } from 'child_process';
import path from 'path';

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const fileUrl = 'file:///' + path.resolve('Tao_Khung_Thoi_Su_Talk11.html').replace(/\\/g, '/');

async function main() {
  console.log('Testing Manual Brush & Custom Keying in Headless Edge...');
  const edgeProc = spawn(EDGE_PATH, [
    '--headless=new',
    '--remote-debugging-port=9231',
    '--window-size=1680,980',
    '--disable-gpu',
    'about:blank'
  ]);

  let res = null;
  for (let i = 0; i < 15; i++) {
    await new Promise(r => setTimeout(r, 400));
    try {
      res = await fetch('http://127.0.0.1:9231/json/new?' + encodeURIComponent(fileUrl), { method: 'PUT' });
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

  console.log('Page loaded, waiting for initialization...');
  await new Promise(r => setTimeout(r, 3000));

  const evalRes = await send('Runtime.evaluate', {
    expression: `(function() {
      const res = {};

      // 1. Wizard Mode UI Elements
      const btnWizCustom = document.getElementById('btnWizBgCustom');
      const wizCustomBox = document.getElementById('wizCustomColorBox');
      const btnWizPick = document.getElementById('btnWizPickColor');
      const inWizColor = document.getElementById('inputWizCustomColor');
      const sliderWizTol = document.getElementById('sliderWizCustomTol');
      const btnWizRemove = document.getElementById('btnWizBrushRemove');
      const btnWizKeep = document.getElementById('btnWizBrushKeep');
      const btnWizAuto = document.getElementById('btnWizBrushAuto');
      const sliderWizSize = document.getElementById('sliderWizBrushSize');
      const btnWizClear = document.getElementById('btnWizClearBrush');

      res.hasBtnWizBgCustom = !!btnWizCustom;
      res.hasWizCustomBox = !!wizCustomBox;
      res.hasBtnWizPickColor = !!btnWizPick;
      res.hasInputWizCustomColor = !!inWizColor;
      res.hasSliderWizCustomTol = !!sliderWizTol;
      res.hasBtnWizBrushRemove = !!btnWizRemove;
      res.hasBtnWizBrushKeep = !!btnWizKeep;
      res.hasBtnWizBrushAuto = !!btnWizAuto;
      res.hasSliderWizBrushSize = !!sliderWizSize;
      res.hasBtnWizClearBrush = !!btnWizClear;

      // 2. Pro Mode UI Elements
      const btnKeyCustom = document.getElementById('btnKeyCustom');
      const btnProPick = document.getElementById('btnProPickColor');
      const inCustomPro = document.getElementById('inputCustomKeyColor');
      const proCustomBar = document.getElementById('proCustomColorBar');

      res.hasBtnKeyCustom = !!btnKeyCustom;
      res.hasBtnProPickColor = !!btnProPick;
      res.hasInputCustomKeyColor = !!inCustomPro;
      res.hasProCustomColorBar = !!proCustomBar;

      // 3. Test Mode Switching to Custom
      btnWizCustom.click();
      res.modeSwitchedToCustom = (studentChromaMode === 'custom');
      res.wizCustomBoxVisible = (wizCustomBox.style.display !== 'none');
      res.proCustomBarVisible = (proCustomBar.style.display !== 'none');

      // 4. Test Brush Tool Selection
      btnWizRemove.click();
      res.toolSwitchedToRemove = (aiMattingTool === 'brush_remove');
      res.btnRemoveActive = btnWizRemove.classList.contains('active');

      btnWizKeep.click();
      res.toolSwitchedToKeep = (aiMattingTool === 'brush_keep');
      res.btnKeepActive = btnWizKeep.classList.contains('active');

      btnWizAuto.click();
      res.toolSwitchedToAuto = (aiMattingTool === 'auto');
      res.btnAutoActive = btnWizAuto.classList.contains('active');

      // 5. Test Brush Size Sync
      sliderWizSize.value = 48;
      sliderWizSize.dispatchEvent(new Event('input'));
      res.brushSizeSynced = (aiMattingBrushSize === 48);
      const sliderMatte = document.getElementById('sliderMatteBrushSize');
      res.proBrushSizeSynced = (sliderMatte && parseInt(sliderMatte.value) === 48);

      // 6. Test Eyedropper Activator
      btnWizPick.click();
      res.isPickingKeyColorActive = (isPickingKeyColor === true);
      const canvas = document.getElementById('mainCanvas');
      res.canvasCursorCrosshair = (canvas && canvas.style.cursor === 'crosshair');

      // Cancel eyedropper with escape
      window.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }));
      res.eyedropperCancelledByEsc = (isPickingKeyColor === false);

      // 7. Test Color Sync
      inWizColor.value = '#FF5500';
      inWizColor.dispatchEvent(new Event('input'));
      res.colorSynced = (studentCustomKeyColor.toLowerCase() === '#ff5500');
      res.proInputColorSynced = (inCustomPro.value.toLowerCase() === '#ff5500');

      // 8. Test Brush Stroke Simulation
      btnWizRemove.click();
      if (!studentVideoElem) {
        studentVideoElem = document.createElement('video');
        studentVideoElem.src = 'student_input_sample.mp4';
      }
      try { Object.defineProperty(studentVideoElem, 'videoWidth', { value: 640, configurable: true }); } catch(e){}
      try { Object.defineProperty(studentVideoElem, 'videoHeight', { value: 360, configurable: true }); } catch(e){}
      const rect = canvas.getBoundingClientRect();
      const sBox = getStudentCharacterScreenBounds();
      const clickX = rect.left + ((sBox ? sBox.centerX : 960) / (canvas.width / rect.width));
      const clickY = rect.top + ((sBox ? sBox.centerY : 640) / (canvas.height / rect.height));

      const fakeDownEvent = new MouseEvent('mousedown', {
        clientX: clickX,
        clientY: clickY,
        bubbles: true
      });
      canvas.dispatchEvent(fakeDownEvent);
      const fakeMoveEvent = new MouseEvent('mousemove', {
        clientX: clickX + 15,
        clientY: clickY + 15,
        bubbles: true
      });
      canvas.dispatchEvent(fakeMoveEvent);
      const fakeUpEvent = new MouseEvent('mouseup', { bubbles: true });
      window.dispatchEvent(fakeUpEvent);

      res.hasCorrectionsAfterStroke = hasUserMatteCorrections;

      // 9. Test Clear Brush
      btnWizClear.click();
      res.correctionsCleared = (hasUserMatteCorrections === false);

      // 10. Switch back to AI Auto
      const btnWizAi = document.getElementById('btnWizBgAi');
      btnWizAi.click();
      res.switchedBackToAi = (studentChromaMode === 'ai_auto');
      res.wizCustomBoxHiddenAfterAi = (wizCustomBox.style.display === 'none');

      return res;
    })()`,
    returnByValue: true
  });

  if (evalRes?.result?.exceptionDetails) {
    console.error('Browser Exception:', JSON.stringify(evalRes.result.exceptionDetails, null, 2));
  }
  const results = evalRes?.result?.result?.value;
  console.log('Test Results:', JSON.stringify(results, null, 2));

  let allPassed = true;
  for (const [key, val] of Object.entries(results || {})) {
    if (!val) {
      console.error(`[FAIL] ${key} is false!`);
      allPassed = false;
    } else {
      console.log(`[PASS] ${key}`);
    }
  }

  if (allPassed) {
    console.log('\n🎉 ALL MANUAL BRUSH & CUSTOM KEYING TESTS PASSED 100%!');
  } else {
    console.error('\n❌ SOME TESTS FAILED!');
  }

  ws.close();
  edgeProc.kill();
  process.exit(allPassed ? 0 : 1);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
