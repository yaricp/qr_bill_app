from asyncio import sleep
from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.methods.send_message import SendMessage

from loguru import logger

from handlers import router
from callback_data_schemas import LangsData
from services import set_user_lang, get_user_lang
from views import result_lang_view

from main import bot


@router.callback_query(LangsData.filter())
async def cq_change_lang_handler(
    query: CallbackQuery, callback_data: LangsData
):
    user_id = query.from_user.id
    logger.info(f"query.message.__dict__: {query.message.__dict__}")
    user_lang = await get_user_lang(user_id)
    lang = callback_data.value
    logger.info(f"callback_data: {callback_data}")
    logger.info(f"lang: {lang}")
    result = await set_user_lang(user_id=user_id, lang=lang)
    logger.info(f"result: {result}")
    if result != user_lang:
        await query.answer(result_lang_view(lang=result["lang"]))
        mess = await bot.send_message(
            chat_id=user_id,
            text=result_lang_view(
                lang=result["lang"],
                changed=True
            ),
            parse_mode="HTML"
        )
        await bot.delete_message(
            chat_id=user_id,
            message_id=query.message.message_id
        )
    else:
        await query.answer(result_lang_view(lang=user_lang))
        mess = await bot.send_message(
            chat_id=user_id,
            text=result_lang_view(lang=user_lang),
            parse_mode="HTML"
        )
        await bot.delete_message(
            chat_id=user_id,
            message_id=query.message.message_id
        )

    await sleep(60)
    await mess.delete()
