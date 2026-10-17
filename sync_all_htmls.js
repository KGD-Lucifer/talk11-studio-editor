import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Root directory
const rootDir = fs.existsSync(path.join(__dirname, 'server.js')) ? __dirname : path.join(__dirname, '..');
const srcFile = path.join(rootDir, 'Tao_Khung_Thoi_Su_Talk11.html');

if (!fs.existsSync(srcFile)) {
  console.error(`[X] Khong tim thay file goc: ${srcFile}`);
  process.exit(1);
}

const content = fs.readFileSync(srcFile, 'utf8');

const targetFiles = [
  path.join(rootDir, 'Tao_Intro_Va_Studio_Thoi_Su_Talk11.html'),
  path.join(rootDir, 'TALK11_Community_Antigravity', 'Tao_Khung_Thoi_Su_Talk11.html'),
  path.join(rootDir, 'TALK11_Community_Antigravity', 'Tao_Intro_Va_Studio_Thoi_Su_Talk11.html'),
  path.join(rootDir, 'TALK11_Community_Antigravity', '03_ASSETS', 'VTV_TALK11_CAPCUT_FRAMES', 'Tao_Khung_Thoi_Su_Talk11.html'),
  path.join(rootDir, 'TALK11_Community_Antigravity', '03_ASSETS', 'VTV_TALK11_CAPCUT_FRAMES', 'Tao_Intro_Va_Studio_Thoi_Su_Talk11.html'),
  path.join(rootDir, 'VIDEO_KHUNG_THOI_SU_CAPCUT', 'Tao_Khung_Thoi_Su_Talk11.html'),
  path.join(rootDir, 'VIDEO_KHUNG_THOI_SU_CAPCUT', 'Tao_Intro_Va_Studio_Thoi_Su_Talk11.html'),
  path.join(rootDir, 'TALK11_News_Studio_v2.1.0_Enhanced.html')
];

let syncedCount = 0;
for (const target of targetFiles) {
  if (fs.existsSync(path.dirname(target))) {
    fs.writeFileSync(target, content, 'utf8');
    console.log(`[✓] Da dong bo: ${target}`);
    syncedCount++;
  }
}

console.log(`\n=> Hoan tat dong bo ${syncedCount} file HTML!`);
