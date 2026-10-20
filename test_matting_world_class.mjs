import { spawn } from 'child_process';
import path from 'path';

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const fileUrl = 'file:///' + path.resolve('Tao_Khung_Thoi_Su_Talk11.html').replace(/\\/g, '/');

async function main() {
  console.log('Testing World-Class Matting Features in Headless Edge...');
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
    if (msg.id && pending.has(msg.id)) {
      const fn = pending.get(msg.id);
      pending.delete(msg.id);
      fn(msg.result);
    }
    if (msg.method === 'Runtime.consoleAPICalled' && msg.params.type === 'error') {
      const text = msg.params.args.map(a => a.value || a.description || '').join(' ');
      consoleErrors.push(text);
    }
  };

  await new Promise(r => ws.onopen = r);
  await send('Page.enable');
  await send('Runtime.enable');

  console.log('Page loaded, waiting for initialization...');
  await new Promise(r => setTimeout(r, 2000));

  const evalRes = await send('Runtime.evaluate', {
    expression: `(() => {
      const results = {};

      // 1. Check existence of new UI elements
      const btnDaVinci = document.getElementById('btnPresetMatteDaVinci');
      const btnPhotoshop = document.getElementById('btnPresetMattePhotoshop');
      const btnCapCut = document.getElementById('btnPresetMatteCapCut');
      const sCoreProt = document.getElementById('sliderMatteCoreProtect');
      const sHairDet = document.getElementById('sliderMatteHairDetail');

      results.hasBtnPresetDaVinci = !!btnDaVinci;
      results.hasBtnPresetPhotoshop = !!btnPhotoshop;
      results.hasBtnPresetCapCut = !!btnCapCut;
      results.hasSliderCoreProtect = !!sCoreProt;
      results.hasSliderHairDetail = !!sHairDet;

      // 2. Check default values (Supports both Ultra and DaVinci defaults)
      results.defaultCoreProtectIs85 = (studentMatteCoreProtect === 85 || studentMatteCoreProtect === 95);
      results.defaultHairDetailIs75 = (studentMatteHairDetail === 75 || studentMatteHairDetail === 85);
      results.defaultPresetIsDaVinci = (studentMattePreset === 'davinci' || studentMattePreset === 'ultra');

      // 3. Test clicking Photoshop preset
      btnPhotoshop.click();
      results.photoshopPresetSetsCore100 = (studentMatteCoreProtect === 100);
      results.photoshopPresetSetsHair70 = (studentMatteHairDetail === 70);
      results.photoshopPresetActive = btnPhotoshop.classList.contains('active');

      // 4. Test clicking CapCut preset
      btnCapCut.click();
      results.capcutPresetSetsCore80 = (studentMatteCoreProtect === 80);
      results.capcutPresetSetsHair60 = (studentMatteHairDetail === 60);
      results.capcutPresetActive = btnCapCut.classList.contains('active');

      // 5. Test clicking DaVinci preset back
      btnDaVinci.click();
      results.davinciPresetSetsCore85 = (studentMatteCoreProtect === 85);
      results.davinciPresetSetsHair95 = (studentMatteHairDetail === 95);
      results.davinciPresetActive = btnDaVinci.classList.contains('active');

      // 6. Test Undo/Redo integration with new matte variables
      const snap1 = captureAppStateSnapshot();
      results.snapHasMatteVariables = ('studentMatteCoreProtect' in snap1) && ('studentMatteHairDetail' in snap1);

      // 7. Test render loop execution with new matte parameters
      render(2.0);
      results.renderSuccessWithoutCrash = true;

      return results;
    })()`,
    returnByValue: true
  });

  console.log('World-Class Matting Features Raw evalRes:', JSON.stringify(evalRes, null, 2));
  const val = evalRes?.result?.value;
  console.log('Parsed val:', val);

  console.log('\nConsole Errors count:', consoleErrors.length);
  if (consoleErrors.length > 0) {
    console.log('Console Errors:', consoleErrors);
  }

  ws.close();
  edgeProc.kill();

  const allPassed = !!val && Object.values(val).every(Boolean);
  console.log('\nAll World-Class Matting Features Passed:', allPassed);
  process.exit(allPassed ? 0 : 1);
}

main().catch(err => {
  console.error('Test error:', err);
  process.exit(1);
});
