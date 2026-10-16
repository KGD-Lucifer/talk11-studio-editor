import fs from 'fs';
import ts from './remotion-prompt-to-video/node_modules/typescript/lib/typescript.js';

const html = fs.readFileSync('Tao_Khung_Thoi_Su_Talk11.html', 'utf8');
const scriptMatches = [...html.matchAll(/<script(?:\s+[^>]*)?>([\s\S]*?)<\/script>/gi)];
const mainScript = scriptMatches[scriptMatches.length - 1][1];

console.log('Script length:', mainScript.length, 'chars');

// Standard browser globals
const standardGlobals = new Set([
  'window', 'document', 'console', 'setTimeout', 'clearTimeout', 'setInterval', 'clearInterval',
  'requestAnimationFrame', 'cancelAnimationFrame', 'Math', 'JSON', 'Date', 'Array', 'Object',
  'String', 'Number', 'Boolean', 'RegExp', 'Map', 'Set', 'WeakMap', 'WeakSet', 'Promise', 'Error',
  'TypeError', 'RangeError', 'ReferenceError', 'SyntaxError', 'Float32Array', 'Uint8Array', 'Uint8ClampedArray',
  'Int32Array', 'ArrayBuffer', 'DataView', 'Blob', 'File', 'FileReader', 'URL', 'Event', 'CustomEvent',
  'AudioContext', 'webkitAudioContext', 'MediaRecorder', 'MediaStream', 'Image', 'Audio', 'ImageData',
  'Path2D', 'HTMLCanvasElement', 'HTMLVideoElement', 'HTMLAudioElement', 'HTMLElement', 'Element', 'Node',
  'indexedDB', 'localStorage', 'sessionStorage', 'fetch', 'Headers', 'Request', 'Response', 'WebSocket',
  'navigator', 'location', 'history', 'screen', 'performance', 'alert', 'confirm', 'prompt',
  'encodeURIComponent', 'decodeURIComponent', 'encodeURI', 'decodeURI', 'parseInt', 'parseFloat',
  'isNaN', 'isFinite', 'escape', 'unescape', 'SelfieSegmentation', 'btoa', 'atob',
  'MutationObserver', 'ResizeObserver', 'IntersectionObserver', 'OffscreenCanvas', 'DOMParser',
  'XMLSerializer', 'Worker', 'MessageChannel', 'crypto'
]);

const sourceFile = ts.createSourceFile('inline.js', mainScript, ts.ScriptTarget.ES2022, true);

// Collect all top-level declared names
const declaredNames = new Set(standardGlobals);

function collectDeclarations(node) {
  if (ts.isVariableDeclaration(node) && ts.isIdentifier(node.name)) {
    declaredNames.add(node.name.text);
  } else if (ts.isFunctionDeclaration(node) && node.name) {
    declaredNames.add(node.name.text);
  } else if (ts.isClassDeclaration(node) && node.name) {
    declaredNames.add(node.name.text);
  }
  ts.forEachChild(node, collectDeclarations);
}

collectDeclarations(sourceFile);
console.log('Total declared / global names:', declaredNames.size);

// Now walk the AST and find all Identifier expressions that are NOT properties (e.g. obj.prop),
// not declarations, and not parameters
const unresolved = new Map();

function checkIdentifiers(node, scope = new Set()) {
  const currentScope = new Set(scope);

  // Add function params or local vars in block
  if (ts.isFunctionDeclaration(node) || ts.isFunctionExpression(node) || ts.isArrowFunction(node)) {
    node.parameters.forEach(p => {
      if (ts.isIdentifier(p.name)) currentScope.add(p.name.text);
    });
  } else if (ts.isCatchClause(node) && node.variableDeclaration && ts.isIdentifier(node.variableDeclaration.name)) {
    currentScope.add(node.variableDeclaration.name.text);
  }

  // Check if identifier is a read/write value
  if (ts.isIdentifier(node)) {
    const name = node.text;
    const parent = node.parent;

    // Skip property access right side (obj.prop), object literal keys, declarations, import/exports
    const isPropName = ts.isPropertyAccessExpression(parent) && parent.name === node;
    const isObjKey = ts.isPropertyAssignment(parent) && parent.name === node;
    const isMethodDef = ts.isMethodDeclaration(parent) && parent.name === node;
    const isVarDecl = ts.isVariableDeclaration(parent) && parent.name === node;
    const isFnDecl = ts.isFunctionDeclaration(parent) && parent.name === node;
    const isParam = ts.isParameter(parent) && parent.name === node;
    const isLabel = ts.isLabeledStatement(parent) && parent.label === node;
    const isBreakTarget = (ts.isBreakStatement(parent) || ts.isContinueStatement(parent)) && parent.label === node;

    if (!isPropName && !isObjKey && !isMethodDef && !isVarDecl && !isFnDecl && !isParam && !isLabel && !isBreakTarget) {
      if (!currentScope.has(name) && !declaredNames.has(name)) {
        // Line number
        const { line } = sourceFile.getLineAndCharacterOfPosition(node.getStart());
        if (!unresolved.has(name)) unresolved.set(name, []);
        unresolved.get(name).push(line + 1);
      }
    }
  }

  ts.forEachChild(node, child => checkIdentifiers(child, currentScope));
}

checkIdentifiers(sourceFile);

console.log('\n=== POTENTIAL UNRESOLVED / UNDEFINED IDENTIFIERS ===');
for (const [name, lines] of unresolved.entries()) {
  console.log(`- "${name}" used at line(s): ${lines.slice(0, 5).join(', ')} (total ${lines.length} occurrences)`);
}
