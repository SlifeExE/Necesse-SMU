<p align="center">
  <img src="https://raw.githubusercontent.com/SlifeExE/Necesse-SAMU/main/icon.png" width="128" alt="Necesse Server & Mod Updater Icon">
</p>


# Necesse Server and Mod Updater (SAMU)

Small tool to keep Necesse server mods up to date using SteamCMD.

It reads `modlist.data` from your Necesse mods folder, resolves Steam Workshop IDs (directly from the file, via overrides, or optional Steam Web API), downloads mods via SteamCMD, and copies the resulting `.jar` files into the server mods folder. Existing `.jar` files in the target folder are removed first (only `modlist.data` stays). After the mods are updated, the tool prompts whether you want to update the Necesse server as well.

## Quick Start (Releases)
- Download the latest `NecesseSAMU.exe` from GitHub Releases.
- Put a `config.json` next to the EXE with this structure:

```
{
  "mods_dir": "C:\\Users\\Administrator\\AppData\\Roaming\\Necesse\\mods",
  "steamcmd_path": "C:\\SteamCMD\\steamcmd.exe",
  "steam_app_id": "1169040",
  "server_install_dir": "C:\\Necesse",
  "server_app_id": "1169370",
  "download_dir": "C:\\SteamCMD\\downloads",
  "temp_ids_file": "C:\\SteamCMD\\mod_ids.txt",
  "workshop_content_dir": "",
  "steam_web_api_key": "",
  "mod_id_overrides": {
    "ExampleModName": "2827931647"
  }
}
```

- Double-click `NecesseSAMU.exe` (or run with `--config <path>`).

## Requirements
- Windows with SteamCMD installed (e.g., `C:\\SteamCMD\\steamcmd.exe`).
- Necesse mods folder (e.g., `C:\\Users\\Administrator\\AppData\\Roaming\\Necesse\\mods`).
- Optional: Steam Web API key for name-to-ID lookups.

## Configuration
Edit `config.json`:

- `mods_dir`: Path to Necesse `mods` folder (where `modlist.data` lives).
- `steamcmd_path`: Path to `steamcmd.exe`.
- `steam_app_id`: App ID (Necesse = `1169040`).
- `server_install_dir`: Install location of your Necesse server (e.g., `C:\\Necesse`).
- `server_app_id`: App ID for the dedicated server (Necesse Dedicated = `1169370`).
- `download_dir`: Temporary download directory for SteamCMD.
- `temp_ids_file`: File where resolved IDs are written.
- `workshop_content_dir`: Optional; default is `<SteamCMD>\\steamapps\\workshop\\content\\1169040`.
- `steam_web_api_key`: Optional; for name search via Steam.
- `mod_id_overrides`: Map of mod name -> Workshop ID (fallback if `modlist.data` doesn't contain IDs).

Note: `modlist.data` may contain numeric IDs (e.g., `2827931647`) or human-readable names. For names, the tool uses overrides first, then the Steam Web API (if a key is set), and finally a best-effort workshop HTML search.

## Using the EXE
- Recommended: Use the prebuilt `NecesseSAMU.exe` from Releases and place `config.json` next to it (see above). Start by double-clicking.

## Build Locally (optional)
If you want to build yourself (requires Python + pip):

```
build.bat   (or)   ./build.ps1
```

## How It Works
- Reads `modlist.data` in `mods_dir`.
- Extracts numeric Workshop IDs; remaining entries are treated as names.
- Resolves names via `mod_id_overrides`, Steam Web API (optional), or HTML fallback.
- Runs SteamCMD with multiple `+workshop_download_item` commands.
- Finds `.jar` files in workshop downloads and copies them into the mods folder.
- Removes existing `.jar` files in the target folder (not `modlist.data`).

### Optional: Server Update
- After a successful mod update, the tool asks: "Update Necesse server now? [Y/N]".
- On confirmation, the following SteamCMD command runs:

```
steamcmd.exe +force_install_dir "C:\\Necesse" +login anonymous +app_update 1169370 validate +quit
```

- Requirement: `server_install_dir` (and optionally `server_app_id`) in `config.json`.

## Example SteamCMD Command (generated internally)

```
steamcmd.exe +force_install_dir "C:\\SteamCMD\\downloads" +login anonymous \
  +workshop_download_item 1169040 2827931647 \
  +workshop_download_item 1169040 3052859125 \
  +quit
```

## Notes
- Workshop content defaults to `<SteamCMD>\\steamapps\\workshop\\content\\1169040\\<ModID>`. The tool searches recursively for `.jar` files there.
- If you don't use the API, maintain `mod_id_overrides` or place numeric IDs directly in `modlist.data`.
- This repo includes `build.bat` and `build.ps1` for a one-click build.

### Custom EXE Icon
- Place an `icon.ico` next to the build scripts to embed it into the EXE.
- Alternatively, place an `icon.png` and the build will auto-convert it to `icon.ico` (uses Pillow) and embed it.
