import { spawn } from 'child_process';
import path from 'path';

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const fileUrl = 'file:///' + path.resolve('Tao_Khung_Thoi_Su_Talk11.html').replace(/\\/g, '/');

async function main() {
  console.log('Testing Tao_Khung_Thoi_Su_Talk11.html in Headless Edge...');
  const edgeProc = spawn(EDGE_PATH, [
    '--headless=new',
    '--remote-debugging-port=9226',
    '--window-size=1680,980',
    '--disable-gpu',
    'about:blank'
  ]);

  let res = null;
  for (let i = 0; i < 15; i++) {
    await new Promise(r => setTimeout(r, 400));
    try {
      res = await fetch('http://127.0.0.1:9226/json/new?' + encodeURIComponent(fileUrl), { method: 'PUT' });
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

  // Evaluate interactive matte controls
  const evalRes = await send('Runtime.evaluate', {
    expression: `(() => {
      const results = {};
      results.btnMatteToolAuto = !!document.getElementById('btnMatteToolAuto');
      results.btnMatteToolSelect = !!document.getElementById('btnMatteToolSelect');
      results.btnMatteToolBrushKeep = !!document.getElementById('btnMatteToolBrushKeep');
      results.btnMatteToolBrushRemove = !!document.getElementById('btnMatteToolBrushRemove');
      results.sliderMatteBrushSize = !!document.getElementById('sliderMatteBrushSize');
      results.btnClearMatteStrokes = !!document.getElementById('btnClearMatteStrokes');
      results.btnPrevModeStudio = !!document.getElementById('btnPrevModeStudio');
      results.btnPrevModeCheckerboard = !!document.getElementById('btnPrevModeCheckerboard');
      results.btnPrevModeAlpha = !!document.getElementById('btnPrevModeAlpha');
      results.btnPrevModeGreen = !!document.getElementById('btnPrevModeGreen');
      results.btnQualityFast = !!document.getElementById('btnQualityFast');
      results.selectExportMode = !!document.getElementById('selectExportMode');
      results.hasVp9Option = Array.from(document.getElementById('selectExportMode').options).some(o => o.value === 'transparent_webm');
      results.hasAlphaOption = Array.from(document.getElementById('selectExportMode').options).some(o => o.value === 'alpha_matte');
      
      // Test clicking interactive buttons
      document.getElementById('btnMatteToolSelect').click();
      results.toolAfterSelect = window.aiMattingTool;

      document.getElementById('btnMatteToolBrushKeep').click();
      results.toolAfterKeep = window.aiMattingTool;

      document.getElementById('btnPrevModeCheckerboard').click();
      results.modeAfterChecker = window.aiMattingPreviewMode;

      document.getElementById('btnPrevModeStudio').click();
      results.modeAfterStudio = window.aiMattingPreviewMode;

      return results;
    })()`,
    returnByValue: true
  });

  console.log('Interactive Matting Evaluation Results:');
  console.log(JSON.stringify(evalRes.result?.value, null, 2));

  console.log('\nConsole Errors count:', consoleErrors.length);
  if (consoleErrors.length > 0) {
    console.log('Console Errors:', consoleErrors);
  }

  ws.close();
  edgeProc.kill();

  const allPassed = Object.values(evalRes.result?.value || {}).every(Boolean);
  console.log('\nAll Interactive Matting Features Passed:', allPassed);
  process.exit(allPassed ? 0 : 1);
}

main().catch(err => {
  console.error('Test error:', err);
  process.exit(1);
});
