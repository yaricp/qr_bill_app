from aiogram import F
from aiogram.types import Location, Message, ReplyKeyboardRemove
from handlers import router
from services import get_user_lang, save_geoposition
from utils import get_logger
from views import ask_altitude_view

logger = get_logger(__name__)


@router.message(F.location)
async def get_tg_location_handler(
    message: Message,
):
    """_summary_

    Args:
        message (Message): _description_
    """
    user_id = str(message.from_user.id)
    logger.info(f"Location: {message.__dict__}")
    location = message.location
    float_coordinates = [location.latitude, location.longitude]
    house_db = save_geoposition(user_id=user_id, coordinates=float_coordinates)
    user_lang = get_user_lang(user_id)
    await message.reply(
        ask_altitude_view(lang=user_lang),
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove(),
    )
