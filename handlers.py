# -*- coding: utf-8 -*-

#from decimal import Decimal
from datetime import datetime

#from telegram import (InlineQueryResultArticle, InputTextMessageContent,
#                      InlineKeyboardMarkup, InlineKeyboardButton, 
#                      InputMediaPhoto)
from pyzbar.pyzbar import decode
from PIL import Image

from config import *
from db_models import *
from views import *

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
    
    
def help(bot, update):
    keyboard = get_button_main()
    text = show_help()
    update.message.reply_text(  text=text,
                                reply_markup=keyboard)
    

@is_allowed_user()
def list_purchase(bot, update):
    keyboard = get_list_purchase()
    update.message.reply_text(  text='List Purchases',
                                reply_markup=keyboard)
                                
@is_allowed_user()
def list_category(bot, update):
    keyboard = get_list_categories()
    update.message.reply_text(  text='List Сategories',
                                reply_markup=keyboard)
                                

@is_allowed_user()
def list_seller(bot, update):
    keyboard = get_list_sellers()
    update.message.reply_text(  text='List Sellers',
                                reply_markup=keyboard)
                                
                                
@is_allowed_user()                                
def menu(bot, update):
    keyboard = show_menu()
    update.message.reply_text(  text='Menu',
                                reply_markup=keyboard)
       
    
def error(bot, update, error_msg):
    module_logger.warning('Update caused error "%s"', error)


@is_allowed_user()
def new_category(bot, update):
    keyboard = get_button_main()
    text = show_new_category(update)
    update.message.reply_text(  text=text,
                                reply_markup=keyboard)
                                
                                
@is_allowed_user()
def new_seller(bot, update):
    keyboard = get_button_main()
    text = show_new_seller(update)
    update.message.reply_text(  text=text,
                                reply_markup=keyboard)
                                

@is_allowed_user()
def list_orders(bot, update):
    keyboard = show_orders()
    update.message.reply_text(  text='Orders',
                                reply_markup=keyboard)
    
                           
@is_allowed_user()
def by_sellers(bot, update):
    keyboard = show_order_by('seller')
    update.message.reply_text(  text='Order by seller',
                                reply_markup=keyboard)
    

@is_allowed_user()
def by_categories(bot, update):
    keyboard = show_order_by('category')
    update.message.reply_text(  text='Order by categories',
                                reply_markup=keyboard)
    
    
@is_allowed_user()
def new_msg(bot, update):
    keyboard = get_button_main()
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
            if type_data == 'QRCODE':
                list_data = rec.data.decode("utf-8").split('&')
                date_time = datetime.strptime(list_data[0].replace('t=', ''), '%Y%m%dT%H%M%S').date()
                summ = float(list_data[1].replace('s=', ''))
                pur = Purchase(name='', 
                                datetime = date_time, 
                                summ = summ
                                )
                pur.save()
                text = show_purchase_item(pur.id)
                keyboard = get_button_categories(pur.id)
    else:
        print(Status.get(name='wait_seller_name').value)
        print(Status.get(name='wait_category_name').value)
        if Status.get(name='wait_seller_name').value:
            new_seller = Seller(name=update.message.text)
            new_seller.save()
            status = Status.get(name='wait_seller_name')
            status.value = False
            status.save()
            text='Seller created!'
        elif Status.get(name='wait_category_name').value:
            new_cat = Category(name=update.message.text)
            new_cat.save()
            status = Status.get(name='wait_category_name')
            status.value = False
            status.save()
            text = 'Category created!'
    update.message.reply_text(  text = text, 
                                reply_markup=keyboard)
            
        
@is_allowed_user()
def button(bot, update):
    but_data = update.callback_query.data
    keyboard = get_button_main()
    type_obj = None
    text = ''
    if but_data == '/purchases':
        keyboard = get_list_purchase()
        text='List Purchase'
    elif but_data == '/new_category':
        text = new_category(bot, update)
    elif but_data == '/new_seller':
        text = new_seller(bot, update)
    elif but_data == '/orders':
        text='Orders'
    elif but_data == '/by_seller':
        text = show_order_by('seller')
    elif but_data == '/by_category':
        text = show_order_by('category')
    elif but_data == '/menu':
        keyboard = show_menu()
        text='Menu'
    elif but_data == '/categories':
        keyboard = get_list_categories()
        text = 'List categories'
    elif but_data == '/sellers':
        keyboard = get_list_sellers()
        text = 'List sellers'
    list_parameters = but_data.split('&')
    if len(list_parameters) == 2:
        type_obj = list_parameters[0]
        id_obj = list_parameters[1]
        if type_obj == 'purchase':
            keyboard = get_button_categories(id_obj)
            text = show_purchase_item(id_obj)
        elif type_obj == 'category':
            keyboard =  get_button_del_item(id_obj, type_obj)
            text = show_category_item(id_obj)
        elif type_obj == 'seller':
            keyboard =  get_button_del_item(id_obj, type_obj)
            text = show_seller_item(id_obj)
    if len(list_parameters) == 3:
        type_obj = list_parameters[0]
        id_obj = list_parameters[1]
        if list_parameters[0] == 'delitem':
            typeitem = list_parameters[1]
            iditem = list_parameters[2]
            text = delete_item(typeitem, iditem)
    if type_obj == 'change_seller':
        purchase = Purchase.get(Purchase.id==list_parameters[1])
        keyboard = get_button_sellers(purchase.id)
        seller = Seller.get(Seller.id==list_parameters[2])
        purchase.seller = seller
        purchase.save()
        text='seller saved! %s %s %s' % (text,  purchase.datetime,  purchase.summ)
    elif type_obj == 'change_category':
        purchase = Purchase.get(Purchase.id==list_parameters[1])
        keyboard = get_button_sellers(purchase.id)
        category = Category.get(Category.id==list_parameters[2])
        purchase.category = category
        purchase.save()
        text='%s %s' % (purchase.datetime,  purchase.summ)
    
    bot.send_message(update.callback_query.message.chat.id,             
                    text=text, 
                    reply_markup=keyboard)
    

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
