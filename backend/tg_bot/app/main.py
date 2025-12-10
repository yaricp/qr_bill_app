"""
BOT
"""

import asyncio
import os

from aiogram import Bot, Dispatcher
from config import tg_bot_config
from utils import get_logger

# from loguru import logger


logger = get_logger(__name__)
logger.info(f"Python path: {os.getcwd()}")

bot = Bot(token=tg_bot_config.TELEGRAM_BOT_TOKEN)

from handlers import router

dp = Dispatcher()


async def main():
    """_summary_"""
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
