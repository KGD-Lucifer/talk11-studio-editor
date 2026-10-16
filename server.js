import http from 'http';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { exec } from 'child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const PORT = process.env.PORT || 8080;
const ROOT = __dirname;

const MIME_TYPES = {
  '.html': 'text/html; charset=UTF-8',
  '.js': 'text/javascript; charset=UTF-8',
  '.mjs': 'text/javascript; charset=UTF-8',
  '.css': 'text/css; charset=UTF-8',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.mp4': 'video/mp4',
  '.webm': 'video/webm',
  '.wav': 'audio/wav',
  '.mp3': 'audio/mpeg',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.wasm': 'application/wasm',
  '.tflite': 'application/octet-stream',
  '.binarypb': 'application/octet-stream'
};

const server = http.createServer((req, res) => {
  const startTime = Date.now();

  // Production Security Headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'SAMEORIGIN');
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
  res.setHeader('Cross-Origin-Resource-Policy', 'cross-origin');
  res.setHeader('Cross-Origin-Opener-Policy', 'same-origin');
  res.setHeader('Cross-Origin-Embedder-Policy', 'credentialless');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  let reqUrl = decodeURI(req.url.split('?')[0]);

  // 1. Production Health Check Endpoint
  if (reqUrl === '/health' || reqUrl === '/api/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      status: 'UP',
      service: 'TALK11 Broadcast Studio',
      uptimeSec: Math.round(process.uptime()),
      timestamp: new Date().toISOString()
    }));
    return;
  }

  if (reqUrl === '/' || reqUrl === '') {
    reqUrl = '/Tao_Khung_Thoi_Su_Talk11.html';
  }

  // 2. Safe Video Save Endpoint with Payload Limit (Max 200MB)
  if (req.method === 'POST' && reqUrl === '/api/save-test-video') {
    const targetFile = path.join(ROOT, 'TALK11_E2E_Test_Output.webm');
    let receivedBytes = 0;
    const MAX_UPLOAD_BYTES = 200 * 1024 * 1024; // 200 MB limit
    const outStream = fs.createWriteStream(targetFile);

    req.on('data', (chunk) => {
      receivedBytes += chunk.length;
      if (receivedBytes > MAX_UPLOAD_BYTES) {
        req.destroy();
        outStream.destroy();
        try { fs.unlinkSync(targetFile); } catch(e) {}
        res.writeHead(413, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Payload Too Large: Toi da 200MB' }));
      }
    });

    req.pipe(outStream);
    req.on('end', () => {
      if (receivedBytes <= MAX_UPLOAD_BYTES) {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: true, file: targetFile, bytes: receivedBytes }));
      }
    });
    return;
  }

  // 2.5 RVM AI Video Matting Endpoint (CapCut Pro Standard)
  if (req.method === 'POST' && reqUrl === '/api/rvm-matte') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        const payload = JSON.parse(body || '{}');
        const inputRel = payload.input || 'student_input_sample.mp4';
        const inputAbs = path.resolve(ROOT, inputRel);
        const outputRel = payload.output || ('TALK11_RVM_Matte_' + Date.now() + '.mp4');
        const outputAbs = path.resolve(ROOT, outputRel);

        if (!fs.existsSync(inputAbs)) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ success: false, error: 'File video khong ton tai' }));
          return;
        }

        const cmd = `python tach_nen_rvm_capcut.py -i "${inputAbs}" -o "${outputAbs}"`;
        exec(cmd, { cwd: ROOT }, (error, stdout, stderr) => {
          if (error) {
            console.error('RVM Execution error:', error, stderr);
            res.writeHead(500, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ success: false, error: stderr || error.message }));
          } else {
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({
              success: true,
              outputFile: outputRel,
              outputUrl: `/${outputRel}`
            }));
          }
        });
      } catch (err) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: false, error: err.message }));
      }
    });
    return;
  }

  // 2.6 Direct Upload & RVM AI Video Matting Endpoint
  if (req.method === 'POST' && reqUrl === '/api/upload-and-rvm-matte') {
    const tempUpload = path.join(ROOT, 'temp_rvm_in_' + Date.now() + '.mp4');
    const outputRel = 'TALK11_RVM_Matte_' + Date.now() + '.mp4';
    const outputAbs = path.join(ROOT, outputRel);
    const outStream = fs.createWriteStream(tempUpload);

    req.pipe(outStream);
    req.on('end', () => {
      const cmd = `python tach_nen_rvm_capcut.py -i "${tempUpload}" -o "${outputAbs}"`;
      exec(cmd, { cwd: ROOT }, (error, stdout, stderr) => {
        try { fs.unlinkSync(tempUpload); } catch(e) {}
        if (error) {
          console.error('Upload RVM error:', error, stderr);
          res.writeHead(500, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ success: false, error: stderr || error.message }));
        } else {
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({
            success: true,
            outputFile: outputRel,
            outputUrl: `/${outputRel}`
          }));
        }
      });
    });
    return;
  }

  // 3. Strict Path Traversal Protection
  const safePath = path.normalize(path.resolve(ROOT, '.' + reqUrl));
  if (!safePath.startsWith(ROOT)) {
    res.writeHead(403, { 'Content-Type': 'text/plain; charset=UTF-8' });
    res.end('403 Forbidden');
    return;
  }

  const filePath = safePath;

  fs.stat(filePath, (err, stats) => {
    if (err || !stats.isFile()) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=UTF-8' });
      res.end('404 Not Found: ' + reqUrl);
      return;
    }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';

    res.writeHead(200, {
      'Content-Type': contentType,
      'Content-Length': stats.size,
      'Cache-Control': 'no-cache'
    });

    const stream = fs.createReadStream(filePath);
    stream.pipe(res);
  });
});

server.listen(PORT, '127.0.0.1', () => {
  const url = `http://127.0.0.1:${PORT}/Tao_Khung_Thoi_Su_Talk11.html`;
  console.log(`=======================================================`);
  console.log(`  TALK11 BROADCAST STUDIO (CAPCUT PC DESKTOP ENGINE)`);
  console.log(`  Server dang chay tai: ${url}`);
  console.log(`=======================================================`);

  // Open browser in Desktop App mode (CapCut PC style frameless window)
  let startCmd = `start "" "${url}"`;
  if (process.platform === 'win32') {
    const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
    const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
    if (fs.existsSync(edgePath)) {
      startCmd = `start "" "${edgePath}" --app="${url}" --window-size=1680,980`;
    } else if (fs.existsSync(chromePath)) {
      startCmd = `start "" "${chromePath}" --app="${url}" --window-size=1680,980`;
    }
  } else if (process.platform === 'darwin') {
    startCmd = `open "${url}"`;
  } else {
    startCmd = `xdg-open "${url}"`;
  }
  if (!process.env.NO_AUTO_OPEN) {
    exec(startCmd, () => {});
  } else {
    console.log(`[TEST MODE] Auto-open browser suppressed (NO_AUTO_OPEN=1)`);
  }
});

server.on('error', (err) => {
  if (err.code === 'EADDRINUSE') {
    const nextPort = Number(PORT) + 1;
    console.log(`Port ${PORT} dang ban, chuyen sang port ${nextPort}...`);
    process.env.PORT = nextPort;
    server.listen(nextPort, '127.0.0.1');
  } else {
    console.error('Server error:', err);
  }
});
