# -*- coding: utf-8 -*-
import time

from telegram import ParseMode, ReplyKeyboardRemove, ForceReply
from telegram.ext import ConversationHandler

from config import *
#from models.wait import Wait
#from models.purchase import Purchase
from store.actions import *
from views import *
from recognize import *
from decorators import *
from utils import *



CUR_DIR = os.path.dirname(os.path.realpath(__file__))

run_waiting_command = {
        'new_category': create_category, 
        'new_seller': create_seller
    }



dict_show_item = {
        'purchase': show_purchase_item, 
        'seller': show_seller_item, 
        'category': show_category_item, 
        'user': show_user_item
    }

dict_keyboard_item = {
        'seller': buttons_for_seller_item, 
        'purchase': buttons_for_purchase_item
    }


@is_not_bot()
@lang()
def start(update, context):
    req_user = update.message.from_user
    keyboard = get_button_main()
    user_id = req_user.id
    user = User.get_or_none(User.tg_user_id==user_id)
    if user and user.is_admin:
        text = _('Yes! And You are admins this bot!')
    elif user and user.is_active:
        text = _('Hello!') + ' \n'
        text += show_help()
    else:
        text = _('Hi! This bot will store your user_id and username in database.\n')
        text += _('Keep in mind this service is not commercial in this time and can`t guarantee safety your data.\n')
        text += _('View on this service as a test of the future commercial solution.\n')
        text += _('We work by donates and quality of this service depend values of donates.\n')
        text += _('Please don`t send photo of important documents here.\n')
        text += _('But you can use it FREE.\n')
        text += _('Do you want to register?')
        keyboard = get_button_register()
    update.message.reply_text(text=text,
                        reply_markup=keyboard
                        )

@is_not_bot()
@lang()
def about(update, context):
    text = show_about()
    update.message.reply_text(text=text)
   

@is_not_bot()
@is_allowed_user()
@lang()
def donate(update, context):
    text = show_sberbank_donate_text()
    text += show_paypal_donate_text()
    text += show_patreon_donate_text()
    update.message.reply_text(text=text)


@is_not_bot()
@is_allowed_user()
@lang()
def change_lang(update, context):
    user = update.message.from_user.id
    lang = update.message.text.replace('/lang', '').replace(' ', '')
    if lang in LANGUAGES:
        text = show_change_lang(user, lang)
        keyboard = get_button_main()
        update.message.reply_text(  text=text,
                                reply_markup=keyboard)
    return false


@is_not_bot()
@is_allowed_user()
@lang()
def langs(update, context):
    keyboard = get_button_lang()
    text=_('Change language')
    update.message.reply_text(  text=text,
                                reply_markup=keyboard)


@is_not_bot()
@lang()
def help(update, context):
    keyboard = get_button_main()
    text = show_help()
    update.message.reply_text(  text=text,
                                reply_markup=keyboard)


@is_not_bot()
@is_allowed_user()
@lang()
def list_purchase(update, context):
    user = update.message.from_user.id
    keyboard = get_button_list_purchase(user)
    update.message.reply_text(  text=_('List Purchases'),
                                reply_markup=keyboard)


@is_not_bot()
@is_allowed_user()
@lang()
def purchase(bot, update, args):
    user = update.message.from_user.id
    id = args[0]
    keyboard = get_button_one_task(user, id)
    update.message.reply_text(  text=_('Purchase'),
                                reply_markup=keyboard)


@is_not_bot()
@is_allowed_user()
@lang()
def del_purchase(bot, update, args):
    user = update.message.from_user.id
    id = args[0]
    #text = delete_item(user, 'purchase', id)
    nrows = Purchase.delete().where(Purchase.id == id, 
                                    Purchase.user == user).execute()
    text = _('Deleted')
    keyboard = get_button_menu(user)
    update.message.reply_text(  text=text,
                                reply_markup=keyboard)


@is_not_bot()                                
@is_allowed_user()
@lang()
def list_category(update, context):
    user = update.message.from_user.id
    keyboard = get_button_list_categories(user)
    update.message.reply_text(  text=_('List Сategories'),
                                reply_markup=keyboard)


