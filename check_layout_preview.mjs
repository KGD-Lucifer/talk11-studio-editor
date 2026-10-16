import fs from 'fs';

const html = fs.readFileSync('Tao_Khung_Thoi_Su_Talk11.html', 'utf8');
const lines = html.split('\n');
for (let j = 3380; j <= 3525; j++) {
  console.log(`L${j}: ${lines[j-1]}`);
}
