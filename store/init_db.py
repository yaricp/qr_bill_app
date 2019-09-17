from peewee import *
from config import *
from .models import *

def initialize_db():
    if DEVEL: print('DB:', db)
    db.connect()
    db.create_tables([  category.Category, 
                        purchase.Purchase, 
                        seller.Seller, 
                        wait.Wait, 
                        language.Language, 
                        user.User, 
                        payment.Payment
                        ], safe = True)
    admin = user.User.get_or_create(username=superuser, 
                                    tg_user_id=allowed_users[superuser], 
                                    is_active=True, 
                                    is_admin=True, 
                                    )
    #if DEVEL: print(admin)
    db.close()
    

