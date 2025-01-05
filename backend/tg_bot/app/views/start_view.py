from config import tg_bot_config


def start_view(
    name: str, lang: str = tg_bot_config.TELEGRAM_BOT_DEFAULT_LANG
) -> str:
    """
    Prepares text for start commND

    Args:
        name (str): name user

    Returns:
        str: text
    """
    dict_text = {
        "ru": f"Привет {name}!  Этот бот можно использовать для сбора "\
            " статистики ваших покупок в Черногории.\n"\
            " Вы можете отправлять сюда фото QR кодов которые есть на чеках,"\
            " которые выдают на кассе магазинов или на счетах в кафе и"\
            " ресторанах.\n"\
            " вы также можете прислать сюда саму ссылку отсканировав код"\
            " самостоятельно.\n"
            " Так же Вы можете открыть веб приложение через временную"\
            " ссылку для входа, которую Вы можете получить нажав: "\
            "<b>/create_link</b>\n\n"\
            " Для просмотра списка команд нажмите: <b>/help</b>"\
            " Чтобы ознакомиться с проектом нажите: <b>/about</b>",
        "en": f"Hello {name}! You can use this bot for calculate"\
            " solar power on surfaces of a buildings.\n"\
            " For start calculation send <b>/start_calc</b>\n\n"\
            " For see list commands send /help",
    }
    return dict_text[lang]