@is_not_bot()
@is_allowed_user()
@lang()
def list_seller(update, context):
    user_id = update.message.from_user.id
    keyboard = get_button_list_sellers(user_id)
    update.message.reply_text(  text=_('List Sellers'),
                                reply_markup=keyboard)

@is_not_bot()                                
@is_allowed_user()
@lang()
def menu(update, context):
    user, chat_id, message_id = get_update_data(update)
    keyboard = get_button_menu(user)
    context.user_data.clear()
    if update.callback_query:
        context.bot.edit_message_text(
                        chat_id=chat_id, 
                        message_id=message_id, 
                        text=_('Menu'), 
                        reply_markup=keyboard
                        )
    else:
        update.message.reply_text(  text=_('Menu'),
                                reply_markup=keyboard)


def error(bot, update, error_msg):
    module_logger.warning(_('Update caused error "%s"'), error)


@is_not_bot()
@lang()
def new_category(bot, update, args):
    user = update.message.from_user.id
    keyboard = get_button_main()
    name = args[0]
    text = create_category(user, name)
    update.message.reply_text(  text=text,
                                reply_markup=keyboard)


@is_not_bot()
@lang()
def new_seller(bot, update, args):
    user = update.message.from_user.id
    keyboard = get_button_main()
    name = args[0]
    text = create_seller(user, name)
    update.message.reply_text(  text=text,
                                reply_markup=keyboard)


@is_not_bot()
@is_allowed_user()
@lang()
def list_orders(update, context):
    user = update.message.from_user.id
    keyboard = get_button_orders(user)
    update.message.reply_text(  text=_('Orders'),
                                reply_markup=keyboard)


@is_not_bot()                           
@is_allowed_user()
@lang()
def by_seller(update, context):
    user = update.message.from_user.id
#    keyboard = get_button_main()
#    text = show_order_by(user, 'seller')
    text = 'by sellers'   #show_order_by(user,'category')
    keyboard = get_button_order_by(user,'seller')
    update.message.reply_text(  text=text,
                                reply_markup=keyboard, 
                                parse_mode=ParseMode.HTML )


@is_not_bot()
@is_allowed_user()
@lang()
def by_category(update, context):
    user = update.message.from_user.id
#    keyboard = get_button_main()
#    text = show_order_by(user, 'category')
    text = 'by categories'   #show_order_by(user,'category')
    keyboard = get_button_order_by(user,'category')
    update.message.reply_text(  text=text,
                                reply_markup=keyboard, 
                                parse_mode=ParseMode.HTML )

@is_not_bot()    
@is_allowed_user()
@lang()
def request_location_item(update, context):
    user, chat_id, message_id = get_update_data(update)
    but_data = update.callback_query.data
    list_parameters = but_data.split('&')
    type_obj = list_parameters[1]
    id_obj = list_parameters[2]
    context.user_data['type_obj'] = type_obj
    context.user_data['obj_id'] = id_obj
    request_location(update, context)
    return True


@is_not_bot()    
@is_allowed_user()
@lang()
def set_location_item(update, context):
    print('set_location_item')
    user, chat_id, message_id = get_update_data(update)
    obj_id = context.user_data['obj_id']
    type_obj = context.user_data['type_obj']
    geo = update.message.location
    keyboard = buttons_for_seller_item(user, obj_id, type_obj)
    save_geo_position('seller', obj_id, geo)
    text = show_seller_item(user, obj_id)
    context.bot.delete_message(
            chat_id=chat_id,  
            message_id=update.message.reply_to_message.message_id, 
            reply_markup=ReplyKeyboardRemove()
            )
    update.message.reply_text(
            text=text, 
            reply_markup=keyboard
            )
    return True


