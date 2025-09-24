from aiogram import F
from aiogram.methods.send_message import SendMessage
from aiogram.types import CallbackQuery
from callback_data_schemas import HaveMeshCallbackData
from handlers import router
from loguru import logger
from services import get_user_lang
from views import command_share_house_view, file_mesh_view


@router.callback_query(HaveMeshCallbackData.filter())
async def cq_mesh_exists_or_not_handler(
    query: CallbackQuery, callback_data: HaveMeshCallbackData
):
    user_id = str(query.from_user.id)
    user_lang = get_user_lang(user_id)
    await query.answer("OK")
    if callback_data.value == "yes":
        await SendMessage(
            chat_id=user_id, text=file_mesh_view(lang=user_lang), parse_mode="HTML"
        )
    else:
        await SendMessage(
            chat_id=user_id,
            text=command_share_house_view(lang=user_lang),
            parse_mode="HTML",
        )
