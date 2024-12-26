from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.methods.send_message import SendMessage

from loguru import logger

from handlers import router
from callback_data_schemas import HouseCallbackData
from services import (
    save_user_current_house,
    get_user_lang,
    get_area_faces
)
from views import (
    house_view,
    geo_position_view,
    dates_view
)
from views.keyboards import get_location_kb


@router.callback_query(HouseCallbackData.filter())
async def cq_get_house_handler(
    query: CallbackQuery, callback_data: HouseCallbackData
):
    user_id = str(query.from_user.id)
    user_lang = get_user_lang(user_id)
    house_id = callback_data.id
    await query.answer(f"{ callback_data }")
    house_db = save_user_current_house(user_id, house_id)
    if not house_db:
        await SendMessage(chat_id=user_id, text="Not found")
    geo = {
            "latitude": house_db.latitude,
            "longitude": house_db.longitude,
            "altitude": house_db.altitude
        }
    needs_geo = True if None in geo.values() else False
    text = house_view(
        house_name=house_db.name,
        meshfile=house_db.meshfile,
        area_faces=get_area_faces(house_db.meshfile),
        geo=geo,
        lang=user_lang
    )
    if needs_geo:
        text += geo_position_view(lang=user_lang)
        kb = get_location_kb(user_lang)
    else:
        text += dates_view(lang=user_lang)
    await SendMessage(
        chat_id=user_id,
        text=text,
        parse_mode="HTML",
        reply_markup=kb
    )