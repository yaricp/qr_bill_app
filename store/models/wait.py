import peewee as pw

from .main import MainModel

class Wait(MainModel):
    command = pw.CharField()
    user = pw.CharField()
