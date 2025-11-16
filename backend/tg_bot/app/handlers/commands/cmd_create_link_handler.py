from asyncio import sleep

from aiogram.filters import Command
from aiogram.types import Message
from handlers import router
from services import get_login_url, get_time_expiry_login_url, get_user_lang
from utils import get_logger
from views import login_url_created_view

logger = get_logger(__name__)


@router.message(
    Command("create_link"),
)
async def cmd_create_link_handler(message: Message):
    user_id = message.from_user.id
    url = await get_login_url(user_id)
    time_expiry = get_time_expiry_login_url()
    user_lang = await get_user_lang(user_id)
    reply_mess = await message.answer(
        login_url_created_view(url=url, time_expiry=time_expiry, lang=user_lang),
        parse_mode="HTML",
    )
    logger.info(f"Here we wait for {time_expiry} sec")
    await message.delete()
    await sleep(time_expiry * 60)
    await reply_mess.delete()
