# -*- coding: utf-8 -*-
import time
import logging
from uuid import uuid4

from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent
from telegram import ParseMode, ReplyKeyboardRemove

from config import *
#from models.wait import Wait
from store.models.seller import Seller
from utils import *


def search_seller(update, context):
    """Handle the inline query."""
    query = update.inline_query.query
    user, query_id = get_update_data(update)

    print('QUERY: ', query)
    
    sellers = Seller.select().where(Seller.user==user)
    print("SELLER: ", sellers)
    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title=s.name,
            input_message_content=InputTextMessageContent(
                s.name )) for s in sellers]

