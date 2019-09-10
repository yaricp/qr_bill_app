# -*- coding: utf-8 -*-
import time

from telegram import ParseMode, ReplyKeyboardRemove, ForceReply
from telegram.ext import ConversationHandler

from config import *
from models.wait import Wait
from models.purchase import Purchase
from views import *
from recognize import *
from decorators import *
from utils import *



CUR_DIR = os.path.dirname(os.path.realpath(__file__))

run_waiting_command = {
        'new_category': create_category, 
        'new_seller': create_seller
    }

dict_types = {
        'purchase': Purchase, 
        'seller': Seller, 
        'category': Category, 
        'user': User
    }
    
dict_show_item = {
        'purchase': show_purchase_item, 
        'seller': show_seller_item, 
        'category': show_category_item, 
        'user': show_user_item
    }
    
#dict_keyboard_item = {
#        'seller':
#
#    }
    

@is_not_bot()
@lang()
def start(bot, update):
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
def about(bot, update):
    text = show_about()
    update.message.reply_text(text=text)
    

@is_not_bot()
@is_allowed_user()
@lang()
def donate(bot, update):
    text = show_sberbank_donate_text()
    text += show_paypal_donate_text()
    text += show_patreon_donate_text()
    update.message.reply_text(text=text)


@is_not_bot()
@is_allowed_user()
@lang()
def change_lang(bot, update):
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
def langs(bot, update):
    keyboard = get_button_lang()
    text=_('Change language')
    update.message.reply_text(  text=text,
                                reply_markup=keyboard)


@is_not_bot()
@lang()
def help(bot, update):
    keyboard = get_button_main()
    text = show_help()
    update.message.reply_text(  text=text,
                                reply_markup=keyboard)


@is_not_bot()
@is_allowed_user()
@lang()
def list_purchase(bot, update):
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
def list_category(bot, update):
    user = update.message.from_user.id
    keyboard = get_button_list_categories(user)
    update.message.reply_text(  text=_('List Сategories'),
                                reply_markup=keyboard)
                                

@is_not_bot()
@is_allowed_user()
@lang()
def list_seller(bot, update):
    user_id = update.message.from_user.id
    keyboard = get_button_list_sellers(user_id)
    update.message.reply_text(  text=_('List Sellers'),
                                reply_markup=keyboard)
                                
@is_not_bot()                                
@is_allowed_user()
@lang()
def menu(bot, update):
    user_id = update.message.from_user.id
    keyboard = get_button_menu(user_id)
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
def list_orders(bot, update):
    user = update.message.from_user.id
    keyboard = get_button_orders(user)
    update.message.reply_text(  text=_('Orders'),
                                reply_markup=keyboard)
    

@is_not_bot()                           
@is_allowed_user()
@lang()
def by_seller(bot, update):
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
def by_category(bot, update):
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
def set_location(bot, update):
    user = update.message.from_user.id
    user_location = update.message.location
    print('LOCATION!')
    print(user_location)
    rows = update.message.reply_to_message.text.split('\n')
    obj_id = int(rows[1].split(':')[1])
    type_obj = rows[2].split(':')[1].replace(' ', '')
    print('TYPE_OBJ: ', type_obj)
    if type_obj != 'seller':
        print('get sellers buttons by geo: ', user_location)
        keyboard = get_button_sellers(user, obj_id, geo=user_location)
        text = show_purchase_item(user, obj_id)
    else:
        keyboard =  get_button_categories(user, obj_id, type_obj)
        result = save_geo_position(type_obj, obj_id, user_location)
        print(result)
        text = show_seller_item(user, obj_id)
    chat_id = update.message.chat.id
    message_id = update.message.message_id
    bot.edit_message_text(
                        chat_id,
                        message_id, 
                        text, 
                        reply_markup=keyboard)
                        #ReplyKeyboardRemove())
    #d
#    bot.send_message(
#                        chat_id=chat_id,
#                        text=text, 
#                        reply_markup=keyboard)

    return ConversationHandler.END
    
    
def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END
    
    
@is_not_bot()    
@is_allowed_user()
@lang()
def new_photo(bot, update):
    date_time = None
    summ = None
    raw = None
    photo_file_id = ''
    user = update.message.from_user.id
    
    nrows = Wait.delete().where(Wait.user == user).execute()
    photo_file_id = update.message.photo[-1].file_id
    foto = bot.getFile(photo_file_id)
    new_file = bot.get_file(foto.file_id)
    new_file.download(os.path.join(PATH_TEMP_FILES,'qrcode.jpg'))
    date_time, summ, raw = scan(image=True, video=False)
    reply_to_new(update, date_time, summ, user, raw, photo_file_id)
