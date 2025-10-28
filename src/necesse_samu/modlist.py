import os
import re
from typing import List, Tuple

from .steam_api import extract_numeric_ids


NAME_RE = re.compile(r"^\s*name\s*=\s*(?P<val>.+?)(?:,\s*)?$", re.IGNORECASE)


def _strip_quotes(s: str) -> str:
    s = s.strip()
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1].strip()
    return s


def read_modlist(mods_dir: str) -> Tuple[List[str], List[str]]:
    """
    Reads `modlist.data` and returns (ids, names).

    - ids: numeric Workshop IDs found directly in the file
    - names: values found after 'name = ...' (one per mod block)
    """
    path = os.path.join(mods_dir, "modlist.data")
    if not os.path.isfile(path):
        raise FileNotFoundError(f"modlist.data not found: {path}")

    ids: List[str] = []
    names: List[str] = []

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#") or line.startswith("//"):
                continue

            # Collect any numeric IDs present in the line (rare)
            ids.extend(extract_numeric_ids([line]))

            # Extract human-readable mod name after 'name ='
            m = NAME_RE.match(line)
            if m:
                val = _strip_quotes(m.group("val")).strip()
                if val:
                    names.append(val)

    # Dedupe while keeping order
    ids = list(dict.fromkeys(ids))
    names = list(dict.fromkeys(names))
    return ids, names
