from telegram import (InlineKeyboardMarkup, InlineKeyboardButton)

from db_models import *


def get_button_main():
    new_button = InlineKeyboardButton(  
        'Menu',
        callback_data='/menu')
    keyboard = InlineKeyboardMarkup([[new_button]])
    return keyboard
    

def get_button_sellers(id_purchase):
    
    sellers = Seller.select()
    menu = []
    buttons = []
    count = 0
    for seller in sellers:
        if count >= 5:
            menu.append(buttons)
            buttons = []
            count = 0
            buttons.append(
                InlineKeyboardButton(  
                    seller.name, 
                    callback_data='seller&%s&%s' % (seller.id, id_purchase )))
        else:
            count += 1
            buttons.append(
                InlineKeyboardButton(  
                    seller.name, 
                    callback_data='seller&%s&%s' % (seller.id, id_purchase )))
    menu.append(buttons)
    new_button = InlineKeyboardButton(  
        'New Seller',
        callback_data='/new_seller')
    menu.append([new_button])
    new_button = InlineKeyboardButton(  
        'Menu',
        callback_data='/menu')
    menu.append([new_button])
    keyboard = InlineKeyboardMarkup(menu)
    return keyboard
    
    
def get_button_categories(id_purchase):
    categories = Category.select()
    menu = []
    buttons = []
    count = 0
    for category in categories:
        if count == 5:
            menu.append(buttons)
            buttons = []
            count = 0
            buttons.append(
                InlineKeyboardButton(  
                    category.name, 
                    callback_data='category&%s&%s' % (category.id, id_purchase )))
        else:
            count += 1
            buttons.append(
                InlineKeyboardButton(  
                    category.name, 
                    callback_data='category&%s&%s' % (category.id, id_purchase )))
    menu.append(buttons)
    new_button = InlineKeyboardButton(  
        'New Category', 
        callback_data='/new_category')
    menu.append([new_button])
    new_button = InlineKeyboardButton(  
        'Menu',
        callback_data='/menu')
    menu.append([new_button])
    keyboard = InlineKeyboardMarkup(menu)
    return keyboard


def get_list_purchase():
    purchases = Purchase.select()
    buttons = []
    for p in purchases:
        buttons.append([InlineKeyboardButton(  
            p.id, 
            callback_data='purchase&'+str(p.id))])
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard
