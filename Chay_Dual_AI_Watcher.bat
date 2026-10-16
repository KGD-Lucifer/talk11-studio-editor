@echo off
chcp 65001 > nul
title TALK11 Dual-AI Auto Watcher (Codex & Antigravity)
echo ===============================================================
echo   TALK11 BROADCAST STUDIO — DUAL-AI AUTOMATION WATCHER
echo ===============================================================
echo.
echo Đang chạy trình giám sát tự động 2 chiều (Codex & Antigravity)...
echo Nhấn Ctrl+C để dừng tiến trình.
echo.

node dual_ai_watcher.mjs --daemon

pause
