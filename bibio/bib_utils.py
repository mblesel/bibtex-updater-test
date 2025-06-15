"""bibio/bib_utils.py"""
def is_dblp_entry(entry: dict) -> bool:
    """dblp entry"""
    return 'url' in entry and 'dblp.org' in entry['url']

def entries_differ(e1: dict, e2: dict) -> bool:
    """entries differ"""
    keys = set(e1.keys()) | set(e2.keys())
    return any(e1.get(k, '').strip() != e2.get(k, '').strip() for k in keys)
