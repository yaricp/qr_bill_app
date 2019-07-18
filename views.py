import gettext, datetime, sys
from peewee import *

from models.seller import Seller
from models.purchase import Purchase
from models.category import Category
from models.wait import Wait
from models.language import Language
from keyboards import *

dict_types = {
        'purchase': Purchase, 
        'seller': Seller, 
        'category':Category
    }

def show_order_by(user, type):
    dict_months = {1: ('January'), 
                    2: ('Februrary'), 
                    3: ('March'), 
                    4: ('April'), 
                    5: ('May'), 
                    6: ('June'), 
                    7: ('July'), 
                    8: ('August'), 
                    9: ('September'), 
                    10: ('Oktober'), 
                    11: ('November'), 
                    12: ('December')
                    }
    #now_month = datetime.datetime.now().month()
    text = ''
    if type == 'seller':
        sellers = Seller.select().where(Seller.user==user)
        #print('sellers: ', sellers)
        for s in sellers:
            summ = Purchase.select(fn.SUM(Purchase.summ)).where(Purchase.seller == s).scalar()
            text += _('Seller: %(seller)s, Summa: %(summ)s\n') % ({'seller':s.name, 'summ':summ})
    else:
        
#        for i in Purchase.select().where(Purchase.user==user):
#            print('Item: ', i)
#            print('User: ', i.user)
#            print('Summ: ', i.summ)
#            print('Cat: ', i.category)
#            print('date: ', i.datetime)
#            print('')
        query = (Purchase
            .select(
                Category.name, 
                fn.Sum(Purchase.summ).alias('average_value'), 
                fn.strftime('%m', Purchase.datetime)
                )
            .join(Category)
            .where(Purchase.user==user)
            .group_by(Purchase.category)
            .group_by(fn.strftime('%m', Purchase.datetime))
            .tuples())
        print('query : ', query)
        for r in query:
            print('R: ', r)
#        )
#
##        for c in categories:
##            query = (Purchase.select(fn.SUM(Purchase.summ))
##                .where(Purchase.category == c)
##                .where(fn.date_part('year', Purchase.datetime) == 2019)
##                #.group_by(Purchase.datetime, month)
##                #.order_by(Purchase.datetime, month)
##                )
#        summ = query.scalar()
#        print('summ: ',summ)
##            #print('nslots :', nslots)
##            text += _('Category: %(cat)s, Summa: %(summ)s\n') % ({'cat':c.name, 'summ':summ})
#        
#        print('summ :', summ)
        categories = Category.select().where(Category.user==user)
