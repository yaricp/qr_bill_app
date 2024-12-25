from telegram import ParseMode

from decorators import *
from utils import *
from keyboards import *
from views import *
from store.actions import *



from store.models.user import User


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
    return False


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
    keyboard = get_button_list_items(user, 'purchase')
    update.message.reply_text(  text=_('List Purchases'),
                                reply_markup=keyboard)


@is_not_bot()
@is_allowed_user()
@lang()
def purchase(bot, update, args):
    user = update.message.from_user.id
    if len(args) < 1:
        update.message.reply_text(  text=_('Needs to send id of purchase.\n /purchase ID'),
                                reply_markup=keyboard)
        return
    id = args[0]
    obj = get_item(user, 'purchase', id)
    keyboard = buttons_for_purchase_item(user, id, media=False, has_media=obj.pic)
    text = show_purchase_item(user, id_obj)
    update.message.reply_text(  text=text,
                                reply_markup=keyboard)
                                
                                
@is_not_bot()                                
@is_allowed_user()
@lang()
def list_category(update, context):
    user = update.message.from_user.id
    keyboard = get_button_list_items(user, 'category')
    update.message.reply_text(  text=_('List Сategories'),
                                reply_markup=keyboard)


@is_not_bot()
@is_allowed_user()
@lang()
def list_seller(update, context):
    user = update.message.from_user.id
    keyboard = get_button_list_items(user, 'seller')
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
        context.bot.delete_message(
                        chat_id=chat_id, 
                        message_id=message_id, 
                        )
        context.bot.send_message(
                        chat_id=chat_id, 
                        message_id=message_id, 
                        text=_('Menu'), 
                        reply_markup=keyboard
                        )
    else:
        update.message.reply_text(  text=_('Menu'),
                                reply_markup=keyboard)
                                
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
