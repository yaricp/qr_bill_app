from datetime import datetime

from aiogram import F
from aiogram.types import FSInputFile, Message
from services import get_user_lang, send_bill_url
from utils import get_logger
from views import result_parse_bill_view

from . import router

# from ..config import tg_bot_config


logger = get_logger(__name__)


@router.message(
    F.text.regexp(
        r"((http|https)://)(www.)?"
        + "[a-zA-Z0-9@:%._\\+~#?&//=]"
        + "{2,256}\\.[a-z]"
        + "{2,6}\\b([-a-zA-Z0-9@:%"
        + "._\\+~#?&//=]*)"
    )
)
async def get_url_handler(message: Message):
    """_summary_

    Args:
        message (Message): _description_
    """

    logger.info(f"get_url_handler text: {message.text}")
    user_id = message.from_user.id
    result_bill = await send_bill_url(url=message.text, user_id=user_id)
    user_lang = await get_user_lang(user_id)

    await message.answer(
        result_parse_bill_view(text=result_bill, lang=user_lang), parse_mode="HTML"
    )
