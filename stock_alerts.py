import pandas as pd
import telegram
import os

# Load the data
try:
    df = pd.read_csv('data/processed.csv')
except FileNotFoundError:
    print("Error: data/processed.csv not found.")
    exit()

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
            one_year_return = f"{row['1Y_Return'] * 100:.1f}%"
            volatility = f"{row['Volatility']:.2f}"

            message = (
                f"📈 Stock Recommendation for {ticker} 📈\n"
                f"✅ SMA 50 is above SMA 200 indicating a potential uptrend.\n"
                f"💰 1 Year Return: {one_year_return}\n"
                f"⚠️ Volatility: {volatility}"
            )
            await send_telegram_message(message)
    else:
        await send_telegram_message("No stock recommendations based on SMA crossover criteria.")

if __name__ == '__main__':
    import asyncio
    asyncio.run(generate_stock_alerts())
