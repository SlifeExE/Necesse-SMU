import os
import shlex
import subprocess
from typing import Iterable, List


def build_steamcmd_command(steamcmd_path: str, force_install_dir: str, ids: Iterable[str], appid: str) -> List[str]:
    # Build command as separate args to avoid quoting issues
    parts: List[str] = []
    parts += ["+force_install_dir", force_install_dir]
    parts += ["+login", "anonymous"]
    for mid in ids:
        parts += ["+workshop_download_item", appid, str(mid)]
    parts += ["+quit"]
    return [steamcmd_path] + parts


def run_steamcmd(cmd: List[str]) -> int:
    # Ensure install dir exists
    try:
        # Create force_install_dir if present
        if "+force_install_dir" in cmd:
            idx = cmd.index("+force_install_dir")
            if idx + 1 < len(cmd):
                dir_path = cmd[idx + 1]
                if dir_path and not os.path.isdir(dir_path):
                    os.makedirs(dir_path, exist_ok=True)
    except Exception:
        pass

    # Run process
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    # Stream output
    if proc.stdout:
        for line in proc.stdout:
            print(line.rstrip())
    return proc.wait()
