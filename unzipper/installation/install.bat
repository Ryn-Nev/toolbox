@echo off
setlocal EnableDelayedExpansion

:: === Set install path ===
set "INSTALL_DIR=%LocalAppData%\Unzipper"
set "EXE_URL=https://raw.githubusercontent.com/Ryn-Nev/toolbox/unzipper/installation/unzipper.exe"
set "REG_URL=https://raw.githubusercontent.com/Ryn-Nev/toolbox/unzipper/installation/add_to_context_menu.reg"
set "DOWNLOADED_REG=%TEMP%\add_to_context_menu.reg"
set "PATCHED_REG=%TEMP%\patched_unzipper.reg"

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

:: === Download REG file ===
echo Downloading registry file...
powershell -Command "try { Invoke-WebRequest -Uri '%REG_URL%' -OutFile '%DOWNLOADED_REG%' } catch { Write-Host 'Error downloading registry file'; exit 1 }"
if errorlevel 1 (
    echo Error: Failed to download registry file
    pause
    exit /b 1
)

:: === Replace placeholder with escaped install path ===
set "ESCAPED_PATH=%INSTALL_DIR:\=\\%"
powershell -Command "try { (Get-Content '%DOWNLOADED_REG%') -replace '<<<INSTALL_PATH>>>', '%ESCAPED_PATH%' | Set-Content '%PATCHED_REG%' } catch { Write-Host 'Error processing registry file'; exit 1 }"
if errorlevel 1 (
    echo Error: Failed to process registry file
    pause
    exit /b 1
)

:: === Import registry settings ===
echo Adding registry entry to context menu...
regedit /s "%PATCHED_REG%"
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
