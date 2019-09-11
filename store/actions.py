from config import *

from models.wait import Wait
from models.purchase import Purchase


def save_purchase(date_time, summ, user, raw=None, photo_file_id=''):
    text = _('summa or datetime not found')
    raw = None
    if date_time and summ:
        print('datetime: ', date_time )
        print('summ: ', summ)
        check_p = Purchase.select().where(Purchase.summ==summ,
                                Purchase.datetime==date_time, 
                                Purchase.user==user)
        print('check_p: ', check_p)
        if not check_p:
            pur = Purchase(name='', 
                        datetime=date_time, 
                        summ=summ, 
                        user=user, 
                        pic=photo_file_id,
                        )
            pur.save()
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
    else:
        text = _('Sorry! I not found nothing\n')
        text += _('You can send me date and summ like this:\n')
        text += _('12.01.19 123.00')
        
    return text
    
    
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
        
