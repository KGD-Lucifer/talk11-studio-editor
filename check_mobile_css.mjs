import fs from 'fs';

const html = fs.readFileSync('Tao_Khung_Thoi_Su_Talk11.html', 'utf8');
const lines = html.split('\n');
for (let j = 1700; j <= 1820; j++) {
  console.log(`L${j}: ${lines[j-1]}`);
}
