import gettext
from peewee import *

from models.seller import Seller
from models.purchase import Purchase
from models.category import Category
from models.wait import Wait
from models.language import Language
from keyboards import *


def show_order_by(user, type):
    text = ''
    if type == 'seller':
        sellers = Seller.select().where(Seller.user==user)
        #print('sellers: ', sellers)
        for s in sellers:
            summ = Purchase.select(fn.SUM(Purchase.summ)).where(Purchase.seller == s).scalar()
            text += _('Seller: %s, Summa: %s\n') % (s.name,  summ)
    else:
        categories = Category.select().where(Category.user==user)
        #print('categories: ', categories)
        for c in categories:
            summ = Purchase.select(fn.SUM(Purchase.summ)).where(Purchase.category == c).scalar()
            text += _('Category: %s, Summa: %s\n') % (c.name, summ)
    return text
                    
                                       
def show_purchase_item(user, id):
    purchase = Purchase.get(Purchase.id==id, 
                            Purchase.user==user)
    category_name = ''
    seller_name = ''
    if purchase.category:
        category_name = purchase.category.name
    if purchase.seller:
        seller_name = purchase.seller.name
    text = _('Date Time: %s\nSumma: %s\nSeller: %s\nCategory: %s\nUser: %s') % ( 
            purchase.datetime, 
            purchase.summ, 
            seller_name, 
            category_name, 
            purchase.user
                            )
    return text


def show_category_item(user, id):
    category = Category.get(Category.id==id, 
                            Category.user==user)
    text = _('Category: %s') % category.name
    return text


def show_seller_item(user, id):
    category_name = ''
    seller = Seller.get(Seller.id==id, 
                        Seller.user==user)
    if seller.category:
        category_name = seller.category.name
    text = _('Seller: %s\nCategory: %s') % (seller.name, category_name)
    return text
    
                  
def delete_item(user, typeitem, iditem):
    
    if typeitem == 'category':
        for p in Purchase.select().where(Purchase.category == iditem, 
                                         Purchase.user == user):
            p.category = None
            p.save()
        item_name = Category.get(id=iditem).name
        text = _('category %s deleted') %  item_name
        nrows = Category.delete().where(Category.id == iditem, 
                                        Category.user == user).execute()
        
    elif typeitem == 'seller':
        item_name = Seller.get(id=iditem).name
        text = _('seller %s deleted') %  item_name
        nrows = Seller.delete().where(Seller.id == iditem, 
                                      Seller.user == user).execute()
        for p in Purchase.select().where(Purchase.seller == iditem, 
                                         Purchase.user == user):
            p.seller = None
            p.save()
    elif typeitem == 'purchase':
        item_name = '%s %s' % (Purchase.get(id=iditem).datetime, 
                                Purchase.get(id=iditem).summ)
        text = _('purchase %s deleted') %  item_name
        nrows = Purchase.delete().where(Purchase.id == iditem, 
                                        Purchase.user == user).execute()
    return text
        
        
def show_new_category(user, args=None):
    
    if not args or args[0] == '':
        w = Wait(user=user, command='new_category')
        w.save()
        text = _('Please! send me name of category')
    else:
        text = ''
        cat = Category(name=args[0], user=user)
        try:
            cat.save()
            text = _('category saved!')
        except:
            text = _('error!')
    return text
    

def show_new_seller(user, category=None, args=None):
    
    if not args or args[0] == '':
        w = Wait(user=user, command='new_seller&%s' % category)
        w.save()
        text = _('Please! send me name of seller')
    else:
        text = ''
        sel = Seller(name=args[0], user=user)
        try:
            sel.save()
            text = _('seller saved!')
        except:
            text = _('error!')
    return text
        
        
def show_help():
    text = '/menu - ' + _('main menu') + '\n'
    text += '/new_category NAME - ' + _('for adding new category') + '\n'
    text += '/new_seller NAME - ' + _('for adding new seller') + '\n'
    text += '/purchases - ' + _('list of purchases') + '\n'
    text += '/sellers - ' + _('list of sellers') + '\n'
    text += '/categories - ' + _('list of categories') + '\n'
    text += '/orders - ' + _('list of orders') + '\n'
    text += '/by_category - ' + _('order by category') + '\n'
    text += '/by_seller - ' + _('order by seller') + '\n'
    text += '/langs - ' + _('list languages') + '\n'
    text += '/lang NAME - ' + _('set language to NAME') + '\n'
    text += _('Now available this languages:') + '\n'
    for lang in LANGUAGES:
        text += lang + '\n'
    text += '/help - ' + _('show this help') + '\n'
    return text
    
    
def create_category(user, name, args=None):
    
    new_category = Category(name=name, user=user)
    new_category.save()
    text=_('Category created!')
    return text
    
    
def create_seller(user, name, args=None):
    
    new_seller = Seller(name=name, user=user)
    if args:
        category = Category.get(Category.id==args)
        new_seller.category = category
    new_seller.save()
    text=_('Seller created!')
    return text


def show_change_lang(user, lang):
    
    user_lang, created = Language.get_or_create(user=user)
    user_lang.lang = lang
    user_lang.save()
    lang_user = gettext.translation('messages', 
                                    localedir='lang', 
                                    languages=[lang])
    lang_user.install()
    text = _('Language changed to ') + lang
    return text
    
    
    
    
