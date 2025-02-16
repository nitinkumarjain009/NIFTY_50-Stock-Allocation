import pandas as pd
import numpy as np

def get_top_performers(duration, risk_level):
    df = pd.read_csv("data/processed_data.csv", index_col=0)

    # Normalize risk_level input
    risk_multiplier = {"low": 0.5, "medium": 1, "high": 1.5}
    risk_factor = risk_multiplier.get(risk_level.lower(), 1)

    # Compute Sharpe Ratio
    df["Sharpe_Ratio"] = df["1Y_Return"] / (df["Volatility"] * risk_factor)

    # Sort by Sharpe Ratio
    df_sorted = df.sort_values(by="Sharpe_Ratio", ascending=False)
    
    # Select top stocks
    top_stocks = df_sorted.head(5)
    
    return top_stocks

if __name__ == "__main__":
    print(get_top_performers(12, "medium"))
