from datetime import datetime
from sqlalchemy import Integer, TIMESTAMP, Column, String, Table

from database import metadata


operation = Table(
    "operation",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, unique=True, nullable=False),
    Column("description", String, nullable=True),
    Column("created_at", TIMESTAMP, default=datetime.now),
    Column("updated_at", TIMESTAMP, onupdate=datetime.now),
)
