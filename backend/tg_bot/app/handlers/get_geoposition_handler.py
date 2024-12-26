from aiogram.types import Message
from aiogram import F

from handlers import router
from services import save_geoposition, get_user_lang
from views import dates_view


@router.message(F.text.regexp(
    r"^(-?\d+(\.\d+)?),\s*(-?\d+(\.\d+)?),\s*(-?\d+(\.\d+)?)$"
))
async def get_geoposition_handler(
    message: Message,
):
    """_summary_

    Args:
        message (Message): _description_
    """
    user_id = str(message.from_user.id)
    text_coordinates = message.text.replace(" ", "").split(",")
    float_coordinates = [float(x) for x in text_coordinates]
    coordinates = float_coordinates[:1]
    altitude = 0
    if len(float_coordinates) == 3:
        altitude = float_coordinates[-1]
    house_db = save_geoposition(
        user_id=user_id,
        coordinates=float_coordinates,
        altitude=altitude
    )
    user_lang = get_user_lang(user_id)
    await message.reply(dates_view(lang=user_lang), parse_mode="HTML")
