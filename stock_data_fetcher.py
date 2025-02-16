import yfinance as yf
import pandas as pd

# List of Nifty 50 stock tickers
NIFTY50_TICKERS = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
    "HINDUNILVR.NS", "ITC.NS", "SBIN.NS", "BHARTIARTL.NS", "KOTAKBANK.NS",
    "LT.NS", "ASIANPAINT.NS", "AXISBANK.NS", "BAJFINANCE.NS", "HCLTECH.NS",
    "MARUTI.NS", "TITAN.NS", "ULTRACEMCO.NS", "SUNPHARMA.NS", "WIPRO.NS",
    "HDFCLIFE.NS", "POWERGRID.NS", "TECHM.NS", "NTPC.NS", "GRASIM.NS",
    "ADANIENT.NS", "INDUSINDBK.NS", "JSWSTEEL.NS", "TATASTEEL.NS", "CIPLA.NS",
    "DRREDDY.NS", "SBILIFE.NS", "HINDALCO.NS", "DIVISLAB.NS", "BAJAJFINSV.NS",
    "TATAMOTORS.NS", "HEROMOTOCO.NS", "COALINDIA.NS", "BPCL.NS", "ONGC.NS",
    "APOLLOHOSP.NS", "EICHERMOT.NS", "BAJAJ-AUTO.NS", "UPL.NS", "M&M.NS",
    "ADANIPORTS.NS", "BRITANNIA.NS", "SHREECEM.NS", "NESTLEIND.NS", "DLF.NS",
    "VEDL.NS"
]

def fetch_nifty50_data():
    stock_data = {}
    for ticker in NIFTY50_TICKERS:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")  # Fetch 1-year data
        stock_data[ticker] = hist['Close']

    df = pd.DataFrame(stock_data)
    df.to_csv("data/nifty50_data.csv")
    print("Nifty 50 stock data saved successfully.")

if __name__ == "__main__":
    fetch_nifty50_data()
