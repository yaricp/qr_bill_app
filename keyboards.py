# -*- coding: utf-8 -*-
from telegram import (InlineKeyboardMarkup, InlineKeyboardButton)


from models.seller import Seller
from models.category import Category
from models.purchase import Purchase

from config import *


def get_button_main():
    new_button = InlineKeyboardButton(  
        _('Menu'),
        callback_data='/menu')
    keyboard = InlineKeyboardMarkup([[new_button]])
    return keyboard
    
    
def get_button_menu():
    buttons = [[InlineKeyboardButton( _('categories'), callback_data='/categories'), 
                InlineKeyboardButton( _('sellers'), callback_data='/sellers')],  
                [InlineKeyboardButton( _('purchases'), callback_data='/purchases')], 
                [InlineKeyboardButton( _('orders'), callback_data='/orders')], 
                [InlineKeyboardButton( _('languages'), callback_data='/langs')], 
                ]
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard
    
    
def get_button_lang():
    
    buttons = []
    for l in LANGUAGES:
        buttons.append(InlineKeyboardButton( l, 
                                            callback_data='lang&%s' % lang))
    return [buttons]
    

def get_button_sellers(user, id_purchase):
    
    sellers = Seller.select().where(Seller.user == user)
    menu = []
    buttons = []
    count = 0
    for seller in sellers:
        sel_name = '--'
        if seller.name: sel_name = seller.name
        if count == 5:
            menu.append(buttons)
            buttons = []
            count = 0
            buttons.append(
                InlineKeyboardButton(  
                    sel_name, 
                    callback_data='change_seller&%s&%s' % ( id_purchase,  seller.id )))
        else:
            count += 1
            buttons.append(
                InlineKeyboardButton(  
                    sel_name, 
                    callback_data='change_seller&%s&%s' % ( id_purchase , seller.id )))
    menu.append(buttons)
    new_button = InlineKeyboardButton(  
        _('New Seller'),
        callback_data='/new_seller')
    menu.append([new_button])
    new_button = InlineKeyboardButton(  
        _('Menu'),
        callback_data='/menu')
    menu.append([new_button])
    keyboard = InlineKeyboardMarkup(menu)
    return keyboard
    
    
def get_button_categories(user, id_purchase):
    categories = Category.select().where(Category.user == user)
    menu = []
    buttons = []
    count = 0
    for category in categories:
        cat_name = '--'
        if category.name: cat_name = category.name
        if count == 5:
            menu.append(buttons)
            buttons = []
            count = 0
            buttons.append(
                InlineKeyboardButton(  
                    cat_name, 
                    callback_data='change_category&%s&%s' % ( id_purchase, category.id )))
        else:
            count += 1
            buttons.append(
                InlineKeyboardButton(  
                    cat_name, 
                    callback_data='change_category&%s&%s' % ( id_purchase, category.id )))
    menu.append(buttons)
    new_button = InlineKeyboardButton(  
        _('New Category'), 
        callback_data='/new_category')
    menu.append([new_button])
    new_button = InlineKeyboardButton(  
        _('Menu'),
        callback_data='/menu')
    menu.append([new_button])
    keyboard = InlineKeyboardMarkup(menu)
    return keyboard


def get_button_list_purchase(user):
    purchases = Purchase.select().where(Purchase.user == user)
    buttons = []
    for p in purchases:
        seller_name = 'None'
        if p.seller_id:
            try:
                sel = Seller.get(id = p.seller_id)
                seller_name = sel.name
            except:
                print('seller not found!')
        #
        buttons.append([
            InlineKeyboardButton(  
                '%s - %s - %s' % (p.id, p.summ, seller_name), 
                callback_data='purchase&'+str(p.id)),
            InlineKeyboardButton( 
                _('Pic'), 
                callback_data='p&%s&%s' % (str(p.id), str(p.pic))), 
            InlineKeyboardButton( 
                _('Delete'), 
                callback_data='delitem&%s&%s' % ('purchase',  str(p.id)))
            ])
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard
    

def get_button_list_categories(user):
    categories = Category.select().where(Category.user == user)
    buttons = []
    for c in categories:
        buttons.append([
            InlineKeyboardButton(  
                '%s - %s' % (c.id, c.name), 
                callback_data='category&'+str(c.id)), 
            InlineKeyboardButton( 
                _('Delete'), 
                callback_data='delitem&%s&%s' % ('category',  str(c.id)))
            ])
    new_button = InlineKeyboardButton(  
        _('New Category'), 
        callback_data='/new_category')
    buttons.append([new_button])
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard


def get_button_orders():
    buttons = [[InlineKeyboardButton( _('by category'), callback_data='/by_category'), 
                InlineKeyboardButton( _('by seller'), callback_data='/by_seller')]]
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard
    

def get_button_list_sellers(user):
    sellers = Seller.select().where(Seller.user == user)
    buttons = []
    for s in sellers:
        buttons.append([
            InlineKeyboardButton(  
                '%s - %s' % (s.id, s.name), 
                callback_data='seller&'+str(s.id)), 
            InlineKeyboardButton( 
                _('Delete'), 
                callback_data='delitem&%s&%s' % ('seller',  str(s.id)))
            ])
    new_button = InlineKeyboardButton(  
        _('New Seller'),
        callback_data='/new_seller')
    buttons.append([new_button])
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
