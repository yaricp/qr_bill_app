import sys

import telebot
from loguru import logger
from telebot import types

from .config import telegram_config
from .metrics.telegram_metrics import metric_telegram_send

token = telegram_config.TELEGRAM_BOT_TOKEN


@metric_telegram_send
def send_mess_to_admin(message: str) -> bool:
    """
    Sends message to telegram chat.

    Parameters:
        message(str): message for chat

    Returns:
        (bool): was sends  successful or not
    """
    admin_chat_id = telegram_config.TELEGRAM_ADMIN_CHAT_ID
    try:
        tb = telebot.TeleBot(token)
        tb.send_message(admin_chat_id, message)
    except Exception as e:
        logger.warning(f"Error {e} while sending notification {message}")
        raise e
    return True


@metric_telegram_send
def send_mess_to_client(user_id: int, message: str, filepath: str = "") -> int:
    """
    Sends message to reg telegram bot.

    Parameters:
        user_id(str): User ID in telegram
        message(str): message for chat

    Returns:
        (bool): was sends  successful or not
    """
    try:
        tb = telebot.TeleBot(token)
        if filepath:
            try:
                logger.info("Sending file")
                return tb.send_document(
                    chat_id=user_id,
                    document=open(filepath, "rb"),
                    caption="Готово!",
                )
            except Exception as e:
                logger.error(
                    f"Error {e} while sending file {filepath} to client {user_id}"
                )
                raise e
        logger.info("sending message")
        return tb.send_message(user_id, message)
    except Exception as e:
        logger.error(f"Error {e} while sending {message} to client {user_id}")
        raise e


@metric_telegram_send
def delete_message(message_id: int) -> bool:
    tb = telebot.TeleBot(token)
    try:
        tb.delete_message(chat_id=message_id)
        return True
    except Exception as err:
        logger.error(f"Error: {err}")
        raise err


if __name__ == "__main__":
    msg = sys.argv[1]
    send_mess_to_admin(msg)
