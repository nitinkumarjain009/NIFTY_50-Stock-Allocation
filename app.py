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
    
    # Download historical data
    data = yf.download(nifty50_tickers, period=period)
    return data

def calculate_metrics(data):
    """
    Calculate key financial metrics for the stocks
    
    Args:
        data (DataFrame): Historical stock data
        
    Returns:
        DataFrame: Financial metrics
    """
    # Extract adjusted close prices
    close_prices = data['Adj Close']
    
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

def optimize_portfolio(data, num_portfolios=10000):
    """
    Optimize portfolio allocation using Monte Carlo simulation
    
    Args:
        data (DataFrame): Historical stock data
        num_portfolios (int): Number of portfolios to simulate
        
    Returns:
        tuple: (optimal_weights, performance_metrics)
    """
    # This is a simplified implementation
    # You would typically use more advanced optimization techniques
    
    # Extract adjusted close prices and calculate returns
    close_prices = data['Adj Close']
    returns = close_prices.pct_change().dropna()
    
    # Get mean returns and covariance matrix
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    
    # Number of assets
    num_assets = len(returns.columns)
    
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

def main():
    """
    Main function to run the stock analysis workflow
    """
    print("NIFTY 50 Stock Analysis and Portfolio Allocation")
    print("------------------------------------------------")
    
    # Fetch data
    print("Fetching NIFTY 50 stock data...")
    data = fetch_nifty50_data()
    
    # Calculate metrics
    print("Calculating financial metrics...")
    metrics = calculate_metrics(data)
    print("\nFinancial Metrics:")
    print(metrics)
    
    # Optimize portfolio
    print("\nOptimizing portfolio allocation...")
    weights, performance = optimize_portfolio(data)
    
    # Display results
    print("\nOptimal Portfolio Performance:")
    print(f"Expected Annual Return: {performance['Return']:.4f}")
    print(f"Expected Annual Risk: {performance['Risk']:.4f}")
    print(f"Sharpe Ratio: {performance['Sharpe Ratio']:.4f}")
    
    print("\nOptimal Portfolio Weights:")
    for i, ticker in enumerate(data['Adj Close'].columns):
        print(f"{ticker}: {weights[i]:.4f}")

if __name__ == "__main__":
    main()
