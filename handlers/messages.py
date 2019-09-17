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
    photo_file_id = update.message.photo[-1].file_id
    #print('ID: ', photo_file_id)
    new_file = update.message.photo[-1].get_file()
    new_file.download(os.path.join(PATH_TEMP_FILES,'qrcode.jpg'))
    date_time, summ, raw = scan(image=True, video=False)
    text, purchase_id, double = save_purchase(date_time, summ, user, raw, photo_file_id=photo_file_id)
    if double:
        keyboard = buttons_for_purchase_item(user, purchase_id)
        text = _('ATTANTION!\nIts looks like:\n')
        text += show_purchase_item(user, purchase_id)
        context.bot.send_message(
                    chat_id=chat_id, 
                    text=text,
                    reply_markup=keyboard)
        return ConversationHandler.END
    elif not purchase_id:
        context.bot.send_message(
                    chat_id=chat_id, 
                    text=text)
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
    user, chat_id, message_id = get_update_data(update)
    if update.message.video:
        video_file_id = update.message.video.file_id
    if update.message.video_note:
        video_file_id = update.message.video_note.file_id
    video = context.bot.getFile(video_file_id)
    new_file = context.bot.get_file(video.file_id)
    new_file.download(os.path.join(PATH_TEMP_FILES,'qrcode.mp4'))
#    context.bot.answer_callback_query(
#                    update.callback_query.id, 
#                    text=_('this seller have not coordinates'), 
#                    show_alert=True
#                    )
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
    user, chat_id, message_id = get_update_data(update)
    date_time, summ = parse_text(update.message.text)
    text, purchase_id, double = save_purchase(date_time, summ, user)
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
def save_media_purchase(update, context):
    user, chat_id, message_id = get_update_data(update)
    id_obj= context.user_data['id']
    if update.message.photo:
        media_file_id = update.message.photo[-1].file_id
    elif update.message.video:
        media_file_id = update.message.video.file_id
    elif update.message.video_note:
        media_file_id = update.message.video_note.file_id
    result = save_media(id_obj, media_file_id)
    keyboard = buttons_for_purchase_item(user, id_obj)
    context.user_data.clear()
    context.bot.delete_message(
                chat_id=chat_id, 
                message_id=message_id
                )
    context.bot.edit_message_text(
                chat_id=chat_id, 
                message_id=message_id-1,
                text=result,
                reply_markup=keyboard)
        
    return ConversationHandler.END
    
