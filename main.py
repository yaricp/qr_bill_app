# -*- coding: utf-8 -*-

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
#from telegram.ext import InlineQueryHandler
from telegram.ext import CallbackQueryHandler

from handlers import (  new_category, 
                        new_msg, 
                        new_seller, 
                        list_purchase, 
                        button, 
                        list_orders, 
                        menu)

from config import *

if development:
    import logging
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():

    updater = Updater(TOKEN, request_kwargs=REQUEST_KWARGS)
    print(REQUEST_KWARGS)
    dispatcher = updater.dispatcher
    
    menu_handler = CommandHandler('menu', menu)
    dispatcher.add_handler(menu_handler)

    new_category_handler = CommandHandler('new_category', new_category)
    dispatcher.add_handler(new_category_handler)
    
    new_seller_handler = CommandHandler('new_seller', new_seller)
    dispatcher.add_handler(new_seller_handler)
    
    list_purchase_handler = CommandHandler('list', list_purchase)
    dispatcher.add_handler(list_purchase_handler)
    
    orders_handler = CommandHandler('orders', list_orders)
    dispatcher.add_handler(orders_handler)
    
    new_msg_handler = MessageHandler(Filters.all, new_msg)
    dispatcher.add_handler(new_msg_handler)

    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()

if __name__ == '__main__':
    #print(os.getcwd())
    main()
