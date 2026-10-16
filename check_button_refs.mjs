import fs from 'fs';

const html = fs.readFileSync('Tao_Khung_Thoi_Su_Talk11.html', 'utf8');

const checkIds = [
  'btnRatio16x9', 'btnRatio9x16', 'btnHeaderSnapshot', 'btnUndo', 'btnRedo',
  'btnSaveProjectJSON', 'tabMobilePreview', 'tabMobileControls', 'tabMobileAll',
  'btnModeSimpleWizard', 'btnModeProStudio', 'btnWizBgAi', 'btnWizBgGreen',
  'btnWizBgRoom', 'btnWizAutoGenerateSubs', 'btnWizExportVideo', 'btnWizSwitchToPro',
  'btnResetToDefaults', 'btnExpandAllSidebar', 'btnCollapseAllSidebar',
  'btnLoadSampleMediaPack', 'btnVaultFilterAll', 'btnVaultFilterImg', 'btnVaultFilterVid',
  'btnVaultViewList', 'btnVaultViewGrid', 'btnSelectStudentFromVault',
  'btnLoadSampleStudentVideo', 'btnClearStudentVideo', 'btnPlayPauseStudentVid',
  'btnKeyAi', 'btnKeyGreen', 'btnKeyBlue', 'btnKeyRoom', 'btnAutoBeautyEnhance',
  'btnPosDeskCenter', 'btnPosTvSide', 'btnPosPipMini', 'btnPosLeft', 'btnPosReset',
  'btnRescanSilence', 'btnFontSocialGuide', 'btnShiftSubMinus1s', 'btnShiftSubMinusHalf',
  'btnShiftSubPlusHalf', 'btnShiftSubPlus1s', 'btnAutoGenerateSubsFromVideo',
  'btnAutoPlaceSfxTransitions', 'btnSfxSocialGuide', 'btnImportSfxFromUrl',
  'btnToggleSafeArea', 'btnFullscreenPreview', 'btnTimelineAutoCutout',
  'btnTimelineLoop', 'btnTimelineSnap', 'btnTrackAutoCutout', 'btnToggleStudentVideoTrack',
  'btnCelebRedownload', 'btnCelebZaloGuide', 'btnCelebClose'
];

const results = {};

for (const id of checkIds) {
  const lines = [];
  const linesArr = html.split('\n');
  linesArr.forEach((line, idx) => {
    if (line.includes(id)) {
      lines.push({ lineNum: idx + 1, content: line.trim() });
    }
  });
  results[id] = lines;
}

for (const [id, lines] of Object.entries(results)) {
  console.log(`\n=== ID: ${id} (matches: ${lines.length}) ===`);
  lines.forEach(l => console.log(`  L${l.lineNum}: ${l.content.slice(0, 100)}`));
}
