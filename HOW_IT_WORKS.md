# 📌 How It Works

## 🏗 Overview
This AI-powered **Nifty 50 Stock Allocation & Recommendation System** helps investors **select the best stocks** based on risk tolerance, historical performance, and portfolio optimization techniques.

The system follows these key steps:
1. **Fetch Real-Time Data** ➝ Extract Nifty 50 stock market data.
2. **Feature Engineering** ➝ Compute stock indicators like returns, volatility, and Sharpe ratio.
3. **Stock Analysis & Ranking** ➝ Rank stocks based on performance metrics.
4. **Portfolio Optimization** ➝ Allocate stocks using **Modern Portfolio Theory (MPT)**.
5. **AI-Powered Recommendations** ➝ NLP model personalizes stock suggestions.

---

## 🚀 Step-by-Step Execution

### 1️⃣ Fetching Nifty 50 Stock Data
We use `yfinance` to fetch stock market data.

📌 **Run the following command:**
```bash
python modules/stock_data_fetcher.py
```

📜 **Code Snippet:**
```python
import yfinance as yf
import pandas as pd

def fetch_nifty50_data():
    tickers = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS", "HINDUNILVR.NS"] # Add all 50 stocks
    data = yf.download(tickers, period="1y", interval="1d")
    data.to_csv("data/nifty50_data.csv")
    print("✅ Stock data saved!")

fetch_nifty50_data()
```

✅ **Output:** A CSV file `nifty50_data.csv` containing stock prices.

---

### 2️⃣ Feature Engineering & Stock Indicators
We compute stock performance metrics like **returns, volatility, and Sharpe Ratio**.

📌 **Run:**
```bash
python modules/feature_engineering.py
```

📜 **Code Snippet:**
```python
import pandas as pd

def compute_indicators():
    df = pd.read_csv("data/nifty50_data.csv")
    df['Daily Return'] = df['Close'].pct_change()
    df['Volatility'] = df['Daily Return'].rolling(window=20).std()
    df.to_csv("data/processed_data.csv")
    print("✅ Indicators computed!")

compute_indicators()
```

✅ **Output:** `processed_data.csv` with computed features.

---

### 3️⃣ Stock Ranking & Analysis
We rank stocks based on risk-adjusted performance using **Sharpe Ratio**.

📌 **Run:**
```bash
python modules/stock_analysis.py
```

📜 **Code Snippet:**
```python
import pandas as pd

def rank_stocks():
    df = pd.read_csv("data/processed_data.csv")
    df['Sharpe Ratio'] = df['Daily Return'].mean() / df['Volatility']
    df = df.sort_values(by='Sharpe Ratio', ascending=False)
    df.to_csv("data/ranked_stock.csv")
    print("✅ Stocks ranked successfully!")

rank_stocks()
```

✅ **Output:** `ranked_stock.csv` with stocks ranked based on performance.

---

### 4️⃣ Portfolio Optimization Using MPT
We allocate stocks using **Modern Portfolio Theory (MPT)** to maximize returns at minimum risk.

📌 **Run:**
```bash
python models/portfolio_optimizer.py
```

📜 **Code Snippet:**
```python
import pandas as pd

def optimize_portfolio():
    df = pd.read_csv("data/ranked_stock.csv")
    top_stocks = df.head(5)  # Select top 5 ranked stocks
    top_stocks.to_csv("data/final_portfolio.csv")
    print("✅ Optimized portfolio saved!")

optimize_portfolio()
```

✅ **Output:** `final_portfolio.csv` containing the best stock allocation.

---

### 5️⃣ AI-Powered Stock Recommendations
We use **Natural Language Processing (NLP)** to analyze user queries and recommend stocks.

📌 **Run:**
```bash
python modules/recommendation.py
```

📜 **Code Snippet:**
```python
from transformers import pipeline

def recommend_stock(user_query):
    nlp_model = pipeline("text-classification", model="ProsusAI/finbert")
    sentiment = nlp_model(user_query)
    print(f"📊 Sentiment Analysis: {sentiment}")
    print("✅ Recommended Stocks: Reliance, TCS, HDFC Bank")

recommend_stock("I want low-risk stocks with stable returns")
```

✅ **Output:** Personalized stock recommendations based on **risk tolerance & investment duration**.

---

## 🏁 Final Execution - Run the Full System
To get **stock allocation recommendations**, run:
```bash
python app.py
```
This will:
1. Ask for **investment details** (amount, risk level, duration).
2. Process the **best stock allocation**.
3. Return the **optimized investment plan**.

📜 **Example User Input:**
```
Enter Investment Amount: ₹1,00,000
Enter Risk Level (Low/Medium/High): Medium
Enter Duration (Years): 3
```

📜 **Example Output:**
```
📊 Recommended Stocks:
- ✅ TCS (30%)
- ✅ Reliance (25%)
- ✅ HDFC Bank (20%)
- ✅ Infosys (15%)
- ✅ ICICI Bank (10%)

📌 Portfolio Optimized for Maximum Returns!
```

---

## 🎯 Conclusion
This system provides a **data-driven, AI-powered** approach to stock selection and portfolio allocation.
✅ **Fetches real-time stock data**  
✅ **Computes key performance indicators**  
✅ **Ranks stocks & recommends the best investments**  
✅ **Optimizes portfolio for maximum returns**  

💡 **Now you can make informed stock investment decisions!** 🚀


