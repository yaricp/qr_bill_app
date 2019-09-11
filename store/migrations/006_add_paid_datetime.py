import os
import sys
from playhouse.migrate import *

sys.path.append(os.getcwd())

from config import *
import peewee as pw
from models.seller import Seller


longitude = pw.FloatField()
latitude = pw.FloatField()
migrate(
    migrator.add_column('Seller', 'longitude', longitude),
    migrator.add_column('Seller', 'latitude', latitude),
)
