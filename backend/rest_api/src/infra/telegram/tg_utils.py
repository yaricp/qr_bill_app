import time

from loguru import logger

from .tg_client import delete_message, send_mess_to_client


def send_verify_link_to_tg(tg_id: int, user_link: str) -> bool:
    message = f"Use this link to verify TG: {user_link}"
    message_id = send_mess_to_client(user_id=tg_id, message=message)
    logger.info(f"Sent tg verify message with id {message_id}")
    logger.info("Start wait before delete tg message")
    time.sleep(5 * 60)
    delete_message(message_id=message_id)
    logger.info("After deleting tg message")
    return True
