# -*- coding: utf-8 -*-
import time

from telegram import ParseMode, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from config import *
#from models.wait import Wait
#from models.purchase import Purchase
from store.actions import *
from keyboards import *
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


def error(bot, update, error_msg):
    module_logger.warning(_('Update caused error "%s"'), error)

  
@is_not_bot()    
@is_allowed_user()
@lang()
def show_change_seller(update, context):
    user, chat_id, message_id = get_update_data(update)
    but_data = update.callback_query.data
    list_parameters = but_data.split('&')
    id_obj = list_parameters[1]
    text = show_purchase_item(user, id_obj)
    keyboard = get_button_sellers(user, id_obj)
    context.bot.edit_message_text(
        chat_id=chat_id, 
        message_id=message_id, 
        text=text, 
        reply_markup=keyboard
        )


@is_not_bot()    
@is_allowed_user()
@lang()
def show_change_category(update, context):
    user, chat_id, message_id = get_update_data(update)
    but_data = update.callback_query.data
    list_parameters = but_data.split('&')
    type_obj = list_parameters[1]
    id_obj = list_parameters[2]
    if type_obj == 'purchase':
        text = show_purchase_item(user, id_obj)
    elif type_obj == 'seller':
        text = show_seller_item(user, id_obj)
    keyboard = get_button_categories(user, id_obj, type_obj)
    context.bot.edit_message_text(
        chat_id=chat_id, 
        message_id=message_id, 
        text=text, 
        reply_markup=keyboard
        )


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
def register(update, context):
    
    user, chat_id, message_id = get_update_data(update)
    username = update.callback_query.from_user.first_name
    user_id = update.callback_query.from_user.id
    if not username:
        username = user_id
    user = User.get_or_none(tg_user_id=user_id)
    keyboard = get_button_main()
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
            context.bot.send_message(
                        v, 
                        text=admin_text, 
                        reply_markup=keyboard
                        )

        text = _('Congratulation! you registered now.\n')
        context.bot.edit_message_text(chat_id=chat_id,
                    message_id=message_id, 
                    text=text, 
                    parse_mode=ParseMode.HTML)
        time.sleep(5)

        text = show_help()
        context.bot.send_message(
                    chat_id=chat_id,
                    text=text, 
                    reply_markup=keyboard, 
                    parse_mode=ParseMode.HTML)


@is_not_bot()
@lang()
def no_register(update, context):
    
    user, chat_id, message_id = get_update_data(update)
    text = _('Ok! Good luck for you.')
    text += _('We hope you return. We will glad to work for you.')
    context.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id, 
                    text=text, 
                    parse_mode=ParseMode.HTML)

       
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
        obj = change_category(obj, user, id_link_obj, type_obj)
    if type_obj == 'purchase':
        text = show_purchase_item(user, obj.id)
        keyboard = buttons_for_purchase_item(user, obj.id)
    else:
        text = show_seller_item(user, obj.id)
        keyboard = buttons_for_seller_item(user, obj.id, type_obj)
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
    type_obj = None
    purchase_id = None
    if 'type_obj' in context.user_data:
        type_obj = context.user_data['type_obj']
    if 'id_obj' in context.user_data:
        purchase_id = context.user_data['id_obj']
    action = context.user_data['action']
    geo = None
    if 'geo' in context.user_data:
        geo = context.user_data['geo']
    if action == 'new_seller':
        text, obj = create_seller(   user, 
                                update.message.text,
                                purchase_id=purchase_id, 
                                geo=geo
                                    )
        if type_obj == 'purchase':
            keyboard = get_button_categories(user, purchase_id, type_obj)
        else:
            keyboard = get_button_categories(user, obj.id, 'seller')
            text += show_seller_item(user, obj.id)
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
        if type_obj == 'purchase':
            keyboard = buttons_for_purchase_item(user, purchase_id)
        else:
            keyboard = get_button_list_items(user, 'category')
        context.user_data.clear()
        update.message.reply_text(
                    text=text, 
                    reply_markup=keyboard
                    )
        print('END CONVERSATION')
        return ConversationHandler.END
    
    
