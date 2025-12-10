from asyncio import sleep

from aiogram.filters import Command
from aiogram.types import Message
from handlers import router
from services import get_or_create_user, get_user_lang
from utils import get_logger
from views import start_view

logger = get_logger(__name__)


@router.message(
    Command("start"),
)
async def cmd_start_handler(message: Message):
    tg_user_id = message.from_user.id
    name = str(message.from_user.id)
    logger.info(f"type of tg_user_id: {type(tg_user_id)}")
    if message.from_user.username:
        name = message.from_user.username
    await get_or_create_user(tg_user_id)
    user_lang = await get_user_lang(tg_user_id)
    await message.answer(start_view(name, lang=user_lang), parse_mode="HTML")
    await message.delete()
