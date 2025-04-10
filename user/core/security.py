from passlib.context import CryptContext
from datetime import datetime, timedelta
from core.config import settings
from jose import jwt
from fastapi import status, HTTPException
from pydantic import EmailStr
from repositories.users import AuthRepository


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password, hash) -> bool:
    return pwd_context.verify(password, hash)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode.update({'exp': datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_MINUTES)}) 
    jwt_encoded = jwt.encode(to_encode, settings.EE_SECRET_KEY, settings.ALGORITHM)
    return jwt_encoded
    
def decode_access_token(token: str):
    payload = jwt.decode(token=token, key=settings.EE_SECRET_KEY, algorithms=settings.ALGORITHM)    
    
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token expired")
    
    return payload

async def auth_user(email: EmailStr, password: str):
    user = await AuthRepository.get_by_email(email_=email)
    print(user)
    if not user and not verify_password(password=password, hash=user.hash_password):
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Incorrect email or password")
    
    return user

def create_refresh_token(data: dict):
    to_encode = data.copy()
    to_encode.update({'exp': datetime.now()+ timedelta(settings.REFRESH_TOKEN_DAYS)})
    jwt_encoded = jwt.encode(to_encode, key=settings.EE_SECRET_KEY, algorithm=settings.ALGORITHM)
    return jwt_encoded    
    
async def check_email_name(email, name):
    if not await AuthRepository.get_one_or_none(email=email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This email already taken")
    if not await AuthRepository.get_one_or_none(name=name):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This name already taken")
    