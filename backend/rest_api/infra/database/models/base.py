from sqlalchemy.ext.declarative import declarative_base

from .. import db_session


Model = declarative_base()
Model.query = db_session.query_property()
