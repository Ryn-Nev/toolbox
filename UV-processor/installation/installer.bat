@echo off
setlocal EnableDelayedExpansion

:: === Set install path ===
set "INSTALL_DIR=%LocalAppData%\UV-processor"
set "EXE_URL=https://raw.githubusercontent.com/Ryn-Nev/toolbox/main/UV-processor/installation/UV-processor.exe"

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
echo Downloading UV-processor.exe...
powershell -Command "try { Invoke-WebRequest -Uri '%EXE_URL%' -OutFile '%INSTALL_DIR%\UV-processor.exe' } catch { Write-Host 'Error downloading UV-processor.exe'; exit 1 }"
if errorlevel 1 (
    echo Error: Failed to download UV-processor.exe
    pause
    exit /b 1
)

:: === Add UV-processor to user PATH ===
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
    echo Adding UV-processor to user PATH...
    setx Path "%NEW_PATH%"
) else (
    echo UV-processor is already in the user PATH.
)
echo.

echo.
echo Installation completed successfully!
echo.

@REM :: === Create desktop shortcut ===
@REM echo Creating desktop shortcut...
@REM set "SHORTCUT_NAME=UV-processor"
@REM set "SHORTCUT_PATH=%UserProfile%\Desktop\%SHORTCUT_NAME%.lnk"
@REM set "ICON_PATH=%INSTALL_DIR%\UV-icon.ico"

@REM :: === Prompt for desktop shortcut ===
@REM choice /M "Do you want to create a desktop shortcut for UV-processor?"
@REM if errorlevel 2 goto skip_shortcut

@REM :: === Create desktop shortcut ===
@REM echo Creating desktop shortcut...
@REM set "SHORTCUT_NAME=UV-processor"
@REM set "SHORTCUT_PATH=%UserProfile%\Desktop\%SHORTCUT_NAME%.lnk"
@REM set "ICON_PATH=%INSTALL_DIR%\UV-icon.ico"

@REM :: Use PowerShell to create the shortcut
@REM powershell -Command ^
@REM $WshShell = New-Object -ComObject WScript.Shell; ^
@REM $Shortcut = $WshShell.CreateShortcut('%SHORTCUT_PATH%'); ^
@REM $Shortcut.TargetPath = '%INSTALL_DIR%\UV-processor.exe'; ^
@REM $Shortcut.IconLocation = '%INSTALL_DIR%\UV-processor.exe,0'
@REM $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; ^
@REM $Shortcut.Save()

pause
