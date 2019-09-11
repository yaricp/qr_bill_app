import peewee as pw

from config import *


class MainModel(pw.Model):
    class Meta:
        database = db
