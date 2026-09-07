"""
user signup endpoint
"""

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

import database
import models
import schemas
import utils

#create all tables (including new 'users' table) in Neon PostgreSQL
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

#database session dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

#POST /users/ - User Signup Endpoint
@app.post("/users/", response_model=schemas.UserResponse, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(models.User).filter(models.User.email == user.email).first()   #1. check if email already exsits in database
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered!"
        )
    
    hashed = utils.hash_password(user.password)     #2. hash the raw password using bcrypt (NEVER STORE RAW PASSWORDS!)

    db_user = models.User(         #3. create new user database row with hashed password
        email=user.email,
        hashed_password=hashed,
        is_active=True,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user