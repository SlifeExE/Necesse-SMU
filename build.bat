@echo off
setlocal

REM Builds a single-file Windows exe with PyInstaller
set SCRIPT=src\necesse_smu\cli.py
set NAME=NecesseSMU

pyinstaller --onefile --name %NAME% --console "%SCRIPT%"

echo.
echo Build finished. EXE: dist\%NAME%.exe
endlocal

