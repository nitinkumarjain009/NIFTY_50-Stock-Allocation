# 🌟 Nifty 50 Stock Allocation & Recommendation System

## 🚀 About the Project
This project is an AI-driven **Nifty 50 stock allocation & recommendation system** that helps investors make **data-driven investment decisions**. It analyzes historical stock performance, risk, and portfolio optimization to suggest the best stocks based on the user's risk tolerance and investment goals.

## 🎯 Features
- ✅ **Real-time Nifty 50 stock data fetching**
- ✅ **Computation of key stock indicators (returns, volatility, Sharpe ratio)**
- ✅ **Stock ranking based on risk-adjusted performance**
- ✅ **Portfolio allocation using Modern Portfolio Theory (MPT)**
- ✅ **AI-powered NLP for personalized stock queries**

---

## 🏠 Project Structure

```
📂 NIFTY50-STOCK-ALLOCATION/
│── 📂 data/                    # Contains stock market datasets
│   ├── final_portfolio.csv      # Final stock allocation recommendations
│   ├── nifty50_data.csv         # Raw Nifty 50 stock dataset
│   ├── processed_data.csv       # Cleaned & transformed stock data
│   └── ranked_stock.csv         # Ranked stocks based on risk-adjusted returns
│── 📂 models/                   # Machine Learning & AI models
│   ├── llm_query_parser.py      # Parses user queries using NLP
│   └── portfolio_optimizer.py   # Optimizes portfolio allocation using MPT
│── 📂 modules/                  # Core stock analysis functions
│   ├── feature_engineering.py   # Computes stock indicators (returns, volatility)
│   ├── recommendation.py        # Generates stock recommendations
│   ├── stock_analysis.py        # Analyzes & ranks stocks based on Sharpe & Sortino ratios
│   └── stock_data_fetcher.py    # Fetches real-time stock data
│── app.py                       # Main script for user input & recommendations
│── README.md                    # Project documentation
│── requirements.txt              # Dependencies list
```

---

## 🔧 Installation & Setup

### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/ShreyasDole/NIFTY50-STOCK-ALLOCATION.git
cd NIFTY50-STOCK-ALLOCATION
```

### 2️⃣ **Create a Virtual Environment & Install Dependencies**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3️⃣ **Fetch Real-Time Stock Data**
```bash
python modules/stock_data_fetcher.py
```
✅ This script downloads the latest **Nifty 50 stock market data**.

### 4️⃣ **Compute Stock Indicators**
```bash
python modules/feature_engineering.py
```
✅ Computes **returns, volatility, moving averages, and risk ratios**.

### 5️⃣ **Generate Stock Recommendations**
```bash
python modules/recommendation.py
```
✅ Generates **top stock recommendations** based on risk and performance.

### 6️⃣ **Optimize Portfolio Allocation**
```bash
python models/portfolio_optimizer.py
```
✅ Allocates stocks in an optimized manner using **Modern Portfolio Theory (MPT)**.

### 7️⃣ **Run the Full Stock Allocation System**
```bash
python app.py
```
✅ Enter your **investment amount, duration & risk level**, and get **stock allocation suggestions**.

