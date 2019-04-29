import peewee as pw

from .main import MainModel

class Language(MainModel):
    lang = pw.CharField()
    user = pw.CharField()
