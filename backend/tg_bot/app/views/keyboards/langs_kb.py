from loguru import logger
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from callback_data_schemas import LangsData
from config import tg_bot_config


def get_inline_kb_langs() -> InlineKeyboardMarkup:
    """_summary_

    Args:
        lang (str): _description_

    Returns:
        InlineKeyboardMarkup: _description_
    """
    btn_list = []
    for item in tg_bot_config.TELEGRAM_LANGUAGES:
        inline_btn = InlineKeyboardButton(
            text=item, callback_data=LangsData(
                value=item
            ).pack()
        )
        btn_list.append(inline_btn)
    inline_kb_langs = InlineKeyboardMarkup(
        inline_keyboard=[btn_list]
    )
    return inline_kb_langs
