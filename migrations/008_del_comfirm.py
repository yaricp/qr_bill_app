import os
import sys
from playhouse.migrate import *

sys.path.append(os.getcwd())

from config import *
#import peewee as pw
from models.purchace import Purchase


migrate(
    migrator.drop_column('Purchase', 'confirm'),
)
