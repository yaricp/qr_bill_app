# -*- coding: utf-8 -*-
from datetime import datetime
from telegram import (InlineKeyboardMarkup, InlineKeyboardButton)


from models.seller import Seller
from models.category import Category
from models.purchase import Purchase
from models.user import User

from config import *


def get_button_main():
    new_button = InlineKeyboardButton(  
        _('Menu'),
        callback_data='/menu')
    keyboard = InlineKeyboardMarkup([[new_button]])
    return keyboard
    

def get_button_register():
    yes_button = InlineKeyboardButton(  
        _('Yes'),
        callback_data='register')
    no_button = InlineKeyboardButton(  
        _('No'),
        callback_data='no_register')
    keyboard = InlineKeyboardMarkup([[yes_button, no_button]])
    return keyboard
    
    
def get_button_menu(user_id):
    buttons = [[InlineKeyboardButton( _('categories'), callback_data='/categories'), 
                InlineKeyboardButton( _('sellers'), callback_data='/sellers')],  
                [InlineKeyboardButton( _('purchases'), callback_data='/purchases')], 
                [InlineKeyboardButton( _('orders'), callback_data='/orders')], 
                [InlineKeyboardButton( _('languages'), callback_data='/langs')],
                [InlineKeyboardButton( _('help'), callback_data='/help')], 
                ]
    user, created = User.get_or_create(tg_user_id=user_id)
    if user.is_admin:
        buttons.append([InlineKeyboardButton( _('users'), callback_data='/users')])
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard
    
    
def get_button_users():
    buttons = []
    users = User.select()
    for user in users:
        row_but = [
                    InlineKeyboardButton( user.username + ' ' + str(user.is_active), callback_data='show&user&%s' % user.id), 
                    #InlineKeyboardButton( _('make admin'), callback_data='makeadmin&user&%s' % user.id), 
                    InlineKeyboardButton( _('block'), callback_data='block&user&%s' % user.id), 
                    InlineKeyboardButton( _('act'), callback_data='activate&user&%s' % user.id)
                    ]
        if not user.is_admin:
            row_but = [
                        InlineKeyboardButton( 'x', callback_data='delitem&user&%s' % user.id),
                        InlineKeyboardButton( user.username + ' ' + str(user.is_active), callback_data='show&user&%s' % user.id), 
                        #InlineKeyboardButton( _('make admin'), callback_data='makeadmin&user&%s' % user.id), 
                        InlineKeyboardButton( _('block'), callback_data='block&user&%s' % user.id), 
                        InlineKeyboardButton( _('act'), callback_data='activate&user&%s' % user.id)
                        ]
        buttons.append(row_but)
    new_button = InlineKeyboardButton(  
        _('Menu'),
        callback_data='/menu')
    buttons.append([new_button])
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard
    
    
def get_button_lang():
    
    buttons = []
    for l in LANGUAGES:
        
        buttons.append(InlineKeyboardButton( l, 
                                            callback_data='lang&%s' % l))
    keyboard = InlineKeyboardMarkup([buttons])
    return keyboard
    

def get_button_sellers(user, id_item):
    purchase = Purchase.get(Purchase.id==id_item, 
                            Purchase.user==user)
    sellers = Seller.select().where(Seller.user==user, 
                                    Seller.category==purchase.category)
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
                    callback_data='change_seller&%s&%s&%s' % ( 'purchase', 
                                                                id_item, 
                                                                seller.id )))
        else:
            count += 1
            buttons.append(
                InlineKeyboardButton(  
                    sel_name, 
                    callback_data='change_seller&%s&%s&%s' % ( 'purchase',
                                                                id_item, 
                                                                seller.id )))
    menu.append(buttons)
    new_button = InlineKeyboardButton(  
        _('New Seller'),
        callback_data='new_seller&purchase&%s' % purchase.id)
    menu.append([new_button])
    new_button = InlineKeyboardButton(  
        _('Menu'),
        callback_data='/menu')
    menu.append([new_button])
    keyboard = InlineKeyboardMarkup(menu)
    return keyboard
    
    
def get_button_categories(user, id_item, type_item):
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
                    callback_data='change_category&%s&%s&%s' % (type_item, 
                                                                id_item,
                                                                category.id 
                                                                )))
        else:
            count += 1
            buttons.append(
                InlineKeyboardButton(  
                    cat_name, 
                    callback_data='change_category&%s&%s&%s' % (type_item,
                                                                id_item,
                                                                category.id
                                                                )))
    menu.append(buttons)
    new_button = InlineKeyboardButton(  
        _('New Category'), 
        callback_data='new_category&%s&%s' % ( type_item, 
                                                id_item
                                                ))
    menu.append([new_button])
    new_button = InlineKeyboardButton(  
        _('Menu'),
        callback_data='/menu')
    menu.append([new_button])
    keyboard = InlineKeyboardMarkup(menu)
    return keyboard


