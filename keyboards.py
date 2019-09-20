# -*- coding: utf-8 -*-
from datetime import datetime
from telegram import (InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton, ReplyKeyboardMarkup)


from config import *
from utils import *
from views import trans_type

from store.models.purchase import Purchase
from store.models.seller import Seller
from store.models.category import Category


def buttons_for_seller_item(user, id_item, type_item):
    buttons = [
    [InlineKeyboardButton( _('change_category'),
        callback_data='show_change_category&seller&%s' % id_item),  
    InlineKeyboardButton( _('set location'), 
        callback_data='location&%s&%s' % ( type_item,id_item))], 
    [InlineKeyboardButton( _('show card'), 
        callback_data='show&%s&%s' % ( type_item,id_item)), 
    InlineKeyboardButton( _('show on map'), 
        callback_data='on_map&%s&%s' % ( type_item,id_item))], 
    [InlineKeyboardButton( _('menu'), callback_data='menu')], 
                
                                                ]
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard
    
    
def buttons_for_purchase_item(user, id_item, media=None, has_media=None):
    buttons = []
    if not media:
        
        buttons = [
            [InlineKeyboardButton( _('change_seller'), 
                                    callback_data='show_change_seller&%s' % id_item), 
            InlineKeyboardButton( _('change_category'),
                                    callback_data='show_change_category&purchase&%s' % id_item)],  
            ]
        if has_media:
            buttons.append([InlineKeyboardButton(_('Media'), 
                        callback_data='show_picture&purchase&%s' % str(id_item))]
                        )
            buttons.append([InlineKeyboardButton( _('Change media'), 
                        callback_data='set_media&'+str(id_item))])
        else:
            buttons.append([InlineKeyboardButton( _('Set media'), 
                        callback_data='set_media&'+str(id_item))])
    else:
        buttons = [
                [InlineKeyboardButton( _('Card'), 
                                    callback_data='show&purchase&'+str(id_item))], 
                    ]
    buttons.append([InlineKeyboardButton( _('menu'), callback_data='menu')])
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard
    

def get_button_main():
    new_button = InlineKeyboardButton(  
        _('Menu'),
        callback_data='menu')
    keyboard = InlineKeyboardMarkup([[new_button]])
    return keyboard
    

def get_button_geo():
    geo = KeyboardButton(  
        _('location'),
        request_location=True)
    keyboard = ReplyKeyboardMarkup([[geo]])
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
    buttons = [[InlineKeyboardButton( _('categories'), callback_data='list_of&category'), 
                InlineKeyboardButton( _('sellers'), callback_data='list_of&seller')],  
                [InlineKeyboardButton( _('purchases'), callback_data='list_of&purchase')], 
                [InlineKeyboardButton( _('orders'), callback_data='orders')], 
                [InlineKeyboardButton( _('languages'), callback_data='langs')],
                [InlineKeyboardButton( _('help'), callback_data='help')], 
                ]
    user, created = User.get_or_create(tg_user_id=user_id)
    if user.is_admin:
        buttons.append([InlineKeyboardButton( _('users'), callback_data='users')])
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard
    
    
def get_button_users():
    #this menu show only for admins
    buttons = []
    users = User.select()
    
    for user in users:
        row_but = []
        if DEVEL: print('USER: ', user)
        if not user.is_admin:
            row_but.append(InlineKeyboardButton( 'x', callback_data='delitem&user&%s' % user.id))
        row_but.append(InlineKeyboardButton( user.username, 
                                                callback_data='show&user&%s' % user.id))
        row_but.append(InlineKeyboardButton( str(user.is_active), 
                                                callback_data='show&user&%s' % user.id))
        #row_but.append(InlineKeyboardButton( _('make admin'), callback_data='makeadmin&user&%s' % user.id))
        row_but.append(InlineKeyboardButton( _('block'), callback_data='block&user&%s' % user.id))
        row_but.append(InlineKeyboardButton( _('act'), callback_data='activate&user&%s' % user.id))
        buttons.append(row_but)
    new_button = InlineKeyboardButton(  
        _('Menu'),
        callback_data='menu')
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
    

