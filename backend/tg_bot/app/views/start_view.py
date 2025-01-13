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
            " Вы можете отправлять сюда фото QR кодов, которые есть на чеках,"\
            " которые выдают на кассе магазинов или на счетах в кафе и"\
            " ресторанах.\n"\
            " Вы также можете прислать сюда саму ссылку, отсканировав код"\
            " самостоятельно.\n"
            " Так же Вы можете открыть веб приложение через временную"\
            " ссылку для входа, которую Вы можете получить нажав: "\
            "<b>/create_link</b>\n\n"\
            " Для просмотра списка команд нажмите: <b>/help</b>"\
            " Чтобы ознакомиться с проектом нажите: <b>/about</b>",
        "en": f"Hello {name}! This bot can be used to collect statistics"\
            " about your purchases in Montenegro.\n"\
            "You can send photos of QR codes found on receipts issued at "\
            "store checkouts or on bills in cafes and restaurants.\n"\
            "Alternatively, you can send the link itself by scanning the code"\
            " manually.\n\n"
            "You can also open the web application using a temporary login"\
            " link, which you can generate by clicking: <b>/create_link</b>.\n"\
            "To view the list of commands, click: <b>/help</b>.\n"\
            "To learn more about the project, click: <b>/about</b>.",
    }
    return dict_text[lang]
