"""
Defines how data is structured inside PostgreSQL database tables
Defined database tables as Python classes
"""

from sqlalchemy import Column, Integer, String, Boolean, Float #import SQL column types from SQLAlchemy
from database import Base #import the Base class from database.py

#Define the Item database model class inheriting from Base
class Item(Base):
    __tablename__ = "items"                                 #1. specifies the exact table name in PostgreSQL

    id = Column (Integer, primary_key=True, index=True)     #2. define the columns in the 'items' table
    title = Column (String, index=True)                    
    description = Column (String)
    price = Column (Float)
    is_offer = Column (Boolean, default=False)
    category = Column(String, nullable=True)

#Adding User class
class User(Base):
    __tablename__ = "users"

    id = Column (Integer, primary_key=True, index=True)    #Unique user ID, auto-incremented
    email = Column (String, unique=True, index=True, nullable=False)    #Email must be unique (no two users can share the same email)
    hashed_password = Column (String, nullable=False)   #Stores the bcrypt-hashed password (NOT THE RAW PASSWORD!!!)
    is_active = Column (Boolean, default=True)  #Soft-disable accounts without deleting them