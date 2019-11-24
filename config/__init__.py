# -*- coding: utf-8 -*-
import os
import peewee as pw
from playhouse.migrate import *

REQUEST_KWARGS={
    #'proxy_url': 'socks5://80.211.38.123:1080',
    'proxy_url': 'socks5://80.211.38.123:12312',
    # Optional, if you need authentication:
    'urllib3_proxy_kwargs': {
        'username': 'user123321',
        'password': '123qweasdzxc',
    }
}

LANGUAGES = ['en', 'ru']
DEFAULT_LANG = 'ru'

PATH_TEMP_FILES = 'files'
superuser = 'yaricp'
allowed_users = {'yaricp':'251241715',
                'yaricp_dev':'556094746', 
                 'Алексей': '470579427'}

                
admins = {'yaricp':'251241715'}
DEVEL_ENV = int(os.getenv('DEVEL', 1))
DEVEL=True
if DEVEL_ENV == 0:
    DEVEL=False
print('DEVEL:', DEVEL)

if DEVEL:
    from config.development import *
else:
    from config.production import *
    
if TYPE_DB == 'sqlite':
    db = pw.SqliteDatabase(PATH_DB, pragmas={
        'journal_mode': 'wal',
        'cache_size': -1024 * 64})
    migrator = SqliteMigrator(db)
elif TYPE_DB == 'pgsql':
    #if DEVEL: print('Init Postgres DB')
    #if DEVEL: print(PG_BATABASE)
    db = pw.PostgresqlDatabase(PG_BATABASE, user=PG_USERNAME, 
                                password=PG_PASSWORD,
                            host=PG_HOST, port=PG_PORT)
    migrator = PostgresqlMigrator(db)
                            

RADIUS_SEARCH_SELLER = 300 # meters 
COUNT_ON_PAGE = 10
