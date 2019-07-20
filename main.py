# -*- coding: utf-8 -*-

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
#from telegram.ext import InlineQueryHandler
from telegram.ext import CallbackQueryHandler

from init_db import initialize_db

from handlers import (  new_category, 
                        new_msg, 
                        new_seller, 
                        list_purchase,
                        purchase, 
                        list_seller,
                        list_category,
                        button, 
                        list_orders, 
                        by_category, 
                        by_seller,
                        help, 
                        about, 
                        donate, 
                        menu, 
                        start, 
                        change_lang, 
                        langs)

from config import *

#if development:
import logging
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
    
    print('TOKEN: ', TOKEN)

    updater = Updater(TOKEN, request_kwargs=REQUEST_KWARGS)
    dispatcher = updater.dispatcher
    
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    
    menu_handler = CommandHandler('menu', menu)
    dispatcher.add_handler(menu_handler)
    
    lang_handler = CommandHandler('lang', change_lang)
    dispatcher.add_handler(lang_handler)
    
    langs_handler = CommandHandler('langs', langs)
    dispatcher.add_handler(langs_handler)

    new_category_handler = CommandHandler('new_category', new_category, pass_args=True)
    dispatcher.add_handler(new_category_handler)
    
    new_seller_handler = CommandHandler('new_seller', new_seller, pass_args=True)
    dispatcher.add_handler(new_seller_handler)
    
    list_purchase_handler = CommandHandler('purchases', list_purchase)
    dispatcher.add_handler(list_purchase_handler)
    
    purchase_handler = CommandHandler('purchase', purchase, pass_args=True)
    dispatcher.add_handler(purchase_handler)
    
    list_seller_handler = CommandHandler('sellers', list_seller)
    dispatcher.add_handler(list_seller_handler)
    
    list_category_handler = CommandHandler('categories', list_category)
    dispatcher.add_handler(list_category_handler)
    
    orders_handler = CommandHandler('orders', list_orders)
    dispatcher.add_handler(orders_handler)
    
    by_categories_handler = CommandHandler('by_category', by_category)
    dispatcher.add_handler(by_categories_handler)
    
    by_sellers_handler = CommandHandler('by_seller', by_seller)
    dispatcher.add_handler(by_sellers_handler)
    
    help_handler = CommandHandler('help', help)
    dispatcher.add_handler(help_handler)
    
    about_handler = CommandHandler('about', about)
    dispatcher.add_handler(about_handler)
    
    donate_handler = CommandHandler('donate', donate)
    dispatcher.add_handler(donate_handler)
    
    new_msg_handler = MessageHandler(Filters.all, new_msg)
    dispatcher.add_handler(new_msg_handler)

    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()

if __name__ == '__main__':
    initialize_db()
    main()
