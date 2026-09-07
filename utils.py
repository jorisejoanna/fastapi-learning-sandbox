import bcrypt
import jwt
from datetime import datetime, timedelta, timezone

#----------JWT Creation Logic----------
#1. secret keys & algorithm for signing tokens
SECRET_KEY = "my_super_very_bewwy_secret_jwt_key_change_in_production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15 

#----------Password Functions----------

# 1. Hashes a plain password using bcrypt
def hash_password(password: str) -> str:
    # bcrypt works with bytes
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

# 2. Checks if a plain password matches the stored hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    pwd_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hashed_bytes)

#----------JWT Token Generator----------
def create_access_token(data: dict, expires_delta: timedelta | None=None) -> str:
    to_encode = data.copy()

    #set token expiration time (default 15 minutes from now)
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)    #cryptographically sign the payload with our SECRET_KEY
    return encoded_jwt

