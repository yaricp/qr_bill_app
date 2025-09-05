from aiogram import Router

router = Router()

from .commands import *
from .callback_queries import *

from .get_url_handler import get_url_handler
from .get_file_handler import get_pic_qr_handler
