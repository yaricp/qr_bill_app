from config import tg_bot_config


def error_lang_view(
    lang: str = tg_bot_config.TELEGRAM_BOT_DEFAULT_LANG
) -> str:
    """_summary_

    Args:
        lang (str, optional): _description_. Defaults to "ru".

    Returns:
        str: _description_
    """
    dict_text = {
        "ru": "Укажите /lang ru или /lang en",
        "en": "Write /lang ru or /lang en"
    }
    return dict_text[lang]
