from config import tg_bot_config


def result_lang_view(
    lang: str = tg_bot_config.TELEGRAM_BOT_DEFAULT_LANG, changed: bool = False
) -> str:
    """_summary_

    Args:
        lang (str): _description_

    Returns:
        str: _description_
    """
    if changed:
        dict_text = {
            "ru": f"Вы сменили язык на: {lang}",
            "en": f"You have selected the language: {lang}",
        }
        return dict_text[lang]
    dict_text = {"ru": f"Ваш язык: {lang}", "en": f"Your language: {lang}"}
    return dict_text[lang]
