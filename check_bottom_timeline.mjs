import fs from 'fs';

const html = fs.readFileSync('Tao_Khung_Thoi_Su_Talk11.html', 'utf8');
const lines = html.split('\n');
lines.forEach((l, i) => {
  if (l.includes('bottomTimelinePanel')) {
    console.log(`L${i+1}: ${l.trim().slice(0, 100)}`);
  }
});
