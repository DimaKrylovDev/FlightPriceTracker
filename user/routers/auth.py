from fastapi import APIRouter, status, HTTPException, Response, Request
from schemas.auth import SUserRegister, SUser, SUserUpdate, SUserLogin, Token
from repositories.users import AuthRepository
from core.security import hash_password, create_access_token, auth_user, create_refresh_token, check_email_name, decode_access_token
from db.database import redis
from datetime import timedelta
from core.config import settings

router = APIRouter(prefix="/user", tags=['auth'])

@router.get("/read")
async def read(id: int):
    result = await AuthRepository.get_by_id(id_=id)
    return result 

@router.post("/registration", status_code=status.HTTP_201_CREATED)
async def registration(
    user: SUserRegister):
    
    check_email_name(email=user.email, name=user.name)
    
    new_user = await AuthRepository.create(
        name = user.name,
        phone_number = user.phone_number,
        email = user.email,
        hash_password = hash_password(user.password)
    )

@router.post("/login", status_code=status.HTTP_200_OK)
async def login(user: SUserLogin, response: Response):
    current_user = await auth_user(email=user.email, password=user.password)
    print(current_user)
    access_token = create_access_token({"sub": user.email})
    response.set_cookie(key="access_token", value=access_token, httponly=True, expires=settings.ACCESS_TOKEN_MINUTES)
    refresh_token = create_refresh_token({"sub": user.email})
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, expires=settings.REFRESH_TOKEN_DAYS)
    print(current_user.id)
    client = redis
    client.hset("user:{current_user.id}", "refresh_token", refresh_token)
    client.expire(f"user:{current_user.id}", time=int(timedelta(days=settings.REFRESH_TOKEN_DAYS).total_seconds()))
    stored_refresh_token = client.hget(f"user:{current_user.id}", "refresh_token")
    if stored_refresh_token:
        print(stored_refresh_token.decode('utf-8')) 
    else:
        print("Refresh token not found or expired")
    
    return Token(
        access_token=access_token,
        token_type='Bearer')
    
@router.post('/refresh', status_code=status.HTTP_200_OK)
async def refresh_token(request: Request, response: Response):
    refresh_token=request.cookies.get("refresh_token")
    
    try:
        payload = decode_access_token(refresh_token)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token is expired")

    email = payload['sub']
    
    user = await AuthRepository.get_by_email(email_=email)
    access_token = create_access_token({'sub': user.email})
    refresh_token = create_refresh_token({'sub': user.email})
    
    client = redis
    client.hset("user: {user.id}", "refresh_token", refresh_token)
    client.expire(f"user:{user.id}", time=int(timedelta(days=settings.REFRESH_TOKEN_DAYS).total_seconds()))
    
    response.set_cookie(key="access_token", value=access_token, expires=settings.ACCESS_TOKEN_MINUTES)
    response.set_cookie(key="refresh_token", value=refresh_token, expires=settings.REFRESH_TOKEN_DAYS)
    
@router.put("/update", status_code=status.HTTP_200_OK)
async def update(
    id: int,
    user: SUserUpdate):
    
    await AuthRepository.update(
        id_=id,
        name=user.name,
        email=user.email,
        phone_number=user.phone_number
    )
    
@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(response: Response):
    response.delete_cookie('refresh_token')
    response.delete_cookie('access_token')
    
@router.delete('/delete', status_code=status.HTTP_200_OK)
async def delete(id: int):
    await AuthRepository.delete(id_=id)
