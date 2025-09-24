from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .connection import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
