from config import *

from models.seller import Seller
from models.purchase import Purchase
from models.category import Category
from models.wait import Wait
from models.language import Language
from models.user import User


dict_types = {
        'purchase': Purchase, 
        'seller': Seller, 
        'category': Category, 
        'user': User
    }


def save_purchase(date_time, summ, user, raw=None, photo_file_id=''):
    text = _('summa or datetime not found')
    raw = None
    double = False
    if date_time and summ:
        check_p = Purchase.select().where(Purchase.summ==summ,
                                Purchase.datetime==date_time, 
                                Purchase.user==user)
        if not check_p:
            pur = Purchase(name='', 
                        datetime=date_time, 
                        summ=summ, 
                        user=user, 
                        pic=photo_file_id,
                        )
            pur.save()
            obj_id = pur.id
            text = get_purchase_item(user, pur.id)
            if raw:
                text = _('Sorry I not found QR code.\n')
                text += _('But I tried to recognize the text and found:\n')
                text += _('Date: ' + date_time + '\n')
                text += _('Sum: ' + summ + '\n')
                text += _('Is it true?\n')
        else:
            text = _('ATTANTION!\nIts looks like:\n')
            text += get_purchase_item(user, check_p[0].id)
            obj_id = check_p[0].id
            double = True
    else:
        text = _('Sorry! I not found nothing\n')
        text += _('You can send me date and summ like this:\n')
        text += _('12.01.19 123.00')
        
    return text, obj_id, double
    
    
def get_purchase_item(user, id):
    purchase = Purchase.get(Purchase.id==id, 
                            Purchase.user==user)
    category_name = ''
    seller_name = ''
    if purchase.category:
        category_name = purchase.category.name
    if purchase.seller:
        seller_name = purchase.seller.name
    text = _('ID: %(id)s\nDate Time: %(datetime)s\nSumma: %(summ)s\nSeller: %(seller)s\nCategory: %(cat)s\nUser: %(user)s') % ( 
            {'id':purchase.id, 
            'datetime':purchase.datetime, 
            'summ':purchase.summ, 
            'seller':seller_name, 
            'cat':category_name, 
            'user':purchase.user}
                            )
    return text
        

def change_category(obj, user, category_id):
    
    category = Category.get(Category.id==category_id, 
                                Category.user==user)
    obj.category = category
    obj.save()
    
    
def change_seller(obj, user,  seller_id):
    
    seller = Seller.get(Seller.id==seller_id, 
                            Seller.user==user)
    obj.seller = seller
    obj.save()
    
    
def get_item(user, type_obj, id_obj):
    
    obj = dict_types[type_obj].get( dict_types[type_obj].id==id_obj, 
                                    dict_types[type_obj].user==user )
    return obj
