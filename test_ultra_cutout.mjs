import { spawn } from 'child_process';
import path from 'path';

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const fileUrl = 'file:///' + path.resolve('Tao_Khung_Thoi_Su_Talk11.html').replace(/\\/g, '/');

async function main() {
  console.log('Testing Ultra Biometric Cutout Features in Headless Edge...');
  const edgeProc = spawn(EDGE_PATH, [
    '--headless=new',
    '--remote-debugging-port=9228',
    '--window-size=1680,980',
    '--disable-gpu',
    'about:blank'
  ]);

  let res = null;
  for (let i = 0; i < 15; i++) {
    await new Promise(r => setTimeout(r, 400));
    try {
      res = await fetch('http://127.0.0.1:9228/json/new?' + encodeURIComponent(fileUrl), { method: 'PUT' });
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
      const results = {};

      // 1. Check UI elements for Ultra Cutout
      const btnUltraPro = document.getElementById('btnPresetMatteUltra');
      const btnUltraWiz = document.getElementById('btnWizPresetUltra');
      const sliderProErode = document.getElementById('sliderAiErode');
      const sliderWizErode = document.getElementById('sliderWizAiErode');

      results.hasBtnPresetUltraPro = !!btnUltraPro;
      results.hasBtnPresetUltraWiz = !!btnUltraWiz;
      results.sliderProErodeMaxIs12 = (sliderProErode && sliderProErode.max === '12');
      results.sliderWizErodeMaxIs12 = (sliderWizErode && sliderWizErode.max === '12');

      // 2. Click Pro Ultra Preset
      btnUltraPro.click();
      results.proUltraActive = btnUltraPro.classList.contains('active');
      results.wizUltraActive = btnUltraWiz.classList.contains('active');
      results.ultraSetsTolerance92 = (studentChromaTolerance === 0.92);
      results.ultraSetsErode2 = (studentAiErodeRadius === 2);
      results.ultraSetsCoreProtect95 = (studentMatteCoreProtect === 95);
      results.ultraSetsHairDetail85 = (studentMatteHairDetail === 85);
      results.ultraSetsFeather2 = (studentChromaFeather === 2);
      results.ultraEnablesPlantRemoval = (enablePlantRemoval === true);

      // 3. Click DaVinci Preset in Wizard
      const btnWizDaVinci = document.getElementById('btnWizPresetDaVinci');
      btnWizDaVinci.click();
      results.davinciSetsTolerance80 = (studentChromaTolerance === 0.80);
      results.davinciSetsHairDetail95 = (studentMatteHairDetail === 95);

      // 4. Click Ultra in Wizard
      btnUltraWiz.click();
      results.wizUltraReactivated = (studentMattePreset === 'ultra');
      results.wizUltraSetsTolerance92Again = (studentChromaTolerance === 0.92);

      // 5. Test rendering frame without crash
      try {
        render(0);
        results.renderUltraNoCrash = true;
      } catch (e) {
        results.renderUltraNoCrash = false;
        results.renderError = e.message;
      }

      return results;
    })()`,
    returnByValue: true
  });

  const resVal = evalRes.result?.result?.value || evalRes.result?.value || evalRes.result;
  console.log('Ultra Cutout Test Results:', JSON.stringify(resVal, null, 2));

  let allPassed = true;
  for (const [k, v] of Object.entries(resVal || {})) {
    if (!v) {
      console.error(`[FAIL] ${k}: ${v}`);
      allPassed = false;
    } else {
      console.log(`[PASS] ${k}`);
    }
  }

  if (consoleErrors.length > 0) {
    console.warn('Console Errors caught:', consoleErrors);
  }

  try { ws.close(); } catch(e) {}
  edgeProc.kill();

  if (allPassed) {
    console.log('\n🎉 ALL ULTRA BIOMETRIC CUTOUT TESTS PASSED 100%!');
    process.exit(0);
  } else {
    console.error('\n❌ SOME ULTRA CUTOUT TESTS FAILED!');
    process.exit(1);
  }
}

main().catch(err => {
  console.error('Test execution error:', err);
  process.exit(1);
});
