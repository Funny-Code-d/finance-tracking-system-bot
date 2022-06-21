from sqlalchemy import Column
from sqlalchemy import String, Integer
import sqlalchemy
from .base import metadata


customers = sqlalchemy.Table(
    "customers",
    metadata,
    Column("customer_sk", Integer),
    Column("first_name", String),
    Column("last_name", String),
    Column("email", String, primary_key=True),
    Column("telegram_id", Integer, primary_key=True)
)