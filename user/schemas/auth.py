from pydantic import BaseModel, EmailStr, Field

class SUserRegister(BaseModel):
    name: str
    email: EmailStr
    phone_number: str = Field(..., pattern=r"^(\+7|8)\d{10}$")
    password: str
    
class SUserUpdate(BaseModel):
    name: str
    email: EmailStr
    phone_number: str = Field(..., pattern=r"^(\+7|8)\d{10}$")

class SUserLogin(BaseModel):
    email: EmailStr
    password: str
    
class SUser(BaseModel):
    name: str
    email: EmailStr
    phone_number: str = Field(..., pattern=r"^(\+7|8)\d{10}$")
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
    
    
