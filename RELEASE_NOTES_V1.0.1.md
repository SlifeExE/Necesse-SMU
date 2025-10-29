# Necesse SAMU – Release Notes 1.0.1

Bug fixes
- Fixed EXE icon using an outdated PNG:
  - Build now prefers `icon.png` and regenerates `icon.ico` each time.
  - Cleans old PyInstaller spec/build (`--clean`, remove `.spec` and `build/`).
- Fixed PyInstaller build issues:
  - Installs requirements automatically and invokes `py -m PyInstaller`.
  - Added a proper entry (`samu_entry.py`) and improved frozen config path detection.
- Fixed mods not copied after download when using `+force_install_dir`:
  - Now searches both default workshop content and `<download_dir>\steamapps\workshop\content\<appid>`.
  - Prints checked paths when no `.jar` files are found.
- Fixed duplicate versioned `.jar` files in mods directory:
  - Added post-copy cleanup to keep only the most recent file per mod prefix (e.g., `RPGMod-...`).
- Improved `modlist.data` parsing:
  - Correctly extracts names from `name = ...` lines; better handling of mixed content.

