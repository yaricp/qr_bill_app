# -*- coding: utf-8 -*-

#from decimal import Decimal
from datetime import datetime

from telegram import (InlineQueryResultArticle, InputTextMessageContent,
                      InlineKeyboardMarkup, InlineKeyboardButton, 
                      InputMediaPhoto)
from pyzbar.pyzbar import decode
from PIL import Image

from config import *
from db_models import *

CUR_DIR = os.path.dirname(os.path.realpath(__file__))

def is_allowed_user():
    def wrap(f):
        def wrapped_f(*args):
            obj = None
            if args[1].message:
                obj = args[1].message
            elif args[1].callback_query:
                obj = args[1].callback_query
            if obj:
                if obj.from_user.first_name in allowed_users:
                    f(*args)
                else:
                    update.message.reply_text('Sorry! it is private bot...')
        return wrapped_f
    return wrap


def get_button_categories(id_purchase):
    categories = Category.select()
    menu = []
    buttons = []
    count = 0
    print('categories: ',  len(categories))
    for category in categories:
        if count == 5:
            menu.append(buttons)
            print('Empty buttons')
            buttons = []
            count = 0
            buttons.append(
                InlineKeyboardButton(  
                    category.name, 
                    callback_data='category&%s&%s' % (category.id, id_purchase )))
        else:
            count += 1
            print(category.id)
            buttons.append(
                InlineKeyboardButton(  
                    category.name, 
                    callback_data='category&%s&%s' % (category.id, id_purchase )))
    menu.append(buttons)
    new_button = InlineKeyboardButton(  
        'New Category', 
        callback_data='/new_category')
    menu.append([new_button])
    keyboard = InlineKeyboardMarkup(menu)
    return keyboard


def get_button_sellers(id_purchase):
    
    sellers = Seller.select()
    menu = []
    buttons = []
    count = 0
    for seller in sellers:
        #print(seller.id)
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
    

def list_purchase(bot, update):
    keyboard = get_list_purchase()
    update.message.reply_text(  text='List Purchases',
                                reply_markup=keyboard)
                                
                                
def menu(bot, update):
    buttons = [[InlineKeyboardButton( 'new_category', callback_data='/new_category'), 
                InlineKeyboardButton( 'new_seller', callback_data='/new_seller')],  
                [InlineKeyboardButton( 'list', callback_data='/list')], 
                [InlineKeyboardButton( 'orders', callback_data='/orders')], 
                ]
    keyboard = InlineKeyboardMarkup(buttons)
    update.message.reply_text(  text='Menu',
                                reply_markup=keyboard)
    
    
def error(bot, update, error_msg):
    module_logger.warning('Update caused error "%s"', error)


@is_allowed_user()
def list_orders(bot, update):
    print('list_orders')
    buttons = [[InlineKeyboardButton( 'by_categories', callback_data='/by_categories'), 
                InlineKeyboardButton( 'by_seller', callback_data='/by_seller')]]
    keyboard = InlineKeyboardMarkup(buttons)
    update.message.reply_text(  text='Orders',
                                reply_markup=keyboard)
                
    
    

@is_allowed_user()
def new_category(bot, update):
    if update.callback_query and update.callback_query.data == '/new_category':
        status = Status.get(name='wait_category_name')
        if status:
            if not status.value:
                status.value = True
        else:
            status = Status(name='wait_category_name', 
                            value=True)
        status.save()
        bot.send_message(update.callback_query.message.chat.id,'send name of category')
    else:
        res = ''
        cat = Category(name=update.message.text.replace('/new_category ', ''))
        try:
            cat.save()
            res = 'category saved!'
        except:
            res = 'error!'
        update.message.reply_text(res)
    
    
