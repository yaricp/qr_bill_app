import peewee as pw

from .main import MainModel

from config import *

class Language(MainModel):
    lang = pw.CharField(default=DEFAULT_LANG)
    user = pw.CharField()
