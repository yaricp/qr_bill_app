import os
from aiogram.types import Message, FSInputFile
from aiogram import F

from main import bot
from recognize import recognize_image
from handlers import router
from services import get_user_lang, send_bill_url
from views import result_parse_bill_view

from utils import get_logger
from config import tg_bot_config


logger = get_logger(__name__)


@router.message(F.document.func(
    lambda x: True if x and x.mime_type in [
        "application/zip",
        "application/vnd.ms-pki.stl",
        "application/octet-stream"
    ] else False
))
async def get_pic_qr_handler(message: Message):
    """_summary_

    Args:
        message (Message): _description_
    """
    user_id = str(message.from_user.id)
    file_id = str(message.document.file_id)
    file_unique_id = str(message.document.file_unique_id)
    filename = str(message.document.file_name)
    file = await bot.get_file(file_id)
    file_path = file.file_path
    user_file_path = os.path.join(
        tg_bot_config.QR_PIC_DIR, user_id,
        f"{file_unique_id}_{filename}"
    )
    await bot.download_file(file_path, user_file_path)
    user_lang = get_user_lang(user_id)

    url = recognize_image(user_file_path)
    result_bill = send_bill_url(
        url=url, user_id=user_id
    )

    await message.answer(
        result_parse_bill_view(
            text=result_bill, lang=user_lang
        ),
        parse_mode="HTML"
    )