def get_button_sellers(user, id_item, geo=None, radius=RADIUS_SEARCH_SELLER):
    
    purchase = Purchase.get(Purchase.id==id_item, 
                            Purchase.user==user)
    sellers = []
    seller_dict_flag = False
    if geo:
        for row in find_sellers_around(user, geo, radius):
            if DEVEL: print(row[0])
            seller = {'name':row[1], 'id':row[0]}
            sellers.append(seller)
            seller_dict_flag = True
#    if not sellers:
#        sellers = Seller.select().where(Seller.user==user)
    menu = []
    buttons = []
    count = 0
    for seller in sellers:
        sel_name = '--'
        if seller_dict_flag:
            sel_name = seller['name']
            sel_id = seller['id']
        else:
            if seller.name: sel_name = seller.name
            sel_id = seller.id
        if count == 5:
            menu.append(buttons)
            buttons = []
            count = 0
        else:
            count += 1
        buttons.append(
            InlineKeyboardButton(  
                sel_name, 
                callback_data='change_seller&%s&%s&%s' % ( 'purchase',
                                                            id_item, 
                                                            sel_id )))
       
    menu.append(buttons)
    #if seller_dict_flag:
    new_radius = int(radius)+100
    new_button = InlineKeyboardButton(  
        _('Search %s meters around' % new_radius),
        callback_data='search_by_radius&%s' % new_radius)
    menu.append([new_button])
    new_button = InlineKeyboardButton(  
        _('Show all sellers'),
        callback_data='show_all_sellers&purchase&%s' % purchase.id)
    menu.append([new_button])
    new_button = InlineKeyboardButton(  
        _('New Seller'),
        callback_data='new_seller&purchase&%s' % purchase.id)
    menu.append([new_button])
    new_button = InlineKeyboardButton(  
        _('Menu'),
        callback_data='menu')
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
    
    keyboard = InlineKeyboardMarkup(menu)
    return keyboard
    
    
def get_button_list_items(user, type_obj, page=1):
    total_count = dict_types[type_obj].select().count()
    last_page = total_count//COUNT_ON_PAGE
    if total_count % COUNT_ON_PAGE > 0:
        last_page = total_count//COUNT_ON_PAGE+1
    
    list_obj = dict_types[type_obj].select().where(dict_types[type_obj].user == user)
    #if type_obj == 'purchase':
    list_obj = list_obj.order_by(dict_types[type_obj].id.desc()).paginate(page, COUNT_ON_PAGE)
    buttons = []
    for obj in list_obj:
#        if type_obj == 'purchase':
#            seller_name = 'None'
#            if obj.seller_id:
#                try:
#                    sel = Seller.get(id = p.seller_id)
#                    seller_name = sel.name
#                except:
#                    if DEVEL: print('seller not found!'
        columns = [InlineKeyboardButton( 
                'X', 
                callback_data='delitem&%s&%s' % (type_obj, str(obj.id)))]
        columns = get_columns_items(columns, type_obj, obj)
        buttons.append(columns)
    
    if total_count > 10:
        if page == 1:
            prev_text = '|'
            callback_data_prev = '|'
            next_text = '>'
            prev = 1
            next = 2
            callback_data_next = 'list_of&%s&%s' % (type_obj, str(next))
        elif page == last_page:
            prev_text = '<'
            next_text = '|'
            callback_data_next = '|'
            prev = page - 1
            next = last_page
            callback_data_prev = 'list_of&%s&%s' % (type_obj, str(prev))
        else:
            prev_text = '<'
            next_text = '>'
            prev = page - 1
            next = page + 1
            callback_data_prev = 'list_of&%s&%s' % (type_obj, str(prev))
            callback_data_next = 'list_of&%s&%s' % (type_obj, str(next))
        
        columns = [ InlineKeyboardButton( 
                    prev_text, 
                    callback_data=callback_data_prev), 
                    InlineKeyboardButton( 
                    next_text, 
                    callback_data=callback_data_next)
                    ]
        buttons.append(columns)
    
    if type_obj != 'purchase':
        if type_obj == 'seller':
            txt_btn = _('New Seller')
        else:
            txt_btn = _('New Category')
        new_button = InlineKeyboardButton(  
            txt_btn, 
            callback_data='new_%s' %type_obj
            )
        buttons.append([new_button])
    new_button = InlineKeyboardButton(  
        _('Menu'),
        callback_data='menu')
    buttons.append([new_button])
    keyboard = InlineKeyboardMarkup(buttons)
    
    return keyboard
    

