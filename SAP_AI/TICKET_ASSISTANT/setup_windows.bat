@echo off
setlocal
cd /d "%~dp0"
py -3 -m venv .venv
if errorlevel 1 goto :error
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m unittest discover -s tests -v
if errorlevel 1 goto :error
echo.
echo Setup complete. Run run_windows.bat.
pause
exit /b 0
:error
echo Setup failed. Review the messages above.
pause
exit /b 1
