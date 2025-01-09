from aiogram import Router

from aiogram.filters import Command
from aiogram.types import Message

from utils import get_logger
from handlers import router
from services import get_user_lang
from views import about_view


logger = get_logger(__name__)


@router.message(
    Command("about"),
)
async def cmd_about_handler(message: Message):
    user_id = str(message.from_user.id)
    user_lang = await get_user_lang(user_id)
    await message.answer(
        about_view(lang=user_lang), parse_mode="HTML"
    )
