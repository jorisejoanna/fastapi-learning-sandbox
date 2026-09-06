"""
To handle creating and reading items directly inside Neon PostgreSQL
"""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import database
import models
import schemas

#1. tell SQLAlchemy to create all tables defined in models.py inside Neon PostgreSQL
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

#2. Dependancy: Opens a database session per HTTP request and closes it after the request finishes
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

#3. POST Endpoint: Create a new item row in Neon PostgreSQL
@app.post("/items/", response_model=schemas.ItemResponse, status_code=201)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(
        title=item.title,
        description=item.description,
        price=item.price,
        is_offer=item.is_offer
    )

    db.add(db_item) #add the new row to the session
    db.commit() #commit changes to Neon PostgreSQL
    db.refresh(db_item) #refresh db_item to load the auto-generated database 'id'
    return db_item

#4. GET Endpoint: Fetch all item rows from Neon PostgreSQL
@app.get("/items", response_model=list[schemas.ItemResponse])
def read_item(db: Session = Depends(get_db)):
    #query the 'items' table inside Neon PostgreSQL
    items = db.query(models.Item).all()
    return items