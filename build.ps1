param(
  [string]$ConfigPath = "config.json"
)

Write-Host "Installing requirements..."
py -m pip install --upgrade pip
py -m pip install -r requirements.txt

Write-Host "Building single-file executable with PyInstaller..."

$iconArg = ""
if (Test-Path "icon.png") {
  Write-Host "Converting icon.png to icon.ico ..."
  py -m pip install --quiet Pillow | Out-Null
  py tools\png_to_ico.py icon.png icon.ico
  if (Test-Path "icon.ico") { $iconArg = "--icon icon.ico" }
} elseif (Test-Path "icon.ico") {
  $iconArg = "--icon icon.ico"
}

# Remove old spec/build to avoid stale settings (like old icon)
if (Test-Path "NecesseSAMU.spec") { Remove-Item "NecesseSAMU.spec" -Force }
if (Test-Path "build") { Remove-Item "build" -Recurse -Force }

py -m PyInstaller --clean --noconfirm -F -n NecesseSAMU -p src $iconArg src\samu_entry.py

Write-Host "Copying config..."
if (Test-Path $ConfigPath) {
  Copy-Item $ConfigPath dist\config.json -Force
} elseif (Test-Path "config.sample.json") {
  Write-Warning "No config.json found. Copying sample."
  Copy-Item config.sample.json dist\config.json -Force
}

Write-Host "Done. Output in dist\\NecesseSAMU.exe"
if ($iconArg) { Write-Host "Included icon from icon.ico" }
