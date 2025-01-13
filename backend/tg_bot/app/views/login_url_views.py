from config import tg_bot_config


def login_url_created_view(
    url: str,
    time_expiry: int,
    lang: str = tg_bot_config.TELEGRAM_BOT_DEFAULT_LANG
) -> str:
    """
    Prepares text created login url

    Args:
        name (str): name user

    Returns:
        str: text
    """
    dict_text = {
        "ru": "Используй эту временную ссылку для авторизации в веб"\
            f' приложении: <a href="{url}">{url}</a> \n'\
            f"Она активна только {time_expiry} минут.",
        "en": "Use this link to log in to the web application: "\
            f"<a href='{url}'>{url}</a>\n"\
            f"It will be active for {time_expiry} minutes.",
    }
    return dict_text[lang]
