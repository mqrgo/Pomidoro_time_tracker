from sqlalchemy import Column, Integer, String
from sqlalchemy.types import LargeBinary
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    username = Column(String(), nullable=False)
    email = Column(String(), nullable=False)
    password = Column(LargeBinary(), nullable=False)


metadata = Base.metadata
