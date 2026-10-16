with open('Tao_Khung_Thoi_Su_Talk11.html', 'r', encoding='utf-8') as f:
    html = f.read()

checks = {
    'quickWizardCard': 'id="quickWizardCard"' in html,
    'celebrationModal': 'id="celebrationModal"' in html,
    'btnModeSimpleWizard': 'id="btnModeSimpleWizard"' in html,
    'btnModeProStudio': 'id="btnModeProStudio"' in html,
    'wizStudentName': 'id="wizStudentName"' in html,
    'wizStudentTitle': 'id="wizStudentTitle"' in html,
    'wizVideoTopic': 'id="wizVideoTopic"' in html,
    'inputWizStudentVideo': 'id="inputWizStudentVideo"' in html,
    'btnWizBgRoom': 'id="btnWizBgRoom"' in html,
    'btnWizBgGreen': 'id="btnWizBgGreen"' in html,
    'wizThemePills': 'id="wizThemePills"' in html,
    'btnWizExportVideo': 'id="btnWizExportVideo"' in html,
    'applyStudentVideoDuration': 'function applyStudentVideoDuration' in html,
    'setAppUIMode': 'function setAppUIMode' in html,
    'setStudentBgMode': 'function setStudentBgMode' in html,
    'showCelebrationModal': 'function showCelebrationModal' in html,
    'student mic audio in export': 'stGain.connect(dest)' in html,
    'bgm audio in export': 'bgmGain.connect(dest)' in html,
    'broadcast led window in canvas': '!studentChromaEnabled' in html,
    'selectAppFont': 'id="selectAppFont"' in html,
    'wizSelectFont': 'id="wizSelectFont"' in html,
    'inputCustomFontFile': 'id="inputCustomFontFile"' in html,
    'inputCustomSfxFile': 'id="inputCustomSfxFile"' in html,
    'btnImportSfxFromUrl': 'id="btnImportSfxFromUrl"' in html,
    'saveCustomFontToDB': 'function saveCustomFontToDB' in html,
    'saveCustomSfxToDB': 'function saveCustomSfxToDB' in html,
    'handleCustomFontFileUpload': 'function handleCustomFontFileUpload' in html,
    'handleCustomSfxUpload': 'function handleCustomSfxUpload' in html,
    'currentSelectedFont canvas integration': 'currentSelectedFont' in html,
    'sliderWizStudentVolume': 'id="sliderWizStudentVolume"' in html,
    'selectWizVocalClean': 'id="selectWizVocalClean"' in html,
    'chkSilenceCutEnable': 'id="chkSilenceCutEnable"' in html,
    'chkWizSilenceCut': 'id="chkWizSilenceCut"' in html,
    'setupStudentAudioChain': 'function setupStudentAudioChain' in html,
    'applyVocalFilterMode': 'function applyVocalFilterMode' in html,
    'detectStudentVideoSilence': 'function detectStudentVideoSilence' in html,
    'setStudentVolume': 'function setStudentVolume' in html,
    'mapCompressedTimeToOriginal': 'function mapCompressedTimeToOriginal' in html,
    'inputTvBorderWidth': 'id="inputTvBorderWidth"' in html,
    'tvColorPill None option': 'data-color="none"' in html,
    'tvBorderWidth variable': 'tvBorderWidth' in html,
    'buildStitchedSpeechClips': 'function buildStitchedSpeechClips' in html,
    'getStudentVideoPlaybackTime': 'function getStudentVideoPlaybackTime' in html,
    'applyRippleStitchSilences': 'function applyRippleStitchSilences' in html,
    'fitMediaSlotsToDuration': 'function fitMediaSlotsToDuration' in html,
    'silenceStitchFlowBadge': 'id="silenceStitchFlowBadge"' in html,
    'wizSilenceStitchBadge': 'id="wizSilenceStitchBadge"' in html,
    'wizSelectTvTransition': 'id="wizSelectTvTransition"' in html,
    'combo_zoom_flash transition': 'value="combo_zoom_flash"' in html,
    'whip_whoosh transition': 'value="whip_whoosh"' in html,
    'news_flash transition': 'value="news_flash"' in html,
    'news_slide_push transition': 'value="news_slide_push"' in html,
    'spin_twist transition': 'value="spin_twist"' in html,
    'tv_glitch_static transition': 'value="tv_glitch_static"' in html,
    'dip_to_black transition': 'value="dip_to_black"' in html,
    # 7 NEW REQUIREMENTS:
    '1. Advanced Audio Noise Gate & De-Esser': 'deEsser' in html and 'id="sliderStudentDenoise"' in html,
    '2. AI Person Segmentation (No Green Screen Needed)': 'btnWizBgAi' in html and 'btnKeyAi' in html and 'initMediaPipeSelfie' in html,
    '2b. Pure-JS Human Saliency Matting Fallback': 'function runPureJsSubjectMattingFallback' in html,
    '3. Auto Lighting / Exposure Lift': 'enableAutoLighting' in html and 'chkBrtAutoLighting' in html,
    '3b. 4K Super-Resolution Sharpness Unsharp Mask': 'sliderBeautySharpness' in html and 'applyUnsharpMaskSharpness' in html,
    '4. Movable Character on Canvas (Drag & Scale)': 'getStudentCharacterScreenBounds' in html and 'isDraggingStudent' in html,
    '5. Undo / Redo Buttons & Shortcuts (Ctrl+Z / Ctrl+Y)': 'btnUndo' in html and 'btnRedo' in html and 'pushUndoState' in html and 'executeUndo' in html,
    '6. Timeline Student Video Track Row': 'id="trackStudentVideoRow"' in html and 'id="trackStudentVideoContent"' in html,
    '6b. Draggable Student Video Timeline Block': 'renderStudentVideoTrackUI' in html and 'block-student-video' in html,
    '7. Auto Speech-to-Text Subtitles From Video': 'id="btnAutoGenerateSubsFromVideo"' in html and 'autoGenerateSubtitlesFromVideo' in html,
    # CapCut Auto Background Removal Upgrades:
    '8. Timeline 1-Click Auto Cutout Button': 'id="btnTimelineAutoCutout"' in html,
    '9. Track 0 Header Quick Cutout Toggle': 'id="btnTrackAutoCutout"' in html,
    '10. Color Decontamination / Defringe': 'despillStrength' in html and 'COLOR DECONTAMINATION' in html,
    '11. Morphological Mask Erode/Expand Slider': 'id="sliderAiErode"' in html and 'studentAiErodeRadius' in html,
    '12. Motion-Adaptive Temporal Matting Filter': 'aiTemporalAlphaBuffer' in html and 'enableAiAntiFlicker' in html,
    '13. Guided Hairline & Fine Detail Recovery': 'Guided Hairline Recovery' in html and 'Hermite smoothstep' in html,
    # P1 - P4 GitHub Upgrades:
    '14. Lead-In & Lead-Out Silence Cut Padding': 'leadInSafetyPadding' in html and 'leadOutSafetyPadding' in html,
    '15. Speech-Burst Aligned Subtitles & SRT/VTT': 'parseSrtOrVtt' in html and 'id="inputDirectSrtVtt"' in html,
    '16. 3D Stage Ambient Contact Floor Shadow': 'AMBIENT CONTACT SHADOW' in html,
    '17. Timeline Magnetic Snapping Engine': 'snapTargets' in html,
    '18. Video Export Safe Cancellation Guard': 'isExportCancelled' in html,
}

all_pass = True
for k, v in checks.items():
    status = "PASS" if v else "FAIL"
    print(f"[{status}] {k}")
    if not v:
        all_pass = False

print(f"\nALL CHECKS PASSED: {all_pass}")
if not all_pass:
    exit(1)
