from telegram import (InlineKeyboardMarkup, InlineKeyboardButton)

from db_models import *
                      
def show_menu(bot, message):
    buttons = [[InlineKeyboardButton( 'new_category', callback_data='/new_category'), 
                InlineKeyboardButton( 'new_seller', callback_data='/new_seller')],  
                [InlineKeyboardButton( 'list', callback_data='/list')], 
                [InlineKeyboardButton( 'orders', callback_data='/orders')], 
                ]
    keyboard = InlineKeyboardMarkup(buttons)
    message.reply_text(  text='Menu',
                                reply_markup=keyboard)
                                

def show_orders(bot, message):
    buttons = [[InlineKeyboardButton( 'by_category', callback_data='/by_category'), 
                InlineKeyboardButton( 'by_seller', callback_data='/by_seller')]]
    keyboard = InlineKeyboardMarkup(buttons)
    message.reply_text( text='Orders',
                        reply_markup=keyboard)
                        

def show_order_by(bot, type, message):
    keyboard = get_main_button()
    text = ''
    if type == 'seller':
        sellers = Seller.select()
        for s in sellers:
            summ = Purchase.select(fn.SUM(Purchase.summ)).where(Purchase.seller == s).scalar()
            text += 'Seller: %s, Summa: %s\n' % (s.name,  summ)
    else:
        categories = Categories.select()
        for c in categories:
            summ = Purchase.select(fn.SUM(Purchase.summ)).where(Purchase.category == c).scalar()
            text += 'Categories: %s, Summa: %s\n' % (c.name, summ)
    bot.send_message(message.chat.id,
                    text=text,
                    reply_markup=keyboard
                    )
                    
                    
def show_purchase_item(bot, message, id):
    purchase = Purchase.get(Purchase.id==id)
    category_name = ''
    seller_name = ''
    keyboard = get_button_categories(id)
    if purchase.category:
        category_name = purchase.category.name
    if purchase.seller:
        seller_name = purchase.seller.name
    text = 'ID: %s\nDate Time: %s\nSumma: %s\nSeller: %s\nCategory: %s' % ( 
            purchase.id, 
            purchase.datetime, 
            purchase.summ, 
            seller_name, 
            category_name
                            )
    bot.send_message(message.chat.id,
                    text=text,
                    reply_markup=keyboard
                    )
