# -*- coding: utf-8 -*-
import psycopg2

from decorators import *
from store.models.seller import Seller
from store.models.category import Category
from store.models.purchase import Purchase

START, LOCATION, SELLER, CATEGORY, NAME_SELLER_CATEGORY, MEDIA = range(6)

dict_types = {
        'purchase': Purchase, 
        'seller': Seller, 
        'category': Category, 
        'user': User
    }

def get_dict_month():
    dict_months = {
                    1: _('January'), 
                    2: _('Februrary'), 
                    3: _('March'), 
                    4: _('April'), 
                    5: _('May'), 
                    6: _('June'), 
                    7: _('July'), 
                    8: _('August'), 
                    9: _('September'), 
                    10: _('Oktober'), 
                    11: _('November'), 
                    12: _('December')
                    }
    return dict_months
    
    
def get_update_data(update):
    if update.callback_query:
        user = update.callback_query.from_user.id
        chat_id = update.callback_query.message.chat.id
        message_id = update.callback_query.message.message_id
    else:
        user = update.message.from_user.id
        chat_id = update.message.chat.id
        message_id = update.message.message_id
    return user, chat_id, message_id
    
    


    
def get_geo_positions(type_obj, id):
    conn = psycopg2.connect(database=PG_BATABASE, 
                            user=PG_USERNAME, 
                            password=PG_PASSWORD)
    curs = conn.cursor()
    geo = None
    sql_text = 'SELECT ST_AsText(geom) FROM %s WHERE id=%s' % (type_obj, id)
    curs.execute(sql_text)
    result = curs.fetchall()[0]
    point = result[0]
    if point:
        point = point.replace('POINT(', '').replace(')', '').split(' ')
        geo = (point[0], point[1])
    conn.close()
    return geo 
    
    
def save_geo_position(type_obj, id, geo):
    conn = psycopg2.connect(database=PG_BATABASE, 
                            user=PG_USERNAME, 
                            password=PG_PASSWORD)
    curs = conn.cursor()
    sql_text = 'UPDATE %s SET geom = ST_SetSRID(ST_MakePoint('\
                '%s, %s), 4326) WHERE id=%s;' % (type_obj, geo.longitude, geo.latitude, id)
    
    
    result = curs.execute(sql_text)
    conn.commit()
    conn.close()
    return result
    
    
def find_sellers_around(geo, radius_mi=RADIUS_SEARCH_SELLER/1000):
    conn = psycopg2.connect(database=PG_BATABASE, 
                                user=PG_USERNAME, 
                                password=PG_PASSWORD)
    curs = conn.cursor()
    print('Search radius: ', radius_mi)
    curs.execute(
        'SELECT id,name FROM seller '\
        'WHERE ST_Distance_Sphere(geom, ST_SetSRID(ST_MakePoint('\
        '%s, %s), 4326)) <= %s * 1609.34;', 
        (geo.longitude, geo.latitude, (radius_mi/1000)))
    print('found')
    
    return curs.fetchall()
