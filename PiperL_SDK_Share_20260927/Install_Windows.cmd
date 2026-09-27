@echo off
setlocal
cd /d "%~dp0"
set "PYTHONUTF8=1"
py -3.12 -c "import struct,sys; sys.exit(0 if struct.calcsize('P')==8 else 1)"
if errorlevel 1 (
  echo Please install Python 3.12 64-bit with the Python launcher first.
  pause
  exit /b 1
)
py -3.12 -m venv .venv
if errorlevel 1 goto fail
".venv\Scripts\python.exe" -m pip install --no-index --find-links="%~dp0wheels" -r requirements-windows.txt
if errorlevel 1 goto fail
".venv\Scripts\python.exe" smoke_test.py
if errorlevel 1 goto fail
echo Installation complete. No robot connection was opened.
pause
exit /b 0
:fail
echo Installation failed. Keep this window for troubleshooting.
pause
exit /b 1
