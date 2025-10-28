@echo off
setlocal

REM Builds a single-file Windows exe with PyInstaller
set NAME=NecesseSAMU

echo Installing requirements...
py -m pip install --upgrade pip
py -m pip install -r requirements.txt

REM Resolve icon
set ICON_ARG=
REM Prefer PNG and always regenerate ICO if PNG exists
if exist icon.png (
  echo Converting icon.png to icon.ico ...
  py -m pip install --quiet Pillow >nul
  py tools\png_to_ico.py icon.png icon.ico
  if exist icon.ico set ICON_ARG=--icon icon.ico
) else (
  if exist icon.ico (
    set ICON_ARG=--icon icon.ico
  )
)

REM Remove old spec to avoid stale icon/config
if exist %NAME%.spec del /q %NAME%.spec
if exist build rmdir /s /q build

echo Building executable...
py -m PyInstaller --clean --noconfirm -F -n %NAME% -p src %ICON_ARG% src\samu_entry.py

if exist config.json (
  copy /Y config.json dist\config.json >nul
) else (
  if exist config.sample.json copy /Y config.sample.json dist\config.json >nul
)

echo.
echo Build finished. EXE: dist\%NAME%.exe
if defined ICON_ARG echo Included icon from icon.ico
endlocal
