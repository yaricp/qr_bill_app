from config import tg_bot_config


def about_view(
    lang: str = tg_bot_config.TELEGRAM_BOT_DEFAULT_LANG
) -> str:
    """
    Prepares text for about command

    Args:
        lang (str): lang user

    Returns:
        str: text
    """
    dict_text = {
        "ru": "Этот бот является расширением веб-приложения, "\
                "которое дает возможность вам проанализировать ваши покупки "\
                "в Черногории и отследить изменения цен на товары. \n\n"\
                "На данный момент этот телеграмм-бот позволяет выполнить"\
                " только некоторые функции:\n"\
                "1. Регистрация пользователя (происходит автоматически, когда"\
                " вы запускаете этот бот).\n"\
                "2. Генерация временной ссылки для входа в веб приложение.\n"\
                "3. Распознавание картинки с QR-кодом с чека покупки. "\
                "Если вы пришлете сюда фото QR-кода из чека, бот сохранит"\
                " информацию о купленных товарах для дальнейшего анализа.\n"\
                "4. Обработка ссылки зашифрованной в QR-коде покупки. "\
                "Если вы пришлете сюда текст ссылки, которая зашифрована в"\
                " QR-коде, то бот сохранит информацию о покупках для"\
                " дальшейшего анализа.\n"\
                "\nБолее расширенные возможности (сканирование чека, анализ"\
                " покупок и прочее) имеются в веб-приложении: "\
                f"{tg_bot_config.TELEGRAM_WEBAPP_ADDRESS}\n"\
                "Вы можете перейти в него сгенерировав временную ссылку "\
                " командой <b>/create_link</b>"\
                ,
        "en": "The purpose of this project is to give you the opportunity"\
            " to evaluate your purchases in Montenegro and track changes in"\
            " product prices.\n At the moment, this Telegram bot allows you to"\
            " configure only a few functions:\n"\
            "1. User registration (happens automatically when you launch this"\
            " bot).\n"\
            "2. Generating a temporary link to access the web application.\n"\
            "3. Recognizing images with a QR code when checking purchases.\n"\
            "If you send a photo of the QR code from the receipt, the bot will"\
            " save information about the purchased goods for further analysis.\n"\
            "4. Processing links encoded in the QR code of a purchase.\n"\
            "If you send the text of a link encoded in the QR code, the bot"\
            " will save information about the purchase for further analysis."\
            "\nMore advanced features (such as scanning receipts, analyzing"\
            " purchases, etc.) are available in the web application: "\
            f"{tg_bot_config.TELEGRAM_WEBAPP_ADDRESS}.\n"\
            "You can access it by generating a temporary link with the"\
            " <b>/create_link</b> command."
    }
    return dict_text[lang]