@is_not_bot()    
@is_allowed_user()
@lang()
def set_location(update, context):
    print('set_location')
    user, chat_id, message_id = get_update_data(update)
    user_location = None
    obj_id = context.user_data['obj_id']
    type_obj = context.user_data['type_obj']
    text = _('Please, choose seller')+ '\n'
    text += show_purchase_item(user, obj_id)
    if update.message.location:
        user_location = update.message.location
        context.user_data['geo'] = user_location
        context.bot.delete_message(
            chat_id=chat_id,  
            message_id=update.message.reply_to_message.message_id, 
            reply_markup=ReplyKeyboardRemove()
            )
    else:
        context.bot.delete_message(
            chat_id=chat_id,  
            message_id=message_id)
        context.bot.delete_message(
            chat_id=chat_id,  
            message_id=message_id-1)
    print('get sellers buttons by geo: ', user_location)
    keyboard = get_button_sellers(user, obj_id, geo=user_location)
    update.message.reply_text(
            text=text, 
            reply_markup=keyboard
            )
    print('RETURN: ', SELLER)
    return SELLER


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END
    

def get_update_data(update):
    if update.callback_query:
        user = update.callback_query.from_user.id
        chat_id = update.callback_query.message.chat.id
        message_id = update.callback_query.message.message_id
    else:
        user = update.message.from_user.id
        chat_id = update.message.chat.id
        message_id = update.message.message_id
    return user, chat_id, message_id
    


@is_not_bot()    
@is_allowed_user()
@lang()
def new_video(update, context):
    date_time = None
    summ = None
    raw = None
    user = update.message.from_user.id
    nrows = Wait.delete().where(Wait.user == user).execute()
    video_file_id = update.message.video.file_id
    video = bot.getFile(video_file_id)
    new_file = bot.get_file(video.file_id)
    new_file.download(os.path.join(PATH_TEMP_FILES,'qrcode.mp4'))
    bot.send_message(
                    update.message.chat.id,
                    text=_('Video uploaded.\nPlease wait. \nRecognize video perhaps take some time.'), 
                    )
    date_time, summ, raw = scan(image=False, video=True)
    bot.delete_message(
            update.message.chat.id, 
            update.message.id+1,
            )
    reply_to_new(update, date_time, summ, user, raw, video_file_id)
    


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
    request_location(update, context)
    context.user_data['type_obj'] = 'purchase'
    context.user_data['obj_id'] = purchase_id
    print('RETURN: ', LOCATION)
    return LOCATION


def request_location(update, context):
    
    keyboard = get_button_geo()
    text = _('Please, send me your location and I find seller around you,\n or press /skip_location')
    if update.message:
        update.message.reply_text(
            text=text, 
            reply_markup=keyboard, 
            )
    else:
        user, chat_id, message_id = get_update_data(update)
        context.bot.send_message(
            chat_id=chat_id, 
            text=text, 
            reply_markup=keyboard
            )


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


def reply_to_new(update, date_time, summ, user, raw=None, photo_file_id=''):
    keyboard = get_button_main()
    text = _('summa or datetime not found')
    raw = None
    if date_time and summ:
        print('datetime: ', date_time )
        print('summ: ', summ)
        check_p = Purchase.select().where(Purchase.summ==summ,
                                Purchase.datetime==date_time, 
                                Purchase.user==user)
        print('check_p: ', check_p)
        if not check_p:
            #confirm = True
            pur = Purchase(name='', 
                        datetime=date_time, 
                        summ=summ, 
                        user=user, 
                        pic=photo_file_id,
                        )
            pur.save()
            keyboard = get_button_categories(user, pur.id, 'purchase')

            text = show_purchase_item(user, pur.id)
            if raw:
                text = _('Sorry I not found QR code.\n')
                text += _('But I tried to recognize the text and found:\n')
                text += _('Date: ' + date_time + '\n')
                text += _('Sum: ' + summ + '\n')
                text += _('Is it true?\n')
                #keyboard = get_button_confirm(pur.id)
                pur.confirm = False
                pur.save()

        else:
            text = _('ATTANTION!\nIts looks like:\n')
            text += show_purchase_item(user, check_p[0].id)
            keyboard = get_button_categories(user, check_p[0].id, 'purchase')
    else:
        text = _('Sorry! I not found nothing\n')
        text += _('You can send me date and summ like this:\n')
        text += _('12.01.19 123.00')
    update.message.reply_text(  text, 
                                reply_markup=keyboard)        

