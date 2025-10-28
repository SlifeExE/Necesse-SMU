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


def query_workshop_ids_by_name_without_key(appid: str, names: List[str]) -> List[str]:
    """
    Best-effort fallback without API key: searches the workshop website and
    extracts the first matching publishedfileid per name.
    """
    results: List[str] = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    def fetch(url: str) -> str:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.read().decode("utf-8", errors="ignore")

    id_patterns = [
        re.compile(r"data-publishedfileid=\"(\d+)\""),
        re.compile(r"/filedetails/\?id=(\d+)")
    ]

    for name in names:
        q = urllib.parse.quote_plus(name)
        url = (
            f"https://steamcommunity.com/workshop/browse/?appid={appid}"
            f"&searchtext={q}&browsesort=textsearch&section=readytouseitems&numperpage=10"
        )
        try:
            html = fetch(url)
            picked: Optional[str] = None
            for pat in id_patterns:
                m = pat.search(html)
                if m:
                    picked = m.group(1)
                    break
            if picked:
                results.append(picked)
        except Exception:
            # ignore and continue; this is best-effort
            pass
    return results
