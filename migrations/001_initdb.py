import os
import sys
from playhouse.migrate import *

sys.path.append(os.getcwd())

from config import *
import peewee as pw

#my_db = SqliteDatabase('../test_qrscanner.db')
#migrator = SqliteMigrator(my_db)

user_field = pw.CharField(default='')

print(migrator.database.__dict__)

migrate(
    migrator.add_column('Category', 'user', user_field),
    migrator.add_column('Seller', 'user', user_field),
    migrator.add_column('Purchase', 'user', user_field),
    
)



