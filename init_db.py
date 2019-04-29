from peewee import *
from config import *
from models import *

def initialize_db():
    db.connect()
    db.create_tables([  category.Category, 
                        purchase.Purchase, 
                        seller.Seller, 
                        wait.Wait, 
                        language.Language], safe = True)
    db.close()
    

