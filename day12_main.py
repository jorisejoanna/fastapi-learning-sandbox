

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import jwt

import database
import models
import schemas
import utils

#create all tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  #1. tells FastAPI where clients should send username/password to get a token

#database session dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

#2. dependency: extracts token from header, validates it, and fethces the logged-in user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials:( SOWWYY",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        #decode and verify the cryptographic signature of the token
        payload = jwt.decode(token, utils.SECRET_KEY, algorithms=[utils.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    #query database to confirm user exists
    user = db.query(models.User).filter(models.User.email==email).first()
    if user is None:
        raise credentials_exception
    return user

#3. LOGIN ENDPOINT: Accepts username & password, returns JWT token
@app.post("/token/", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email==form_data.username).first()
    if not user or not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password ohhh naurr",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    #create signed JWT token with user's email stored in 'sub' (subject)
    access_token = utils.create_access_token(data={"sub":user.email})
    return{"access_token": access_token, "token_type": "bearer"}

#4. PROTECTED ENDPOINT: Only accessible with a valid tokennn!!!
@app.get("/users/me", response_model=schemas.UserResponse)
def read_users_me(current_user:models.User=Depends(get_current_user)):
    return current_user