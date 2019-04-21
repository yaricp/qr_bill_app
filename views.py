
from db_models import *
from keyboards import *

                    

def show_order_by(type):
    text = ''
    if type == 'seller':
        sellers = Seller.select()
        for s in sellers:
            summ = Purchase.select(fn.SUM(Purchase.summ)).where(Purchase.seller == s).scalar()
            text += 'Seller: %s, Summa: %s\n' % (s.name,  summ)
    else:
        categories = Category.select()
        for c in categories:
            summ = Purchase.select(fn.SUM(Purchase.summ)).where(Purchase.category == c).scalar()
            text += 'Categories: %s, Summa: %s\n' % (c.name, summ)
    return text
                    
                                       
def show_purchase_item(id):
    purchase = Purchase.get(Purchase.id==id)
    category_name = ''
    seller_name = ''
    if purchase.category:
        category_name = purchase.category.name
    if purchase.seller:
        seller_name = purchase.seller.name
    text = 'ID: %s\nDate Time: %s\nSumma: %s\nSeller: %s\nCategory: %s' % ( 
            purchase.id, 
            purchase.datetime, 
            purchase.summ, 
            seller_name, 
            category_name
                            )
    return text


def show_category_item(id):
    category = Category.get(Category.id==id)
    text = 'ID: %s\nCategory: %s' % ( 
            category.id, 
            category.name
                            )
    return text


def show_seller_item(id):
    seller = Seller.get(Seller.id==id)
    text = 'ID: %s\nSeller: %s' % ( 
            seller.id, 
            seller.name
                            )
    return text
    
                  
def delete_item(typeitem, iditem):
    text = '%s with ID = %s' % (typeitem, iditem)
    if typeitem == 'category':
        nrows = Category.delete().where(Category.id == iditem).execute()
    elif typeitem == 'seller':
        nrows = Seller.delete().where(Seller.id == iditem).execute()
    elif typeitem == 'purchase':
        nrows = Purchase.delete().where(Purchase.id == iditem).execute()
    print('nrows: ',  nrows)
    text += ' deleted'
    return text
        
        
def show_new_category(args=None):
    print('ARGS: ', args)
    if not args or args[0] == '':
        status = Status.get(name='wait_category_name')
        if status:
            if not status.value:
                status.value = True
        else:
            status = Status(name='wait_category_name', 
                            value=True)
        status.save()
        text = 'Please! send me name of category'
    else:
        text = ''
        cat = Category(name=args[0])
        try:
            cat.save()
            text = 'category saved!'
        except:
            text = 'error!'
    return text
    

def show_new_seller(args=None):
    print('ARGS: ', args)
    if not args or args[0] == '':
        status = Status.get(name='wait_seller_name')
        if status:
            if not status.value:
                status.value = True
        else:
            status = Status(name='wait_seller_name', 
                            value=True)
        status.save()
        text = 'Please! send me name of seller'
    else:
        text = ''
        seller = Seller(name=args[0])
        try:
            seller.save()
            text = 'Seller saved!'
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
    
    
