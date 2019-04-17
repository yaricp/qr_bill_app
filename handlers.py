# -*- coding: utf-8 -*-
import pickle
import emoji
import time, datetime

from telegram import (InlineQueryResultArticle, InputTextMessageContent,
                      InlineKeyboardMarkup, InlineKeyboardButton, 
                      InputMediaPhoto)


import facebook_bot as fb
from config import *


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


def get_buttons(target, data='like:0,dislike:0', count_like=0, count_dislike=0):
    
    buttons_post = [[InlineKeyboardButton(  emoji.emojize(':thumbs_up: ')+str(count_like), 
                                            callback_data=data+',like'),
                    InlineKeyboardButton(   emoji.emojize(':thumbs_down: ')+str(count_dislike), 
                                            callback_data=data+',dis')],
                    ]
    #[InlineKeyboardButton("comments", callback_data="comments")]]
    
    
    buttons_channel = [[InlineKeyboardButton(channel_name, 
                        callback_data=channel_name) for channel_name in CHANNELS]]
    buttons = buttons_post if target == 'post' else buttons_channel
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard

    
def error(bot, update, error_msg):
    module_logger.warning('Update caused error "%s"', error)



@is_allowed_user()
def start(bot, update):

    keyboard = get_buttons()
    update.message.reply_text('Hello! I am bot of sibecodome. It is smart home!',
                              reply_markup=keyboard)


@is_allowed_user()
def new_msg(bot, update):
    #print("Start New MSG")
    #print("Update.message.photo: ", update.message.photo)
    keyboard = get_buttons('channel')
    if update.message.media_group_id:
        #print('MediaGroup')
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
        #print("Photo")
        photo_file = update.message.photo[-1].get_file()
        update.message.reply_photo(
            photo=photo_file.file_id, 
            caption=update.message.caption, 
            reply_markup=keyboard)
    elif update.message.video:
        update.message.reply_video(video=update.message.video,
                              reply_markup=keyboard)
    else:
        update.message.reply_text(text=update.message.text,
                              reply_markup=keyboard)
    #print("reply")

def get_like_dislike(data):
    """ make dict of like - dislike.
    You can test it:   
    >>> get_like_dislike('like:5,dislike:4')
    {'like': 5, 'dislike': 4}
    """
    dict_out ={'like':int(data.split(',')[0].split(':')[1]),
               'dis':int(data.split(',')[1].split(':')[1])}
    return dict_out
    
    
def get_liked_from_database():
    dict_liked = {}
    if os.path.exists("database.pickle"):
        with open('database.pickle', 'rb+') as file:
            if file.read():
                file.seek(0)
                dict_liked = pickle.load(file)
    else:
        with open('database.pickle', 'wb') as file:
            pickle.dump({}, file)
            
    return dict_liked


def write_liked_to_database(key, value):
    dict_liked = get_liked_from_database()
    dict_liked.update({key:value})
    with open('database.pickle', 'wb') as file:
        pickle.dump(dict_liked, file)
    
    
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

def like_button_pressed(bot, update):
    '''
    handler of like or dislike button press.

    '''
    query = update.callback_query
    keyboard = get_buttons('post')
    id_chat = query.chat_instance
    id_post = query.message.message_id
    id_user = query.from_user.id
    key_like_database = '%s%s%s' % (id_chat, id_post, id_user)
    is_user_liked_post = get_liked_from_database().get(key_like_database, 0)
    dict_like_dislike = get_like_dislike(query.data)
    action = query.data.split(',')[2]
    if is_user_liked_post == 0:
            dict_like_dislike[action] += 1
            write_liked_to_database(key_like_database, action)  #press one button
            print('pressed ',action)
    else:
        if is_user_liked_post == action :
            dict_like_dislike[action] -=1
            write_liked_to_database(key_like_database, 0)  #unpress one button
            print('unpressed ',action)
        else:
            dict_like_dislike[action] +=1
            dict_like_dislike[is_user_liked_post] -=1
            write_liked_to_database(key_like_database, action)  #unpress one button
            print('change ',is_user_liked_post, ' to ',action)
    count_like = dict_like_dislike['like']
    count_dislike = dict_like_dislike['dis']
    data_button = 'like:%i,dislike:%i' % (count_like,count_dislike)
    keyboard = get_buttons('post',
                            data=data_button,
                            count_like=count_like,
                            count_dislike=count_dislike)
    bot.edit_message_text(text=query.message.text,
                          chat_id=query.message.chat.id, 
                          message_id=query.message.message_id, 
                          reply_markup=keyboard)
    


@is_allowed_user()
def publication_to_channel(channel,message):
    query.message.reply_text(message,reply_markup=keyboard)


@is_allowed_user()
def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)


@is_allowed_user()
def inline_caps(bot, update):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
             id=query.upper(),
             title='Caps',
             input_message_content=InputTextMessageContent(query.upper())
         )
     )
    bot.answer_inline_query(update.inline_query.id, results)
    
    
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
