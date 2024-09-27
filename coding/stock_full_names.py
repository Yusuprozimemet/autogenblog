# filename: stock_full_names.py
import requests
from bs4 import BeautifulSoup

def get_stock_full_name(ticker):
    url = f"https://finance.yahoo.com/quote/{ticker}?p={ticker}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        full_name = soup.find('h1', {"class": "D(ib) Fz(18px)"}).text
    except AttributeError:
        full_name = f"Could not retrieve full name for {ticker}"
    return full_name.strip()

tickers = ["UCG.MI", "ADS.DE"]

full_names = {ticker: get_stock_full_name(ticker) for ticker in tickers}
print(full_names)