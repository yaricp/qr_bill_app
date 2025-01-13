from loguru import logger
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from config import tg_bot_config


def get_inline_kb_yes_no(
    lang: str = tg_bot_config.TELEGRAM_BOT_DEFAULT_LANG
) -> InlineKeyboardMarkup:
    """_summary_

    Args:
        lang (str): _description_

    Returns:
        InlineKeyboardMarkup: _description_
    """
    dict_text = {
        "yes": {"ru": "Да", "en": "Yes"},
        "no": {"ru": "Нет", "en": "No"},
    }
    inline_btn_yes = InlineKeyboardButton(
        text=dict_text["yes"][lang], callback_data="yes"
    )
    inline_btn_no = InlineKeyboardButton(
        text=dict_text["no"][lang], callback_data="no"
    )

    inline_kb_yes_no = InlineKeyboardMarkup(
        inline_keyboard=[[inline_btn_yes, inline_btn_no]]
    )
    return inline_kb_yes_no
