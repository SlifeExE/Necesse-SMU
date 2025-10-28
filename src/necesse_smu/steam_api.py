import json
import re
import urllib.parse
import urllib.request
from typing import Iterable, List, Optional


WORKSHOP_QUERY_URL = "https://api.steampowered.com/IPublishedFileService/QueryFiles/v1/"


def extract_numeric_ids(tokens: Iterable[str]) -> List[str]:
    ids = []
    for t in tokens:
        for m in re.finditer(r"\b(\d{6,})\b", t):
            ids.append(m.group(1))
    return list(dict.fromkeys(ids))  # dedupe, keep order


def query_workshop_ids_by_name(api_key: str, appid: str, names: List[str]) -> List[str]:
    # This is a best-effort name search using the workshop query endpoint.
    # For each name, we query and take the top result if it matches reasonably.
    results: List[str] = []
    for name in names:
        params = {
            "key": api_key,
            "appid": appid,
            "return_short_description": 0,
            "query_type": 12,  # RankedByTextSearch
            "numperpage": 5,
            "search_text": name,
        }
        data = urllib.parse.urlencode(params).encode()
        req = urllib.request.Request(WORKSHOP_QUERY_URL, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=20) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        items = payload.get("response", {}).get("publishedfiledetails", []) or payload.get("response", {}).get("matches", [])
        # Normalize possible shapes
        if not items:
            items = payload.get("response", {}).get("publishedfiledetails", [])
        picked: Optional[str] = None
        for it in items:
            title = (it.get("title") or "").lower()
            if name.lower() in title:
                picked = str(it.get("publishedfileid"))
                break
        if not picked and items:
            picked = str(items[0].get("publishedfileid"))
        if picked:
            results.append(picked)
    return results

