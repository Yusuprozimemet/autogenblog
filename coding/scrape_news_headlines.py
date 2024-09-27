# filename: scrape_news_headlines.py

import requests
from bs4 import BeautifulSoup

def fetch_news_headlines(query):
    url = f"https://www.bing.com/news/search?q={query}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve news for {query}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = soup.find_all('a', class_='title', limit=10)
    
    headlines_list = [headline.get_text() for headline in headlines]
    return headlines_list

def main():
    stocks = {
        "UniCredit S.p.A.": "UCG.MI",
        "adidas AG": "ADS.DE"
    }

    for name, symbol in stocks.items():
        print(f"\nFetching news headlines for {name} ({symbol})...\n")
        headlines = fetch_news_headlines(name)
        if headlines:
            for idx, headline in enumerate(headlines, 1):
                print(f"{idx}. {headline}")
        else:
            print("No headlines found.")
        
if __name__ == "__main__":
    main()