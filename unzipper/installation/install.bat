@echo off
setlocal

:: === Set install path ===
set "INSTALL_DIR=%LocalAppData%\Unzipper"
set "EXE_URL=https://raw.githubusercontent.com/YOUR_USERNAME/unzipper-installer/main/unzipper.exe"
set "REG_URL=https://raw.githubusercontent.com/YOUR_USERNAME/unzipper-installer/main/add_unzipper_context.reg"
set "DOWNLOADED_REG=%TEMP%\add_unzipper_context.reg"
set "PATCHED_REG=%TEMP%\patched_unzipper.reg"

echo Creating install directory at: %INSTALL_DIR%
mkdir "%INSTALL_DIR%" >nul 2>&1

:: === Download EXE ===
echo Downloading unzipper.exe...
powershell -Command "Invoke-WebRequest -Uri '%EXE_URL%' -OutFile '%INSTALL_DIR%\unzipper.exe'"

:: === Download REG file ===
echo Downloading registry file...
powershell -Command "Invoke-WebRequest -Uri '%REG_URL%' -OutFile '%DOWNLOADED_REG%'"

:: === Replace placeholder with escaped install path ===
set "ESCAPED_PATH=%INSTALL_DIR:\=\\%"
powershell -Command "(Get-Content '%DOWNLOADED_REG%') -replace '<<<INSTALL_PATH>>>', '%ESCAPED_PATH%' | Set-Content '%PATCHED_REG%'"

:: === Import registry settings ===
echo Adding registry entry to context menu...
regedit /s "%PATCHED_REG%"

echo Done! You can now right-click any .zip file and select 'Unzip with Unzipper'.
pause
