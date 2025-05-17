@echo off
setlocal EnableDelayedExpansion

:: === Set install path ===
set "INSTALL_DIR=%LocalAppData%\Unzipper"
set "EXE_URL=https://raw.githubusercontent.com/Ryn-Nev/toolbox/main/unzipper/installation/unzipper.exe"
set "REG_FILE=%TEMP%\add_to_context_menu.reg"

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

:: === Create and apply registry file ===
echo Creating registry file...
echo Windows Registry Editor Version 5.00 > "%REG_FILE%"
echo. >> "%REG_FILE%"
echo [HKEY_CURRENT_USER\Software\Classes\SystemFileAssociations\.zip\shell\Unzip with Unzipper] >> "%REG_FILE%"
echo @="Unzip with Unzipper" >> "%REG_FILE%"
echo "Icon"="%INSTALL_DIR%\unzipper.exe" >> "%REG_FILE%"
echo "NoWorkingDirectory"="" >> "%REG_FILE%"
echo. >> "%REG_FILE%"
echo [HKEY_CURRENT_USER\Software\Classes\SystemFileAssociations\.zip\shell\Unzip with Unzipper\command] >> "%REG_FILE%"
echo @="\"%INSTALL_DIR%\unzipper.exe\" \"%%1\"" >> "%REG_FILE%"

:: === Import registry settings ===
echo Adding registry entry to context menu...
regedit /s "%REG_FILE%"
if errorlevel 1 (
    echo Error: Failed to add context menu entry
    pause
    exit /b 1
)

echo.
echo Installation completed successfully!
echo You can now right-click any .zip file and select 'Unzip with Unzipper'.
echo.
pause
