import os
from typing import List, Tuple

from .steam_api import extract_numeric_ids


def read_modlist(mods_dir: str) -> Tuple[List[str], List[str]]:
    """
    Reads `modlist.data` from the given mods directory and returns a tuple:
    (ids, names_or_tokens)

    - ids: list of numeric IDs found directly in the file
    - names_or_tokens: leftover tokens (likely names) to be resolved via API or overrides
    """
    path = os.path.join(mods_dir, "modlist.data")
    if not os.path.isfile(path):
        raise FileNotFoundError(f"modlist.data nicht gefunden: {path}")

    ids: List[str] = []
    names: List[str] = []

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#") or line.startswith("//"):
                continue
            # Split on common separators
            tokens = [t.strip() for t in [line] if t]
            numeric = extract_numeric_ids(tokens)
            if numeric:
                ids.extend(numeric)
            else:
                names.extend(tokens)

    # Dedupe while keeping order
    ids = list(dict.fromkeys(ids))
    names = list(dict.fromkeys(names))
    return ids, names