@is_allowed_user()
def new_seller(bot, update):
    if update.callback_query and update.callback_query.data == '/new_seller':
        status = Status.get(name='wait_seller_name')
        if status:
            if not status.value:
                status.value = True
        else:
            status = Status(name='wait_seller_name', 
                            value=True)
        status.save()
        bot.send_message(update.callback_query.message.chat.id,'send name of seller')
    else:
        res = ''
        seller = Seller(name=update.message.text.replace('/new_seller ', ''))
        try:
            seller.save()
            res = 'Ok!'
        except:
            res = 'error!'
        update.message.reply_text(res)
        

@is_allowed_user()
def new_msg(bot, update):
    
    if update.message.media_group_id:
        flag_send = False
        photo_file_id = update.message.photo[-1].get_file().file_id
        if not os.path.exists('files/'+update.message.media_group_id+'.txt'):
            flag_send = True
        with open('files/'+update.message.media_group_id+'.txt', 'a') as file:
            file.write(photo_file_id+',')
        if flag_send:
            new_caption = update.message.caption.replace('#','')
            update.message.reply_photo(
                photo=photo_file_id, 
                caption="%s # %s" % (new_caption,update.message.media_group_id), 
                reply_markup=keyboard)
    elif update.message.photo:
        photo_file_id = update.message.photo[-1].file_id
        foto = bot.getFile(photo_file_id)
        new_file = bot.get_file(foto.file_id)
        new_file.download(os.path.join(PATH_TEMP_FILES,'qrcode.jpg'))
        list_decoded = decode(Image.open(os.path.join(PATH_TEMP_FILES,'qrcode.jpg')))
        for rec in list_decoded:
            type_data = rec.type
            print(type_data)
            if type_data == 'QRCODE':
                list_data = rec.data.decode("utf-8").split('&')
                date_time = datetime.strptime(list_data[0].replace('t=', ''), '%Y%m%dT%H%M%S').date()
                summ = float(list_data[1].replace('s=', ''))
                pur = Purchase(name='', 
                                datetime = date_time, 
                                summ = summ
                                )
                pur.save()
                show_purchase_item(bot, update.message, pur.id)
    else:
        if Status.get(name='wait_seller_name').value:
            new_seller = Seller(name=update.message.text)
            new_seller.save()
            status = Status.get(name='wait_seller_name')
            status.value = False
            status.save()
            update.message.reply_text(text='Seller created!')
        elif Status.get(name='wait_category_name').value:
            new_cat = Category(name=update.message.text)
            new_cat.save()
            status = Status.get(name='wait_category_name')
            status.value = False
            status.save()
            update.message.reply_text(text='Category created!')
        

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


def button(bot, update):
    but_data = update.callback_query.data
    if but_data == '/list':
        keyboard = get_list_purchase()
        bot.send_message(update.callback_query.message.chat.id,             
                        text='List Purchase', 
                        reply_markup=keyboard)
    elif but_data == '/new_category':
        new_category(bot, update)
    elif but_data == '/new_seller':
        new_seller(bot, update)
    list_ids = but_data.split('&')
    type_obj = list_ids[0]
    if len(list_ids) >= 3:
        purchase = Purchase.get(Purchase.id==list_ids[2])
    if type_obj == 'seller':
        seller = Seller.get(Seller.id==list_ids[1])
        purchase.seller = seller
        purchase.save()
        keyboard = get_button_sellers(purchase.id)
        text = 'seller saved!'
        bot.send_message(update.callback_query.message.chat.id,
                        text='%s %s %s' % (text,  purchase.datetime,  purchase.summ)
                        )
    elif type_obj == 'category':
        category = Category.get(Category.id==list_ids[1])
        purchase.category = category
        purchase.save()
        keyboard = get_button_sellers(purchase.id)
        bot.send_message(update.callback_query.message.chat.id,
                        text='%s %s' % (purchase.datetime,  purchase.summ), 
                        reply_markup=keyboard)
    elif type_obj == 'purchase':
        show_purchase_item(bot, update.callback_query.message, list_ids[1])


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
