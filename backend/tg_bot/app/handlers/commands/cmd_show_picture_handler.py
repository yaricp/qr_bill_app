from aiogram import Router
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message
from handlers import router
from services import get_user_current_house, get_user_lang
from utils import get_logger
from views import short_picture_answer_view

logger = get_logger(__name__)


@router.message(
    Command("show_mesh"),
)
async def cmd_show_picture_handler(message: Message):
    user_id = str(message.from_user.id)
    user_lang = get_user_lang(user_id)
    house_db = get_user_current_house(user_id)
    picture = FSInputFile(house_db.picture)
    user_lang = get_user_lang(user_id)
    await message.reply_photo(picture)
    await message.answer(short_picture_answer_view(lang=user_lang), parse_mode="HTML")
