from fastapi import FastAPI
import database #import database engine and Base from database.py
import models # import models to register the Item class

#1. tell SQLAlchemy to create all tables defined in models.py inside Neon PostgreSQL
models.Base.metadata.create_all(bind=database.engine) 

#2. initialise FastAPI app
app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "FastAPI is connected to Neon PostgreSQL!!!😛😛😛😛"}