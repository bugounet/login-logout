from pydantic import BaseModel, EmailStr


class LoginParameters(BaseModel):
    username: EmailStr
    password: str
