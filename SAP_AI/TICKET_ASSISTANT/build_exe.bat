@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Run setup_windows.bat first.
  pause
  exit /b 1
)
call .venv\Scripts\activate.bat
python -m PyInstaller --noconfirm --clean --windowed --name SAP_AI_Ticket_Assistant --add-data "config;config" --hidden-import PIL._tkinter_finder main.py
if errorlevel 1 goto :error
if not exist "dist\SAP_AI_Ticket_Assistant\config" mkdir "dist\SAP_AI_Ticket_Assistant\config"
xcopy /E /I /Y config "dist\SAP_AI_Ticket_Assistant\config" >nul
for %%D in (TicketData reports screenshots logs exports) do if not exist "dist\SAP_AI_Ticket_Assistant\%%D" mkdir "dist\SAP_AI_Ticket_Assistant\%%D"
echo.
echo EXE created under dist\SAP_AI_Ticket_Assistant\SAP_AI_Ticket_Assistant.exe
echo Keep the dist folder together because it contains editable configuration files.
pause
exit /b 0
:error
echo Build failed.
pause
exit /b 1
