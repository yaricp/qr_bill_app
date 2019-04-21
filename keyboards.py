from telegram import (InlineKeyboardMarkup, InlineKeyboardButton)

from db_models import *


def get_button_main():
    new_button = InlineKeyboardButton(  
        'Menu',
        callback_data='/menu')
    keyboard = InlineKeyboardMarkup([[new_button]])
    return keyboard
    
    
def get_button_menu():
    buttons = [[InlineKeyboardButton( 'categories', callback_data='/categories'), 
                InlineKeyboardButton( 'sellers', callback_data='/sellers')],  
                [InlineKeyboardButton( 'purchases', callback_data='/purchases')], 
                [InlineKeyboardButton( 'orders', callback_data='/orders')], 
                ]
    keyboard = InlineKeyboardMarkup(buttons)
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
                    callback_data='change_seller&%s&%s' % ( id_purchase,  seller.id )))
        else:
            count += 1
            buttons.append(
                InlineKeyboardButton(  
                    seller.name, 
                    callback_data='change_seller&%s&%s' % ( id_purchase , seller.id )))
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
                    callback_data='change_category&%s&%s' % ( id_purchase, category.id )))
        else:
            count += 1
            buttons.append(
                InlineKeyboardButton(  
                    category.name, 
                    callback_data='change_category&%s&%s' % ( id_purchase, category.id )))
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


def get_button_list_purchase():
    purchases = Purchase.select()
    buttons = []
    for p in purchases:
        buttons.append([InlineKeyboardButton(  
            p.id, 
            callback_data='purchase&'+str(p.id))])
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard
    

def get_button_list_categories():
    categories = Category.select()
    buttons = []
    for c in categories:
        buttons.append([InlineKeyboardButton(  
            '%s - %s' % (c.id, c.name), 
            callback_data='category&'+str(c.id))])
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard


def get_button_orders():
    buttons = [[InlineKeyboardButton( 'by_category', callback_data='/by_category'), 
                InlineKeyboardButton( 'by_seller', callback_data='/by_seller')]]
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard
    

def get_button_list_sellers():
    sellers = Seller.select()
    buttons = []
    for s in sellers:
        buttons.append([InlineKeyboardButton(  
            '%s - %s' % (s.id, s.name), 
            callback_data='seller&'+str(s.id))])
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard
    
    
def get_button_del_item(id, type):
    buttons = [[InlineKeyboardButton( 'Delete', callback_data='delitem&%s&%s' % 
                (type,  str(id)))]]
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard
    
    
#def get_button_crud(id):
#    buttons = [[InlineKeyboardButton( 'Delete', callback_data='delitem&%s&%s' % 
#                (type,  str(id)))]]
#    keyboard = InlineKeyboardMarkup(buttons)
#    return keyboard
