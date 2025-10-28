# Necesse SAMU v1.0 Release Notes

## Highlights
- **Automated mod syncing** powered by SteamCMD. The tool reads `modlist.data`, resolves Workshop IDs, downloads the latest `.jar` files, and replaces outdated copies in your Necesse server mods folder.
- **Flexible ID resolution** that supports direct IDs, configurable overrides, and optional Steam Web API lookups with an HTML fallback when names are provided.
- **Integrated server upkeep** with a post-update prompt that can run the dedicated server `app_update` command so your Necesse installation stays current.
- **One-click usage** via the prebuilt `NecesseSAMU.exe`, backed by a simple `config.json` that describes your SteamCMD paths, download locations, and overrides.

## Getting Started
1. Download the prebuilt `NecesseSAMU.exe` from the Releases page and place it next to your customized `config.json`.
2. Fill in required paths such as `mods_dir`, `steamcmd_path`, `server_install_dir`, and `download_dir`, plus any optional overrides or Steam Web API key.
3. Double-click the executable (or run it with `--config <path>`) to synchronize workshop mods and optionally trigger the dedicated server update.

## Build & Customization
- Build the executable yourself with `build.bat` or `./build.ps1` if you prefer local builds or custom icons.
- Drop an `icon.ico` (or `icon.png` for auto-conversion) alongside the build scripts to embed it in the final executable.

Enjoy streamlined mod and server management with Necesse SAMU v1.0!