@is_not_bot()
@lang()
def button(update, context):
    chat_id = update.callback_query.message.chat.id
    message_id = update.callback_query.message.message_id
    but_data = update.callback_query.data
    keyboard = get_button_main()
    if but_data == 'register':
        username = update.callback_query.from_user.username
        if not username:
            username = ''
        user_id = update.callback_query.from_user.id
        user = User.get_or_none(tg_user_id=user_id)
        if not user:
            user = User(
                    username=username, 
                    tg_user_id=user_id,
                    is_active=True, 
                    paid_datetime=''
                    )
            user.save()
            admin_text = _('user %(username)s with %(user_id)s\n registered.') % {
                                                    'username': user.username, 
                                                    'user_id': str(user.tg_user_id)
                                                    }
            for k, v in admins.items():
                bot.send_message(
                            v, 
                            text=admin_text, 
                            reply_markup=keyboard
                            )

            text = _('Congratulation! you registered now.\n')
            bot.edit_message_text(chat_id=chat_id,
                        message_id=message_id, 
                        text=text, 
                        parse_mode=ParseMode.HTML)
            time.sleep(5)
#            text = show_about()
#            bot.send_message(
#                        chat_id=chat_id,
#                        text=text)
#            time.sleep(20)
            text = show_help()
            bot.send_message(
                        chat_id=chat_id,
                        text=text, 
                        reply_markup=keyboard, 
                        parse_mode=ParseMode.HTML)
    elif but_data == 'no_register':
        text = _('Ok! Good luck for you.')
        text += _('We hope you return. We will glad to work for you.')
        bot.edit_message_text(chat_id=chat_id,
                        message_id=message_id, 
                        text=text, 
                        parse_mode=ParseMode.HTML)
    else:
        private_actions(update, context)
        return True
       
@is_not_bot()        
@is_allowed_user()
@lang()      
def show_all_sellers(update, context):
    print('show_all_sellers')
    but_data = update.callback_query.data
    user, chat_id, message_id = get_update_data(update)
    list_parameters = but_data.split('&')
    type_obj = list_parameters[1]
    id_obj = list_parameters[2]
    obj = get_item(user, type_obj, id_obj)
    text = show_purchase_item(user, obj.id)
    keyboard = get_button_sellers(user, obj.id)
    context.bot.edit_message_text(
                chat_id=chat_id, 
                message_id=message_id, 
                text=text, 
                reply_markup=keyboard
                )
    print('RETURN: ', SELLER)
    return SELLER

@is_not_bot()        
@is_allowed_user()
@lang()
def change_seller_category_purchase(update, context):
    print('change_seller_category_purchase')
    but_data = update.callback_query.data
    user, chat_id, message_id = get_update_data(update)
    list_parameters = but_data.split('&')
    action = list_parameters[0]
    type_obj = list_parameters[1]
    id_obj = list_parameters[2]
    id_link_obj = list_parameters[3]
    obj = get_item(user, type_obj, id_obj)
    geo = None
    if 'geo' in context.user_data:
        geo = context.user_data['geo']
    if action == 'change_seller':
        obj = change_seller(obj, user, id_link_obj, geo)
        if not obj.category:
            keyboard = get_button_categories(user, obj.id, 'purchase')
            text = _('Please, choose category of purchase')+'\n'
            text += show_purchase_item(user, obj.id)
            context.bot.edit_message_text(
                chat_id=chat_id, 
                message_id=message_id, 
                text=text, 
                reply_markup=keyboard
                )
            print('RETURN: ', CATEGORY)
            return CATEGORY
    else:
        obj = change_category(obj, user, id_link_obj)
    text = show_purchase_item(user, obj.id)
    keyboard = buttons_for_purchase_item(user, obj.id)
    context.user_data.clear()
    context.bot.edit_message_text(
        chat_id=chat_id, 
        message_id=message_id, 
        text=text, 
        reply_markup=keyboard
        )
    print('END CONVERSATION')
    return ConversationHandler.END
    

