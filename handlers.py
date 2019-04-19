# -*- coding: utf-8 -*-
import pickle
#import emoji
import time, datetime
from decimal import Decimal
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


def get_category():
    
    categories = Category.select()
    
    buttons = []
    for category in categories:
        buttons.append(
            InlineKeyboardButton(  
                category.name, 
                callback_data=category.id))
    keyboard = InlineKeyboardMarkup([buttons])
    return keyboard

    
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
def new_msg(bot, update):
    keyboard = get_category()
    if update.message.media_group_id:
        flag_send = False
        photo_file_id = update.message.photo[-1].get_file().file_id
        if not os.path.exists('files/'+update.message.media_group_id+'.txt'):
            flag_send = True
        with open('files/'+update.message.media_group_id+'.txt', 'a') as file:
            file.write(photo_file_id+',')
            #print('save to file: ', photo_file_id)
        
        if flag_send:
            new_caption = update.message.caption.replace('#','')
            update.message.reply_photo(
                photo=photo_file_id, 
                caption="%s # %s" % (new_caption,update.message.media_group_id), 
                reply_markup=keyboard)
            #print("reply_photo for group")
    elif update.message.photo:
        photo_file_id = update.message.photo[-1].file_id
        foto = bot.getFile(photo_file_id)
        new_file = bot.get_file(foto.file_id)
        new_file.download(os.path.join(PATH_TEMP_FILES,'qrcode.jpg'))
        list_decoded = decode(Image.open(os.path.join(PATH_TEMP_FILES,'qrcode.jpg')))
        for rec in list_decoded:
            list_data = rec.data.decode("utf-8").split('&')
            date_time = datetime.strptime(list_data[0].replace('t=', ''), '%Y%m%dT%H%M').date()
            sum = Decimal(list_data[1].replace('s=', ''))
            type_data = rec.type
            result_text = "%s %s %s" % (date_time,  sum,  type_data)+'  '
        update.message.reply_text(
            text=result_text, 
            reply_markup=keyboard)
    else:
        update.message.reply_text(text=update.message.text,
                              reply_markup=keyboard)


def button(bot, update):
    if update.callback_query.data in CHANNELS:
        channel_button_pressed(bot,update)
    elif update.callback_query.data == 'comments':
        text = make_measure(bot,update)
    elif update.callback_query.data.find('like') != -1:
        like_button_pressed(bot,update)


@is_allowed_user()
def channel_button_pressed(bot, update):
    query = update.callback_query
    keyboard = get_buttons('post')
    
    if query.data.find('fb_') != -1:
        #if query.data.find('kefir') != -1:
        #elif query.data.find('ecodome') != -1:
        fb.publication_post(query.data,text)
    else:
        if query.message.caption:
            media_id = query.message.caption.split('#')[1].replace(' ','')
            reply_caption = query.message.caption.split('#')[0].split('published')[0]
            if media_id:
                list_media=[]
                with open('files/'+media_id+'.txt', 'r') as file:
                    count_id = 0
                    for id in file.read().split(','):
                        count_id += 1
                        if id:
                            list_media.append(InputMediaPhoto(id))
                bot.send_media_group(
                    chat_id=CHANNELS[query.data],
                    media=list_media, 
                    caption=reply_caption, 
                    reply_markup=keyboard)
                bot.send_message(
                        chat_id=CHANNELS[query.data],
                        text=reply_caption, 
                        reply_markup=keyboard)
                    
            else:
                query_text = query.message.caption
                photo_file_id = query.message.photo[-1].get_file().file_id
                bot.send_photo(
                    chat_id=CHANNELS[query.data],
                    photo=photo_file_id, 
                    caption=update.message.caption, 
                    reply_markup=keyboard)
        else:
            query_text = query.message.text
            text = query_text.split('published')[0]
            bot.send_message(
                        chat_id=CHANNELS[query.data],
                        text=text, 
                        reply_markup=keyboard)
    keyboard = get_buttons('channel')
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    if query.message.caption:
        bot.edit_message_caption(caption='%s \npublished to %s (%s)' % (query.message.caption,query.data,st),
                          chat_id=query.message.chat.id,
                          message_id=query.message.message_id,
                          reply_markup=keyboard)
    else:
        bot.edit_message_text(text='%s \npublished to %s (%s)' % (query.message.text,query.data,st),
                          chat_id=query.message.chat.id,
                          message_id=query.message.message_id,
                          reply_markup=keyboard)


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
