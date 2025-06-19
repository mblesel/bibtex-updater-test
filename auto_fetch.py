"""auto_fetch.py — Automatically search DBLP with config-driven queries"""

import json, requests, time, re

CONFIG_FILE = "dblp_config.json"
DBLP_SEARCH_URL = "https://dblp.org/search/publ/api"
HEADERS = {"Accept": "application/x-bibtex"}
BIB_FILE = "references.bib"

def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config["queries"], config.get("max_results_per_query", 3)

def fetch_search_results(query, limit):
    params = {"q": query, "format": "json", "h": limit}
    r = requests.get(DBLP_SEARCH_URL, params=params, timeout=10)
    r.raise_for_status()

    hits = r.json()["result"]["hits"]
    results = hits.get("hit", [])
    if not results:
        print(f"⚠️ No results found for query: '{query}'")
    return results

def fetch_bibtex(entry_url, retries=2):
    for attempt in range(retries):
        try:
            r = requests.get(entry_url, headers=HEADERS, timeout=10)
            if r.status_code == 200:
                return r.text.strip()
        except Exception:
            time.sleep(1)
    return None

def get_existing_keys():
    try:
        with open(BIB_FILE, "r", encoding="utf-8") as f:
            return set(re.findall(r"@\w+\{([^,]+),", f.read()))
    except FileNotFoundError:
        return set()

def append_entry(bibtex):
    key_match = re.match(r"@\w+\{([^,]+),", bibtex)
    new_key = key_match.group(1) if key_match else None
    if not new_key:
        return False
    if new_key in get_existing_keys():
        print(f"⚠️  Skipped duplicate: {new_key}")
        return False
    with open(BIB_FILE, "a", encoding="utf-8") as f:
        f.write("\n\n" + bibtex)
    print(f"✅ Added: {new_key}")
    return True

def main():
    queries, limit = load_config()
    print(f"🔁 Running auto-fetch for {len(queries)} queries...")

    total_added = 0
    for q in queries:
        print(f"\n🔍 Searching: '{q}'")
        try:
            results = fetch_search_results(q, limit)
        except Exception as e:
            print(f"❌ Failed to fetch results for '{q}': {e}")
            continue

        for hit in results:
            info = hit["info"]
            dblp_url = f"https://dblp.org/rec/{info['key']}"
            bibtex = fetch_bibtex(dblp_url)
            if bibtex and append_entry(bibtex):
                total_added += 1
            time.sleep(1.2)

    print(f"\n🎯 Auto-fetch complete. {total_added} new entries added.")

if __name__ == "__main__":
    main()
