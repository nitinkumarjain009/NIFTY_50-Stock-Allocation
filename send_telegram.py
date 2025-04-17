from telegram import Bot
import asyncio
import os

async def send_message():
    bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
    await bot.send_message(
        chat_id=os.getenv('TELEGRAM_CHAT_ID'),
        text='Stock Recommendations Generated: Check the latest output from recommendation.py'
    )

if __name__ == "__main__":
    asyncio.run(send_message())
