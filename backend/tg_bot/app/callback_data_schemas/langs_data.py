from aiogram.filters.callback_data import CallbackData


class LangsData(CallbackData, prefix="lang"):
    value: str
