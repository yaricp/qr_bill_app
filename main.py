# -*- coding: utf-8 -*-

from telegram.ext import Updater
from telegram.ext.picklepersistence import PicklePersistence
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters, ConversationHandler
#from telegram.ext import InlineQueryHandler
from telegram.ext import CallbackQueryHandler

from store.init_db import initialize_db
from utils import *
from config import *

from handlers.callbacks import *
from handlers.commands import *
from handlers.messages import *


if development:
    import logging
    logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
    
    print('TOKEN: ', TOKEN)
    my_persistence = PicklePersistence(filename='work_data')
    updater = Updater(
        TOKEN, 
        request_kwargs=REQUEST_KWARGS, 
        persistence=my_persistence,
        use_context=True, 
        )
    dispatcher = updater.dispatcher

    
    new_summ_handler = MessageHandler(Filters.regex('^\d\d\d \d\d$'), new_text)
    new_fn_handler = MessageHandler(Filters.regex('.*&fn='), new_text)
    new_photo_handler = MessageHandler(Filters.photo, new_photo)
    new_video_handler = MessageHandler(Filters.video, new_video)
    cancel_handler = CommandHandler('cancel', cancel)
    
    
    bill_location_handler = MessageHandler(
                            Filters.location, 
                            set_location)
                            
    change_seller_handler = CallbackQueryHandler(  
                                            change_seller_category_purchase, 
                                            pattern='change_seller'
                                            )
    show_all_sellers_handler = CallbackQueryHandler(  
                                            show_all_sellers, 
                                            pattern='show_all_sellers'
                                            )
    change_category_handler = CallbackQueryHandler(  
                                            change_seller_category_purchase, 
                                            pattern='change_category'
                                            )
    add_seller_purchase_handler = CallbackQueryHandler(  
                                            add_seller_category_purchase, 
                                            pattern='new_seller&purchase'
                                            )
    add_category_purchase_handler = CallbackQueryHandler(  
                                            add_seller_category_purchase, 
                                            pattern='new_category&purchase'
                                            )
    show_menu_handler = CallbackQueryHandler( menu, 
                                            pattern='menu'
                                            )
    
    
    new_bill_handler = ConversationHandler(
        name='new_bill_conv', 
        entry_points=[
                    new_summ_handler, 
                    new_fn_handler, 
                    new_photo_handler, 
                    new_video_handler
                    ],
        states={
            LOCATION: [ bill_location_handler, 
                        CommandHandler('skip_location', set_location)
                        ],
            SELLER: [   change_seller_handler, 
                        add_seller_purchase_handler,
                        show_all_sellers_handler, 
                        ], 
            CATEGORY: [ change_category_handler,
                        add_category_purchase_handler,
                        ], 
            NAME_SELLER_CATEGORY: [ MessageHandler(Filters.text, 
                                                    name_new_seller_category), ], 
            
            }, 
        fallbacks=[cancel_handler, show_menu_handler], 
        allow_reentry=True, 
        persistent=True
    )
    dispatcher.add_handler(new_bill_handler)
    dispatcher.add_handler(show_menu_handler)
    dispatcher.add_handler(change_seller_handler)
    dispatcher.add_handler(change_category_handler)
    
    set_location_item_handler = MessageHandler(
                            Filters.location, 
                            set_location_item)
    dispatcher.add_handler(set_location_item_handler)
    
    delitem_handler = CallbackQueryHandler( delitem, 
                                            pattern='delitem'
                                            )
    dispatcher.add_handler(delitem_handler)
    
    show_item_on_map_handler = CallbackQueryHandler( show_item_on_map, 
                                            pattern='on_map'
                                            )
    dispatcher.add_handler(show_item_on_map_handler)
    
    list_items_handler = CallbackQueryHandler( list_items, 
                                            pattern='list_of'
                                            )
    dispatcher.add_handler(list_items_handler)
    
    
    request_location_item_handler = CallbackQueryHandler( request_location_item, 
                                            pattern='location'
                                            )
    dispatcher.add_handler(request_location_item_handler)
    
    show_change_seller_handler = CallbackQueryHandler( show_change_seller, 
                                            pattern='show_change_seller'
                                            )
    dispatcher.add_handler(show_change_seller_handler)
    
    show_change_category_handler = CallbackQueryHandler( show_change_category, 
                                            pattern='show_change_category'
                                            )
    dispatcher.add_handler(show_change_category_handler)
    
    register_handler = CallbackQueryHandler( register, 
                                            pattern='register'
                                            )
    dispatcher.add_handler(register_handler)
    
    
    show_item_handler = CallbackQueryHandler( show_item, 
                                            pattern='show'
                                            )
    dispatcher.add_handler(show_item_handler)
    
    orders_handler = CallbackQueryHandler( orders, 
                                            pattern='orders'
                                            )
    dispatcher.add_handler(orders_handler)
    
    order_by_handler = CallbackQueryHandler( order_by, 
                                            pattern='order_by'
                                            )
    dispatcher.add_handler(order_by_handler)
    
    langs_handler = CallbackQueryHandler( list_langs, 
                                            pattern='langs'
                                            )
    dispatcher.add_handler(langs_handler)
    
    set_lang_handler = CallbackQueryHandler( set_lang, 
                                            pattern='lang&'
                                            )
    dispatcher.add_handler(set_lang_handler)
    
    help_handler = CallbackQueryHandler( but_help, 
                                            pattern='help'
                                            )
    dispatcher.add_handler(help_handler)
    
    list_users_handler = CallbackQueryHandler( list_users, 
                                            pattern='users'
                                            )
    dispatcher.add_handler(list_users_handler)
    
    block_handler = CallbackQueryHandler( block, 
                                            pattern='block'
                                            )
    dispatcher.add_handler(block_handler)
    
    activate_handler = CallbackQueryHandler( activate, 
                                            pattern='activate'
                                            )
    dispatcher.add_handler(activate_handler)
    
    register_handler = CallbackQueryHandler( register, 
                                            pattern='register'
                                            )
    dispatcher.add_handler(register_handler)
    
    no_register_handler = CallbackQueryHandler( no_register, 
                                            pattern='no_register'
                                            )
    dispatcher.add_handler(no_register_handler)
    
    show_pic_handler = CallbackQueryHandler( show_picture, 
                                            pattern='show_picture'
                                            )
    dispatcher.add_handler(show_pic_handler)
    
    by_cat_handler = CallbackQueryHandler( order_by_category, 
                                            pattern='by_category'
                                            )
    dispatcher.add_handler(by_cat_handler)
    
    by_sel_handler = CallbackQueryHandler( order_by_seller, 
                                            pattern='by_seller'
                                            )
    dispatcher.add_handler(by_sel_handler)
    
    add_seller_handler = CallbackQueryHandler( add_seller_category, 
                                            pattern='new_seller'
                                            )
    add_category_handler = CallbackQueryHandler( add_seller_category, 
                                            pattern='new_category'
                                            )
    new_cat_handler = ConversationHandler(
        name='new_cat_conv', 
        entry_points=[
                    add_category_handler, 
                    add_seller_handler
                    ],
        states={
            NAME_SELLER_CATEGORY: [ MessageHandler(Filters.text, 
                                                    name_new_seller_category), ],
            CATEGORY: [ change_category_handler,
                        add_category_handler,
                        ], 
            }, 
            fallbacks=[cancel_handler, show_menu_handler], 
            allow_reentry=True, 
            persistent=True
        )
    dispatcher.add_handler(new_cat_handler)


    
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
    

    updater.start_polling()

if __name__ == '__main__':
    initialize_db()
    main()
