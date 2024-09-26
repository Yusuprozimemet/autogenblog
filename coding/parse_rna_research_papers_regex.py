# filename: parse_rna_research_papers_regex.py
import re

# Sample HTML data should be the output you obtained earlier.
html_content = """<PASTE_HTML_HERE>"""

def extract_paper_details(html):
    papers = []
    
    # Regular expressions to find information
    titles = re.findall(r'<a class="docsum-title" href=".*?">(.*?)</a>', html)
    authors = re.findall(r'<span class="docsum-authors full-authors">(.*?)</span>', html)
    journals = re.findall(r'<span class="docsum-journal-citation full-journal-citation">(.*?)</span>', html)
    pmids = re.findall(r'PMID: <span class="docsum-pmid">(.*?)</span>', html)
    
    # Combine extracted data into a list of dictionaries
    for i in range(len(titles)):
        papers.append({
            'title': titles[i],
            'authors': authors[i],
            'journal': journals[i],
            'pmid': pmids[i]
        })

    return papers

# Extract the papers
rna_papers_data = extract_paper_details(html_content)
for paper in rna_papers_data:
    print(paper)