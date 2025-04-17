# stock_alerts.py
import pandas as pd
import telegram
import os
import asyncio

# Load the data
try:
    df = pd.read_csv('data/processed_data.csv')
except FileNotFoundError:
    print("Error: data/processed.csv not found.")
    exit()

# Rename the first column to 'ticker' if it's blank or unnamed
if df.columns[0] == '':
    df.rename(columns={'' : 'ticker'}, inplace=True)
elif 'Unnamed: 0' in df.columns:
    df.rename(columns={'Unnamed: 0' : 'ticker'}, inplace=True)
else:
    df.rename(columns={df.columns[0] : 'ticker'}, inplace=True)

# Assign column names if not already present
expected_columns = ['ticker', '1Y_Return', 'Volatility', 'SMA_50', 'SMA_200']
if len(df.columns) != len(expected_columns):
    if len(df.columns) < len(expected_columns):
        df.columns = expected_columns[:len(df.columns)]
        if 'ticker' not in df.columns:
            print("Error: 'ticker' column not found after assigning names.")
            exit()
    else:
        df = df.iloc[:, :len(expected_columns)]
        df.columns = expected_columns
else:
    if 'ticker' not in df.columns:
        df.columns = expected_columns

# Telegram Bot Token and Chat ID
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    print("Error: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables must be set.")
    exit()

async def send_telegram_message(message):
    """Sends a message to the specified Telegram chat."""
    bot = telegram.Bot(token=BOT_TOKEN)
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='HTML')
    except telegram.error.TelegramError as e:
        print(f"Error sending Telegram message: {e}")

async def generate_stock_alerts():
    """Generates stock alerts based on SMA crossover and sends them to Telegram in one message with colorful background."""
    recommendations = df[df['SMA_50'] > df['SMA_200']].copy()

    if not recommendations.empty:
        message = "<pre><span style='background-color: #e6ffe6;'><b>📈 Stock Recommendations (SMA 50 > SMA 200) 📈</b></span>\n\n"
        for index, row in recommendations.iterrows():
            ticker = row['ticker']
            message += f"<span style='background-color: #ccffcc;'><b>🚀 {ticker}</b> - BUY</span>\n"
        message += "</pre>"
        await send_telegram_message(message)
    else:
        await send_telegram_message("<pre>No stock recommendations based on SMA crossover criteria.</pre>")

if __name__ == '__main__':
    asyncio.run(generate_stock_alerts())
