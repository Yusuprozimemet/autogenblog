# filename: fetch_rna_papers.py
import requests
from bs4 import BeautifulSoup

# Function to fetch recent RNA research articles
def fetch_rna_research():
    url = "https://arxiv.org/search/?query=rna+splicing+OR+rna+stability&searchtype=all&source=header&order=-announced_date_first&size=50"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    papers = []
    for result in soup.select('.meta'):
        title = result.select_one('.title').text.strip()
        authors = result.select_one('.authors').text.strip()
        date = result.select_one('.date').text.strip()
        papers.append({'title': title, 'authors': authors, 'date': date})

    return papers

# Fetch RNA research papers
rna_papers = fetch_rna_research()

# Print the titles of the research papers
for paper in rna_papers:
    print(f"Title: {paper['title']} | Authors: {paper['authors']} | Date: {paper['date']}")