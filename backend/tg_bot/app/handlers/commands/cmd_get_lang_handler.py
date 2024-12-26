from aiogram import Router

from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from utils import get_logger
from handlers import router
from services import save_language, get_user_lang
from views import result_lang_view, error_lang_view


logger = get_logger(__name__)


@router.message(
    Command("lang"),
)
async def cmd_get_lang_handler(
    message: Message,
    command: CommandObject
):
    """_summary_

    Args:
        message (Message): _description_
    """
    user_id = str(message.from_user.id)
    user_lang = get_user_lang(user_id)
    lang = command.args

    if not lang:
        await message.answer(result_lang_view(user_lang))
        return

    lang = lang.replace("'", "").replace('"', '')
    logger.info(f"lang: {lang}")
    if lang != "en" and lang != "ru":
        await message.answer(error_lang_view(user_lang))
        return
    result = save_language(user_id=user_id, lang=lang)
    if result:
        await message.answer(result_lang_view(lang))
        return
    await message.answer("Error!")