# filename: fetch_rna_research.py
import requests
from bs4 import BeautifulSoup

def get_rna_research_papers():
    url = "https://www.researchgate.net/search?q=rna%20research&queryType=all"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    papers = []
    for item in soup.find_all('div', class_='nova-e-grid__item'):
        title = item.find('a', class_='nova-e-link').text.strip()
        if title:
            papers.append(title)
    
    return papers[:10]  # Get top 10 papers for brevity

rna_papers = get_rna_research_papers()
print(rna_papers)