#    keyboard = get_button_geo(user, pur.id)
#    update.message.reply_text(  _('what is location?'), 
#                        reply_markup=keyboard)
#    print('return LOCATION: ', LOCATION)
#    command = 'location&%s' % (type, obj_id)
#    w = Wait(user=user, command=command)
#    w.save()
#    return LOCATION
    
    
@is_not_bot()    
@is_allowed_user()
@lang()
def new_text(bot, update):
    date_time = None
    summ = None
    wait_command =None
    photo_file_id = ''
    user = update.message.from_user.id
    
    query = Wait.select().where(Wait.user == user)
    if query.exists():
        wait_command = Wait.get(user=user).command
    if wait_command:
        splitted_wait_command = wait_command.split('&')
        command = splitted_wait_command[0]
        if command == 'new_category':
            text = create_category(  user, 
                                    update.message.text)
        elif command == 'new_seller':
            text = create_seller(  user, 
                                    update.message.text)
        elif command == 'new_seller_purchase':
            purchase_id = splitted_wait_command[1]
            text, seller_id = create_seller(user, 
                                update.message.text,
                                purchase_id=purchase_id
                                )
            #keyboard = get_button_sellers(user, purchase_id)
            
            keyboard = get_button_geo()
            update.message.reply_text(text)
            chat_id = update.message.chat.id
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
    
#@is_not_bot()    
#@is_allowed_user()
#@lang()
#def new_msg(bot, update):
#    wait_command = None
#    date_time = None
#    summ = None
#    raw = None
#    photo_file_id = ''
#    user = update.message.from_user.id
#    keyboard = get_button_main()
#    text = _('summa or datetime not found')
#    if update.message.media_group_id:
#        flag_send = False
#        photo_file_id = update.message.photo[-1].get_file().file_id
#        if not os.path.exists('files/'+update.message.media_group_id+'.txt'):
#            flag_send = True
#        with open('files/'+update.message.media_group_id+'.txt', 'a') as file:
#            file.write(photo_file_id+',')
#        if flag_send:
#            new_caption = update.message.caption.replace('#','')
#            update.message.reply_photo(
#                photo=photo_file_id, 
#                caption="%s # %s" % (new_caption,update.message.media_group_id), 
#                reply_markup=keyboard)
#    elif update.message.video:
#        nrows = Wait.delete().where(Wait.user == user).execute()
#        #print(update.message.video.__dict__)
#        video_file_id = update.message.video.file_id
#        video = bot.getFile(video_file_id)
#        new_file = bot.get_file(video.file_id)
#        new_file.download(os.path.join(PATH_TEMP_FILES,'qrcode.mp4'))
#        bot.send_message(
#                        update.message.chat.id,
#                        text=_('Video uploaded.\nPlease wait. \nRecognize video perhaps take some time.'), 
#                        )
#        date_time, summ, raw = scan(image=False, video=True)
#        
#    elif update.message.photo:
#        nrows = Wait.delete().where(Wait.user == user).execute()
#        photo_file_id = update.message.photo[-1].file_id
#        foto = bot.getFile(photo_file_id)
#        new_file = bot.get_file(foto.file_id)
#        new_file.download(os.path.join(PATH_TEMP_FILES,'qrcode.jpg'))
#        date_time, summ, raw = scan(image=True, video=False)
#    else:
#        query = Wait.select().where(Wait.user == user)
#        if query.exists():
#            wait_command = Wait.get(user=user).command
#        if wait_command:
#            splitted_wait_command = wait_command.split('&')
#            command = splitted_wait_command[0]
#            if command == 'new_category':
#                text = create_category(  user, 
#                                        update.message.text)
#            elif command == 'new_seller':
#                text = create_seller(  user, 
#                                        update.message.text)
#            elif command == 'new_seller_purchase':
#                purchase_id = splitted_wait_command[1]
#                text = create_seller(user, 
#                                    update.message.text,
#                                    purchase_id=purchase_id
#                                    )
#                keyboard = get_button_sellers(user, purchase_id)
#            elif command == 'new_category_purchase':
#                purchase_id = splitted_wait_command[1]
#                text = create_category( user, 
#                                        update.message.text, 
#                                        purchase_id=purchase_id)
#                keyboard = get_button_sellers(user, purchase_id)
#            elif command == 'new_category_seller':
#                seller_id = splitted_wait_command[1]
#                text = create_category( user, 
#                                        update.message.text, 
#                                        seller_id=seller_id)
#                keyboard = get_button_categories(user, seller_id, 'seller')
#            nrows = Wait.delete().where(Wait.user == user).execute()
#            update.message.reply_text(  text, 
#                                reply_markup=keyboard)
#            return True
#        else:
#            date_time, summ = parse_text(update.message.text)
#    if date_time and summ:
#        print('datetime: ', date_time )
#        print('summ: ', summ)
#        check_p = Purchase.select().where(Purchase.summ==summ,
#                                Purchase.datetime==date_time, 
#                                Purchase.user==user)
#        print('check_p: ', check_p)
#        if not check_p:
#            confirm = True
#            pur = Purchase(name='', 
#                        datetime=date_time, 
#                        summ=summ, 
#                        user=user, 
#                        pic=photo_file_id,
#                        confirm=confirm
#                        )
#            pur.save()
#            keyboard = get_button_categories(user, pur.id, 'purchase')
#            text = show_purchase_item(user, pur.id)
#            if raw:
#                text = _('Sorry I not found QR code.\n')
#                text += _('But I tried to recognize the text and found:\n')
#                text += _('Date: ' + date_time + '\n')
#                text += _('Sum: ' + summ + '\n')
#                text += _('Is it true?\n')
#                keyboard = get_button_confirm(pur.id)
#                pur.confirm = False
#                pur.save()
#            print('123123')
#            keyboard = get_button_geo(user, pur.id)
#            update.message.reply_text(  _('what is location?'), 
#                                reply_markup=keyboard)
#            print('return LOCATION: ', LOCATION)
#            return LOCATION
#        else:
#            text = _('ATTANTION!\nIts looks like:\n')
#            text += show_purchase_item(user, check_p[0].id)
#            keyboard = get_button_categories(user, check_p[0].id, 'purchase')
#    else:
#        text = _('Sorry! I not found nothing\n')
#        text += _('You can send me date and summ like this:\n')
#        text += _('12.01.19 123.00')
#    update.message.reply_text(  text, 
#                                reply_markup=keyboard)
#            

