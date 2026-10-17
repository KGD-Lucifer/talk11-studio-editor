@echo off
chcp 65001 >nul
cd /d "%~dp0"
title TALK11 BROADCAST STUDIO - NLE DESKTOP ENGINE (CAPCUT PC)

if "%1"=="2" goto sync_html
if "%1"=="--sync" goto sync_html

echo ============================================================================== 
echo       TALK11 BROADCAST STUDIO - HE THONG DUNG VIDEO THOI SU 3D
echo       Dinh huong thay the CapCut PC: Tu dong hoa - NLE Chuyen nghiep
echo ============================================================================== 
echo [*] Dang khoi dong Web Server va mo ngay giao dien Desktop Studio...
echo.

where node >nul 2>nul
if %errorlevel% equ 0 (
    echo [*] Tim thay Node.js. Dang chay server.js tai cong 8080...
    if exist "%~dp0server.js" (
        node "%~dp0server.js"
    ) else if exist "%~dp0..\server.js" (
        node "%~dp0..\server.js"
    )
    goto end
)

where python >nul 2>nul
if %errorlevel% equ 0 (
    echo [*] Tim thay Python. Dang khoi dong python server tai cong 8080...
    if exist "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" (
        start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --app="http://127.0.0.1:8080/Tao_Khung_Thoi_Su_Talk11.html" --window-size=1680,980
    ) else if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
        start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --app="http://127.0.0.1:8080/Tao_Khung_Thoi_Su_Talk11.html" --window-size=1680,980
    ) else (
        start "" "http://127.0.0.1:8080/Tao_Khung_Thoi_Su_Talk11.html"
    )
    python -m http.server 8080
    goto end
)

echo [!] Khong tim thay Node/Python. Dang mo truc tiep file HTML trong trinh duyet...
if exist "%~dp0Tao_Khung_Thoi_Su_Talk11.html" (
    start "" "%~dp0Tao_Khung_Thoi_Su_Talk11.html"
) else (
    start "" "%~dp0..\Tao_Khung_Thoi_Su_Talk11.html"
)
goto end

:sync_html
echo.
echo [*] Dang dong bo tat ca cac file HTML trong du an...
if exist "%~dp0sync_all_htmls.py" (
    python "%~dp0sync_all_htmls.py"
) else if exist "%~dp0sync_all_htmls.js" (
    node "%~dp0sync_all_htmls.js"
)
echo [v] Dong bo hoan tat!
pause
exit /b

:end
pause
