import os
import sys
from playhouse.migrate import *

sys.path.append(os.getcwd())

from config import *


migrate(
    migrator.drop_column('seller', 'longitude'),
    migrator.drop_column('seller', 'latitude'), 
)