def get_button_list_purchase(user):
    purchases = Purchase.select().where(Purchase.user == user).order_by(Purchase.id.desc()).paginate(1, 10)
    #count_rows = purchases.count()
    
    buttons = []
    #print(purchases)
    for p in purchases:
        try:
            
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
                    'X', 
                    callback_data='delitem&purchase&%s' % str(p.id)), 
                InlineKeyboardButton(  
                    '%s - %s - %s' % (p.summ, p.datetime, seller_name), 
                    callback_data='show&purchase&'+str(p.id)),
                InlineKeyboardButton( 
                    _('Pic'), 
                    callback_data='show_picture&purchase&%s' % str(p.id)), 
                
                ])
        except:
            print('p: ', p.__dict__)
    new_button = InlineKeyboardButton(  
        _('Menu'),
        callback_data='/menu')
    buttons.append([new_button])
    keyboard = InlineKeyboardMarkup(buttons)
    
    return keyboard
    

def get_button_list_categories(user):
    categories = Category.select().where(Category.user == user)
    buttons = []
    for c in categories:
        buttons.append([
            InlineKeyboardButton( 
                'X', 
                callback_data='delitem&%s&%s' % ('category',  str(c.id))), 
            InlineKeyboardButton(  
                c.name, 
                callback_data='show&category&'+str(c.id))
            ])
    new_button = InlineKeyboardButton(  
        _('New Category'), 
        callback_data='/new_category')
    buttons.append([new_button])
    new_button = InlineKeyboardButton(  
        _('Menu'),
        callback_data='/menu')
    buttons.append([new_button])
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard


def get_button_orders():
    buttons = [[InlineKeyboardButton( _('by category'), callback_data='/by_category'), 
                InlineKeyboardButton( _('by seller'), callback_data='/by_seller')]]
    new_button = InlineKeyboardButton(  
        _('Menu'),
        callback_data='/menu')
    buttons.append([new_button])
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard
    

def get_button_list_sellers(user):
    sellers = Seller.select().where(Seller.user == user)
    buttons = []
    for s in sellers:
        buttons.append([
            InlineKeyboardButton( 
                'X', 
                callback_data='delitem&%s&%s' % ('seller',  str(s.id))), 
            InlineKeyboardButton(  
                s.name, 
                callback_data='show&seller&'+str(s.id))
            ])
    new_button = InlineKeyboardButton(  
        _('New Seller'),
        callback_data='/new_seller')
    buttons.append([new_button])
    new_button = InlineKeyboardButton(  
        _('Menu'),
        callback_data='/menu')
    buttons.append([new_button])
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard
    
    
def get_button_del_item(id, type):
    buttons = [[InlineKeyboardButton( _('Delete'), callback_data='delitem&%s&%s' % 
                (type,  str(id)))]]
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard


def get_button_confirm(id):
    buttons = [[
        InlineKeyboardButton( _('Yes'), callback_data='confirm&purchase&%s&yes' % id ), 
        InlineKeyboardButton( _('No'), callback_data='confirm&purchase&%s&no' % id )
        ]]
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard
    

def get_button_order_by(user, type_c):
    month_now = datetime.now().month
    keyboard = []
    if type_c == 'seller':
        list_by_for = Seller.select().where(Seller.user==user)
        by_for_field = Purchase.seller
        c_name = 'Seller'
    else:
        list_by_for = Category.select().where(Category.user==user)
        by_for_field = Purchase.category
        c_name = 'Category'
        
    for c in list_by_for:
        buttons = []
        c_name = '-'
        if c.name:
            c_name = c.name
        buttons.append(InlineKeyboardButton( c_name, callback_data='/by_category&%s' % c_name ))
        for m in (month_now-2, month_now-1, month_now):
            month = str(m)
            if m < 10:
                month = '0'+str(m)
            summ = (Purchase
                .select(fn.SUM(Purchase.summ))
                .where(by_for_field==c, Purchase.user==user, fn.strftime('%m', Purchase.datetime)==month)
                .scalar()
                )
            if summ: summ = str(round(summ, 2))
            else: summ = ''
            buttons.append(InlineKeyboardButton( summ, callback_data='/by_category&%s&%s' % (c_name, m) ))
        keyboard.append(buttons)
    return keyboard
