# author_auto_fetch.py — Auto-fetch DBLP entries by author names (from dblp_config.json)

import json, requests, time, re
from typing import Iterable

CONFIG_FILE = "dblp_config.json"
DBLP_SEARCH_URL = "https://dblp.org/search/publ/api"
HEADERS = {"Accept": "application/x-bibtex"}
BIB_FILE = "references.bib"
TIMEOUT = 10

def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    authors = cfg.get("authors", [])
    max_per_author = cfg.get("max_results_per_author", 10)
    y_min = cfg.get("year_min")
    y_max = cfg.get("year_max")
    return authors, max_per_author, y_min, y_max

def year_in_range(year_str: str, y_min: int | None, y_max: int | None) -> bool:
    if not year_str or not year_str.isdigit():
        return True  # keep if unknown
    y = int(year_str)
    if y_min is not None and y < y_min:
        return False
    if y_max is not None and y > y_max:
        return False
    return True

def fetch_search_results_by_author(author: str, limit: int) -> list[dict]:
    params = {"q": f'author:"{author}"', "format": "json", "h": limit}
    r = requests.get(DBLP_SEARCH_URL, params=params, timeout=TIMEOUT)
    r.raise_for_status()
    hits = r.json()["result"]["hits"]
    return hits.get("hit", [])

def fetch_bibtex(entry_url: str, retries: int = 2) -> str | None:
    for attempt in range(retries):
        try:
            r = requests.get(entry_url, headers=HEADERS, timeout=TIMEOUT)
            if r.status_code == 200:
                return r.text.strip()
        except Exception:
            time.sleep(1)
    return None

def get_existing_keys() -> set[str]:
    try:
        with open(BIB_FILE, "r", encoding="utf-8") as f:
            return set(re.findall(r"@\w+\{([^,]+),", f.read()))
    except FileNotFoundError:
        return set()

def append_entry(bibtex: str) -> bool:
    key_match = re.match(r"@\w+\{([^,]+),", bibtex)
    new_key = key_match.group(1) if key_match else None
    if not new_key:
        return False
    if new_key in get_existing_keys():
        print(f"Skipped duplicate: {new_key}")
        return False
    with open(BIB_FILE, "a", encoding="utf-8") as f:
        f.write("\n\n" + bibtex)
    print(f"Added: {new_key}")
    return True

def iter_hits_filtered(hits: Iterable[dict], y_min, y_max):
    for hit in hits:
        info = hit.get("info", {})
        year = info.get("year", "")
        if year_in_range(year, y_min, y_max):
            yield hit

def main():
    authors, limit, y_min, y_max = load_config()
    if not authors:
        print("No authors configured in dblp_config.json -> 'authors'. Nothing to do.")
        return

    print(f"Running author auto-fetch for {len(authors)} author(s)...")
    total_added = 0

    for author in authors:
        print(f"\nAuthor: {author}")
        try:
            hits = fetch_search_results_by_author(author, limit)
        except Exception as e:
            print(f"Failed to fetch results for '{author}': {e}")
            continue

        count_this_author = 0
        for hit in iter_hits_filtered(hits, y_min, y_max):
            info = hit.get("info", {})
            key = info.get("key")
            if not key:
                continue
            dblp_url = f"https://dblp.org/rec/{key}"
            bibtex = fetch_bibtex(dblp_url)
            if bibtex and append_entry(bibtex):
                total_added += 1
                count_this_author += 1
            time.sleep(1.0)  # be polite to DBLP

        print(f"Added for {author}: {count_this_author}")

    print(f"\nAuthor auto-fetch complete. {total_added} new entries added.")

if __name__ == "__main__":
    main()

