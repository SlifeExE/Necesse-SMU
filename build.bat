@echo off
setlocal

REM Builds a single-file Windows exe with PyInstaller
set NAME=NecesseSMU

echo Installing requirements...
py -m pip install --upgrade pip
py -m pip install -r requirements.txt

echo Building executable...
py -m PyInstaller -F -n %NAME% -p src src\necesse_smu\__main__.py

if exist config.json (
  copy /Y config.json dist\config.json >nul
) else (
  if exist config.sample.json copy /Y config.sample.json dist\config.json >nul
)

echo.
echo Build finished. EXE: dist\%NAME%.exe
endlocal
