from peewee import *
from config import *

#def get_db():
#
#    if TYPE_DB == 'sqlite':
#        db = SqliteDatabase(PATH_DB, pragmas={
#            'journal_mode': 'wal',
#            'cache_size': -1024 * 64})
#    elif TYPE_DB == 'pgsql':
#        db = PostgresqlDatabase(PG_BATABASE, user=PG_USERNAME, 
#                                password=PG_PASSWORD,
#                            host=PG_HOST, port=PG_PORT)
#    return db
#
#                     
#class Status(Model):
#    name = CharField()
#    value = BooleanField()
#    user = CharField()
#    
#    class Meta:
#        database = get_db()
#        
#        
#class Wait(Model):
#    command = CharField()
#    user = CharField()
#    
#    class Meta:
#        database = get_db()
#    
#    
#class Category(Model):
#    name = CharField()
#    user = CharField()
#    
#    class Meta:
#        database = get_db()
#        
#class Seller(Model):
#    name = CharField()
#    user = CharField()
#    
#    class Meta:
#        database = get_db()
#           
#          
#class Purchase(Model):
#    category = ForeignKeyField(Category, backref='categories', null=True)
#    name = CharField()
#    datetime = DateTimeField()
#    summ = DecimalField()
#    seller = ForeignKeyField(Seller, backref='sellers', null=True)
#    user = CharField()
#
#    class Meta:
#        database = get_db()
        
        
def initialize_db():
    db = get_db()
    db.connect()
    db.create_tables([Category, Purchase, Seller, Wait], safe = True)
    db.close()
    
        
initialize_db()
