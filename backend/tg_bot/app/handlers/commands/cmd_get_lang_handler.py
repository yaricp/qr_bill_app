from asyncio import sleep
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from utils import get_logger
from handlers import router
from services import set_user_lang, get_user_lang
from views import result_lang_view, error_lang_view


logger = get_logger(__name__)


@router.message(
    Command("lang"),
)
async def cmd_get_lang_handler(
    message: Message
):
    """_summary_

    Args:
        message (Message): _description_
    """
    user_id = message.from_user.id
    user_lang = await get_user_lang(user_id)

    ans = await message.answer(
        result_lang_view(lang=user_lang)
    )

    await message.delete()
    await sleep(60)
    await ans.delete()
