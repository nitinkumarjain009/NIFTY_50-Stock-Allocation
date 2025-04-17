#!/usr/bin/env python3
"""
Stock Recommendations Generator
Analyzes stock data and generates recommendations for NIFTY 50 stocks
"""

import pandas as pd
import numpy as np
import os
import requests
from datetime import datetime

# Telegram bot configuration
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')  # Set this as an environment variable
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')      # Set this as an environment variable

def load_processed_data(filepath='data/processed.csv'):
    """
    Load the processed stock data from CSV
    
    Args:
        filepath (str): Path to the processed data CSV file
        
    Returns:
        DataFrame: Processed stock data
    """
    try:
        if not os.path.exists(filepath):
            print(f"Error: Processed data file not found at {filepath}")
            return None
            
        data = pd.read_csv(filepath)
        print(f"Loaded processed data with shape: {data.shape}")
        return data
    except Exception as e:
        print(f"Error loading processed data: {e}")
        return None

def generate_recommendations(data):
    """
    Generate stock recommendations based on financial metrics
    
    Args:
        data (DataFrame): Processed stock data
        
    Returns:
        DataFrame: Stock recommendations with buy/hold/sell signals
    """
    if data is None or data.empty:
        print("No data available for generating recommendations")
        return None
        
    try:
        # Create a copy of the data to avoid modifying the original
        recommendations = data.copy()
        
        # Example criteria for recommendations
        # These are simplified examples - you should adjust based on your strategy
        recommendations['Signal'] = 'Hold'  # Default to Hold
        
        # Example: Buy signal for stocks with high Sharpe ratio and low volatility
        buy_condition = (recommendations['Sharpe Ratio'] > recommendations['Sharpe Ratio'].quantile(0.7)) & \
                         (recommendations['Volatility'] < recommendations['Volatility'].quantile(0.3))
        recommendations.loc[buy_condition, 'Signal'] = 'Buy'
        
        # Example: Sell signal for stocks with low Sharpe ratio and high volatility
        sell_condition = (recommendations['Sharpe Ratio'] < recommendations['Sharpe Ratio'].quantile(0.3)) & \
                          (recommendations['Volatility'] > recommendations['Volatility'].quantile(0.7))
        recommendations.loc[sell_condition, 'Signal'] = 'Sell'
        
        # Add a recommendation strength score (0-100)
        recommendations['Strength'] = 50  # Default neutral score
        
        # Adjust strength based on Sharpe ratio (higher is better)
        sharpe_min = recommendations['Sharpe Ratio'].min()
        sharpe_max = recommendations['Sharpe Ratio'].max()
        sharpe_range = sharpe_max - sharpe_min
        
        if sharpe_range > 0:
            recommendations['Strength'] += 25 * (recommendations['Sharpe Ratio'] - sharpe_min) / sharpe_range
            
        # Adjust strength based on volatility (lower is better)
        vol_min = recommendations['Volatility'].min()
        vol_max = recommendations['Volatility'].max()
        vol_range = vol_max - vol_min
        
        if vol_range > 0:
            recommendations['Strength'] -= 25 * (recommendations['Volatility'] - vol_min) / vol_range
        
        # Ensure strength is between 0 and 100
        recommendations['Strength'] = recommendations['Strength'].clip(0, 100)
        recommendations['Strength'] = recommendations['Strength'].round(0).astype(int)
        
        # Sort by Strength (descending)
        recommendations = recommendations.sort_values('Strength', ascending=False)
        
        return recommendations
        
    except Exception as e:
        print(f"Error generating recommendations: {e}")
        import traceback
        traceback.print_exc()
        return None

