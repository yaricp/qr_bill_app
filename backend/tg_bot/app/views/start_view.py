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
        "ru": f"Привет {name}!  Этот бот можно использовать для расчетов"\
            " количества солнечной энергии получаемой на поверхностях"\
            " зданий.\n"\
            " Для начала расчета пришлите команду <b>/start_calc</b>\n\n"\
            " Для просмотра списка команд пришлите /help",
        "en": f"Hello {name}! You can use this bot for calculate"\
            " solar power on surfaces of a buildings.\n"\
            " For start calculation send <b>/start_calc</b>\n\n"\
            " For see list commands send /help",
    }
    return dict_text[lang]
