
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
    text = ''
    if typeitem == 'category':
        cat = Category.get(id=iditem).delete().execute()
        text += 'category %s' % cat.name
    elif typeitem == 'seller':
        seller = Seller.get(id=iditem).delete().execute()
        text += 'seller %s' % seller.name
    text += 'deleted'
    return text
        
        
def new_category(bot, update):
    if update.callback_query and update.callback_query.data == '/new_category':
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
        cat = Category(name=update.message.text.replace('/new_category ', ''))
        try:
            cat.save()
            text = 'category saved!'
        except:
            text = 'error!'
    return text
    

def new_seller(bot, update):
    if update.callback_query and update.callback_query.data == '/new_seller':
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
        seller = Seller(name=update.message.text.replace('/new_seller ', ''))
        try:
            seller.save()
            text = 'Ok!'
        except:
            text = 'error!'
    return text 
        
