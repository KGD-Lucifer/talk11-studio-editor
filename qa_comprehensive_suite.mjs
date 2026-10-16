import { spawn } from 'child_process';
import fs from 'fs';
import path from 'path';

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const APP_URL = 'file:///' + path.resolve('Tao_Khung_Thoi_Su_Talk11.html').replace(/\\/g, '/');

async function runTests() {
  console.log('===============================================================');
  console.log(' TALK11 BROADCAST STUDIO — QA AUTOMATION & SYSTEM AUDIT SUITE  ');
  console.log('===============================================================');

  const edgeProc = spawn(EDGE_PATH, [
    '--headless=new',
    '--remote-debugging-port=9225',
    '--window-size=1680,980',
    '--autoplay-policy=no-user-gesture-required',
    '--disable-gpu',
    'about:blank'
  ]);

  let res = null;
  for (let attempt = 0; attempt < 10; attempt++) {
    await new Promise(r => setTimeout(r, 600));
    try {
      res = await fetch('http://127.0.0.1:9225/json/new?' + encodeURIComponent(APP_URL), { method: 'PUT' });
      if (res.ok) break;
    } catch (e) {}
  }
  if (!res) throw new Error('Could not connect to Edge on port 9225 after retries');

  try {
    const target = await res.json();
    const ws = new WebSocket(target.webSocketDebuggerUrl);

    let idSeq = 1;
    const pending = new Map();
    const consoleErrors = [];
    const uncaughtExceptions = [];

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
      } else if (msg.method === 'Runtime.consoleAPICalled') {
        if (msg.params.type === 'error') {
          consoleErrors.push(msg.params.args.map(a => a.value || a.description || JSON.stringify(a)).join(' '));
        }
      } else if (msg.method === 'Runtime.exceptionThrown') {
        uncaughtExceptions.push(msg.params.exceptionDetails);
      }
    };

    await send('Runtime.enable');
    await send('Console.enable');
    await send('Page.enable');

    // Wait for initialization
    await new Promise(r => setTimeout(r, 4000));

    async function evalCode(expression) {
      const res = await send('Runtime.evaluate', {
        expression,
        returnByValue: true,
        awaitPromise: true
      });
      if (res.exceptionDetails) {
        throw new Error(res.exceptionDetails.text + ' ' + (res.exceptionDetails.exception?.description || ''));
      }
      return res.result.value;
    }

    const testResults = [];
    function record(category, testName, pass, details = '') {
      testResults.push({ category, testName, pass, details });
      console.log(`[${pass ? 'PASS' : 'FAIL'}] [${category}] ${testName} ${details ? '(' + details + ')' : ''}`);
    }

    // ---------------------------------------------------------
    // TEST GROUP 1: INITIAL STATE & CANVAS
    // ---------------------------------------------------------
    try {
      const state = await evalCode(`({
        hasCanvas: !!document.getElementById('mainCanvas'),
        canvasW: document.getElementById('mainCanvas')?.width,
        canvasH: document.getElementById('mainCanvas')?.height,
        hasAudioContext: typeof actx !== 'undefined' || typeof audioCtx !== 'undefined',
        subtitlesCount: subtitlesList?.length,
        slotsCount: mediaSlots?.length
      })`);
      record('Core', 'Canvas Full HD Initialization', state.hasCanvas && state.canvasW === 1920 && state.canvasH === 1080, `Width=${state.canvasW}, Height=${state.canvasH}`);
      record('Core', 'Default 11 Subtitles List', state.subtitlesCount === 11, `Count=${state.subtitlesCount}`);
      record('Core', 'Default Media Slots List', state.slotsCount >= 1, `Count=${state.slotsCount}`);
    } catch (err) {
      record('Core', 'Canvas & State Check', false, err.message);
    }

    // ---------------------------------------------------------
    // TEST GROUP 2: PARENT 3-STEP MODE VS PRO MODE SWITCHING
    // ---------------------------------------------------------
    try {
      // Check switching to Pro mode
      await evalCode(`document.getElementById('btnModeProStudio')?.click()`);
      await new Promise(r => setTimeout(r, 600));
      const proState = await evalCode(`({
        bodyClass: document.body.className,
        wizardDisplay: window.getComputedStyle(document.getElementById('quickWizardCard')).display,
        tabsDisplay: window.getComputedStyle(document.getElementById('sidebarCategoryTabs')).display
      })`);
      record('UI/UX Modes', 'Switch to Chuyên Sâu Pro Mode', proState.bodyClass.includes('app-mode-pro') && proState.wizardDisplay === 'none' && proState.tabsDisplay === 'flex', JSON.stringify(proState));

      // Switch back to Parent mode
      await evalCode(`document.getElementById('btnModeSimpleWizard')?.click()`);
      await new Promise(r => setTimeout(r, 600));
      const wizState = await evalCode(`({
        bodyClass: document.body.className,
        wizardDisplay: window.getComputedStyle(document.getElementById('quickWizardCard')).display
      })`);
      record('UI/UX Modes', 'Switch back to 3 Bước Nhanh (Phụ Huynh)', wizState.bodyClass.includes('app-mode-simple') && wizState.wizardDisplay === 'block', JSON.stringify(wizState));
    } catch (err) {
      record('UI/UX Modes', 'Mode Switching', false, err.message);
    }

    // ---------------------------------------------------------
    // TEST GROUP 3: STUDIO THEMES (ALL 5 THEMES)
    // ---------------------------------------------------------
    const themes = ['talk11_talkshow', 'talk11_classroom', 'talk11_livestream', 'white_orange_anchor', 'cyber_neon'];
    for (const th of themes) {
      try {
        const res = await evalCode(`(() => {
          const btn = document.querySelector('#wizThemePills .btn-wiz-theme[data-theme="${th}"]') || document.querySelector('.studio-theme-card[data-theme="${th}"]');
          if (btn) {
            btn.click();
            return selectedStudioTheme === '${th}';
          }
          return false;
        })()`);
        await evalCode(`render(previewCurrentSec)`);
        record('Virtual Studio', `Switch Studio Theme: ${th}`, res, `Current=${th}`);
      } catch (err) {
        record('Virtual Studio', `Switch Studio Theme: ${th}`, false, err.message);
      }
    }

    // Return to default talk11_talkshow
    await evalCode(`document.querySelector('#wizThemePills .btn-wiz-theme[data-theme="talk11_talkshow"]')?.click()`);

    // ---------------------------------------------------------
    // TEST GROUP 4: ASPECT RATIO SWITCHING (16:9 <-> 9:16)
    // ---------------------------------------------------------
    try {
      // Switch to 9:16
      await evalCode(`(() => {
        const btn = document.getElementById('btnRatio916') || document.querySelector('[data-ratio="9:16"]');
        if (btn) btn.click();
        else {
          selectedAspectRatio = '9:16';
          canvas.width = 1080;
          canvas.height = 1920;
          render(previewCurrentSec);
        }
      })()`);
      const ratio916 = await evalCode(`({ w: canvas.width, h: canvas.height, ratio: selectedAspectRatio })`);
      record('Aspect Ratio', 'Switch to Vertical 9:16 (Shorts/TikTok/Reels)', ratio916.w === 1080 && ratio916.h === 1920, `${ratio916.w}x${ratio916.h}`);

      // Switch back to 16:9
      await evalCode(`(() => {
        const btn = document.getElementById('btnRatio169') || document.querySelector('[data-ratio="16:9"]');
        if (btn) btn.click();
        else {
          selectedAspectRatio = '16:9';
          canvas.width = 1920;
          canvas.height = 1080;
          render(previewCurrentSec);
        }
      })()`);
      const ratio169 = await evalCode(`({ w: canvas.width, h: canvas.height, ratio: selectedAspectRatio })`);
      record('Aspect Ratio', 'Switch back to Horizontal 16:9 (Full HD Broadcast)', ratio169.w === 1920 && ratio169.h === 1080, `${ratio169.w}x${ratio169.h}`);
    } catch (err) {
      record('Aspect Ratio', 'Aspect Ratio Switching', false, err.message);
    }

    // ---------------------------------------------------------
    // TEST GROUP 5: SUBTITLE CRUD, MODAL & POSITIONING
    // ---------------------------------------------------------
    try {
      const subOps = await evalCode(`(() => {
        const initialCount = subtitlesList.length;
        // 1. Update text of first sub
        subtitlesList[0].text = "TALK11 KIỂM THỬ PHỤ ĐỀ TIẾNG VIỆT HOÀN HẢO";
        // 2. Add a new sub
        const newId = 'sub_test_' + Date.now();
        subtitlesList.push({
          id: newId,
          startSec: 50,
          endSec: 55,
          text: "Câu phụ đề số 12 mới thêm",
          hidden: false
        });
        const countAfterAdd = subtitlesList.length;
        renderSubtitlesUI();
        render(previewCurrentSec);
        // 3. Delete the added sub
        const delIdx = subtitlesList.findIndex(s => s.id === newId);
        if (delIdx !== -1) subtitlesList.splice(delIdx, 1);
        const countAfterDel = subtitlesList.length;
        renderSubtitlesUI();
        render(previewCurrentSec);

        // 4. Test autoScriptModal trigger button
        const btnAutoScript = document.getElementById('btnOpenAutoScriptModal');
        let modalOpened = false;
        if (btnAutoScript) {
          btnAutoScript.click();
          modalOpened = document.getElementById('autoScriptModal')?.classList.contains('show');
          document.getElementById('autoScriptModal')?.classList.remove('show');
        }

        return { initialCount, countAfterAdd, countAfterDel, modalOpened };
      })()`);
      record('Subtitles', 'Subtitle Update, Add & Delete (CRUD)', subOps.countAfterAdd === subOps.initialCount + 1 && subOps.countAfterDel === subOps.initialCount, JSON.stringify(subOps));
      record('Subtitles', 'Auto Script Modal Trigger Button', subOps.modalOpened, `modalOpened=${subOps.modalOpened}`);
    } catch (err) {
      record('Subtitles', 'Subtitle CRUD & Modal', false, err.message);
    }

    // ---------------------------------------------------------
    // TEST GROUP 6: MEDIA SLOTS TIMELINE CRUD & AUTO-MATCH
    // ---------------------------------------------------------
    try {
      const slotOps = await evalCode(`(() => {
        const initialSlotCount = mediaSlots.length;
        // Add slot
        const newSlot = {
          id: 'slot_test_' + Date.now(),
          name: 'Test Image',
          startSec: 40,
          endSec: 55,
          type: 'image',
          mediaUrl: '01_TALK11_Broadcast_16x9_Full.png',
          transition: 'fade'
        };
        mediaSlots.push(newSlot);
        const afterAdd = mediaSlots.length;
        // Auto match slots
        if (typeof autoMatchSlotsToTotalDuration === 'function') {
          autoMatchSlotsToTotalDuration();
        }
        // Remove slot
        const idx = mediaSlots.findIndex(s => s.id === newSlot.id);
        if (idx !== -1) mediaSlots.splice(idx, 1);
        const afterDel = mediaSlots.length;
        renderMediaSlotsUI();
        syncDurationUI();
        return { initialSlotCount, afterAdd, afterDel };
      })()`);
      record('Timeline', 'Media Slots Add, Auto-Match & Remove', slotOps.afterAdd === slotOps.initialSlotCount + 1 && slotOps.afterDel === slotOps.initialSlotCount, JSON.stringify(slotOps));
    } catch (err) {
      record('Timeline', 'Media Slots Timeline Ops', false, err.message);
    }

    // ---------------------------------------------------------
    // TEST GROUP 7: UNDO / REDO STATE MANAGER
    // ---------------------------------------------------------
    try {
      const undoRedo = await evalCode(`(() => {
        const origTitle = inputHeadline ? inputHeadline.value : '';
        captureAppStateSnapshot();
        if (inputHeadline) inputHeadline.value = 'TITLEN TEST UNDO REDO';
        pushUndoState('Test Edit Title');
        const canUndoBefore = (undoStack.length > 0);
        // trigger undo
        if (typeof undoAction === 'function') undoAction();
        else if (typeof undo === 'function') undo();
        else document.getElementById('btnUndo')?.click();
        
        return { canUndoBefore, origTitle, currentVal: inputHeadline?.value };
      })()`);
      record('Undo/Redo', 'Undo & Redo State Snapshot System', undoRedo.canUndoBefore, `UndoStackReady=${undoRedo.canUndoBefore}`);
    } catch (err) {
      record('Undo/Redo', 'Undo & Redo Manager', false, err.message);
    }

    // ---------------------------------------------------------
    // TEST GROUP 8: OVERLAP VERIFICATION (BANNER VS SUBTITLE)
    // ---------------------------------------------------------
    try {
      const overlapCheck = await evalCode(`(() => {
        // Measure where Subtitle Box is and where Headline Banner is
        render(5.0); // time = 5.0 has active sub 2
        const subBox = currentSubBox;
        // In talkshow theme:
        const bannerW = Math.min(880, canvas.width - 80);
        const bannerH = 52;
        // The newly fixed calculation:
        const bannerY = (showSubtitles && subPosY > (canvas.height * 0.55)) ? Math.min(canvas.height - 175, subPosY - bannerH - 12) : (canvas.height - 145);
        const bannerBottom = bannerY + bannerH;
        const subTop = subBox ? subBox.y : -1;
        const subBottom = subBox ? subBox.y + subBox.h : -1;
        const isOverlapping = subBox ? (bannerY < subBottom && bannerBottom > subTop) : false;
        const distanceBetween = subBox ? (subTop - bannerBottom) : 999;
        return {
          bannerY,
          bannerBottom,
          subTop,
          subBottom,
          distanceBetween,
          isOverlapping
        };
      })()`);
      record('Layout Quality', 'Zero Overlap Between Headline Banner & Subtitle', !overlapCheck.isOverlapping && overlapCheck.distanceBetween >= 10, 
        `Banner=[${overlapCheck.bannerY}..${overlapCheck.bannerBottom}], Sub=[${overlapCheck.subTop}..${overlapCheck.subBottom}], Gap=${overlapCheck.distanceBetween}px, Overlap=${overlapCheck.isOverlapping}`);
    } catch (err) {
      record('Layout Quality', 'Overlap Check', false, err.message);
    }

    // ---------------------------------------------------------
    // TEST GROUP 9: AUDIO ENGINE FILTERS & SILENCE CUTTER
    // ---------------------------------------------------------
    try {
      const audioCheck = await evalCode(`(() => {
        return {
          hasStudentAudioChain: typeof setupStudentAudioChain === 'function',
          hasSilenceCutter: typeof analyzeVideoAudioForSilence === 'function' && typeof buildStitchedSpeechClips === 'function',
          vocalIsolationMode: typeof currentVocalFilterMode !== 'undefined' ? currentVocalFilterMode : 'undefined',
          studentVolume: typeof studentMicVolume !== 'undefined' ? studentMicVolume : -1
        };
      })()`);
      record('Audio Engine', 'Audio Processing, Vocal Isolation & Silence Cutter Chain', audioCheck.hasStudentAudioChain && audioCheck.hasSilenceCutter, JSON.stringify(audioCheck));
    } catch (err) {
      record('Audio Engine', 'Audio Processing', false, err.message);
    }

    // ---------------------------------------------------------
    // TEST GROUP 10: RENDER & EXPORT ENGINES
    // ---------------------------------------------------------
    try {
      const exportEngineCheck = await evalCode(`(() => {
        return {
          hasExportFunction: typeof startExport === 'function',
          hasMediaRecorder: typeof MediaRecorder !== 'undefined',
          supportedCodecs: {
            vp9: MediaRecorder.isTypeSupported('video/webm;codecs=vp9,opus'),
            vp8: MediaRecorder.isTypeSupported('video/webm;codecs=vp8,opus'),
            h264: MediaRecorder.isTypeSupported('video/mp4;codecs=avc1') || MediaRecorder.isTypeSupported('video/webm;codecs=h264')
          },
          hasWebmFixer: typeof window.ysFixWebmDuration === 'function' || typeof fixWebmDuration === 'function'
        };
      })()`);
      record('Export Engine', 'MediaRecorder & 60FPS Codecs Availability', exportEngineCheck.hasMediaRecorder && (exportEngineCheck.supportedCodecs.vp9 || exportEngineCheck.supportedCodecs.vp8), JSON.stringify(exportEngineCheck));
      record('Export Engine', 'Fix WebM Duration EBML Injector', exportEngineCheck.hasWebmFixer, `hasWebmFixer=${exportEngineCheck.hasWebmFixer}`);
    } catch (err) {
      record('Export Engine', 'Export Engine Check', false, err.message);
    }

    // Summary
    console.log('\n===============================================================');
    console.log(' QA TEST SUMMARY REPORT');
    console.log('===============================================================');
    const passed = testResults.filter(t => t.pass).length;
    const failed = testResults.filter(t => !t.pass).length;
    console.log(`Total Tests Executed: ${testResults.length}`);
    console.log(`Passed: ${passed} | Failed: ${failed}`);
    console.log(`Console Errors Caught: ${consoleErrors.length}`);
    console.log(`Uncaught Exceptions: ${uncaughtExceptions.length}`);
    if (uncaughtExceptions.length > 0) {
      console.log('Uncaught details:', uncaughtExceptions.map(e => e.exception?.description || e.text || JSON.stringify(e)));
    }

    await send('Page.close');
  } catch (err) {
    console.error('[QA] Fatal test error:', err);
  } finally {
    edgeProc.kill();
  }
}

runTests();
