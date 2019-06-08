import gettext
from models.language import Language

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
                user_id = obj.from_user.id
                user = User.get(User.tg_user_id==user_id)
                if user.is_active:
                    f(*args)
                else:
                    if args[1].callback_query:
                        args[1].callback_query.answer(_('Sorry! it is private bot...'))
                    else:
                        obj.reply_text(_('Sorry! it is private bot...'))
        return wrapped_f
    return wrap
    
    
def is_admin():
    def wrap(f):
        def wrapped_f(*args):
            obj = None
            if args[1].message:
                obj = args[1].message
            elif args[1].callback_query:
                obj = args[1].callback_query
            if obj:
                if obj.from_user.first_name in admins:
                    f(*args)
                else:
                    if args[1].callback_query:
                        args[1].callback_query.answer('Sorry! you are not admin...')
                    else:
                        obj.reply_text('Sorry! you are not admin...')
        return wrapped_f
    return wrap
    

def is_not_bot():
    def wrap(f):
        def wrapped_f(*args):
            obj = None
            if args[1].message:
                obj = args[1].message
            elif args[1].callback_query:
                obj = args[1].callback_query
            if obj:
                if not obj.from_user.is_bot:
                    f(*args)
        return wrapped_f
    return wrap
    

def lang():
    def wrap(f):
        def wrapped_f(*args):
            obj = None
            if args[1].message:
                obj = args[1].message
            elif args[1].callback_query:
                obj = args[1].callback_query
            if obj:
                user = obj.from_user.id
                user_lang, created = Language.get_or_create(user=user)
                lang = user_lang.lang
                lang_user = gettext.translation('messages', 
                                                localedir='lang', 
                                                languages=[lang])
                lang_user.install()
                f(*args)
        return wrapped_f
    return wrap
    
