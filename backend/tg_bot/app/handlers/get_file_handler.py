import os

from aiogram import F
from aiogram.types import FSInputFile, Message
from config import tg_bot_config
from handlers import router
from main import bot
from recognize import recognize_image
from services import get_user_lang, send_bill_url
from utils import get_logger
from views import result_parse_bill_view

logger = get_logger(__name__)


@router.message(F.photo)
async def get_pic_qr_handler(message: Message):
    """_summary_

    Args:
        message (Message): _description_
    """
    user_id = message.from_user.id
    logger.info(f"message.photo: {message.photo}")
    file_id = str(message.photo[-1].file_id)
    file_unique_id = str(message.photo[-1].file_unique_id)
    file = await bot.get_file(file_id)
    file_path = file.file_path

    user_file_path = os.path.join(tg_bot_config.TELEGRAM_QR_PIC_DIR, str(user_id))
    # f"{file_unique_id}"
    if not os.path.exists(user_file_path):
        os.makedirs(user_file_path)

    user_file_fullname = os.path.join(user_file_path, file_unique_id)
    await bot.download_file(file_path, user_file_fullname)

    # picture = FSInputFile(user_file_fullname)
    # await message.reply_photo(picture)

    url = recognize_image(user_file_fullname)
    logger.info(f"url : {url}")
    if not url:
        await message.answer("Maybe its not a QR of bill.")
    result_bill = await send_bill_url(url=url, user_id=user_id)
    user_lang = await get_user_lang(user_id)
    await message.answer(
        result_parse_bill_view(text=result_bill, lang=user_lang), parse_mode="HTML"
    )
