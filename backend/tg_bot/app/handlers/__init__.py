from aiogram import Router

router = Router()

from .commands.cmd_start_handler import cmd_start_handler
from .commands.cmd_create_link_handler import cmd_create_link_handler

from .get_url_handler import get_url_handler
from .get_file_handler import get_pic_qr_handler