def get_columns_items(columns, type_obj, obj):
    if type_obj == 'purchase':
        seller_name = ''
        if obj.seller:
            seller_name=obj.seller.name
        columns.append(InlineKeyboardButton(  
                    '%s - %s - %s' % (obj.summ, obj.datetime, seller_name), 
                    callback_data='show&purchase&'+str(obj.id)))
        columns.append(InlineKeyboardButton( 
                    _('Media'), 
                    callback_data='show_picture&purchase&%s' % str(obj.id)))
    elif type_obj == 'seller':
        columns.append(InlineKeyboardButton(  
                obj.name, 
                callback_data='show&seller&'+str(obj.id)))
    elif type_obj == 'category':
        columns.append(InlineKeyboardButton(  
                obj.name, 
                callback_data='show&category&'+str(obj.id)))
    return columns
    

def get_button_orders():
    buttons = [[InlineKeyboardButton( _('by category'), callback_data='order_by&category'), 
                InlineKeyboardButton( _('by seller'), callback_data='order_by&seller')]]
    new_button = InlineKeyboardButton(  
        _('Menu'),
        callback_data='menu')
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
    buttons = [] 
    rows = []
    if type_c == 'seller':
        list_by_for = Seller.select().where(Seller.user==user)
        by_for_field = Purchase.seller
        c_name = _('Seller')
        arg_commang_what = 'Seller'
        command = 'by_seller'
    else:
        list_by_for = Category.select().where(Category.user==user)
        by_for_field = Purchase.category
        c_name = _('Category')
        arg_commang_what = 'Category'
        command = 'by_category'
    rows.append(InlineKeyboardButton( c_name, callback_data='-' ))
    
    for m in (month_now-2, month_now-1, month_now):
        rows.append(InlineKeyboardButton( get_dict_month()[m], callback_data='-' ))
    buttons.append(rows)
    for c in list_by_for:
        rows = []
        c_name = '-'
        if c.name:
            c_name = c.name
        rows.append(InlineKeyboardButton( c_name, callback_data='%s&%s' % (command, c_name) ))
        for m in (month_now-2, month_now-1, month_now):
            month = str(m)
            if m < 10:
                month = '0'+str(m)

            summ = (Purchase
                .select(fn.SUM(Purchase.summ))
                .where( by_for_field==c, 
                        Purchase.user==user, 
                        fn.date_part('month', Purchase.datetime)==month)
                .scalar()
                )
            if summ: summ = str(round(summ, 2))
            else: summ = '-'
            rows.append(InlineKeyboardButton( summ, callback_data='%s&%s&%s' % (command, c_name, m) ))
        buttons.append(rows)
    new_button = InlineKeyboardButton(  
        _('Menu'),
        callback_data='menu')
    buttons.append([new_button])
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard
    
    
def get_button_purchases_by(user, name, by_what, month=None):
    buttons = []
    if by_what == 'Category':
        obj = Category.get_or_none(name=name)
        by_field = Purchase.category
    else:
        obj = Seller.get_or_none(name=name)
        by_field = Purchase.seller
    purchases = (Purchase.select()
                .where(Purchase.user==user, by_field==obj)
                .order_by(Purchase.id.desc())
                .paginate(1, 20))
    if month:
        if int(month) < 10:
            month = '0'+month
        #if DEVEL: print('month: ', month)
        purchases = (Purchase.select()
                .where( Purchase.user==user, 
                        by_field==obj, 
                        fn.date_part('month', Purchase.datetime)==month)
                .order_by(Purchase.id.desc())
                )
    for p in purchases:
        rows = []
        category_name = ''
        seller_name = ''
        if p.category:
            category_name = p.category.name
        if p.seller:
            seller_name = p.seller.name
        
        rows.append(InlineKeyboardButton(  
                    '%s - %s - %s' % (p.summ, p.datetime, seller_name), 
                    callback_data='show&purchase&'+str(p.id)))
                    
        rows.append(InlineKeyboardButton( 
                    _('Media'), 
                    callback_data='show_picture&purchase&%s' % str(p.id)))
        buttons.append(rows)
    new_button = InlineKeyboardButton(  
        _('Menu'),
        callback_data='menu')
    buttons.append([new_button])
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard
