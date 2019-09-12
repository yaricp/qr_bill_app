# -*- coding: utf-8 -*-
from datetime import datetime
from telegram import (InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton, ReplyKeyboardMarkup)


from config import *
from utils import *


def buttons_for_seller_item(user, id_item, type_item):
    keyboard = get_button_categories(user, id_item, type_item)
    loc = InlineKeyboardButton(  
        _('Location'), 
        callback_data='location&%s&%s' % ( type_item, 
                                                id_item
                                                ))
    on_map = InlineKeyboardButton(  
        _('show on map'), 
        callback_data='on_map&%s&%s' % ( type_item, 
                                                id_item
                                                ))
    keyboard['inline_keyboard'].append([loc, on_map])
    new_button = InlineKeyboardButton(  
        _('Menu'),
        callback_data='/menu')
    keyboard['inline_keyboard'].append([new_button])
    return keyboard
    
    
def buttons_for_purchase_item(user, id_item):
    buttons = [
                [InlineKeyboardButton( _('change_seller'), 
                                        callback_data='show_change_seller&%s' % id_item)], 
                [InlineKeyboardButton( _('change_category'),
                                        callback_data='show_change_category&%s' % id_item)],  
                [InlineKeyboardButton( _('menu'), callback_data='/menu')], 
                ]
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard
    


def get_button_main():
    new_button = InlineKeyboardButton(  
        _('Menu'),
        callback_data='/menu')
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
    

def get_button_sellers(user, id_item, geo=None):
    
    purchase = Purchase.get(Purchase.id==id_item, 
                            Purchase.user==user)
    print('PURCHASE: ', purchase)
    sellers = []
    seller_dict_flag = False
    if geo:
        conn = psycopg2.connect(database=PG_BATABASE, 
                                user=PG_USERNAME, 
                                password=PG_PASSWORD)
        curs = conn.cursor()

        radius_mi = RADIUS_SEARCH_SELLER
        curs.execute(
            'SELECT id,name FROM seller '\
            'WHERE category_id = %s AND ST_Distance_Sphere(geom, ST_SetSRID(ST_MakePoint('\
            '%s, %s), 4326)) <= %s * 1609.34;', 
            (purchase.category.id, geo.longitude, geo.latitude, radius_mi))
        print('found')
        for row in curs.fetchall():
            print(row[0])
            seller = {'name':row[1], 'id':row[0]}
            sellers.append(seller)
            seller_dict_flag = True
    print('SELLERS: ', sellers)
    if not sellers:
        sellers = Seller.select().where(Seller.user==user)
        print('SELLERS: ', sellers)
    menu = []
    buttons = []
    count = 0
    for seller in sellers:
        print(seller)
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
    
    keyboard = InlineKeyboardMarkup(menu)
    return keyboard
    
    
def get_button_one_task(user, id):
    p = Purchase.get_or_none(user=user, id=id)
    buttons = []
    seller_name = 'None'
    if p.seller:
        try:
            sel = Seller.get_or_none(id = p.seller_id)
            seller_name = sel.name
        except:
            print('seller not found!')
    buttons.append([
                InlineKeyboardButton( 
                    'X', 
                    callback_data='delitem&purchase&%s' % str(p.id)), 
#                InlineKeyboardButton( 
#                    str(p.id), 
#                    callback_data='show&purchase&'+str(p.id)),
                InlineKeyboardButton(  
                    '%s - %s - %s' % (p.summ, p.datetime, seller_name), 
                    callback_data='show&purchase&'+str(p.id)),
                InlineKeyboardButton( 
                    _('Pic'), 
                    callback_data='show_picture&purchase&%s' % str(p.id)), 
                
                ])
    new_button = InlineKeyboardButton(  
        _('Menu'),
        callback_data='/menu')
    buttons.append([new_button])
    keyboard = InlineKeyboardMarkup(buttons)
    
    return keyboard
    
def get_button_list_items(user, type_obj):
    list_obj = dict_types[type_obj].select().where(dict_types[type_obj].user == user)
    if type_obj == 'purchase':
        list_obj = list_obj.order_by(Purchase.id.desc()).paginate(1, 10)
    buttons = []
    for obj in list_obj:
#        if type_obj == 'purchase':
#            seller_name = 'None'
#            if obj.seller_id:
#                try:
#                    sel = Seller.get(id = p.seller_id)
#                    seller_name = sel.name
#                except:
#                    print('seller not found!')
        buttons.append([
            InlineKeyboardButton( 
                'X', 
                callback_data='delitem&%s&%s' % (type_obj, str(obj.id))), 
                get_columns_items(type_obj)
                ])
    if type_obj != 'purchase':
        new_button = InlineKeyboardButton(  
        _('New %s') % type_obj, 
        callback_data='new_%s' %type_obj)
    buttons.append([new_button])
    new_button = InlineKeyboardButton(  
        _('Menu'),
        callback_data='/menu')
    buttons.append([new_button])
    keyboard = InlineKeyboardMarkup(buttons)
    
    return keyboard
    

def get_columns_items(type_obj):
    if type_obj == 'purchase':
        return (InlineKeyboardButton(  
                    '%s - %s - %s' % (p.summ, p.datetime, seller_name), 
                    callback_data='show&purchase&'+str(p.id)),
                InlineKeyboardButton( 
                    _('Pic'), 
                    callback_data='show_picture&purchase&%s' % str(p.id)))
    elif type_obj == 'seller':
        return InlineKeyboardButton(  
                s.name, 
                callback_data='show&seller&'+str(s.id))
    elif type_obj == 'category':
        return InlineKeyboardButton(  
                c.name, 
                callback_data='show&category&'+str(c.id))
    
    
        

def get_button_list_purchase(user):
    purchases = Purchase.select().where(Purchase.user == user).order_by(Purchase.id.desc()).paginate(1, 10)
    #count_rows = purchases.count()
    
    buttons = []
    print(purchases)
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
#                InlineKeyboardButton( 
#                    str(p.id), 
#                    callback_data='show&purchase&'+str(p.id)),
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
    buttons = [] 
    rows = []
    if type_c == 'seller':
        list_by_for = Seller.select().where(Seller.user==user)
        by_for_field = Purchase.seller
        c_name = _('Seller')
        arg_commang_what = 'Seller'
        command = '/by_seller'
    else:
        list_by_for = Category.select().where(Category.user==user)
        by_for_field = Purchase.category
        c_name = _('Category')
        arg_commang_what = 'Category'
        command = '/by_category'
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
        callback_data='/menu')
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
        #print('month: ', month)
        purchases = (Purchase.select()
                .where(Purchase.user==user, by_field==obj, fn.strftime('%m', Purchase.datetime)==month)
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
                    _('Pic'), 
                    callback_data='show_picture&purchase&%s' % str(p.id)))
        buttons.append(rows)
    new_button = InlineKeyboardButton(  
        _('Menu'),
        callback_data='/menu')
    buttons.append([new_button])
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard
