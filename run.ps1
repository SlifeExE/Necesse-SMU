param(
  [string]$ConfigPath = "config.json"
)

$env:PYTHONPATH = Join-Path $PSScriptRoot "src"
py -m pip install -r requirements.txt
py -m necesse_smu --config $ConfigPath
