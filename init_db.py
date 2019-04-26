from peewee import *
from config import *
from models import *

def initialize_db():
    db.connect()
    print(type(category))
    db.create_tables([category.Category, purchase.Purchase, seller.Seller, wait.Wait], safe = True)
    db.close()
    

