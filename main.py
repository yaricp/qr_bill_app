# -*- coding: utf-8 -*-

from telegram.ext import Updater
#from telegram.ext.picklepersistence import PicklePersistence
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters, ConversationHandler
#from telegram.ext import InlineQueryHandler
from telegram.ext import CallbackQueryHandler

from init_db import initialize_db
from utils import *
from config import *

from handlers import (  new_category, 
                        #new_msg, 
                        new_photo,
                        new_video, 
                        new_text,  
                        change_seller_category, 
                        new_seller, 
                        list_purchase,
                        purchase, 
                        del_purchase, 
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
                        langs, 
                        set_location, 
                        cancel)

from config import *

if development:
    import logging
    logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
    
    print('TOKEN: ', TOKEN)
    #persistence = PicklePersistence(filename='work_data')
    updater = Updater(
        TOKEN, 
        request_kwargs=REQUEST_KWARGS, 
        use_context=True, 
        )
    dispatcher = updater.dispatcher

    
    new_summ_handler = MessageHandler(Filters.regex('^\d\d\d \d\d$'), new_text)
    new_fn_handler = MessageHandler(Filters.regex('^&fn='), new_text)
    new_photo_handler = MessageHandler(Filters.photo, new_photo)
    new_video_handler = MessageHandler(Filters.video, new_video)
    cancel_handler = CommandHandler('cancel', cancel)
    location_handler = MessageHandler(
                            Filters.location, 
                            set_location, 
                            edited_updates=True, 
                            pass_user_data=True)
    
    new_bill_handler = ConversationHandler(
        name='new_bill_conv', 
        entry_points=[
                    new_summ_handler, 
                    new_fn_handler, 
                    new_photo_handler, 
                    new_video_handler
                    ],
        states={
            LOCATION: [location_handler, ],
            SELLER: [CallbackQueryHandler(  change_seller_category, 
                                            pattern='change_seller', 
                                            pass_user_data=True )], 
            CATEGORY: [CallbackQueryHandler(change_seller_category, 
                                            pattern='change_category')]
            }, 
        fallbacks=[cancel_handler, ], 
        allow_reentry=True, 
        persistent=True
    )
    #
    dispatcher.add_handler(new_bill_handler)


#    location_handler = MessageHandler(
#                            Filters.location, 
#                            set_location, 
#                            edited_updates=True)
#    dispatcher.add_handler(location_handler)
    
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
    
    del_purchase_handler = CommandHandler('del_purchase', del_purchase, pass_args=True)
    dispatcher.add_handler(del_purchase_handler)
    
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
    
#    new_msg_handler = MessageHandler(Filters.text, new_text)
#    dispatcher.add_handler(new_msg_handler)
#    
#    new_photo_handler = MessageHandler(Filters.photo, new_photo)
#    dispatcher.add_handler(new_photo_handler)
    
#    new_video_handler = MessageHandler(Filters.video, new_video)
#    dispatcher.add_handler(new_video_handler)

    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()

if __name__ == '__main__':
    initialize_db()
    main()