@is_not_bot()        
@is_allowed_user()
@lang()
def add_seller_category_purchase(update, context):
    print('add_seller_category_purchase')
    but_data = update.callback_query.data
    user, chat_id, message_id = get_update_data(update)
    list_parameters = but_data.split('&')
    action = list_parameters[0]
    type_obj = list_parameters[1]
    id_obj = list_parameters[2]
    obj = dict_types[type_obj].get( dict_types[type_obj].id==id_obj, 
                                    dict_types[type_obj].user==user )
    
    context.user_data['type_obj'] = type_obj
    context.user_data['id_obj'] = id_obj
    context.user_data['action'] = action
    context.bot.send_message(
                chat_id=chat_id, 
                text=_('Send me name of %s' % trans_type(action))
                )
    print('RETURN: ', NAME_SELLER_CATEGORY )
    return NAME_SELLER_CATEGORY 
        
        
@is_not_bot()        
@is_allowed_user()
@lang()
def name_new_seller_category(update, context):
    print('name_new_seller_category')
    user, chat_id, message_id = get_update_data(update)
    type_obj = context.user_data['type_obj']
    purchase_id = context.user_data['id_obj']
    action = context.user_data['action']
    geo = None
    if 'geo' in context.user_data:
        geo = context.user_data['geo']
    if action == 'new_seller':
        text = create_seller(   user, 
                                update.message.text,
                                purchase_id=purchase_id, 
                                geo=geo
                                    )
        keyboard = get_button_categories(user, purchase_id, type_obj)
        context.bot.delete_message(
                    chat_id=chat_id, 
                    message_id=message_id-2
                    )
        update.message.reply_text(
                        text=text, 
                        reply_markup=keyboard
                        )
        print('RETURN: ', CATEGORY)
        return CATEGORY
    else:
        text = create_category( user, 
                                update.message.text, 
                                purchase_id=purchase_id)
        keyboard = buttons_for_purchase_item(user, purchase_id)
        context.user_data.clear()
        update.message.reply_text(
                    text=text, 
                    reply_markup=keyboard
                    )
        print('END CONVERSATION')
        return ConversationHandler.END
    
    
    
#@is_not_bot()        
#@is_allowed_user()
#@lang()
#def add_category_purchase(update, context):
#    
#    but_data = update.callback_query.data
#    user, chat_id, message_id = get_update_data(update)
#    list_parameters = but_data.split('&')
#    action = list_parameters[0]
#    type_obj = list_parameters[1]
#    id_obj = list_parameters[2]
#    obj = dict_types[type_obj].get(dict_types[type_obj].id==id_obj, 
#                                            dict_types[type_obj].user==user )
#    text = show_new_category(user, type=type_obj, obj_id=id_obj)
#    context.bot.send_message(
#                chat_id=chat_id, 
#                text=_('Send me name of %s' % trans_type(action))
#                )
#    return NAME_SELLER_CATEGORY
    

@is_not_bot()        
@is_allowed_user()
@lang()
def delitem(update, context):
    but_data = update.callback_query.data
    print('DIR CALLBACK: ', dir(update.callback_query))
    user, chat_id, message_id = get_update_data(update)
    list_parameters = but_data.split('&')
    #action = list_parameters[0]
    type_obj = list_parameters[1]
    id_obj = list_parameters[2]
    if type_obj == 'user':
        send_delete_info_to_user(bot, id_obj)
    text = delete_item(user, type_obj, id_obj)
    text, keyboard = get_list_items(user, type_obj)
    update.callback_query.answer(_('%s with ID: %s was deleted' %
                                                    (type_obj, id_obj)))
    context.bot.edit_message_text(
                            chat_id=chat_id, 
                            message_id=message_id, 
                            text=text, 
                            reply_markup=keyboard
                            )                                                
    return True
    

@is_not_bot()        
@is_allowed_user()
@lang()
def list_items(update, context):
    but_data = update.callback_query.data
    user, chat_id, message_id = get_update_data(update)
    list_parameters = but_data.split('&')
    type_obj = list_parameters[1]
    text, keyboard = get_list_items(user, type_obj)
    print('USER_DATA: ', context.user_data)
    print('DIR USER_DATA: ', dir(context.user_data))
    print('DIR CONTEXT: ', dir(context))
    context.bot.edit_message_text(
                    chat_id=chat_id, 
                    message_id=message_id,
                    text=text,
                    reply_markup=keyboard)
    return True
    
    
