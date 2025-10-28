param(
  [string]$ConfigPath = "config.json"
)

Write-Host "Installing requirements..."
py -m pip install --upgrade pip
py -m pip install -r requirements.txt

Write-Host "Building single-file executable with PyInstaller..."
py -m PyInstaller -F -n NecesseSMU -p src src\necesse_smu\__main__.py

Write-Host "Copying config..."
if (Test-Path $ConfigPath) {
  Copy-Item $ConfigPath dist\NecesseSMU\ -Force
} else {
  Write-Warning "No config.json found. Copying sample."
  Copy-Item config.sample.json dist\NecesseSMU\config.json
}

Write-Host "Done. Output in dist\\NecesseSMU.exe and dist\\NecesseSMU\\"
