import fs from 'fs';

const html = fs.readFileSync('Tao_Khung_Thoi_Su_Talk11.html', 'utf8');

// Find all elements with id='btn...' or <button id='...'
const buttonTagRegex = /<button\b([^>]*)>/gi;
let match;
const buttons = [];

while ((match = buttonTagRegex.exec(html)) !== null) {
  const attrs = match[1];
  const idMatch = attrs.match(/id=["']([^"']+)["']/i);
  const onclickMatch = attrs.match(/onclick=["']([^"']+)["']/i);
  const textMatch = attrs.match(/title=["']([^"']+)["']/i) || '';
  if (idMatch) {
    buttons.push({
      id: idMatch[1],
      hasInlineOnclick: !!onclickMatch,
      inlineOnclick: onclickMatch ? onclickMatch[1] : null
    });
  }
}

console.log('Total button elements with id:', buttons.length);

const unhandled = [];
for (const btn of buttons) {
  if (btn.hasInlineOnclick) continue;
  
  // Check if id is attached via document.getElementById('id').addEventListener / onclick
  // or id.addEventListener
  const id = btn.id;
  const p1 = new RegExp("['\"]" + id + "['\"]\\s*\\)\\s*\\.\\s*(addEventListener|onclick)", 'g');
  const p2 = new RegExp("\\b" + id + "\\s*\\.\\s*(addEventListener|onclick)", 'g');
  const p3 = new RegExp("document\\.querySelector\\(['\"][^'\"]*#" + id + "['\"]\\)", 'g');
  const p4 = new RegExp("\\$\\(['\"]#" + id + "['\"]\\)", 'g');
  
  const found = p1.test(html) || p2.test(html) || p3.test(html) || p4.test(html);
  if (!found) {
    // Check if referenced at all in JS
    const pRef = new RegExp("['\"]" + id + "['\"]", 'g');
    const refs = (html.match(pRef) || []).length;
    unhandled.push({ id, refs });
  }
}

console.log('Buttons without detected direct event listeners:', unhandled);
