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
    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.create_task(send_message())
    else:
        asyncio.run(send_message())
