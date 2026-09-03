from sqlalchemy import Column, Integer, String, Boolean, Float
from database import Base

class Item(Base):
    __tablename__ = "items"
    id = Column (Integer, primary_key=True, index=True)
    title = Column (String, index=True)
    description = Column (String)
    price = Column (Float)
    is_offer = Column (Boolean, default=False)