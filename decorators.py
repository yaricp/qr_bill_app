import gettext
from models.language import Language
from models.user import User

from config import *

def is_allowed_user():
    def wrap(f):
        def wrapped_f(*args, **kwargs):
            obj = None
            if args[0].message:
                obj = args[0].message
            elif args[0].callback_query:
                obj = args[0].callback_query
            if obj:
                user_id = obj.from_user.id
                user = User.get_or_none(User.tg_user_id==user_id)
                if user and user.is_active:
                    return f(*args, **kwargs)
                else:
                    if args[0].callback_query:
                        args[0].callback_query.answer('Sorry! you need to register. Use /start for this.')
                    else:
                        obj.reply_text('Sorry! you need to register. Use /start for this.')
        return wrapped_f
    return wrap
    
    
def is_admin():
    def wrap(f):
        def wrapped_f(*args, **kwargs):
            obj = None
            if args[0].message:
                obj = args[0].message
            elif args[0].callback_query:
                obj = args[0].callback_query
            if obj:
                if obj.from_user.first_name in admins:
                    f(*args, **kwargs)
                else:
                    if args[0].callback_query:
                        args[0].callback_query.answer('Sorry! you are not admin...')
                    else:
                        obj.reply_text('Sorry! you are not admin...')
        return wrapped_f
    return wrap
    

def is_not_bot():
    def wrap(f):
        def wrapped_f(*args, **kwargs):
            obj = None
            #print('args[1]: ', args[1].__dict__)
            #print('args[0]: ', args[0].__dict__)
            if args[0].message:
                obj = args[0].message
            elif args[0].callback_query:
                obj = args[0].callback_query
            if obj:
                if not obj.from_user.is_bot:
                    return f(*args, **kwargs)
        return wrapped_f
    return wrap
    

def lang():
    def wrap(f):
        def wrapped_f(*args, **kwargs):
            obj = None
            if args[0].message:
                obj = args[0].message
            elif args[0].callback_query:
                obj = args[0].callback_query
            if obj:
                user = obj.from_user.id
                lang = obj.from_user.language_code
                user_lang, created = Language.get_or_create(user=user)
                if user_lang.lang:
                    lang = user_lang.lang
                lang_user = gettext.translation('messages', 
                                                localedir='lang', 
                                                languages=[lang])
                lang_user.install()
                return f(*args, **kwargs)
        return wrapped_f
    return wrap
    
