@echo off
REM Author: Ryan Neville Hansen | Stellenbosch University
REM Email: 25088521@sun.ac.za
REM Created with assistance from Claude AI

setlocal

REM Check if python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python not found. Downloading and installing Python 3.13.3...
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.11.7/python-3.13.3-amd64.exe -OutFile python-installer.exe"
    IF NOT EXIST python-installer.exe (
        echo Failed to download Python installer
        exit /b 1
    )
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1
    del python-installer.exe
    
    REM Verify Python installation
    python --version >nul 2>&1
    IF %ERRORLEVEL% NEQ 0 (
        echo Python installation failed
        exit /b 1
    )
) ELSE (
    echo Python is already installed.
)

REM Ensure pip is available
python -m pip --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Pip not found. Attempting to install pip...
    python -m ensurepip --upgrade
    IF %ERRORLEVEL% NEQ 0 (
        echo Failed to install pip
        exit /b 1
    )
) ELSE (
    echo Pip is already installed.
)

REM Upgrade pip
python -m pip install --upgrade pip
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to upgrade pip
    exit /b 1
)

REM Install required packages
echo Installing required packages...
python -m pip install pandas numpy matplotlib scipy plotly
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to install required packages
    exit /b 1
)

:: === Download UV-processor.py ===
echo Installing UV-processor.py...

set "INSTALL_DIR=%LocalAppData%\UV-processor"
set "SCRIPT_URL=https://raw.githubusercontent.com/Ryn-Nev/toolbox/main/UV-processor/UV-processor.py"
set "SCRIPT_PATH=%INSTALL_DIR%\UV-processor.py"

if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%" >nul 2>&1
)

echo Downloading script to %SCRIPT_PATH%...
powershell -Command "try { Invoke-WebRequest -Uri '%SCRIPT_URL%' -OutFile '%SCRIPT_PATH%' } catch { Write-Host 'Error downloading UV-processor.py'; exit 1 }"
if errorlevel 1 (
    echo Error: Failed to download UV-processor.py
    pause
    exit /b 1
)

:: === Download UVP.cmd shim ===
set "SHIM_URL=https://raw.githubusercontent.com/Ryn-Nev/toolbox/main/UV-processor/installation/UVP.cmd"
set "SHIM_PATH=%INSTALL_DIR%\UVP.cmd"

echo Downloading UVP.cmd shim to %SHIM_PATH%...
powershell -Command "try { Invoke-WebRequest -Uri '%SHIM_URL%' -OutFile '%SHIM_PATH%' } catch { Write-Host 'Error downloading UVP.cmd'; exit 1 }"
if errorlevel 1 (
    echo Error: Failed to download UVP.cmd
    pause
    exit /b 1
)

:: === Add script directory to user PATH if not already ===
set "NEW_PATH=%INSTALL_DIR%"
set "CUR_PATH="
for /f "tokens=2*" %%A in ('reg query "HKCU\Environment" /v Path 2^>nul') do set "CUR_PATH=%%B"

echo Current user PATH: %CUR_PATH%
echo.

echo %CUR_PATH% | find /I "%NEW_PATH%" >nul
if errorlevel 1 (
    if defined CUR_PATH (
        set "NEW_PATH=%CUR_PATH%;%NEW_PATH%"
    )
    echo Adding UV-processor to user PATH...
    setx Path "%NEW_PATH%"
) else (
    echo UV-processor.py directory is already in the user PATH.
)

echo UV-processor.py installed successfully.

echo.
echo Installation complete! All required packages have been installed.
pause
endlocal