@is_not_bot()        
@is_allowed_user()
@lang()
def show_item(update, context):
    but_data = update.callback_query.data
    user, chat_id, message_id = get_update_data(update)
    list_parameters = but_data.split('&')
    type_obj = list_parameters[1]
    id_obj = list_parameters[2]
    keyboard = get_button_main()
    if type_obj == 'purchase':
        keyboard = buttons_for_purchase_item(user, id_obj)
        text = show_purchase_item(user, id_obj)
    elif type_obj == 'category':
        keyboard =  get_button_del_item(id_obj, type_obj)
        text = show_category_item(user, id_obj)
    elif type_obj == 'seller':
        keyboard = buttons_for_seller_item(user, id_obj, type_obj)
        text = show_seller_item(user, id_obj)
    elif type_obj == 'user':
        text = show_user_item(user, id_obj)
        
    context.bot.edit_message_text(
                    chat_id=chat_id, 
                    message_id=message_id,
                    text=text,
                    reply_markup=keyboard)
    return True
    

@is_not_bot()        
@is_allowed_user()
@lang()
def show_item_on_map(update, context):
    but_data = update.callback_query.data
    user, chat_id, message_id = get_update_data(update)
    list_parameters = but_data.split('&')
    type_obj = list_parameters[1]
    id_obj = list_parameters[2]
    title, position = show_on_map(type_obj, id_obj)
    keyboard = buttons_for_seller_item(user, id_obj, type_obj)
    if position:
        context.bot.delete_message(
            chat_id=chat_id,  
            message_id=message_id, 
            )
        context.bot.send_venue(chat_id, 
                    latitude=position[1], 
                    longitude=position[0], 
                    address=' ', 
                    title=title, 
                    disable_notification=False, 
                    reply_to_message_id=message_id, 
                    reply_markup=keyboard
                    )
    else:
        context.bot.answer_callback_query(
                    callback_query_id, 
                    text=_('this seller have not coordinates'), 
                    show_alert=True
                    )
    return True
    

def get_list_items(user, type_obj):
    text_type = '%ss' % type_obj
    if type_obj == 'category':
        text_type = _('categories')
    text = _('List of %s' % text_type )
    keyboard = get_button_list_items(user, type_obj)
    return text, keyboard
        
        
                    
