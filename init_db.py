from peewee import *
from config import *
from models import *

def initialize_db():
    print('DB:', db)
    db.connect()
    db.create_tables([  category.Category, 
                        purchase.Purchase, 
                        seller.Seller, 
                        wait.Wait, 
                        language.Language, 
                        user.User
                        ], safe = True)
    admin = user.User.get_or_create(username=superuser, 
                                    tg_user_id=allowed_users[superuser], 
                                    is_active=True, 
                                    is_admin=True, 
                                    paid_datetime=''
                                    )
    #print(admin)
    db.close()
    

