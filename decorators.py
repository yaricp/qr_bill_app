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
                if obj.from_user.first_name in allowed_users:
                    f(*args)
                else:
                    if args[1].callback_query:
                        args[1].callback_query.answer('Sorry! it is private bot...')
                    else:
                        obj.reply_text('Sorry! it is private bot...')
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
    
