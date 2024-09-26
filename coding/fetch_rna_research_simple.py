# filename: fetch_rna_research_simple.py
import requests
import re

def get_rna_research_papers():
    url = "https://www.researchgate.net/search?q=rna%20research"
    response = requests.get(url)
    
    # Simple regex to find paper titles in the response text
    titles = re.findall(r'data-publication-title="(.*?)"', response.text)
    
    return titles[:10]  # Get top 10 papers for brevity

rna_papers = get_rna_research_papers()
print(rna_papers)