def send_telegram_message(message):
    """
    Send a message to Telegram
    
    Args:
        message (str): Message to send
        
    Returns:
        bool: True if message was sent successfully, False otherwise
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram bot token or chat ID not set. Skipping Telegram notification.")
        print("Please set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables.")
        return False
        
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        response = requests.post(url, data=payload)
        
        if response.status_code == 200:
            print("Message sent to Telegram successfully")
            return True
        else:
            print(f"Failed to send message to Telegram: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
        return False

def format_recommendations_message(recommendations):
    """
    Format recommendations as a Telegram message
    
    Args:
        recommendations (DataFrame): Stock recommendations
        
    Returns:
        str: Formatted message
    """
    if recommendations is None or recommendations.empty:
        return "No recommendations available."
        
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    message = f"*NIFTY 50 Stock Recommendations - {current_date}*\n\n"
    
    # Add top 3 buy recommendations
    buy_recs = recommendations[recommendations['Signal'] == 'Buy'].head(3)
    if not buy_recs.empty:
        message += "*Top Buy Recommendations:*\n"
        for idx, row in buy_recs.iterrows():
            message += f"- {row.name}: Strength {row['Strength']}, Sharpe {row['Sharpe Ratio']:.2f}\n"
        message += "\n"
    
    # Add top 3 sell recommendations
    sell_recs = recommendations[recommendations['Signal'] == 'Sell'].head(3)
    if not sell_recs.empty:
        message += "*Top Sell Recommendations:*\n"
        for idx, row in sell_recs.iterrows():
            message += f"- {row.name}: Strength {100-row['Strength']}, Sharpe {row['Sharpe Ratio']:.2f}\n"
        message += "\n"
    
    # Add general market outlook
    avg_sharpe = recommendations['Sharpe Ratio'].mean()
    avg_volatility = recommendations['Volatility'].mean()
    
    message += "*Market Outlook:*\n"
    message += f"- Average Sharpe Ratio: {avg_sharpe:.2f}\n"
    message += f"- Average Volatility: {avg_volatility:.2f}\n"
    
    if avg_sharpe > 0.5:
        message += "- Market shows positive risk-adjusted returns\n"
    else:
        message += "- Market shows cautious risk-adjusted returns\n"
        
    if avg_volatility > 0.02:
        message += "- Market volatility is elevated\n"
    else:
        message += "- Market volatility is moderate\n"
    
    return message

def send_processed_data(filepath='data/processed.csv'):
    """
    Send processed data from CSV file to Telegram
    
    Args:
        filepath (str): Path to the processed data CSV file
        
    Returns:
        bool: True if data was sent successfully, False otherwise
    """
    try:
        if not os.path.exists(filepath):
            message = f"Error: Processed data file not found at {filepath}"
            send_telegram_message(message)
            return False
            
        data = pd.read_csv(filepath)
        
        # Format the data as a message
        current_date = datetime.now().strftime("%Y-%m-%d")
        message = f"*NIFTY 50 Processed Data - {current_date}*\n\n"
        
        # Add summary statistics
        message += "*Summary Statistics:*\n"
        message += f"- Number of stocks: {len(data)}\n"
        
        # Add top 5 performing stocks
        if 'Average Return' in data.columns:
            top_performers = data.sort_values('Average Return', ascending=False).head(5)
            message += "\n*Top Performers (Average Return):*\n"
            for idx, row in top_performers.iterrows():
                message += f"- {row.name if hasattr(row, 'name') else idx}: {row['Average Return']:.4f}\n"
        
        # If message is too long, truncate it (Telegram has a 4096 character limit)
        if len(message) > 4000:
            message = message[:3950] + "\n\n*[Message truncated due to length]*"
            
        return send_telegram_message(message)
        
    except Exception as e:
        print(f"Error sending processed data: {e}")
        send_telegram_message(f"Error processing data: {str(e)}")
        return False

def main():
    """
    Main function to run the stock recommendations workflow
    """
    print("NIFTY 50 Stock Recommendations Generator")
    print("---------------------------------------")
    
    # Load processed data
    data = load_processed_data()
    if data is None:
        print("Failed to load processed data. Exiting.")
        return
    
    # Generate recommendations
    print("Generating stock recommendations...")
    recommendations = generate_recommendations(data)
    if recommendations is None:
        print("Failed to generate recommendations. Exiting.")
        return
    
    # Save recommendations to file
    try:
        os.makedirs('data', exist_ok=True)
        recommendations.to_csv('data/recommendations.csv')
        print("Recommendations saved to data/recommendations.csv")
    except Exception as e:
        print(f"Error saving recommendations: {e}")
    
    # Format and send recommendations
    message = format_recommendations_message(recommendations)
    success = send_telegram_message(message)
    
    if success:
        print("Recommendations sent to Telegram successfully")
    else:
        print("Failed to send recommendations to Telegram")
    
    # Send processed data
    print("Sending processed data to Telegram...")
    success = send_processed_data()
    
    if success:
        print("Processed data sent to Telegram successfully")
    else:
        print("Failed to send processed data to Telegram")

if __name__ == "__main__":
    main()
