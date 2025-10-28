import os
import shutil
from typing import Iterable, List, Tuple

from .config import Config
from .modlist import read_modlist
from .steam_api import query_workshop_ids_by_name, query_workshop_ids_by_name_without_key
from .steamcmd import build_steamcmd_command, run_steamcmd, build_app_update_command


def resolve_mod_ids(cfg: Config) -> Tuple[List[str], List[str]]:
    ids, names = read_modlist(cfg.mods_dir)

    # Apply overrides first
    if cfg.mod_id_overrides:
        mapped = []
        remaining = []
        for name in names:
            if name in cfg.mod_id_overrides:
                mapped.append(str(cfg.mod_id_overrides[name]))
            else:
                remaining.append(name)
        ids.extend(mapped)
        names = remaining

    # Resolve via API or fallback HTML search
    if names:
        if cfg.steam_web_api_key:
            try:
                found = query_workshop_ids_by_name(cfg.steam_web_api_key, cfg.steam_app_id, names)
                ids.extend(found)
            except Exception as e:
                print(f"Warning: Steam API request failed: {e}")
        # Fallback without API key (or if API returns nothing)
        try:
            unresolved = [n for n in names]
            found_html = query_workshop_ids_by_name_without_key(cfg.steam_app_id, unresolved)
            ids.extend(found_html)
        except Exception as e:
            print(f"Warning: Fallback search without API failed: {e}")

    # Dedupe while keeping order
    ids = list(dict.fromkeys([str(i) for i in ids]))
    return ids, names


def write_ids_temp(path: str, ids: Iterable[str]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for mid in ids:
            f.write(str(mid) + "\n")


def download_mods(cfg: Config, ids: List[str]) -> int:
    if not ids:
        print("No mod IDs to download.")
        return 0
    force_dir = cfg.resolve_download_dir()
    cmd = build_steamcmd_command(cfg.steamcmd_path, force_dir, ids, cfg.steam_app_id)
    print("Starting SteamCMD download...")
    return run_steamcmd(cmd)


def find_downloaded_jar_paths(cfg: Config, ids: Iterable[str]) -> List[str]:
    base = cfg.resolve_workshop_content_dir()
    jars: List[str] = []
    for mid in ids:
        mod_dir = os.path.join(base, str(mid))
        if not os.path.isdir(mod_dir):
            continue
        for root, _dirs, files in os.walk(mod_dir):
            for fn in files:
                if fn.lower().endswith('.jar'):
                    jars.append(os.path.join(root, fn))
    return jars


def clear_old_jars(mods_dir: str) -> None:
    if not os.path.isdir(mods_dir):
        return
    for fn in os.listdir(mods_dir):
        p = os.path.join(mods_dir, fn)
        if os.path.isfile(p) and fn.lower().endswith('.jar') and fn.lower() != 'modlist.data':
            try:
                os.remove(p)
            except Exception as e:
                print(f"Failed to delete old file: {p} - {e}")


def copy_jars_to_mods(mods_dir: str, jar_paths: Iterable[str]) -> List[str]:
    os.makedirs(mods_dir, exist_ok=True)
    copied: List[str] = []
    for jar in jar_paths:
        try:
            dest = os.path.join(mods_dir, os.path.basename(jar))
            shutil.copy2(jar, dest)
            copied.append(dest)
        except Exception as e:
            print(f"Failed to copy jar: {jar} - {e}")
    return copied


def run_update(cfg: Config) -> int:
    print(f"Mods directory: {cfg.mods_dir}")
    print(f"SteamCMD: {cfg.steamcmd_path}")
    ids, unresolved = resolve_mod_ids(cfg)
    if unresolved:
        print("Unresolved names in modlist.data:")
        for n in unresolved:
            print(f"  - {n}")
        print("Hint: Add 'mod_id_overrides' in config or set 'steam_web_api_key' for automatic lookup.")
        try:
            # Print a small JSON skeleton to help filling overrides quickly
            import json
            skeleton = {name: "<WORKSHOP_ID>" for name in unresolved}
            print("Suggestion for config.json -> mod_id_overrides:")
            print(json.dumps(skeleton, ensure_ascii=False, indent=2))
        except Exception:
            pass

    if not ids:
        print("No workshop IDs resolved. Aborting.")
        return 1

    write_ids_temp(cfg.resolve_temp_ids_file(), ids)
    code = download_mods(cfg, ids)
    if code != 0:
        print(f"SteamCMD exit code: {code}")
        # Continue to jar copy attempt; sometimes steamcmd returns nonzero even with partial success

    jars = find_downloaded_jar_paths(cfg, ids)
    if not jars:
        print("No .jar files found in downloads.")
        return 2

    clear_old_jars(cfg.mods_dir)
    copied = copy_jars_to_mods(cfg.mods_dir, jars)
    print(f"Copied: {len(copied)} jars")

    # Optional: Ask for server update
    ask_and_update_server(cfg)
    return 0


def ask_and_update_server(cfg: Config) -> None:
    try:
        import colorama
        from colorama import Fore, Style
        colorama.init(autoreset=True)
    except Exception:
        class Fore:  # type: ignore
            CYAN = GREEN = YELLOW = RED = ""
        class Style:  # type: ignore
            BRIGHT = NORMAL = ""

    if not cfg.server_install_dir:
        print("Note: 'server_install_dir' is not set. Skipping server update.")
        return

    print("")
    print(Fore.CYAN + Style.BRIGHT + "Update Necesse server now? [Y/N]")
    ans = input(Fore.YELLOW + "> ").strip().lower()
    if ans not in ("y", "yes"):
        print("Server update skipped.")
        return

    cmd = build_app_update_command(cfg.steamcmd_path, cfg.server_install_dir, cfg.server_app_id)
    print(Fore.GREEN + "Starting server update via SteamCMD:")
    print(" ".join(cmd))
    code = run_steamcmd(cmd)
    if code == 0:
        print(Fore.GREEN + "Server update completed successfully.")
    else:
        print(Fore.RED + f"Server update failed (exit {code}).")