@is_not_bot()        
@is_allowed_user()
@lang()
def add_seller_category(update, context):
    print('add_seller_category')
    user, chat_id, message_id = get_update_data(update)
    action = update.callback_query.data
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
def delitem(update, context):
    but_data = update.callback_query.data
    print('DIR CALLBACK: ', dir(update.callback_query))
    user, chat_id, message_id = get_update_data(update)
    list_parameters = but_data.split('&')
    type_obj = list_parameters[1]
    id_obj = list_parameters[2]
    if type_obj == 'user':
        send_delete_info_to_user(context.bot, id_obj)
    text = delete_item(user, type_obj, id_obj)
    if type_obj == 'user':
        keyboard = get_button_users()
        text = _('List users')
    else:
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
        
#    context.bot.edit_message_text(
#                    chat_id=chat_id, 
#                    message_id=message_id,
#                    text=text,
#                    reply_markup=keyboard)
    context.bot.delete_message(
        chat_id=chat_id,  
        message_id=message_id, 
        )
    context.bot.send_message(
                chat_id=chat_id, 
                text=text,
                reply_markup=keyboard)
    return True
    
    
@is_not_bot()        
@is_allowed_user()
@lang()
def show_picture(update, context):
    but_data = update.callback_query.data
    user, chat_id, message_id = get_update_data(update)
    list_parameters = but_data.split('&')
    type_obj = list_parameters[1]
    id_obj = list_parameters[2]
    obj = get_item(user, type_obj, id_obj)
    text = show_purchase_item(user, id_obj)
    keyboard = buttons_for_purchase_item(user, id_obj)
    context.bot.delete_message(
            chat_id=chat_id, 
            message_id=message_id
            )
    try:
        context.bot.send_photo(
            update.callback_query.message.chat.id, 
            photo=obj.pic, 
            caption=text, 
            reply_markup=keyboard)
    except Exception as e:
        print('ERROR: ', e.__dict__)
        print('ERROR: ', e)
        if e.message == 'Type of file mismatch':
            try:
                print('ERROR: ', e.__dict__)
                print('ERROR: ', e)
                context.bot.send_video(
                    update.callback_query.message.chat.id, 
                    video=obj.pic, 
                    caption=text, 
                    reply_markup=keyboard)
            except Exception as e:
                if e.message == 'Type of file mismatch':
                    print('ERROR: ', e.__dict__)
                    print('ERROR: ', e)
                    context.bot.send_video_note(
                        update.callback_query.message.chat.id, 
                        video_note=obj.pic, 
                        caption=text, 
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
                    reply_markup=keyboard
                    )
    else:
        context.bot.answer_callback_query(
                    update.callback_query.id, 
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
def orders(update, context):
    
    user, chat_id, message_id = get_update_data(update)
    keyboard = get_button_orders()
    text=_('Orders')
    context.bot.edit_message_text(
                chat_id=chat_id, 
                message_id=message_id,
                text=text,
                reply_markup=keyboard)


@is_not_bot()        
@is_allowed_user()
@lang()
def order_by(update, context):
    
    user, chat_id, message_id = get_update_data(update)
    but_data = update.callback_query.data
    list_parameters = but_data.split('&')
    type_obj = list_parameters[1]
    text = _('summs by %ss and months') %  type_obj
    keyboard = get_button_order_by(user, type_obj)
    
    context.bot.edit_message_text(
                chat_id=chat_id, 
                message_id=message_id,
                text=text,
                reply_markup=keyboard)


@is_not_bot()        
@is_allowed_user()
@lang()
def order_by_category(update, context):
    
    user, chat_id, message_id = get_update_data(update)
    but_data = update.callback_query.data
    list_parameters = but_data.split('&')
    cat = list_parameters[1]
    month = None
    if len(list_parameters) > 2:
        month = list_parameters[2]
    text = _('By Category %s') %  list_parameters[1]  #show_purchases_by(user, list_parameters[1], 'Category')
    keyboard = get_button_purchases_by(user, cat, 'Category', month)
            
    context.bot.edit_message_text(
                chat_id=chat_id, 
                message_id=message_id,
                text=text,
                reply_markup=keyboard)
            

@is_not_bot()        
@is_allowed_user()
@lang()
def order_by_seller(update, context):
    
    user, chat_id, message_id = get_update_data(update)
    but_data = update.callback_query.data
    list_parameters = but_data.split('&')
    seller = list_parameters[1]
    month = None
    if len(list_parameters) > 2:
        month = list_parameters[2]
    text = _('By Seller %s') %  list_parameters[1]  #show_purchases_by(user, list_parameters[1], 'Category')
    keyboard = get_button_purchases_by(user, seller, 'Seller', month)
            
    context.bot.edit_message_text(
                chat_id=chat_id, 
                message_id=message_id,
                text=text,
                reply_markup=keyboard)


@is_not_bot()        
@is_allowed_user()
@lang()
def list_langs(update, context):
    
    user, chat_id, message_id = get_update_data(update)
    keyboard = get_button_lang()
    text=_('Change language')
    context.bot.edit_message_text(
                chat_id=chat_id, 
                message_id=message_id,
                text=text,
                reply_markup=keyboard)


@is_not_bot()        
@is_allowed_user()
@lang()
def set_lang(update, context):
    
    user, chat_id, message_id = get_update_data(update)
    but_data = update.callback_query.data
    list_parameters = but_data.split('&')
    text = show_change_lang(user, list_parameters[1])
    keyboard = get_button_main()
    context.bot.edit_message_text(
                chat_id=chat_id, 
                message_id=message_id,
                text=text,
                reply_markup=keyboard)
    

@is_not_bot()        
@is_allowed_user()
@lang()
def but_help(update, context):
    
    user, chat_id, message_id = get_update_data(update)
    text = show_help()
    keyboard = get_button_main()
    context.bot.edit_message_text(
                chat_id=chat_id, 
                message_id=message_id,
                text=text,
                reply_markup=keyboard)


@is_not_bot()        
@is_allowed_user()
@lang()
def list_users(update, context):
    
    user, chat_id, message_id = get_update_data(update)
    keyboard = get_button_users()
    text = _('List users')
    context.bot.edit_message_text(
                chat_id=chat_id, 
                message_id=message_id,
                text=text,
                reply_markup=keyboard)
    
    
@is_not_bot()        
@is_allowed_user()
@lang()
def block(update, context):
    but_data = update.callback_query.data
    user, chat_id, message_id = get_update_data(update)
    list_parameters = but_data.split('&')
    type_obj = list_parameters[1]
    id_obj = list_parameters[2]
    obj = get_item(user, type_obj, id_obj)
    if obj.is_active:
        obj.is_active = False
        obj.save()
        user_text = _('Your account is blocked.\n')
        user_text += _('You can write to administrators of bot.\n')
        context.bot.send_message(obj.tg_user_id,             
                    text=user_text)
        text = _('User %s blocked') % obj.username
    else:
        text = _('User %s is not active') % obj.username
    keyboard = get_button_users()
    context.bot.edit_message_text(
                chat_id=chat_id, 
                message_id=message_id,
                text=text,
                reply_markup=keyboard)
    
    
@is_not_bot()        
@is_allowed_user()
@lang()
def activate(update, context):
    but_data = update.callback_query.data
    user, chat_id, message_id = get_update_data(update)
    list_parameters = but_data.split('&')
    type_obj = list_parameters[1]
    id_obj = list_parameters[2]
    obj = get_item(user, type_obj, id_obj)
    if not obj.is_active:
        obj.is_active = True
        obj.save()
        user_text = _('Your account is activated by admin.\n')
        user_text += _('You can send me photo or video with QR code on bill and I try to decode or recognize date and summ.\n')
        user_text += _('Also you can use any programm for decore QR codes and send me result.\n')
        user_text += _('Finally you can send me date and summ in format: dd.mm.yy 123.00')
        context.bot.send_message(obj.tg_user_id,             
                text=user_text)
        text = _('User %s activated') % obj.username
    else:
        text = _('User %s is active') % obj.username
    keyboard = get_button_users()
    context.bot.edit_message_text(
                chat_id=chat_id, 
                message_id=message_id,
                text=text,
                reply_markup=keyboard)


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
