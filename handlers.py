# -*- coding: utf-8 -*-

from config import *
from models.wait import Wait
from views import *
from recognize import *
from decorators import *


CUR_DIR = os.path.dirname(os.path.realpath(__file__))

run_waiting_command = {
        'new_category': create_category, 
        'new_seller': create_seller
    }

dict_types = {
        'purchase': Purchase, 
        'seller': Seller, 
        'category':Category
    }
    
dict_show_item = {
        'purchase': show_purchase_item, 
        'seller': show_seller_item, 
        'category': show_category_item
    }

@is_not_bot()
@lang()
def start(bot, update):
    user = update.message.from_user
    keyboard = get_button_main()
    if user.first_name in admins:
        text = _('Yes! And You are admins this bot!')
        update.message.reply_text(  text=text,
                                reply_markup=keyboard)
    elif user.first_name in allowed_users:
        text = _('Hello!') + ' \n'
        text += show_help()
        update.message.reply_text(  text=text,
                                reply_markup=keyboard)
    else:
        username = user.first_name
        user_id = user.id
        text = _('user %s with %s\n Wanted to use your bot.') % (username, user_id)
        for k, v in admins.items():
            bot.send_message(
                        v, 
                        text=text, 
                        reply_markup=keyboard
                        )
        text = _('Ок! we send request to admin of this bot\n After confirm you will take a message')
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
def list_category(bot, update):
    user = update.message.from_user.id
    keyboard = get_button_list_categories(user)
    update.message.reply_text(  text=_('List Сategories'),
                                reply_markup=keyboard)
                                

@is_not_bot()
@is_allowed_user()
@lang()
def list_seller(bot, update):
    user = update.message.from_user.id
    keyboard = get_button_list_sellers(user)
    update.message.reply_text(  text=_('List Sellers'),
                                reply_markup=keyboard)
                                
@is_not_bot()                                
@is_allowed_user()
@lang()
def menu(bot, update):
    keyboard = get_button_menu()
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
    keyboard = get_button_main()
    text = show_order_by(user, 'seller')
    update.message.reply_text(  text=text,
                                reply_markup=keyboard)
    

@is_not_bot()
@is_allowed_user()
@lang()
def by_category(bot, update):
    user = update.message.from_user.id
    keyboard = get_button_main()
    text = show_order_by(user, 'category')
    update.message.reply_text(  text=text,
                                reply_markup=keyboard)
    

@is_not_bot()    
@is_allowed_user()
@lang()
def new_msg(bot, update):
    wait_command = None
    date_time = None
    summ = None
    photo_file_id = ''
    user = update.message.from_user.id
    keyboard = get_button_main()
    text = _('summa or datetime not found')
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
    elif update.message.video:
        nrows = Wait.delete().where(Wait.user == user).execute()
        video_file_id = update.message.video[-1].file_id
        video = bot.getFile(video_file_id)
        new_file = bot.get_file(video.file_id)
        new_file.download(os.path.join(PATH_TEMP_FILES,'qrcode.mp4'))
        date_time, summ = scan(video=True)
    elif update.message.photo:
        nrows = Wait.delete().where(Wait.user == user).execute()
        photo_file_id = update.message.photo[-1].file_id
        foto = bot.getFile(photo_file_id)
        new_file = bot.get_file(foto.file_id)
        new_file.download(os.path.join(PATH_TEMP_FILES,'qrcode.jpg'))
        date_time, summ = scan(image=True)
    else:
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
                text = create_seller(user, 
                                    update.message.text,
                                    purchase_id=purchase_id
                                    )
                keyboard = get_button_sellers(user, purchase_id)
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
        else:
            date_time, summ = parse_text(update.message.text)
    if date_time and summ:
        check_p = Purchase.select().where(Purchase.summ==summ,
                                Purchase.datetime==date_time, 
                                Purchase.user==user)
        if not check_p:
            pur = Purchase(name='', 
                        datetime=date_time, 
                        summ=summ, 
                        user=user, 
                        pic=photo_file_id
                        )
            pur.save()
            text = show_purchase_item(user, pur.id)
            keyboard = get_button_categories(user, pur.id, 'purchase')
        else:
            text = _('ATTANTION!\nIts looks like:\n')
            text += show_purchase_item(user, check_p[0].id)
            keyboard = get_button_categories(user, check_p[0].id, 'purchase')
    update.message.reply_text(  text, 
                                reply_markup=keyboard)
            

@is_not_bot()        
@is_allowed_user()
@lang()
def button(bot, update):
    but_data = update.callback_query.data
    user = update.callback_query.from_user.id
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
        text = show_order_by(user,'seller')
    elif but_data == '/by_category':
        text = show_order_by(user,'category')
    elif but_data == '/menu':
        keyboard = get_button_menu()
        text=_('Menu')
    elif but_data == '/help':
        text = show_help()
    elif but_data == '/langs':
        keyboard = get_button_lang()
        text=_('Change language')
    elif but_data == '/categories':
        keyboard = get_button_list_categories(user)
        text = _('List categories')
    elif but_data == '/sellers':
        keyboard = get_button_list_sellers(user)
        text = _('List sellers')
    list_parameters = but_data.split('&')
    
    if len(list_parameters) > 2:
        action = list_parameters[0]
        type_obj = list_parameters[1]
        id_obj = list_parameters[2]
        if action == 'new_category':
            text = show_new_category(user, type=type_obj, obj_id=id_obj)
        elif action == 'new_seller':
            text = show_new_seller(user, purchase_id=id_obj) 
        elif action == 'show':
            if type_obj == 'purchase':
                keyboard = get_button_categories(user, id_obj, type_obj)
                text = show_purchase_item(user, id_obj)
            elif type_obj == 'lang':
                text = show_change_lang(user, id_obj)
                keyboard = get_button_main()
            elif type_obj == 'category':
                keyboard =  get_button_del_item(id_obj, type_obj)
                text = show_category_item(user, id_obj)
            elif type_obj == 'seller':
                #keyboard =  get_button_del_item(id_obj, type_obj)
                keyboard = get_button_categories(user, id_obj, type_obj)
                text = show_seller_item(user, id_obj)
        if action == 'delitem':
            text = delete_item(user, type_obj, id_obj)
    if len(list_parameters) > 3:
        id_link_obj = list_parameters[3]
        obj = dict_types[type_obj].get(dict_types[type_obj].id==id_obj, 
                                        dict_types[type_obj].user==user )
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
            obj.save()
            if type_obj != 'seller':
                keyboard = get_button_sellers(user, obj.id)
            else:
                keyboard = get_button_categories(user, id_obj, type_obj)
            text = dict_show_item[type_obj](user, obj.id)
        elif action == 'show_picture':
            text = show_purchase_item(user, id_obj)
            bot.send_photo(
                update.callback_query.message.chat.id, 
                photo=obj.pic, 
                caption=text, 
                reply_markup=keyboard)
            return true
    bot.send_message(update.callback_query.message.chat.id,             
                    text=text, 
                    reply_markup=keyboard)
    

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
