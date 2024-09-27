# filename: stock_analysis.py
import yfinance as yf
import matplotlib.pyplot as plt

def fetch_stock_info(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        'full_name': info.get('longName') or info.get('shortName', 'N/A'),
        'current_price': info.get('currentPrice', 'N/A'),
        'pe_ratio': info.get('trailingPE', 'N/A'),
        'forward_pe': info.get('forwardPE', 'N/A'),
        'dividends': info.get('dividendYield', 'N/A'),
        'price_to_book': info.get('priceToBook', 'N/A'),
        'debt_eq': info.get('debtToEquity', 'N/A'),
        'roe': info.get('returnOnEquity', 'N/A')
    }

tickers = ["UCG.MI", "ADS.DE"]
stock_data = {ticker: fetch_stock_info(ticker) for ticker in tickers}

print("Stock Data:")
for ticker, data in stock_data.items():
    print(f"{data['full_name']} ({ticker}):")
    print(f"  Current Price: {data['current_price']}")
    print(f"  P/E Ratio: {data['pe_ratio']}")
    print(f"  Forward P/E: {data['forward_pe']}")
    print(f"  Dividends: {data['dividends']}")
    print(f"  Price to Book: {data['price_to_book']}")
    print(f"  Debt to Equity: {data['debt_eq']}")
    print(f"  ROE: {data['roe']}")
    print()

# Fetch historical data for the past 6 months
import pandas as pd

def fetch_historical_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="6mo")
    return hist

historical_data = {ticker: fetch_historical_data(ticker) for ticker in tickers}

# Normalize and plot the data
plt.figure(figsize=(14, 7))

for ticker, hist in historical_data.items():
    normalized_price = hist['Close'] / hist['Close'].iloc[0]
    plt.plot(normalized_price, label=ticker)

plt.title('Normalized Stock Prices over the Past 6 Months')
plt.xlabel('Date')
plt.ylabel('Normalized Price')
plt.legend()
plt.savefig('normalized_prices.png')

# Calculate the percentage performance over the past 6 months
performance = {}
for ticker, hist in historical_data.items():
    start_price = hist['Close'].iloc[0]
    end_price = hist['Close'].iloc[-1]
    performance[ticker] = ((end_price - start_price) / start_price) * 100

print("Performance Over the Past 6 Months:")
for ticker, change in performance.items():
    print(f"{ticker}: {change:.2f}%")

# Calculate and display the correlation matrix
prices_df = pd.DataFrame({
    ticker: data['Close']
    for ticker, data in historical_data.items()
})

correlation_matrix = prices_df.corr()
print("Correlation Matrix:")
print(correlation_matrix)