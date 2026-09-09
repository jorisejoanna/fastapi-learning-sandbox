
"""
Day 12 - JWT Token Authentication
-Logging in with credentials to receive a cryptographically signed JSON Web Token (JWT), and using that token to protect private routes like /users/me
-Web APIs are stateless, which means the server doesn't remember who you are from one request to the next
-We never wnat a frontend app to send user's password with every single button click or API call
-Instead, the user logs in once via /token
-The server verifies the password, stams a temporary signed digital badge called a JWT Token (valid for, say, 30 minutes), and hands it back
-For every future request (e.g. GET/users/me), the user simply flashes this token in the request header (Authorization: Bearer <token>)!
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

import jwt
import database
import models
import schemas
import utils

#create all tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  #1. tells FastAPI where clients should send username/password to get a token

#add CORS Middleware which allows React frontend on different domain to talk to the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

#----------Day 14 SIGNUP ENDPOINT----------
@app.post("/users/", response_model=schemas.UserResponse, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email==user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered! satu kali cukup la HAHAHHA"
        )
    hashed = utils.hash_password(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed, is_active=True)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#4. PROTECTED ENDPOINT: Only accessible with a valid tokennn!!!
@app.get("/users/me", response_model=schemas.UserResponse)
def read_users_me(current_user:models.User=Depends(get_current_user)):
    return current_user