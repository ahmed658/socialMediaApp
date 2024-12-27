import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from . import schemas, models
from .config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    print(ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    enocded_jwt = jwt.encode(payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    
    return enocded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(jwt= token, key= SECRET_KEY, algorithms=[ALGORITHM])
        userId = payload.get("user_id")
        if userId is None:
            raise credentials_exception
        TokenData = schemas.TokenData(id= userId)
    except InvalidTokenError:
        raise credentials_exception
    return TokenData

def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    user_id = verify_access_token(token= token, credentials_exception= credentials_exception).id
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user