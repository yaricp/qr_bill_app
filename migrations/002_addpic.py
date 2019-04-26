import os
import sys
from playhouse.migrate import *

sys.path.append(os.getcwd())

from config import *
import peewee as pw

pic_field = pw.CharField(default='')

migrate(
    migrator.add_column('Purchase', 'pic', pic_field),
    
)
