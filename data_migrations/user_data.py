import os
import sys

sys.path.append(os.getcwd())


from models.seller import Seller
from models.purchase import Purchase
from models.category import Category
from model.wait import Wait

user_id = '251241715'

for p in Purchase.select():
    p.user = user_id
    p.save()
    
for s in Seller.select():
    s.user = user_id
    s.save()
    
for c in Category.select():
    c.user = user_id
    c.save()
    
for w in Wait.select():
    w.user = user_id
    w.save()
