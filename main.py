"""main.py"""
import time
import os
import logging
from bibio import (
    load_bib_file, save_bib_file,
    fetch_dblp_entry, parse_dblp_bibtex,
    lint_entry, is_dblp_entry, entries_differ
)

# Configure logging for offline mode
logging.basicConfig(
    filename="offline_mode.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def main():
    """main function"""
    start_time = time.time()
    logging.info("=" * 60)
    logging.info("=== BibTeX Updater started ===")
    offline_mode = os.getenv("BIBTEX_OFFLINE", "false").lower() == "true"

    db = load_bib_file('references.bib')
    updated = False
    failed_entries = []
    linted_entries = []

    for entry in db.entries:
        if is_dblp_entry(entry):
            if offline_mode:
                entry_id = entry.get('ID', 'UNKNOWN_ID')
                print(f"[OFFLINE] Skipping DBLP fetch for entry: {entry_id}")
                logging.info("[OFFLINE] Skipping DBLP fetch for entry: %s", entry_id)
                continue
            new_raw = fetch_dblp_entry(entry['url'])
            if new_raw is None:
                failed_entries.append(entry.get('ID', 'UNKNOWN_ID'))
                continue
            new_entry = parse_dblp_bibtex(new_raw)
            if entries_differ(entry, new_entry):
                entry.update(new_entry)
                updated = True
                logging.info("Updated DBLP entry: %s", entry.get('ID', 'UNKNOWN_ID'))
        else:
            linted = lint_entry(entry)
            if entries_differ(entry, linted):
                entry.update(linted)
                updated = True
                logging.info("Linted non-DBLP entry: %s", entry.get('ID', 'UNKNOWN_ID'))
                linted_entries.append(entry.get('ID', 'UNKNOWN_ID'))

    if updated:
        save_bib_file(db, 'references.bib')
        print("✅ Updated .bib file written.")
        if offline_mode:
            logging.info("references.bib updated in offline mode.")
    else:
        print("ℹ️  No updates needed.")

    if failed_entries:
        print(f"⚠️  Could not fetch {len(failed_entries)} entries from DBLP:")
        for entry_id in failed_entries:
            print(f"   - {entry_id}")

    if offline_mode and linted_entries:
        logging.info("Linted entries in offline mode:")
        for entry_id in linted_entries:
            logging.info("   - %s", entry_id)

    if updated:
        logging.info("Total entries updated: %d",
                    len(linted_entries) + len([e for e in db.entries if is_dblp_entry(e)]))
    else:
        logging.info("No entries updated.")

    elapsed = time.time() - start_time
    logging.info("Execution time: %.2f seconds", elapsed)
    logging.info("=== BibTeX Updater finished ===")
    logging.info("=" * 60)

if __name__ == "__main__":
    main()
