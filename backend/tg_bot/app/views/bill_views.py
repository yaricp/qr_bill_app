from config import tg_bot_config


def result_parse_bill_view(
    text: str, lang: str = tg_bot_config.TELEGRAM_BOT_DEFAULT_LANG
) -> str:
    """
    Prepares text for start commND

    Args:
        name (str): name user

    Returns:
        str: text
    """
    dict_text = {
        "ru": f"Вот твой счет: {text}!",
        "en": f"Here you bill {text}!",
    }
    return dict_text[lang]
