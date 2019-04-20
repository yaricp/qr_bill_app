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


def get_category(id_purchase):
    print('id_purchase: ',  id_purchase)
    categories = Category.select()
    buttons = []
    for category in categories:
        print(category)
        buttons.append(
            InlineKeyboardButton(  
                category.name, 
                callback_data='category&%s&%s' % (category.id, id_purchase )))
    keyboard = InlineKeyboardMarkup([buttons])
    return keyboard


def get_seller(id_purchase):
    
    sellers = Seller.select()
    buttons = []
    for seller in sellers:
        buttons.append(
            InlineKeyboardButton(  
                seller.name, 
                callback_data='seller&%s&%s' % (seller.id, id_purchase )))
    keyboard = InlineKeyboardMarkup([buttons])
    return keyboard


def list_purchase(bot, update):
    purchases = Purchase.select()
    buttons = []
    for p in purchases:
        buttons.append([InlineKeyboardButton(  
            p.id, 
            callback_data='purchase&'+str(p.id))])
    keyboard = InlineKeyboardMarkup(buttons)
    update.message.reply_text(  text='List Purchases',
                                reply_markup=keyboard)
                                

def menu(bot, update):
    buttons = [[InlineKeyboardButton( 'new_category', callback_data='/new_category'), 
                InlineKeyboardButton( 'new_seller', callback_data='/new_seller')],  
                [InlineKeyboardButton( 'list', callback_data='/list')]]
    keyboard = InlineKeyboardMarkup(buttons)
    update.message.reply_text(  text='Menu',
                                reply_markup=keyboard)
    
def error(bot, update, error_msg):
    module_logger.warning('Update caused error "%s"', error)


@is_allowed_user()
def new_category(bot, update):
    res = ''
    cat = Category(name=update.message.text.replace('/new_category ', ''))
    try:
        cat.save()
        res = 'Ok!'
    except:
        res = 'error!'
    update.message.reply_text(res)
    
    
@is_allowed_user()
def new_seller(bot, update):
    if update.message.data and update.message.data == '/new_seller':
        update.message.reply_text('send name of seller')
    elif update.message.data and update.message.data == '/new_category':
        update.message.reply_text('send name of category')
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
        result_text = ''
        for rec in list_decoded:
            list_data = rec.data.decode("utf-8").split('&')
            date_time = datetime.strptime(list_data[0].replace('t=', ''), '%Y%m%dT%H%M%S').date()
            summ = float(list_data[1].replace('s=', ''))
            type_data = rec.type
            pur = Purchase(name='', 
                            datetime = date_time, 
                            summ = summ
                            )
            pur.save()
            print('pur: ',  pur)
            keyboard = get_category(pur.id)
            result_text = "%s %s %s" % (date_time,  summ,  type_data)+'  '
        update.message.reply_text(
            text=result_text, 
            reply_markup=keyboard)
    else:
        update.message.reply_text(text=update.message.text,
                              reply_markup=keyboard)


def button(bot, update):
    but_data = update.callback_query.data
    if but_data == '/list':
        list_purchase(bot, update)
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
        keyboard = get_seller(purchase.id)
        text = 'seller saved!'
        update.message.reply_text(text=text)
    elif type_obj == 'category':
        category = Category.get(Category.id==list_ids[1])
        purchase.category = category
        purchase.save()
        keyboard = get_seller(purchase.id)
        text = 'category saved!'
        update.message.reply_text(text=text,
                                reply_markup=keyboard)


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
