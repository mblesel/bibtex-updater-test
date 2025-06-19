"""search_and_add.py - Search DBLP and add BibTeX entries to references.bib"""

import requests
import time

DBLP_SEARCH_URL = "https://dblp.org/search/publ/api"
HEADERS = {"Accept": "application/x-bibtex"}
BIB_FILE = "references.bib"

def search_dblp(query, max_results=10):
    """Search DBLP and return a list of hits (may be empty)"""
    params = {
        "q": query,
        "h": max_results,
        "format": "json"
    }
    response = requests.get(DBLP_SEARCH_URL, params=params, timeout=10)
    response.raise_for_status()
    hits = response.json()["result"]["hits"]
    return hits.get("hit", [])  # Return empty list if 'hit' key is missing

def display_results(results):
    for idx, hit in enumerate(results):
        info = hit["info"]
        title = info.get("title", "No title")
        authors_raw = info.get("authors", {}).get("author", [])
        
        # Normalize authors
        if isinstance(authors_raw, dict):
            authors = authors_raw.get("text", "Unknown")
        elif isinstance(authors_raw, list):
            authors = ", ".join(
                a["text"] if isinstance(a, dict) else str(a) for a in authors_raw
            )
        else:
            authors = str(authors_raw)

        year = info.get("year", "N/A")
        print(f"[{idx}] {title}\n     🧑 {authors}\n     📅 {year}\n")


def fetch_bibtex(entry_url, retries=2):
    for attempt in range(retries):
        try:
            response = requests.get(entry_url, headers=HEADERS, timeout=10)
            if response.status_code == 200:
                return response.text.strip()
            else:
                raise Exception(f"Status code: {response.status_code}")
        except Exception as e:
            print(f"⚠️ Attempt {attempt+1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(1)
            else:
                raise

def append_to_bib(bibtex_entry):
    try:
        with open(BIB_FILE, "r", encoding="utf-8") as f:
            existing = f.read()
    except FileNotFoundError:
        existing = ""

    # Extract the BibTeX key from the new entry
    import re
    match = re.match(r"@\w+\{([^,]+),", bibtex_entry)
    new_key = match.group(1) if match else None

    if new_key and new_key in existing:
        print(f"⚠️ Entry '{new_key}' already exists in references.bib. Skipped.")
        return

    with open(BIB_FILE, "a", encoding="utf-8") as f:
        f.write("\n\n" + bibtex_entry)
    print(f"✅ Entry '{new_key}' added to references.bib.")

def main():
    query = input("Enter your search query (e.g., 'python numerical methods'): ")
    results = search_dblp(query)

    if not results:
        print("⚠️  No results found. Try a different query.")
        return

    display_results(results)

    selection = input("Enter the numbers of the entries you want to add (comma-separated): ")
    try:
        indexes = [int(i.strip()) for i in selection.split(",")]
    except ValueError:
        print("❌ Invalid input. Please enter numbers separated by commas.")
        return

    for idx in indexes:
        try:
            info = results[idx]["info"]
            dblp_url = "https://dblp.org/rec/" + info["key"]
            print(f"\n⏳ Fetching BibTeX for: {info['title']}")
            bibtex = fetch_bibtex(dblp_url)
            append_to_bib(bibtex)
            time.sleep(1)  # gentle delay
        except Exception as e:
            print(f"⚠️ Failed to fetch/add entry {idx}: {e}")

if __name__ == "__main__":
    main()
