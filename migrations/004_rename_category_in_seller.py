import os
import sys
from playhouse.migrate import *

sys.path.append(os.getcwd())

from config import *
#import peewee as pw

migrate(
    migrator.rename_column('Seller', 'category', 'category_id'),
)
