import os
import shutil
from typing import Iterable, List, Tuple

from .config import Config
from .modlist import read_modlist
from .steam_api import query_workshop_ids_by_name, query_workshop_ids_by_name_without_key
from .steamcmd import build_steamcmd_command, run_steamcmd


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
                print(f"Warnung: Steam API Abfrage fehlgeschlagen: {e}")
        # Fallback ohne API-Key (oder falls API nichts liefert)
        try:
            unresolved = [n for n in names]
            found_html = query_workshop_ids_by_name_without_key(cfg.steam_app_id, unresolved)
            ids.extend(found_html)
        except Exception as e:
            print(f"Warnung: Fallback-Suche ohne API fehlgeschlagen: {e}")

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
        print("Keine Mod-IDs zum Download gefunden.")
        return 0
    force_dir = cfg.resolve_download_dir()
    cmd = build_steamcmd_command(cfg.steamcmd_path, force_dir, ids, cfg.steam_app_id)
    print("Starte SteamCMD Download...")
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
                print(f"Konnte alte Datei nicht löschen: {p} - {e}")


def copy_jars_to_mods(mods_dir: str, jar_paths: Iterable[str]) -> List[str]:
    os.makedirs(mods_dir, exist_ok=True)
    copied: List[str] = []
    for jar in jar_paths:
        try:
            dest = os.path.join(mods_dir, os.path.basename(jar))
            shutil.copy2(jar, dest)
            copied.append(dest)
        except Exception as e:
            print(f"Konnte Jar nicht kopieren: {jar} - {e}")
    return copied


def run_update(cfg: Config) -> int:
    print(f"Mods-Verzeichnis: {cfg.mods_dir}")
    print(f"SteamCMD: {cfg.steamcmd_path}")
    ids, unresolved = resolve_mod_ids(cfg)
    if unresolved:
        print("Nicht aufgelöste Namen in modlist.data:")
        for n in unresolved:
            print(f"  - {n}")
        print("Hinweis: Fügen Sie 'mod_id_overrides' in der config hinzu oder setzen Sie 'steam_web_api_key' für automatische Suche.")
        try:
            # Print a small JSON skeleton to help filling overrides quickly
            import json
            skeleton = {name: "<WORKSHOP_ID>" for name in unresolved}
            print("Vorschlag für config.json -> mod_id_overrides:")
            print(json.dumps(skeleton, ensure_ascii=False, indent=2))
        except Exception:
            pass

    if not ids:
        print("Keine Mod-IDs ermittelt. Abbruch.")
        return 1

    write_ids_temp(cfg.resolve_temp_ids_file(), ids)
    code = download_mods(cfg, ids)
    if code != 0:
        print(f"SteamCMD Rückgabecode: {code}")
        # Continue to jar copy attempt; sometimes steamcmd returns nonzero even with partial success

    jars = find_downloaded_jar_paths(cfg, ids)
    if not jars:
        print("Keine .jar Dateien in Downloads gefunden.")
        return 2

    clear_old_jars(cfg.mods_dir)
    copied = copy_jars_to_mods(cfg.mods_dir, jars)
    print(f"Kopiert: {len(copied)} JARs")
    return 0
