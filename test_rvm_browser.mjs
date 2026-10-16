import { spawn } from 'child_process';

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const APP_URL = 'http://127.0.0.1:8080/Tao_Khung_Thoi_Su_Talk11.html';

async function testRvmInBrowser() {
  console.log('Testing RVM loading in headless browser...');
  const edgeProc = spawn(EDGE_PATH, [
    '--headless=new',
    '--remote-debugging-port=9258',
    '--window-size=1280,720',
    'about:blank'
  ]);

  await new Promise(r => setTimeout(r, 1500));

  try {
    const res = await fetch('http://127.0.0.1:9258/json/new?' + encodeURIComponent(APP_URL), { method: 'PUT' });
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

    await new Promise(r => { ws.onopen = r; });
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

    // Dynamically inject tf.min.js and test loading RVM model
    console.log('Injecting tf.js and loading RVM graph model...');
    const result = await send('Runtime.evaluate', {
      expression: `(async () => {
        if (typeof tf === 'undefined') {
          await new Promise((resolve, reject) => {
            const s = document.createElement('script');
            s.src = '03_ASSETS/tfjs/tf.min.js';
            s.onload = resolve;
            s.onerror = reject;
            document.head.appendChild(s);
          });
        }
        
        const tfVersion = tf.version.tfjs;
        console.log('TFJS loaded, version:', tfVersion);
        
        // Load RVM model
        const modelUrl = '03_ASSETS/models/rvm/rvm_mobilenetv3_tfjs_int8/model.json';
        const model = await tf.loadGraphModel(modelUrl);
        
        // Test dummy input
        const dummyInput = tf.zeros([1, 240, 320, 3]);
        const r1 = tf.tensor(0.);
        const r2 = tf.tensor(0.);
        const r3 = tf.tensor(0.);
        const r4 = tf.tensor(0.);
        const ds = tf.tensor(0.25);
        
        const outputs = await model.executeAsync(
          { src: dummyInput, r1i: r1, r2i: r2, r3i: r3, r4i: r4, downsample_ratio: ds },
          ['fgr', 'pha', 'r1o', 'r2o', 'r3o', 'r4o']
        );
        
        const fgrShape = outputs[0].shape;
        const phaShape = outputs[1].shape;
        
        tf.dispose([dummyInput, r1, r2, r3, r4, ds, ...outputs]);
        
        return {
          tfVersion,
          modelLoaded: !!model,
          fgrShape,
          phaShape
        };
      })()`,
      awaitPromise: true,
      returnByValue: true
    });

    console.log('RVM Browser Execution Result:', JSON.stringify(result.result.value, null, 2));
    ws.close();
  } catch (err) {
    console.error('Error during test:', err);
  } finally {
    edgeProc.kill();
  }
}

testRvmInBrowser();
