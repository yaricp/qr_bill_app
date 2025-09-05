from loguru import logger


def get_logger(name_module: str):
    """_summary_

    Args:
        name_module (_type_): _description_

    Returns:
        _type_: _description_
    """
    # logging.basicConfig(level=logging.INFO)
    # return logging.getLogger(name_module)
    return logger
