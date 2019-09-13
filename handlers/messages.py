from telegram.ext import ConversationHandler

from store.actions import *
from views import *
from keyboards import *
from recognize import *
from decorators import *
from utils import *

from handlers.callbacks import request_location

@is_not_bot()    
@is_allowed_user()
@lang()
def new_photo(update, context):
    date_time = None
    summ = None
    raw = None
    photo_file_id = ''
    user, chat_id, message_id = get_update_data(update)
    bot = context.bot
    print('NEW PHOTO')
    new_file = update.message.photo[-1].get_file()
    new_file.download(os.path.join(PATH_TEMP_FILES,'qrcode.jpg'))
    date_time, summ, raw = scan(image=True, video=False)
    text, purchase_id, double = save_purchase(date_time, summ, user, raw, photo_file_id)
    if double:
        keyboard = buttons_for_purchase_item(user, purchase_id)
        text = _('ATTANTION!\nIts looks like:\n')
        text += show_purchase_item(user, purchase_id)
        context.bot.send_message(
                    chat_id=chat_id, 
                    text=text,
                    reply_markup=keyboard)
        return ConversationHandler.END
    request_location(update, context)
    context.user_data['type_obj'] = 'purchase'
    context.user_data['obj_id'] = purchase_id
    print('RETURN: ', LOCATION)
    return LOCATION
    
    
@is_not_bot()    
@is_allowed_user()
@lang()
def new_video(update, context):
    date_time = None
    summ = None
    raw = None
    print('NEW VIDEO')
    user = update.message.from_user.id
    video_file_id = update.message.video.file_id
    video = context.bot.getFile(video_file_id)
    new_file = context.bot.get_file(video.file_id)
    new_file.download(os.path.join(PATH_TEMP_FILES,'qrcode.mp4'))
    context.bot.send_message(
                    update.message.chat.id,
                    text=_('Video uploaded.\nPlease wait. \nRecognize video perhaps take some time.'), 
                    )
    date_time, summ, raw = scan(image=False, video=True)
    text, purchase_id, double = save_purchase(date_time, summ, user, raw, video_file_id)
    if double:
        keyboard = buttons_for_purchase_item(user, purchase_id)
        text = _('ATTANTION!\nIts looks like:\n')
        text += show_purchase_item(user, purchase_id)
        context.bot.send_message(
                    chat_id=chat_id, 
                    text=text,
                    reply_markup=keyboard)
        return ConversationHandler.END
    request_location(update, context)
    context.user_data['type_obj'] = 'purchase'
    context.user_data['obj_id'] = purchase_id
    print('RETURN: ', LOCATION)
    return LOCATION
    

@is_not_bot()    
@is_allowed_user()
@lang()
def new_text(update, context):
    date_time = None
    summ = None
    wait_command=None
    photo_file_id = ''
    user = update.message.from_user.id
    chat_id = update.message.chat.id
    query = Wait.select().where(Wait.user == user)
    if query.exists():
        wait_command = Wait.get(user=user).command
    if wait_command:
        splitted_wait_command = wait_command.split('&')
        command = splitted_wait_command[0]
        print('command: ', command)
        if command == 'new_category':
            text = create_category(  user, 
                                    update.message.text)
        elif command == 'new_seller':
            text, seller_id = create_seller(  user, 
                                    update.message.text)
            keyboard = get_button_categories(user, seller_id, 'seller')
                       
        elif command == 'new_seller_purchase':
            purchase_id = splitted_wait_command[1]
            text, seller_id = create_seller(user, 
                                update.message.text,
                                purchase_id=purchase_id
                                )
            keyboard = get_button_geo()
            update.message.reply_text(text)
            text_loc =  _('what is location?\nID: %s\n TYPE: %s' % (seller_id, 'seller'))
            bot.send_message(
                    chat_id=chat_id,
                    text=text_loc, 
                    reply_markup=keyboard
                    )
            return
        elif command == 'new_category_purchase':
            purchase_id = splitted_wait_command[1]
            text = create_category( user, 
                                    update.message.text, 
                                    purchase_id=purchase_id)
            keyboard = get_button_sellers(user, purchase_id)
        elif command == 'new_category_seller':
            seller_id = splitted_wait_command[1]
            text = create_category( user, 
                                    update.message.text, 
                                    seller_id=seller_id)
            keyboard = get_button_categories(user, seller_id, 'seller')
        nrows = Wait.delete().where(Wait.user == user).execute()
        update.message.reply_text(  text, 
                            reply_markup=keyboard)
        return True
    else:
        date_time, summ = parse_text(update.message.text)
    reply_to_new(update, date_time, summ, user)
