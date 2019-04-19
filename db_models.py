from peewee import *
from config import PATH_DB
db = SqliteDatabase(PATH_DB, pragmas={
    'journal_mode': 'wal',
    'cache_size': -1024 * 64})
    
    
#pg_db = PostgresqlDatabase('my_app', user='postgres', password='secret',
#                           host='10.1.0.9', port=5432)
    
class Category(Model):
    name = CharField()
    
    class Meta:
        database = db
        
class Seller(Model):
    name = CharField()
    
    class Meta:
        database = db
           
          
class Purchase(Model):
    category = ForeignKeyField(Category, backref='categories', null=True)
    name = CharField()
    datetime = DateTimeField()
    summ = DecimalField()
    seller = ForeignKeyField(Seller, backref='sellers', null=True)

    class Meta:
        database = db
        
        
def initialize_db():
    db.connect()
    db.create_tables([Category, Purchase, Seller], safe = True)
    db.close()
        
initialize_db()
