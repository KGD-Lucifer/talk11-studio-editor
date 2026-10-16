import fs from 'fs';

const html = fs.readFileSync('Tao_Khung_Thoi_Su_Talk11.html', 'utf8');
const lines = html.split('\n');
lines.forEach((l, i) => {
  if (l.includes('.timeline-panel') && l.includes('{')) {
    console.log(`L${i+1}: ${l.trim()}`);
    for (let j = i; j <= Math.min(lines.length - 1, i + 25); j++) {
      console.log(`  ${j+1}: ${lines[j]}`);
      if (lines[j].includes('}')) break;
    }
  }
});
