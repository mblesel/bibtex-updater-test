-BibTeX Auto Updater

A simple Python tool that automatically fetches recent DBLP publications from specified authors and appends them to a references.bib file. Designed to reduce manual BibTeX updates when writing scientific reports or theses.

- Project Structure

author_auto_fetch.py – Main script to fetch and append BibTeX entries.

dblp_config.json – Configuration file for author names, year range, and max results.

references.bib – BibTeX output file where new entries are saved.

.github/workflows/bibtex-updater.yml – GitHub Actions workflow for automation.

- Requirements

Python 3.9+

requests library (install with pip install requests)

- Configuration

Edit the dblp_config.json file to include the authors you want to track and the filters you want to apply:

{
  "authors": ["Fatima Zahra Beni Azza", "Jane Doe"],
  "max_results_per_author": 10,
  "year_min": 2019,
  "year_max": 2025
}

- Usage

Once your config is ready, run:

python author_auto_fetch.py


This will:

Query DBLP using author:"<Full Name>"

Fetch up to the configured number of results

Filter them based on the year range

Append new BibTeX entries to references.bib (skipping duplicates)

GitHub Actions Automation

You can automate the fetch process using the provided GitHub Actions workflow:

.github/workflows/bibtex-updater.yml


This workflow:

Runs author_auto_fetch.py on a schedule or push

Keeps your BibTeX file up-to-date automatically

To enable it:

Push your project to a public GitHub repository

Activate GitHub Actions from the "Actions" tab

- License

This project is licensed under the GNU GPLv3 to ensure that improvements stay open and publicly available.

- References

DBLP. (n.d.). How to use the DBLP search API?
https://dblp.org/faq/How+to+use+the+dblp+search+API.html

Python Software Foundation. (n.d.). requests library.
https://docs.python-requests.org/

Python Software Foundation. (n.d.). bibtexparser documentation.
https://bibtexparser.readthedocs.io/
