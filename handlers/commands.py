from decorators import *
from utils import *
from keyboards import *

from store.models.user import User
#from models.purchase import Purchase


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
                                
                                
                                
