from peewee import *
from config import PATH_DB

if TYPE_DB == 'sqlite':
    db = SqliteDatabase(PATH_DB, pragmas={
        'journal_mode': 'wal',
        'cache_size': -1024 * 64})
elif TYPE_DB == 'pgsql':
    db = PostgresqlDatabase(PG_BATABASE, user=PG_USERNAME, 
                            password=PG_PASSWORD,
                            host=PG_HOST, port=PG_PORT)
                            
                            
class Status(Model):
    name = CharField()
    value = BooleanField()
    
    class Meta:
        database = db
    
    
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
    db.create_tables([Category, Purchase, Seller, Status], safe = True)
    st = Status(name='wait_seller_name', value=False)
    st.save()
    st = Status(name='wait_category_name', value=False)
    st.save()
    db.close()
    
        
initialize_db()
