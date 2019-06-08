import os
import sys
from playhouse.migrate import *

sys.path.append(os.getcwd())

from config import *
import peewee as pw
from models.user import User


paid_datetime = pw.DateTimeField(null=True)
migrate(
    migrator.add_column('User', 'paid_datetime', paid_datetime),
    
)
