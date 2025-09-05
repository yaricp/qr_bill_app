from uuid import UUID
from loguru import logger
from datetime import datetime, timedelta


def is_valid_uuid(uuid_to_test, version=4):
    """
    Check if uuid_to_test is a valid UUID.

     Parameters
    ----------
    uuid_to_test : str
    version : {1, 2, 3, 4}

     Returns
    -------
    `True` if uuid_to_test is a valid UUID, otherwise `False`.

     Examples
    --------
    >>> is_valid_uuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a')
    True
    >>> is_valid_uuid('c9bf9e58')
    False
    """

    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


def get_last_day_of_month_by_datetime(datetime_for: datetime) -> datetime:
    next_month = datetime_for.replace(day=28) + timedelta(days=4)
    res = next_month - timedelta(days=next_month.day)
    return res


def get_fisrt_day_month_by_delta_month(delta_month: int) -> datetime:
    current_year = datetime.now().year
    logger.info(f"current_year: {current_year}")
    current_month = datetime.now().month
    logger.info(f"current_month: {current_month}")
    result_year = current_year - (
        1 if (current_month - abs(delta_month)) <= 0 else 0
    )
    logger.info(f"result_year: {result_year}")
    result_month = current_month - abs(delta_month) if (
        current_month - abs(delta_month)
    ) > 0 else 12 - abs(current_month - abs(delta_month))
    logger.info(f"result_month: {result_month}")
    return datetime(result_year, result_month, 1)