@is_not_bot()
@lang()
def button(bot, update):
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
        private_actions(bot, update)
        return True
    
    

@is_not_bot()        
@is_allowed_user()
@lang()
def private_actions(bot, update):
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
    elif but_data == '/menu':
        keyboard = get_button_menu(user)
        text=_('Menu')
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
            if action == 'on_map':
                #TODO make dict for defend menu for object
                title, position = show_on_map(type_obj, obj.id)
                if position:
                    bot.send_venue(chat_id, 
                                latitude=position[1], 
                                longitude=position[0], 
                                title=title, 
                                disable_notification=False, 
                                reply_to_message_id=message_id, 
                                reply_markup=keyboard
                                )
                else:
                    bot.answer_callback_query(
                                callback_query_id, 
                                text=_('this seller have not coordinates'), 
                                show_alert=True
                                )
                return
            if action == 'location':
                keyboard = get_button_geo()
                text_loc =  _('what is location?\nID: %s\n TYPE: %s' % (obj.id, type_obj))
                text = dict_show_item[type_obj](user, obj.id)
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id, 
                    text=text
                    )
                bot.send_message(
                    chat_id=chat_id,
                    text=text_loc, 
                    reply_markup=keyboard
                    )
                return   
            elif action == 'new_category':
                text = show_new_category(user, type=type_obj, obj_id=id_obj)
            elif action == 'new_seller':
                text = show_new_seller(user, purchase_id=id_obj)
            elif action == 'show':
                if type_obj == 'purchase':
                    keyboard = buttons_for_seller_item(user, id_obj, type_obj)
                    text = show_purchase_item(user, id_obj)
                elif type_obj == 'category':
                    keyboard =  get_button_del_item(id_obj, type_obj)
                    text = show_category_item(user, id_obj)
                elif type_obj == 'seller':
                    #keyboard =  get_button_del_item(id_obj, type_obj)
                    keyboard = buttons_for_seller_item(user, id_obj, type_obj)
                    text = show_seller_item(user, id_obj)
                elif type_obj == 'user':
                    text = show_user_item(user, id_obj)
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
            elif action == 'delitem':
                if type_obj == 'user':
                    send_delete_info_to_user(bot, id_obj)
                text = delete_item(user, type_obj, id_obj)
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
        
        if action == 'change_seller':
            keyboard = get_button_sellers(user, obj.id)
#            Category = Category.get(Category.id==id_link_obj, 
#                                    Category.user==user)
            seller = Seller.get(Seller.id==id_link_obj, 
                                Seller.user==user)
            obj.seller = seller
            obj.save()
            text = show_purchase_item(user, obj.id)
            #text='seller saved! %s %s %s' % (text,  purchase.datetime,  purchase.summ)
        elif action == 'change_category':
            
            category = Category.get(Category.id==id_link_obj, 
                                    Category.user==user)
            obj.category = category
            print('Category: ', category)
            obj.save()
            if type_obj != 'seller':
                #keyboard = get_button_sellers(user, obj.id)
                #print(keyboard)
                keyboard = get_button_geo()
                text_loc =  _('what is location?\nID: %s\n TYPE: %s' % (obj.id, type_obj))
                text = dict_show_item[type_obj](user, obj.id)
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id, 
                    text=text
                    )
                bot.send_message(
                    chat_id=chat_id,
                    text=text_loc, 
                    reply_markup=keyboard
                    )
                
                return
            else:
                keyboard = get_button_categories(user, id_obj, type_obj)
                
            text += dict_show_item[type_obj](user, obj.id)
        
        elif action == 'confirm':
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
