import os
# import logging
from loguru import logger

from config import tg_bot_config


def get_logger(name_module):
    """_summary_

    Args:
        name_module (_type_): _description_

    Returns:
        _type_: _description_
    """
    # logging.basicConfig(level=logging.INFO)
    # return logging.getLogger(name_module)
    return logger
