from config import tg_bot_config


def about_view(
    lang: str = tg_bot_config.TELEGRAM_BOT_DEFAULT_LANG
) -> str:
    """
    Prepares text for start commND

    Args:
        name (str): name user

    Returns:
        str: text
    """
    dict_text = {
        "ru": " Идея этого проекта заключается в том чтобы "\
                "распознать QR код чека, получить ссылку на фискальную службу "\
                " и получить список купленных товаров",
        "en": ""
    }
    return dict_text[lang] + "\n\n/start"
