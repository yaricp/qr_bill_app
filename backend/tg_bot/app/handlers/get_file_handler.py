from aiogram.types import Message, FSInputFile
from aiogram import F

from handlers import router
# from services import (
#     get_mesh_file,
#     create_or_update_house,
#     create_save_picture_house,
#     get_user_lang,
#     get_count_faces
# )
# from views import (
#     short_picture_answer_view,
#     picture_view, geo_position_view,
#     too_much_faces_view,
# )

# from utils import get_logger
from config import tg_bot_config
from loguru import logger


# logger = get_logger(__name__)


@router.message(F.document.func(
    lambda x: True if x and x.mime_type in [
        "application/zip",
        "application/vnd.ms-pki.stl",
        "application/octet-stream"
    ] else False
))
async def get_file_mesh_handler(message: Message):
    """_summary_

    Args:
        message (Message): _description_
    """
    tg_user_id = str(message.from_user.id)
    username = str(message.from_user.username)
    file_id = str(message.document.file_id)
    file_unique_id = str(message.document.file_unique_id)
    filename = str(message.document.file_name)
    user_file_path, check_sum_file = await get_mesh_file(
        user_id=tg_user_id,
        file_id=file_id,
        file_unique_id=file_unique_id,
        filename=filename
    )

    house_db = create_or_update_house(
        user_id=tg_user_id,
        user_file_path=user_file_path,
        check_sum_file=check_sum_file
    )
    user_lang = get_user_lang(tg_user_id)
    count_faces = get_count_faces(user_file_path)
    logger.info(f"Count faces: {count_faces}")
    if count_faces > config.max_count_faces:
        await message.answer(
            too_much_faces_view(lang=user_lang)
        )
        return
    picture_path = create_save_picture_house(house_db.id)
    picture = FSInputFile(picture_path)
    
    await message.reply_photo(picture)
    await message.answer(
        short_picture_answer_view(lang=user_lang), parse_mode="HTML"
    )
    await message.answer(
        geo_position_view(lang=user_lang), parse_mode="HTML"
    )
