import datetime
import peewee as pw

from .main import MainModel
from .user import User

class Payment(MainModel):
    
    paid = pw.BooleanField(default=False)
    paid_datetime = pw.DateTimeField(null=True, default=datetime.datetime.now)
    user = pw.ForeignKeyField(User, backref='users', null=True)
