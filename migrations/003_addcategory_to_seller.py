import os
import sys
from playhouse.migrate import *

sys.path.append(os.getcwd())

from config import *
import peewee as pw

cat_field = pw.ForeignKeyField('Category', backref='categories', null=True)
migrate(
    migrator.add_column('Seller', 'category', cat_field),
    
)
