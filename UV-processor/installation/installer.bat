@echo off
setlocal EnableDelayedExpansion

:: === Set install path ===
set "INSTALL_DIR=%LocalAppData%\UV-processor"
set "EXE_URL=https://raw.githubusercontent.com/Ryn-Nev/toolbox/main/unzipper/installation/unzipper.exe"

echo Creating install directory at: %INSTALL_DIR%
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%" >nul 2>&1
    if errorlevel 1 (
        echo Error: Could not create installation directory.
        pause
        exit /b 1
    )
)

:: === Download EXE ===
echo Downloading unzipper.exe...
powershell -Command "try { Invoke-WebRequest -Uri '%EXE_URL%' -OutFile '%INSTALL_DIR%\unzipper.exe' } catch { Write-Host 'Error downloading unzipper.exe'; exit 1 }"
if errorlevel 1 (
    echo Error: Failed to download unzipper.exe
    pause
    exit /b 1
)

:: === Add Unzipper to user PATH ===
set "NEW_PATH=%INSTALL_DIR%"
set "CUR_PATH="
for /f "tokens=2*" %%A in ('reg query "HKCU\Environment" /v Path 2^>nul') do set "CUR_PATH=%%B"
echo Current user PATH: %CUR_PATH%
echo.

:: Check if already in PATH
echo %CUR_PATH% | find /I "%NEW_PATH%" >nul
if errorlevel 1 (
    if defined CUR_PATH (
        set "NEW_PATH=%CUR_PATH%;%NEW_PATH%"
    )
    echo Adding Unzipper to user PATH...
    setx Path "%NEW_PATH%"
) else (
    echo Unzipper is already in the user PATH.
)
echo.

echo.
echo Installation completed successfully!
echo You can now right-click any .zip file and select 'Unzip with Unzipper'.
echo.
pause
