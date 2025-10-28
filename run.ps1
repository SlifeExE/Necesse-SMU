param(
  [string]$ConfigPath = "config.json"
)

$env:PYTHONPATH = Join-Path $PSScriptRoot "src"
py -m pip install -r requirements.txt
py -m necessse_smu --config $ConfigPath
