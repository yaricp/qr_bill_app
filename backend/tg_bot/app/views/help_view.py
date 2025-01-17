from config import tg_bot_config


def help_view(
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
        "ru": " <b>Команды:</b>\n"\
            " <b>/start</b> - стартовая страница.\n"\
            " <b>/create_link</b> - генерит новую временную ссылку для входа"\
            f" в веб-приложение {tg_bot_config.TELEGRAM_WEBAPP_ADDRESS}."\
            " Спомощью этой ссылки Вы можете зайти"\
            " в аккаунт приложения и сменить логин и пароль\n"\
            " <b>/lang</b> - показывает текущий язык.\n"\
            " <b>/change_lang</b> - меняет язык.\n"\
            " <b>/help</b> - показывает список команд.\n"\
            " <b>/about</b> - описание проекта.\n",
        "en": " <b>Commands:</b>\n"\
            " <b>/start</b> - shows start page.\n"\
            " <b>/create_link</b> - generates a new temporary link for "\
            f" logging into the web app at {tg_bot_config.TELEGRAM_WEBAPP_ADDRESS}."\
            " You can use it to change the login and password for your account.\n"\
            " <b>/lang</b> - shows current language.\n"\
            " <b>/change_lang</b> - changes language.\n"\
            " <b>/help</b> - shows list commands.\n"\
            " <b>/about</b> - about this project.\n"
    }
    return dict_text[lang]
