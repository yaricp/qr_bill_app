# -*- coding: utf-8 -*-

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
#from telegram.ext import InlineQueryHandler
from telegram.ext import CallbackQueryHandler

from handlers import start, new_msg, button

from config import *

if development:
    import logging
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():

    updater = Updater(TOKEN, request_kwargs=REQUEST_KWARGS)
    #print(REQUEST_KWARGS)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    
    new_msg_handler = MessageHandler(Filters.all, new_msg)
    dispatcher.add_handler(new_msg_handler)

    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()

if __name__ == '__main__':
    #print(os.getcwd())
    main()
