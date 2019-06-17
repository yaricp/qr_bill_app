import datetime
import peewee as pw

from .main import MainModel


class User(MainModel):
    username = pw.CharField()
    tg_user_id = pw.IntegerField()
    start_time = pw.DateTimeField(default=datetime.datetime.now)
    is_active = pw.BooleanField(default=False)
    is_admin = pw.BooleanField(default=False)
    paid = pw.BooleanField(default=False)
    paid_datetime = pw.DateTimeField(null=True, default='')
