import { spawn } from 'child_process';

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const APP_URL = 'http://127.0.0.1:8080/Tao_Khung_Thoi_Su_Talk11.html';

async function test() {
  const edgeProc = spawn(EDGE_PATH, [
    '--headless=new',
    '--remote-debugging-port=9232',
    '--window-size=1680,980',
    '--autoplay-policy=no-user-gesture-required',
    '--disable-gpu',
    'about:blank'
  ]);

  await new Promise(r => setTimeout(r, 1500));

  try {
    const res = await fetch('http://127.0.0.1:9232/json/new?' + encodeURIComponent(APP_URL), { method: 'PUT' });
    const target = await res.json();
    const ws = new WebSocket(target.webSocketDebuggerUrl);

    let idSeq = 1;
    const pending = new Map();

    function send(method, params = {}) {
      return new Promise((resolve, reject) => {
        const id = idSeq++;
        pending.set(id, { resolve, reject });
        ws.send(JSON.stringify({ id, method, params }));
      });
    }

    await new Promise((resolve, reject) => {
      ws.onopen = resolve;
      ws.onerror = reject;
    });

    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.id && pending.has(msg.id)) {
        const p = pending.get(msg.id);
        pending.delete(msg.id);
        if (msg.error) p.reject(msg.error);
        else p.resolve(msg.result);
      }
    };

    await send('Runtime.enable');
    await send('Page.enable');
    await new Promise(r => setTimeout(r, 2000));

    console.log('Testing Test 4...');
    const t4 = await send('Runtime.evaluate', {
      expression: `(() => {
        try {
          const btnCancel = document.getElementById('btnCancelExport');
          if (btnCancel) btnCancel.click();
          return {
            isRecording: typeof isRecording !== 'undefined' ? isRecording : null,
            isExportCancelled: typeof isExportCancelled !== 'undefined' ? isExportCancelled : null,
            btnExists: !!btnCancel
          };
        } catch (e) {
          return { err: e.message, stack: e.stack };
        }
      })()`,
      returnByValue: true
    });
    console.log('T4 result:', t4);

    console.log('Testing Test 5...');
    const t5 = await send('Runtime.evaluate', {
      expression: `(() => {
        try {
          const snapshot = captureAppStateSnapshot();
          const jsonStr = JSON.stringify(snapshot);
          const parsed = JSON.parse(jsonStr);
          restoreAppState(parsed);
          return {
            snapshotOk: !!snapshot,
            jsonLen: jsonStr.length,
            subCount: subtitlesList.length
          };
        } catch (e) {
          return { err: e.message, stack: e.stack };
        }
      })()`,
      returnByValue: true
    });
    console.log('T5 result:', t5);

    ws.close();
  } catch (err) {
    console.error(err);
  } finally {
    edgeProc.kill();
  }
}

test();
