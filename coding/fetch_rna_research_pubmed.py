# filename: fetch_rna_research_pubmed.py
import requests
from urllib.parse import quote

def get_rna_research_papers():
    query = quote("RNA research[Title/Abstract] AND (2023[Date - Publication] : 3000[Date - Publication])")
    url = f"https://pubmed.ncbi.nlm.nih.gov/?term={query}&size=10"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.text
    else:
        return []

html_content = get_rna_research_papers()
print(html_content)