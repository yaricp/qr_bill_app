from datetime import datetime
from aiogram.types import Message, FSInputFile
from aiogram import F

from . import router
from views import result_parse_bill_view
from services import send_bill_url, get_user_lang

from utils import get_logger
# from ..config import tg_bot_config


logger = get_logger(__name__)


@router.message(
    F.text.regexp(
        r"((http|https)://)(www.)?" +
        "[a-zA-Z0-9@:%._\\+~#?&//=]" +
        "{2,256}\\.[a-z]" +
        "{2,6}\\b([-a-zA-Z0-9@:%" +
        "._\\+~#?&//=]*)"
    )
)
async def get_url_handler(message: Message):
    """_summary_

    Args:
        message (Message): _description_
    """

    logger.info(f"text: {message.text}")
    user_id = message.from_user.id
    user_lang = get_user_lang(user_id)
    result_bill = send_bill_url(
        url=message.text, user_id=user_id
    )

    await message.answer(
        result_parse_bill_view(
            text=result_bill, lang=user_lang
        ),
        parse_mode="HTML"
    )
