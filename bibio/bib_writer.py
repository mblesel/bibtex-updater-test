"""bibio/bib_writer.py"""
from bibtexparser.bwriter import BibTexWriter

def save_bib_file(db, filepath: str):
    """save bib file"""
    writer = BibTexWriter()
    writer.indent = '    '
    writer.order_entries_by = ('ID',)
    with open(filepath, 'w', encoding='utf-8') as bibfile:
        bibfile.write(writer.write(db))
