"""bibio/bib_linter.py"""

def lint_entry(entry: dict) -> dict:
    """lint entry"""
    preferred_order = ['author', 'title', 'journal', 'booktitle',
                        'year', 'volume', 'number', 'pages', 'doi', 'url']
    linted = {k: entry[k] for k in preferred_order if k in entry}
    for key in sorted(entry):
        if key not in linted:
            linted[key] = entry[key]
    return linted
