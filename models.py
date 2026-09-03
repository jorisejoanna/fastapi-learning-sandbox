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