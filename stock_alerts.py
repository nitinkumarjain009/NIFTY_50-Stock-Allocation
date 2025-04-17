# stock_alerts.py
import pandas as pd
import telegram
import os
import asyncio

# Load the data
try:
    df = pd.read_csv('data/processed.csv')  # Let pandas infer the header (including the blank one)
except FileNotFoundError:
    print("Error: data/processed.csv not found.")
    exit()

# Rename the first column (which might have a blank or unnamed header) to 'ticker'
if df.columns[0] == '':  # Check if the first column's name is an empty string
    df.rename(columns={'' : 'ticker'}, inplace=True)
elif 'Unnamed: 0' in df.columns: # Check for a default unnamed column name
    df.rename(columns={'Unnamed: 0' : 'ticker'}, inplace=True)
else:
    # If the first column has some other unexpected name, you might need to adjust this
    print(f"Warning: First column header is '{df.columns[0]}'. Assuming it's the ticker.")
    df.rename(columns={df.columns[0] : 'ticker'}, inplace=True)

# Ensure other columns have the expected names (in case there was no header at all)
expected_columns = ['ticker', '1Y_Return', 'Volatility', 'SMA_50', 'SMA_200']
if len(df.columns) < len(expected_columns):
    print("Warning: Number of columns in CSV is less than expected. Check your file.")
elif len(df.columns) == len(expected_columns):
    df.columns = expected_columns
else:
    # If there are more columns, we assume the first few are the ones we need
    df = df.iloc[:, :len(expected_columns)]
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
        await bot.send_message(chat_id=CHAT_ID, text=message)
    except telegram.error.TelegramError as e:
        print(f"Error sending Telegram message: {e}")

async def generate_stock_alerts():
    """Generates stock alerts based on SMA crossover and sends them to Telegram."""
    recommendations = df[df['SMA_50'] > df['SMA_200']].copy()

    if not recommendations.empty:
        for index, row in recommendations.iterrows():
            ticker = row['ticker']
            message = (
                f"🚀 {ticker} - BUY 📈\n"
                f"Technical Reason: SMA 50 > SMA 200 indicates a potential uptrend."
            )
            await send_telegram_message(message)
    else:
        await send_telegram_message("No stock recommendations based on SMA crossover criteria.")

if __name__ == '__main__':
    asyncio.run(generate_stock_alerts())
