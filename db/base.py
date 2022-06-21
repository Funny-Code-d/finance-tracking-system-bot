from databases import Database
from sqlalchemy import create_engine, MetaData
from os import getenv

DATABASE_URL = getenv("DATABASE_CONNECT")
database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(
    DATABASE_URL
)