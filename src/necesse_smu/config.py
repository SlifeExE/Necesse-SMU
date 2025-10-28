import json
import os
import sys
from dataclasses import dataclass
from typing import Dict, Optional


DEFAULT_CONFIG_FILENAME = "config.json"


@dataclass
class Config:
    mods_dir: str
    steamcmd_path: str
    steam_app_id: str = "1169040"
    download_dir: Optional[str] = None
    temp_ids_file: Optional[str] = None
    workshop_content_dir: Optional[str] = None
    steam_web_api_key: Optional[str] = None
    mod_id_overrides: Optional[Dict[str, str]] = None

    @property
    def steamcmd_dir(self) -> str:
        return os.path.dirname(os.path.abspath(self.steamcmd_path))

    def resolve_workshop_content_dir(self) -> str:
        if self.workshop_content_dir:
            return self.workshop_content_dir
        # Default SteamCMD workshop content location
        return os.path.join(self.steamcmd_dir, "steamapps", "workshop", "content", self.steam_app_id)

    def resolve_download_dir(self) -> str:
        if self.download_dir:
            return self.download_dir
        # Fallback to a temp folder inside steamcmd dir
        return os.path.join(self.steamcmd_dir, "downloads")

    def resolve_temp_ids_file(self) -> str:
        if self.temp_ids_file:
            return self.temp_ids_file
        return os.path.join(self.steamcmd_dir, "mod_ids.txt")


def find_config_path() -> str:
    # Prefer config in the directory of the executable/script
    base_dir = os.path.dirname(os.path.abspath(getattr(sys.modules.get("__main__"), "__file__", os.getcwd())))
    candidate = os.path.join(base_dir, DEFAULT_CONFIG_FILENAME)
    if os.path.isfile(candidate):
        return candidate
    # Fallback to CWD
    candidate = os.path.join(os.getcwd(), DEFAULT_CONFIG_FILENAME)
    return candidate


def load_config(path: Optional[str] = None) -> Config:
    cfg_path = path or find_config_path()
    if not os.path.isfile(cfg_path):
        raise FileNotFoundError(f"Config not found at {cfg_path}")
    with open(cfg_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Normalize paths
    mods_dir = os.path.expandvars(os.path.expanduser(data.get("mods_dir", "")))
    steamcmd_path = os.path.expandvars(os.path.expanduser(data.get("steamcmd_path", "")))

    return Config(
        mods_dir=mods_dir,
        steamcmd_path=steamcmd_path,
        steam_app_id=str(data.get("steam_app_id", "1169040")),
        download_dir=os.path.expandvars(os.path.expanduser(data.get("download_dir"))) if data.get("download_dir") else None,
        temp_ids_file=os.path.expandvars(os.path.expanduser(data.get("temp_ids_file"))) if data.get("temp_ids_file") else None,
        workshop_content_dir=os.path.expandvars(os.path.expanduser(data.get("workshop_content_dir"))) if data.get("workshop_content_dir") else None,
        steam_web_api_key=data.get("steam_web_api_key"),
        mod_id_overrides=data.get("mod_id_overrides", {}),
    )
