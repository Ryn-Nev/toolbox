@echo off
REM Author: Ryan Neville Hansen | Stellenbosch University
REM Email: 25088521@sun.ac.za
REM Created with assistance from Claude AI

setlocal

REM Check if python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python not found. Downloading and installing Python 3.11.7...
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.13.3/python-3.13.3-amd64.exe -OutFile python-installer.exe"
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
python -m pip install pandas numpy matplotlib scipy
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to install required packages
    exit /b 1
)

echo.
echo Installation complete! All required packages have been installed.
pause