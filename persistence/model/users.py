from connection.connect import Base
from sqlalchemy import Column, String, DateTime

class User(Base):
    __tablename__ = "users"

    id = Column(String(50), primary_key=True, unique=True)
    email = Column(String(255))
    country = Column(String(2))
    register_date = Column(DateTime, nullable=False)