# filename: parse_rna_research_papers.py
from bs4 import BeautifulSoup

# Sample HTML data should be the output you obtained earlier.
html_content = """<PASTE_HTML_HERE>"""

def extract_paper_details(html):
    soup = BeautifulSoup(html, 'html.parser')
    papers = []

    for item in soup.find_all('article'):
        title = item.find('a', class_='docsum-title').text.strip()
        authors = item.find('span', class_='docsum-authors full-authors').text.strip()
        journal = item.find('span', class_='docsum-journal-citation full-journal-citation').text.strip()
        pmid = item.find('span', class_='docsum-pmid').text.strip()

        papers.append({
            'title': title,
            'authors': authors,
            'journal': journal,
            'pmid': pmid
        })

    return papers

# Extract the papers
rna_papers_data = extract_paper_details(html_content)
for paper in rna_papers_data:
    print(paper)