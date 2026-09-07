"""
Validates data coming in from user's JSON payload and formats data going out in the HTTP response
"""

from pydantic import BaseModel #import BaseModel from Pydantic for data validation

#1. base schema (shared fields for creating/reading items)
class ItemBase(BaseModel):
    title: str
    description: str | None = None
    price: float
    is_offer: bool = False

#2. schema for CREATING an item (inherits title, description, price, is_offer)
class ItemCreate(ItemBase):
    pass #needs all fields from ItemBase

#3. schema for READING an item from the database (includes the DB-generated 'id')
class ItemResponse(ItemBase):
    id: int

# tells Pydantic to read data directly from SQLAlchemy database objects
class Config:
    from_attributes = True

#----------User Schemas----------

#1. schema for creating a new user (signup form input)
class UserCreate(BaseModel):
    email:str
    password:str    #raw password from the user (will be hashed before storing)

#2. schema for returning user data in API responses (NEVER RETURNS PASSWORD!)
class UserResponse(BaseModel):
    id:int
    email:str
    is_active:bool

    class Config:
        from_attributes=True