@is_not_bot()        
@is_allowed_user()
@lang()
def private_actions(update, context):
    bot = context.bot
    but_data = update.callback_query.data
    callback_query_id = update.callback_query.id
    user = update.callback_query.from_user.id
    chat_id = update.callback_query.message.chat.id
    message_id = update.callback_query.message.message_id
    keyboard = get_button_main()
    type_obj = None
    text = ''
    nrows = Wait.delete().where(Wait.user == user).execute()
    if but_data == '/purchases':
        keyboard = get_button_list_purchase(user)
        text=_('List Purchase')
    elif but_data == '/new_category':
        #TODO telegram.ReplyKeyboardRemove
        text = show_new_category(user)
    elif but_data == '/new_seller':
        #TODO telegram.ReplyKeyboardRemove
        text = show_new_seller(user)
    elif but_data == '/orders':
        keyboard = get_button_orders()
        text=_('Orders')
    elif but_data == '/by_seller':
        text = _('summs by sellers and months')   #show_order_by(user,'seller')
        keyboard = get_button_order_by(user,'seller')
    elif but_data == '/by_category':
        text = _('summs by categories and months')   #show_order_by(user,'category')
        keyboard = get_button_order_by(user,'category')
    elif but_data == '/help':
        text = show_help()
    elif but_data == '/langs':
        keyboard = get_button_lang()
        text=_('Change language')
    elif but_data == '/categories':
        keyboard = get_button_list_categories(user)
        text = _('List categories')
        #print('Categories')
        #print(keyboard)
    elif but_data == '/sellers':
        keyboard = get_button_list_sellers(user)
        text = _('List sellers')
    elif but_data == '/users':
        keyboard = get_button_users()
        text = _('List users')
    list_parameters = but_data.split('&')

    if len(list_parameters) > 1:
        action = list_parameters[0]
        #print('action: ',  action)
        keyboard = get_button_main()
        if action == 'lang':
            text = show_change_lang(user, list_parameters[1])
        elif action == '/by_category':
            text = _('By Category %s') %  list_parameters[1]  #show_purchases_by(user, list_parameters[1], 'Category')
            keyboard = get_button_purchases_by(user, list_parameters[1], 'Category')
        elif action == '/by_seller':
            text = _('By Seller: %s') %  list_parameters[1] #show_purchases_by(user, list_parameters[1], 'Seller')
            keyboard = get_button_purchases_by(user, list_parameters[1], 'Seller')
    if len(list_parameters) > 2:
        list_action = ['/by_category', '/by_category']
        if action in list_action:
            month = get_month(int(list_parameters[2]))
            if action == '/by_category':
                text = _('By Category %s and month: %s') %  (list_parameters[1], month)  
                keyboard = get_button_purchases_by(user, list_parameters[1], 'Category', list_parameters[2])
            elif action == '/by_seller':
                text = _('By Seller %s and month: %s') %  (list_parameters[1], month)  
                keyboard = get_button_purchases_by(user, list_parameters[1], 'Seller', list_parameters[2])
        else:
            type_obj = list_parameters[1]
            id_obj = list_parameters[2]
            if type_obj =='user':
                obj = dict_types[type_obj].get(dict_types[type_obj].id==id_obj)
            else:
                obj = dict_types[type_obj].get(dict_types[type_obj].id==id_obj, 
                                            dict_types[type_obj].user==user )
            
            if action == 'new_category':
                text = show_new_category(user, type=type_obj, obj_id=id_obj)
            elif action == 'new_seller':
                text = show_new_seller(user, purchase_id=id_obj)
            
            elif action == 'activate':
                if not obj.is_active:
                    obj.is_active = True
                    obj.save()
                    user_text = _('Your account is activated by admin.\n')
                    user_text += _('You can send me photo or video with QR code on bill and I try to decode or recognize date and summ.\n')
                    user_text += _('Also you can use any programm for decore QR codes and send me result.\n')
                    user_text += _('Finally you can send me date and summ in format: dd.mm.yy 123.00')
                    bot.send_message(obj.tg_user_id,             
                            text=user_text)
                    text = _('User %s activated') % obj.username
                else:
                    text = _('User %s is active') % obj.username
            elif action == 'block':
                if obj.is_active:
                    obj.is_active = False
                    obj.save()
                    user_text = _('Your account is blocked.\n')
                    user_text += _('You can write to administrators of bot.\n')
                    bot.send_message(obj.tg_user_id,             
                                text=user_text)
                    text = _('User %s blocked') % obj.username
                else:
                    text = _('User %s is not active') % obj.username

            elif action == 'show_picture':
                text = show_purchase_item(user, id_obj)
                bot.send_photo(
                    update.callback_query.message.chat.id, 
                    photo=obj.pic, 
                    caption=text, 
                    reply_markup=keyboard)
                return True
    if len(list_parameters) > 3:
        id_link_obj = list_parameters[3]

        if action == 'confirm':
            if id_link_obj == 'yes':
                obj.confirm = True
                obj.save()
                text = _('Confirmed!\n')
                keyboard = get_button_categories(user, id_obj, type_obj)
                text += show_purchase_item(user, id_obj)
            else:
                text += _('You can send me date and summ like this:\n')
                text += _('12.01.19 123.00')
    bot.edit_message_text(chat_id=chat_id,
                        message_id=message_id, 
                        text=text, 
                        reply_markup=keyboard, 
                        parse_mode=ParseMode.HTML 
                        )


def send_delete_info_to_user(bot, id_obj):
    tg_user_id = User.get_or_none(id=id_obj).tg_user_id
    if tg_user_id:
        text = _('Sorry, your account has been deleted.\n')
        text += _('Please contact to administrators of this bot.')
        bot.send_message(chat_id=tg_user_id, text=text)
    return True


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
