@echo off
REM Get the full path to the Python script (UV-processor.py).
REM %~dp0 expands to the drive and path of this batch file (UVP.cmd).
REM So, PYTHON_SCRIPT_FULL_PATH will be like C:\MyScripts\UV-processor.py
set "PYTHON_SCRIPT_FULL_PATH=%~dp0UV-processor.py"

REM Now, run the Python script using its full path.
REM CRUCIALLY: We do *not* use pushd/popd here. This means the
REM current working directory of the command prompt will remain
REM whatever directory you were in when you typed 'UVP'.
python "%PYTHON_SCRIPT_FULL_PATH%"

REM Optional: Keep the command prompt window open after the script finishes
REM PAUSE