import { spawn } from 'child_process';

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const APP_URL = 'http://127.0.0.1:8080/Tao_Khung_Thoi_Su_Talk11.html';

async function runBenchmark() {
  console.log('================================================================');
  console.log(' TALK11 BROADCAST STUDIO — PERFORMANCE & STRESS BENCHMARK SUITE ');
  console.log('================================================================');

  const edgeProc = spawn(EDGE_PATH, [
    '--headless=new',
    '--remote-debugging-port=9241',
    '--window-size=1680,980',
    '--autoplay-policy=no-user-gesture-required',
    '--disable-gpu',
    'about:blank'
  ]);

  await new Promise(r => setTimeout(r, 1500));

  try {
    const res = await fetch('http://127.0.0.1:9241/json/new?' + encodeURIComponent(APP_URL), { method: 'PUT' });
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

    console.log('[1/4] Measuring Memory Baseline...');
    const memBaseline = await send('Runtime.evaluate', {
      expression: `(() => {
        const mem = window.performance && window.performance.memory ? window.performance.memory : null;
        return {
          usedHeapMB: mem ? (mem.usedJSHeapSize / (1024 * 1024)).toFixed(2) : 'N/A',
          totalHeapMB: mem ? (mem.totalJSHeapSize / (1024 * 1024)).toFixed(2) : 'N/A'
        };
      })()`,
      returnByValue: true
    });
    console.log('Baseline Memory:', memBaseline.result.value);

    console.log('[2/4] Measuring Canvas 2D Composite Frame Rate & Latency (120 consecutive frames)...');
    const renderBench = await send('Runtime.evaluate', {
      expression: `(() => {
        const frameTimes = [];
        const start = performance.now();
        for (let i = 0; i < 120; i++) {
          const t0 = performance.now();
          render(i * 0.05); // render across timeline
          const t1 = performance.now();
          frameTimes.push(t1 - t0);
        }
        const totalDuration = performance.now() - start;
        const avgFrameMs = frameTimes.reduce((a, b) => a + b, 0) / frameTimes.length;
        const maxFrameMs = Math.max(...frameTimes);
        const minFrameMs = Math.min(...frameTimes);
        const effectiveFps = 1000 / avgFrameMs;
        
        return {
          totalFrames: 120,
          totalDurationMs: totalDuration.toFixed(1),
          avgFrameMs: avgFrameMs.toFixed(2),
          minFrameMs: minFrameMs.toFixed(2),
          maxFrameMs: maxFrameMs.toFixed(2),
          effectiveFps: Math.round(effectiveFps)
        };
      })()`,
      returnByValue: true
    });
    console.log('Render Benchmark:', renderBench.result.value);

    console.log('[3/4] Benchmarking Subtitle & Audio Analysis Speed...');
    const audioBench = await send('Runtime.evaluate', {
      expression: `(() => {
        const t0 = performance.now();
        // Benchmark audio silence calculations over synthetic audio buffer
        const sampleRate = 44100;
        const durationSec = 60; // 60s of audio
        const samplesCount = sampleRate * durationSec;
        const mockPcm = new Float32Array(samplesCount);
        
        // Fill half speech, half silence
        for (let i = 0; i < samplesCount; i++) {
          if (i % 88200 < 44100) {
            mockPcm[i] = Math.sin(i * 0.05) * 0.4; // speech
          } else {
            mockPcm[i] = (Math.random() - 0.5) * 0.0002; // near silence
          }
        }
        
        // Run silence detection algorithm
        const threshold = 0.015;
        const minSilenceSec = 0.4;
        const windowSize = Math.floor(sampleRate * 0.05); // 50ms window
        let silentWindows = 0;
        for (let i = 0; i < samplesCount; i += windowSize) {
          let sum = 0;
          const end = Math.min(i + windowSize, samplesCount);
          for (let j = i; j < end; j++) sum += mockPcm[j] * mockPcm[j];
          const rms = Math.sqrt(sum / (end - i));
          if (rms < threshold) silentWindows++;
        }
        const t1 = performance.now();
        
        return {
          simulatedAudioSec: durationSec,
          analysisTimeMs: (t1 - t0).toFixed(2),
          speedFactor: (durationSec / ((t1 - t0) / 1000)).toFixed(1) + 'x realtime'
        };
      })()`,
      returnByValue: true
    });
    console.log('Audio Analysis Benchmark:', audioBench.result.value);

    console.log('[4/4] Measuring Post-Load Memory & Leak Check...');
    const memAfter = await send('Runtime.evaluate', {
      expression: `(() => {
        const mem = window.performance && window.performance.memory ? window.performance.memory : null;
        return {
          usedHeapMB: mem ? (mem.usedJSHeapSize / (1024 * 1024)).toFixed(2) : 'N/A',
          totalHeapMB: mem ? (mem.totalJSHeapSize / (1024 * 1024)).toFixed(2) : 'N/A'
        };
      })()`,
      returnByValue: true
    });
    console.log('Post-Load Memory:', memAfter.result.value);

    ws.close();
  } catch (err) {
    console.error('Benchmark error:', err);
  } finally {
    edgeProc.kill();
  }
}

runBenchmark();
