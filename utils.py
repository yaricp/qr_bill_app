# -*- coding: utf-8 -*-
import psycopg2

from decorators import *

GENDER, PHOTO, LOCATION, BIO = range(4)

def get_month(m):
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
    return dict_months[m]
    
    
def get_geo_positions(type, id):
    conn = psycopg2.connect(database=PG_BATABASE, 
                            user=PG_USERNAME, 
                            password=PG_PASSWORD)
    curs = conn.cursor()
    geo = None
    sql_text = 'SELECT ST_AsText(geom) FROM %s WHERE id=%s' % (type, id)
    curs.execute(sql_text)
    result = curs.fetchall()[0] 
    point = result[0]
    if len(point) == 2:
        geo = (point[0], point[1])
    return geo 
    
    
def save_geo_position(type, id, geo):
    conn = psycopg2.connect(database=PG_BATABASE, 
                            user=PG_USERNAME, 
                            password=PG_PASSWORD)
    curs = conn.cursor()
    geo = None
    sql_text = 'UPDATE %s SET geom = ST_SetSRID(ST_MakePoint('\
                '%s, %s), 4326) WHERE id=%s;' % (type, geo[1], geo[0], id)
    result = curs.execute(sql_text)
    return result
