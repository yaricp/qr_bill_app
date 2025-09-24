from asyncio import sleep

from aiogram.filters import Command
from aiogram.types import Message
from handlers import router
from services import get_user_lang
from utils import get_logger
from views import change_lang_view, get_inline_kb_langs

logger = get_logger(__name__)


@router.message(
    Command("change_lang"),
)
async def cmd_change_lang_handler(message: Message):
    """_summary_

    Args:
        message (Message): _description_
    """
    user_id = message.from_user.id
    user_lang = await get_user_lang(user_id)

    await message.answer(
        change_lang_view(user_lang),
        parse_mode="HTML",
        reply_markup=get_inline_kb_langs(),
    )
    await message.delete()
