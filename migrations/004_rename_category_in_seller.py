import os
import sys
from playhouse.migrate import *

sys.path.append(os.getcwd())

from config import *
import peewee as pw

category = pw.ForeignKeyField(Category, field=Category.id, backref='categories', null=True)
migrate(
    migrator.rename_column('Seller', 'category', 'category_id'),
)
