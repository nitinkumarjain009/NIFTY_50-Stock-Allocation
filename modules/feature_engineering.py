import pandas as pd
import numpy as np

def compute_indicators():
    df = pd.read_csv("data/nifty50_data.csv", index_col=0, parse_dates=True)
    
    indicators = {}
    for col in df.columns:
        data = df[col].dropna()
        indicators[col] = {
            "1Y_Return": (data[-1] - data[0]) / data[0] * 100,
            "Volatility": np.std(data.pct_change()) * np.sqrt(252),
            "SMA_50": data.rolling(50).mean().iloc[-1],
            "SMA_200": data.rolling(200).mean().iloc[-1],
        }
    
    indicator_df = pd.DataFrame(indicators).T
    indicator_df.to_csv("data/processed_data.csv")
    print("Indicators computed and saved.")

if __name__ == "__main__":
    compute_indicators()
