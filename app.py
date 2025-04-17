#!/usr/bin/env python3
"""
Stock Analysis Workflow
A tool for analyzing NIFTY 50 stocks and optimizing portfolio allocation
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta
import sys

def fetch_nifty50_data(period='1y'):
    """
    Fetches historical data for NIFTY 50 stocks
    
    Args:
        period (str): Time period for data (e.g., '1y' for 1 year)
        
    Returns:
        DataFrame: Historical stock data
    """
    # You'll need to replace this with actual NIFTY 50 tickers
    nifty50_tickers = [
        "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "HINDUNILVR.NS",
        "ICICIBANK.NS", "BHARTIARTL.NS", "ITC.NS", "KOTAKBANK.NS", "SBIN.NS"
        # Add more tickers as needed
    ]
    
    try:
        # Download historical data
        print(f"Downloading data for {len(nifty50_tickers)} stocks...")
        data = yf.download(nifty50_tickers, period=period)
        
        # Print detailed information about the DataFrame structure
        print(f"Data shape: {data.shape}")
        print("Data columns structure:")
        print(data.columns)
        print("\nColumn levels (if multi-index):")
        if isinstance(data.columns, pd.MultiIndex):
            for i, level in enumerate(data.columns.levels):
                print(f"Level {i}: {list(level)}")
        
        # Print the first few rows to see the data structure
        print("\nFirst few rows of data:")
        print(data.head(2))
        
        if data.empty:
            print("Warning: Downloaded data is empty")
            return None
            
        return data
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return None

def calculate_metrics(data):
    """
    Calculate key financial metrics for the stocks
    
    Args:
        data (DataFrame): Historical stock data
        
    Returns:
        DataFrame: Financial metrics
    """
    if data is None or data.empty:
        print("No data available for metric calculation")
        return None
        
    # Handle the DataFrame structure based on what we get from yfinance
    try:
        # First, try to determine if we have a MultiIndex DataFrame
        if isinstance(data.columns, pd.MultiIndex):
            print("Working with MultiIndex DataFrame")
            # Get first level column names
            first_level_columns = list(data.columns.levels[0])
            print(f"First level columns: {first_level_columns}")
            
            # Check what price columns are available
            if 'Close' in first_level_columns:
                print("Using 'Close' column")
                close_prices = data['Close']
            elif 'Adj Close' in first_level_columns:
                print("Using 'Adj Close' column")
                close_prices = data['Adj Close']
            else:
                print(f"Could not find closing prices. Available columns: {first_level_columns}")
                # Try to use the first available price column
                if len(first_level_columns) > 0:
                    print(f"Falling back to first available column: {first_level_columns[0]}")
                    close_prices = data[first_level_columns[0]]
                else:
                    return None
        else:
            print("Working with standard DataFrame")
            # Handle flat DataFrame
            columns = list(data.columns)
            print(f"Available columns: {columns}")
            
            if 'Close' in columns:
                print("Using 'Close' column")
                close_prices = data['Close']
            elif 'Adj Close' in columns:
                print("Using 'Adj Close' column")
                close_prices = data['Adj Close']
            else:
                print("Could not find standard closing price columns")
                return None
                
        # Print information about close_prices to verify
        print(f"\nClose prices DataFrame shape: {close_prices.shape}")
        print("Close prices DataFrame columns:")
        print(close_prices.columns)
        print("\nFirst few rows of close prices:")
        print(close_prices.head(2))
        
        # Calculate daily returns
        returns = close_prices.pct_change().dropna()
        
        # Calculate metrics
        avg_returns = returns.mean()
        volatility = returns.std()
        sharpe_ratio = avg_returns / volatility
        
        # Create metrics dataframe
        metrics = pd.DataFrame({
            'Average Return': avg_returns,
            'Volatility': volatility,
            'Sharpe Ratio': sharpe_ratio
        })
        
        return metrics
        
    except Exception as e:
        print(f"Error calculating metrics: {e}")
        import traceback
        traceback.print_exc()
        return None

def optimize_portfolio(data, num_portfolios=1000):
    """
    Optimize portfolio allocation using Monte Carlo simulation
    
    Args:
        data (DataFrame): Historical stock data
        num_portfolios (int): Number of portfolios to simulate
        
    Returns:
        tuple: (optimal_weights, performance_metrics)
    """
    if data is None or data.empty:
        print("No data available for portfolio optimization")
        return None, None
    
    try:
        # Use the same logic as in calculate_metrics to get close prices
        if isinstance(data.columns, pd.MultiIndex):
            # Get first level column names
            first_level_columns = list(data.columns.levels[0])
            
            # Check what price columns are available
            if 'Close' in first_level_columns:
                close_prices = data['Close']
            elif 'Adj Close' in first_level_columns:
                close_prices = data['Adj Close']
            else:
                if len(first_level_columns) > 0:
                    close_prices = data[first_level_columns[0]]
                else:
                    return None, None
        else:
            # Handle flat DataFrame
            columns = list(data.columns)
            
            if 'Close' in columns:
                close_prices = data['Close']
            elif 'Adj Close' in columns:
                close_prices = data['Adj Close']
            else:
                return None, None
        
        # Extract and calculate returns
        returns = close_prices.pct_change().dropna()
        
        # Get mean returns and covariance matrix
        mean_returns = returns.mean()
        cov_matrix = returns.cov()
        
        # Number of assets
        num_assets = len(returns.columns)
        print(f"Optimizing portfolio with {num_assets} assets")
        
        # Arrays to store results
        results = np.zeros((3, num_portfolios))
        weights_record = []
        
        # Run Monte Carlo simulation
        for i in range(num_portfolios):
            # Generate random weights
            weights = np.random.random(num_assets)
            weights /= np.sum(weights)
            weights_record.append(weights)
            
            # Calculate portfolio metrics
            portfolio_return = np.sum(mean_returns * weights) * 252
            portfolio_std_dev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
            
            # Store results
            results[0,i] = portfolio_std_dev
            results[1,i] = portfolio_return
            results[2,i] = results[1,i] / results[0,i]  # Sharpe ratio
        
        # Find the optimal portfolio
        max_sharpe_idx = np.argmax(results[2])
        optimal_weights = weights_record[max_sharpe_idx]
        
        # Get performance metrics for the optimal portfolio
        optimal_performance = {
            'Return': results[1, max_sharpe_idx],
            'Risk': results[0, max_sharpe_idx],
            'Sharpe Ratio': results[2, max_sharpe_idx]
        }
        
        return optimal_weights, optimal_performance
        
    except Exception as e:
        print(f"Error optimizing portfolio: {e}")
        import traceback
        traceback.print_exc()
        return None, None

def main():
    """
    Main function to run the stock analysis workflow
    """
    print("NIFTY 50 Stock Analysis and Portfolio Allocation")
    print("------------------------------------------------")
    
    # Print Python and package versions for debugging
    print(f"Python version: {sys.version}")
    print(f"Pandas version: {pd.__version__}")
    print(f"NumPy version: {np.__version__}")
    print(f"yfinance version: {yf.__version__}")
    print("------------------------------------------------")
    
    # Fetch data
    print("Fetching NIFTY 50 stock data...")
    data = fetch_nifty50_data()
    
    if data is None or data.empty:
        print("Failed to obtain stock data. Exiting.")
        return
    
    # Calculate metrics
    print("Calculating financial metrics...")
    metrics = calculate_metrics(data)
    if metrics is not None:
        print("\nFinancial Metrics:")
        print(metrics)
    else:
        print("Failed to calculate metrics. Exiting.")
        return
    
    # Optimize portfolio
    print("\nOptimizing portfolio allocation...")
    weights, performance = optimize_portfolio(data)
    
    if weights is not None and performance is not None:
        # Display results
        print("\nOptimal Portfolio Performance:")
        print(f"Expected Annual Return: {performance['Return']:.4f}")
        print(f"Expected Annual Risk: {performance['Risk']:.4f}")
        print(f"Sharpe Ratio: {performance['Sharpe Ratio']:.4f}")
        
        # Get the ticker names
        tickers = close_prices.columns if 'close_prices' in locals() else [f"Asset_{i}" for i in range(len(weights))]
        
        print("\nOptimal Portfolio Weights:")
        for i, ticker in enumerate(tickers):
            print(f"{ticker}: {weights[i]:.4f}")
    else:
        print("Failed to optimize portfolio.")

if __name__ == "__main__":
    main()