#        text += _('Total:')+ '\n'
#        for m in (now_month-2, now_month-1, now_month):
#            text += dict_months[m] + ' '
#        text += '/n'
        for c in categories:
            summ = (Purchase
                .select(fn.strftime('%m', Purchase.datetime), fn.SUM(Purchase.summ))
                .where(Purchase.category==c, Purchase.user==user)
                .group_by(fn.strftime('%m', Purchase.datetime))
                .tuples()
                )
            
            text += ('Category: %s: ') % c.name
            print(summ)
            for s in summ:
                print(s)
                text+= str(s[0]) + '  '
            text+= '\n'
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
    text = _('Date Time: %(datetime)s\nSumma: %(summ)s\nSeller: %(seller)s\nCategory: %(cat)s\nUser: %(user)s') % ( 
            {'datetime':purchase.datetime, 
            'summ':purchase.summ, 
            'seller':seller_name, 
            'cat':category_name, 
            'user':purchase.user}
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
    text = _('Seller: %(seller)s\nCategory: %(cat)s') % ({'seller':seller.name, 'cat':category_name})
    return text
    
     
dict_show_item = {
        'purchase': show_purchase_item, 
        'seller': show_seller_item, 
        'category': show_category_item
    }
     
def delete_item(user, typeitem, iditem):
    
    if typeitem == 'user':
        item_name = User.get(id=iditem).username
        text = _('user %(item)s deleted') %  {'item':item_name}
        nrows = User.delete().where(User.id == iditem).execute()
    if typeitem == 'category':
        for p in Purchase.select().where(Purchase.category == iditem, 
                                         Purchase.user == user):
            p.category = None
            p.save()
        item_name = Category.get(id=iditem).name
        text = _('category %(item)s deleted') %  {'item':item_name}
        nrows = Category.delete().where(Category.id == iditem, 
                                        Category.user == user).execute()
        
    elif typeitem == 'seller':
        item_name = Seller.get(id=iditem).name
        text = _('seller %(item)s deleted') %  {'item':item_name}
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
        
        
def show_new_category(user, type=None, obj_id=None):
    command = 'new_category'
    if type and obj_id:
        command = 'new_category_%s&%s' % (type, obj_id)
    w = Wait(user=user, command=command)
    w.save()
    text = _('Please! send me name of category')
    
    return text
    

def show_new_seller(user, purchase_id=None):
    command = 'new_seller'
    if purchase_id:
        command = 'new_seller_purchase&%s' % purchase_id
    w = Wait(user=user, command=command)
    w.save()
    text = _('Please! send me name of seller')
    
    return text
        
        
def show_help():
    text = _('Help.\n')
    text += '/menu - ' + _('main menu') + '\n'
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
    text += ' /about - ' + _('About this bot') + '\n'
    text += ' /donate - ' + _('Donate') + '\n'
    return text
    

def show_about():
    text = _('About.\n')
    text += _('This bot help you to keep and analize your purchases.\n')
    text += _('You can send to bot photo of bill with QR code and bot try to decode QR code and save this purchase in database.\n')
    text += _('You can send also video with QR code.\n')
    text += _('If bot can`t to recognize QR code you can use any application for decode QR code and then send to bot result.\n')
    text += _('For each purchase bot save link to photo of bill and you can check it anytime.\n')
    text += _('You can create categories and sellers (name of seller) for each purchase.\n')
    text += _('And then bot can show you reports by sellres and by categories.\n')
    text += _('If you twice send photo with QR code bot notice about it.\n')
    text += _('We have more plans to make this bot better. For example:\n')
    text += _(' - make send reports to email each week, month or other period.\n')
    text += _(' - make connection to third party database what user want (for example for more strong safety of finance data).\n')
    text += _(' - save geoposition of purchase (it maybe good for travellers).\n')
    text += _('But notice we work by /donate.\n')
    text += _('And how long we will release new features depend of free time and how much donated we will have.\n')
    text += _('Now we use simple database on weak server because it cheap.\n')
    text += _('Note! This is not commercial service and it can`t guarantee safety your data.\n')
    text += _('View on this service as a test of the future commercial solution.\n')
    text += _('Discuss in chat of channel:https://t.me/qrscanner_order_bot .\n')
    return text
    
    
def create_category(user, name, purchase_id=None, seller_id=None):
    
    new_category = Category(name=name, user=user)
    new_category.save()
    text=_('Category created!\n')
    if purchase_id:
        purchase = Purchase.get(Purchase.id==purchase_id, 
                                Purchase.user==user
                                )
        purchase.category = new_category
        purchase.save()
        text += show_purchase_item(user, purchase_id)
    elif seller_id:
        seller = Seller.get(Seller.id==seller_id, 
                            Seller.user==user
                            )
        seller.category = new_category
        seller.save()
        text += show_seller_item(user, seller_id)
    return text
    
    
def create_seller(user, name, purchase_id=None):
    
    new_seller = Seller(name=name, user=user)
    new_seller.save()
    text=_('Seller created!\n')
    if purchase_id:
        purchase = Purchase.get(Purchase.id==purchase_id, 
                                Purchase.user==user
                                )
        purchase.seller = new_seller
        purchase.save()
        new_seller.category = purchase.category
        new_seller.save()
        text += show_purchase_item(user, purchase_id)
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


def show_user_item(user,  id_obj):
    
    user = User.get(User.id==id_obj)
    text = 'username: %s\ndatetime: %s\nactive: %s\nadmin: %s\npaid: %s\ndate payment: %s' % (
                                            user.username, 
                                            user.start_time,
                                            user.is_active, 
                                            user.is_admin, 
                                            user.paid, 
                                            user.paid_datetime
                                            )
    return text
    
    
def show_sberbank_donate_text():
    text = _('For donate in sberbank-online\n')
    text += _('Copy this number:\n')
    text += _('5484 0144 0994 4498\n')
    text += _('Go to: https://online.sberbank.ru\n')
    text += _('And then fill number of card in field for payment\n')
    return text
    
    
def show_paypal_donate_text():
    text = _('Paypal Donate:\n')
    text += _('https://www.paypal.me/yaricpisarev\n')
    return text
    
    
def show_patreon_donate_text():
    text = _('Patreon Donate:\n')
    text += _('https://www.patreon.com/qrscanner_order_bot\n')
    return text
    

def show_donate_link_ru():
    text = 'https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=F444B9FSAE4XW&source=url'
    return text
    

#def show_donate_form_ru():
#    text = '<form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top">'\
#    '<input type="hidden" name="cmd" value="_s-xclick" />'\
#    '<input type="hidden" name="hosted_button_id" value="F444B9FSAE4XW" />'\
#    '<input type="image" src="https://www.paypalobjects.com/ru_RU/RU/i/btn/btn_donateCC_LG.gif"'\
#    ' border="0" name="submit" title="PayPal - The safer, easier way to pay online!"'\
#    '/>'\
#    '<img alt="" border="0" src="https://www.paypal.com/ru_RU/i/scr/pixel.gif" width="1"'\
#    ' height="1" />'\
#    '</form>'
#    return text
    
    
#def show_donate_link_en():
#    text = 'https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=6FQEGNXMVMF8C&source=url'
#    return text
#
#
#def show_donate_form_en():
#    text = '<form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top">'\
#    '<input type="hidden" name="cmd" value="_s-xclick" />'\
#    '<input type="hidden" name="hosted_button_id" value="6FQEGNXMVMF8C" />'\
#    '<input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif"'\
#    ' border="0" name="submit" title="PayPal - The safer, easier way to pay online!"'\
#    ' alt="Donate with PayPal button" />'\
#    '<img alt="" border="0" src="https://www.paypal.com/en_US/i/scr/pixel.gif"'\
#    ' width="1" height="1" />'\
#    '</form>'
#    return text
