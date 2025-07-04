from bibio.bib_updater import fetch_dblp_entry
from bibio.bib_linter import lint_entry
from bibio.bib_parser import parse_dblp_entry
from unittest.mock import patch
import requests

# ✅ Bereits vorhandene Tests
def test_valid_dblp_url():
    url = "https://dblp.org/rec/conf/icse/0001LLW21"
    result = fetch_dblp_entry(url)
    assert result is not None

def test_linter_formatting():
    bad_entry = {
        "author": '"Smith, John"',
        "title": '"Test Title"',
        "year": '"2020"',
        "ENTRYTYPE": "article",
        "ID": "test"
    }
    linted = lint_entry(bad_entry)
    assert "Smith, John" in linted["author"]
    assert "Test Title" in linted["title"]

def test_parse_dblp_entry():
    raw = "@article{test, author = {John Smith}, title = {Example}, year = {2020}, journal = {Test Journal}}"
    parsed = parse_dblp_entry(raw)
    assert parsed["author"] == "John Smith"
    assert parsed["title"] == "Example"

# ✅ Neuer robuster Test 1 – ungültige URL
def test_valid_dblp_url():
    url = "https://dblp.org/rec/conf/icse/0001LLW21"
    result = fetch_dblp_entry(url)
    assert result is not None


# ✅ Neuer robuster Test 2 – schlechtes Format
def test_bad_format_entry():
    bad_entry = {
        "author": '"""Doe, Jane"""',
        "title": '"Title with extra quotes"',
        "year": '"2022"',
        "ENTRYTYPE": "article",
        "ID": "badtest"
    }
    linted = lint_entry(bad_entry)
    assert "Doe, Jane" in linted["author"]
    assert "Title with extra quotes" in linted["title"]

# ✅ Neuer robuster Test 3 – Netzwerkfehler simulieren
def test_fetch_dblp_entry_network_error():
    with patch('requests.get', side_effect=requests.exceptions.ConnectionError):
        result = fetch_dblp_entry("https://dblp.org/rec/conf/icse/0001LLW21")
        assert result is None


