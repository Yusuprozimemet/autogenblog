# filename: parse_rna_research_papers_adjusted.py
import re

# Sample HTML data should be the output you obtained earlier.
html_content = """<PASTE_HTML_HERE>"""

def extract_paper_details(html):
    papers = []
    
    # Adjusted regular expressions to find information
    titles = re.findall(r'<a class="docsum-title".*?>(.*?)<\/a>', html, re.DOTALL)
    authors = re.findall(r'<span class="docsum-authors full-authors">(.*?)<\/span>', html, re.DOTALL)
    journals = re.findall(r'<span class="docsum-journal-citation.*?>(.*?)<\/span>', html, re.DOTALL)
    pmids = re.findall(r'PMID: <span class="docsum-pmid">(.*?)<\/span>', html, re.DOTALL)
    
    # Debugging outputs
    print("Titles:", titles)
    print("Authors:", authors)
    print("Journals:", journals)
    print("PMIDs:", pmids)
    
    # Combine the extracted data into a list of dictionaries
    for i in range(len(titles)):
        papers.append({
            'title': titles[i].strip(),
            'authors': authors[i].strip(),
            'journal': journals[i].strip(),
            'pmid': pmids[i].strip()
        })

    return papers

# Extract the papers
rna_papers_data = extract_paper_details(html_content)
for paper in rna_papers_data:
    print(paper)