from config import tg_bot_config


def change_lang_view(lang: str = tg_bot_config.TELEGRAM_BOT_DEFAULT_LANG) -> str:
    """_summary_

    Args:
        lang (str): _description_

    Returns:
        str: _description_
    """
    dict_text = {"ru": "Выберите ваш язык:", "en": "Choose your language"}
    return dict_text[lang]
