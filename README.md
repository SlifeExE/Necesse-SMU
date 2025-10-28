# Necesse Server Mod Updater (SMU)

Kleines Tool zum Aktualisieren der Mods eines Necesse Servers mit SteamCMD.

Es liest `modlist.data` aus dem Necesse Mods-Ordner, ermittelt die Steam Workshop IDs (direkt aus der Datei, per Overrides oder optional via Steam Web API) und lädt die Mods mit SteamCMD herunter. Danach werden die `.jar` Dateien in den Server-Mods-Ordner kopiert. Vorher vorhandene `.jar` im Zielordner werden gelöscht (nur `modlist.data` bleibt erhalten).

## Voraussetzungen
- Windows mit SteamCMD installiert (z. B. `C:\SteamCMD\steamcmd.exe`).
- Necesse Mods-Ordner (z. B. `C:\Users\Administrator\AppData\Roaming\Necesse\mods`).
- Optional: Steam Web API Key, falls Mod-Namen auf Workshop-IDs aufgelöst werden sollen.

## Konfiguration
Passe die Datei `config.json` an:

- `mods_dir`: Pfad zum Necesse `mods` Ordner (dort liegt `modlist.data`).
- `steamcmd_path`: Pfad zur `steamcmd.exe`.
- `steam_app_id`: AppID (Necesse = `1169040`).
- `download_dir`: Temporäres Download-Verzeichnis für SteamCMD.
- `temp_ids_file`: Datei, in die die ermittelten Mod-IDs geschrieben werden.
- `workshop_content_dir`: Optional; Standard ist `<SteamCMD>\steamapps\workshop\content\1169040`.
- `steam_web_api_key`: Optional; für Namenssuche im Workshop.
- `mod_id_overrides`: Mapping von Mod-Namen -> Workshop-ID (fallback, wenn keine IDs in `modlist.data` stehen).

Hinweis: `modlist.data` darf entweder direkt IDs enthalten (z. B. `2827931647`) oder Mod-Namen. Für Namen werden zuerst `mod_id_overrides` geprüft und optional die Steam Web API (falls `steam_web_api_key` gesetzt ist).

## Nutzung (Python)

PowerShell (setzt PYTHONPATH automatisch und installiert Requirements):

```
./run.ps1 -ConfigPath config.json
```

Oder manuell:

```
py -m pip install -r requirements.txt
$env:PYTHONPATH = "src"
py -m necesse_smu --config config.json
```

- `--dry-run` zeigt nur an, was passieren würde (kein Download/Kopieren).

## Nutzung (EXE)

1) Baue die EXE mit PyInstaller (erfordert Python + `pip install -r requirements.txt`):

```
build.bat   (oder)   ./build.ps1
```

2) Starte die EXE per Doppelklick: `dist\NecesseSMU.exe` (legt Config neben die EXE oder nutze `--config`).

## Funktionsweise
- Liest `modlist.data` im `mods_dir`.
- Extrahiert alle numerischen Workshop-IDs; verbleibende Einträge gelten als Namen.
- Mappt Namen via `mod_id_overrides` und optional via Steam Web API.
- Führt einen SteamCMD-Aufruf mit mehreren `+workshop_download_item` aus.
- Sucht `.jar` Dateien in den Workshop-Downloads und kopiert sie in den Mods-Ordner.
- Löscht vorher alle `.jar` im Zielordner (nicht `modlist.data`).

## Beispiel SteamCMD Befehl (intern generiert)

```
steamcmd.exe +force_install_dir "C:\SteamCMD\downloads" +login anonymous \
  +workshop_download_item 1169040 2827931647 \
  +workshop_download_item 1169040 3052859125 \
  +quit
```

## Hinweise
- Workshop-Inhalte landen standardmäßig unter `<SteamCMD>\steamapps\workshop\content\1169040\<ModID>`. Das Tool sucht dort rekursiv nach `.jar`.
- Wenn keine API genutzt wird, pflege `mod_id_overrides`, oder trage die IDs direkt in `modlist.data` ein.
- Dieses Repo enthält `build.bat` und `build.ps1` für einen Ein-Klick-Build der EXE.

