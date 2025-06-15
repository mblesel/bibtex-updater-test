"""bibio/bib_updater.py"""
import logging
import requests
import bibtexparser

# Configuring logging
logging.basicConfig(
    filename="offline_mode.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s -\n%(message)s\n",
    level=logging.INFO
)


def fetch_dblp_entry(url: str) -> str | None:
    """Fetch a DBLP BibTeX entry and log problems if any occur."""
    bib_url = url.rstrip('/') + '/bibtex'
    try:
        response = requests.get(bib_url, timeout=10)
        if response.status_code == 200:
            return response.text
        else:
            msg = f"[WARNING] Error fetching {bib_url} - Status: {response.status_code}"
            print(msg)
            logging.warning(msg)
            if response.text:
                # limit to 500 characters
                logging.warning("Response content: %s", response.text[:500])
    except requests.exceptions.RequestException as e:
        msg = f"[ERROR] Exception fetching {bib_url}: {str(e)}"
        print(msg)
        logging.error(msg)
    return None


def parse_dblp_bibtex(raw_bibtex: str):
    """parse dblp bibtex"""
    parser = bibtexparser.bparser.BibTexParser(common_strings=True)
    return bibtexparser.loads(raw_bibtex, parser=parser).entries[0]
