import os
import sys
from playhouse.migrate import *

sys.path.append(os.getcwd())

from config import *
import peewee as pw
from models.category import Category


category = pw.ForeignKeyField(Category, field=Category.id, backref='categories', null=True)
migrate(
    migrator.add_column('Seller', 'category', category),
    
)
