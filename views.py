from peewee import *

from models.seller import Seller
from models.purchase import Purchase
from models.category import Category
from models.wait import Wait
from keyboards import *


def show_order_by(user, type):
    text = ''
    if type == 'seller':
        sellers = Seller.select().where(Seller.user==user)
        print('sellers: ', sellers)
        for s in sellers:
            summ = purchase.Purchase.select(fn.SUM(Purchase.summ)).where(Purchase.seller == s).scalar()
            text += 'Seller: %s, Summa: %s\n' % (s.name,  summ)
    else:
        categories = Category.select().where(Category.user==user)
        print('categories: ', categories)
        for c in categories:
            summ = Purchase.select(fn.SUM(Purchase.summ)).where(Purchase.category == c).scalar()
            text += 'Category: %s, Summa: %s\n' % (c.name, summ)
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
    text = 'ID: %s\nDate Time: %s\nSumma: %s\nSeller: %s\nCategory: %s\nUser: %s' % ( 
            purchase.id, 
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
    text = 'ID: %s\nCategory: %s' % ( 
            category.id, 
            category.name
                            )
    return text


def show_seller_item(user, id):
    seller = Seller.get(Seller.id==id, 
                        Seller.user==user)
    text = 'ID: %s\nSeller: %s' % ( 
            seller.id, 
            seller.name
                            )
    return text
    
                  
def delete_item(user, typeitem, iditem):
    text = '%s with ID = %s' % (typeitem, iditem)
    if typeitem == 'category':
        for p in Purchase.select().where(Purchase.category == iditem, 
                                         Purchase.user == user):
            p.category = None
            p.save()
        nrows = Category.delete().where(Category.id == iditem, 
                                        Purchase.user == user).execute()
        
    elif typeitem == 'seller':
        nrows = Seller.delete().where(Seller.id == iditem, 
                                        Purchase.user == user).execute()
        for p in Purchase.select().where(Purchase.seller == iditem, 
                                            Purchase.user == user):
            p.seller = None
            p.save()
    elif typeitem == 'purchase':
        nrows = Purchase.delete().where(Purchase.id == iditem, 
                                        Purchase.user == user).execute()
    text += ' deleted'
    return text
        
        
def show_new_category(user, args=None):
    
    if not args or args[0] == '':
        w = Wait(user=user, command='new_category')
        w.save()
        text = 'Please! send me name of category'
    else:
        text = ''
        cat = Category(name=args[0], user=user)
        try:
            cat.save()
            text = 'category saved!'
        except:
            text = 'error!'
    return text
    

def show_new_seller(user, args=None):
    
    if not args or args[0] == '':
        w = Wait(user=user, command='new_seller')
        w.save()
        text = 'Please! send me name of seller'
    else:
        text = ''
        sel = Seller(name=args[0], user=user)
        try:
            sel.save()
            text = 'seller saved!'
        except:
            text = 'error!'
    return text
        
        
def show_help():
    text = '/menu - main menu\n'
    text += '/new_category NAME - for adding new category\n'
    text += '/new_seller NAME - for adding new seller\n'
    text += '/purchases - list of purchases\n'
    text += '/sellers - list of sellers\n'
    text += '/categories - list of categories\n'
    text += '/orders - list of orders\n'
    text += '/by_category - order by category\n'
    text += '/by_seller - order by seller\n'
    text += '/help - show this help\n'
    return text
    
    
def create_category(user, name):
    
    new_category = Category(name=name, user=user)
    new_category.save()
    text='Seller created!'
    return text
    
    
def create_seller(user, name):
    
    new_seller = Seller(name=name, user=user)
    new_seller.save()
    text='Seller created!'
    return text
