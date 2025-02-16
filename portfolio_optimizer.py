import pandas as pd
import numpy as np

def allocate_portfolio(amount, stocks):
    allocation = {}
    weights = np.array([0.25, 0.2, 0.15, 0.2, 0.2])  # Sample weights
    stock_names = stocks.index.tolist()

    for i in range(len(stock_names)):
        allocation[stock_names[i]] = round(amount * weights[i], 2)

    return allocation

if __name__ == "__main__":
    top_stocks = pd.read_csv("data/processed_data.csv", index_col=0).head(5)
    print(allocate_portfolio(100000, top_stocks))
