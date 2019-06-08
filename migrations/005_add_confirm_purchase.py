import os
import sys
from playhouse.migrate import *

sys.path.append(os.getcwd())

from config import *
import peewee as pw
from models.purchase import Purchase


confirm = pw.BooleanField(default=True)
migrate(
    migrator.add_column('Purchase', 'confirm', confirm),
    
)
