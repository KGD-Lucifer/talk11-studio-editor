import fs from 'fs';

const html = fs.readFileSync('Tao_Khung_Thoi_Su_Talk11.html', 'utf8');
const lines = html.split('\n');

console.log('=== NETWORK CALLS IN HTML ===');
lines.forEach((line, idx) => {
  if (line.includes('fetch(') || line.includes('XMLHttpRequest') || line.includes('new WebSocket') || line.includes('navigator.sendBeacon') || line.includes('http://') || line.includes('https://')) {
    // Filter out standard doctype, cdn script tags, or schemas
    console.log(`L${idx + 1}: ${line.trim().slice(0, 120)}`);
  }
});
