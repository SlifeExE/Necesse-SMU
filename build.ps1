param(
  [string]$ConfigPath = "config.json"
)

Write-Host "Installing requirements..."
py -m pip install --upgrade pip
py -m pip install -r requirements.txt

Write-Host "Building single-file executable with PyInstaller..."
py -m PyInstaller -F -n NecesseSMU -p src src\smu_entry.py

Write-Host "Copying config..."
if (Test-Path $ConfigPath) {
  Copy-Item $ConfigPath dist\config.json -Force
} elseif (Test-Path "config.sample.json") {
  Write-Warning "No config.json found. Copying sample."
  Copy-Item config.sample.json dist\config.json -Force
}

Write-Host "Done. Output in dist\\NecesseSMU.exe"
