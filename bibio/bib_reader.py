"""bibio/bib_reader.py"""
import bibtexparser

def load_bib_file(filepath: str):
    """Load bib file"""
    with open(filepath, encoding="utf-8") as bibtex_file:
        parser = bibtexparser.bparser.BibTexParser(common_strings=True)
        return bibtexparser.load(bibtex_file, parser=parser)
