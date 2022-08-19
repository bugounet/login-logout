from typing import Literal

from pydantic import BaseModel, EmailStr, PositiveInt, SecretStr, constr

from msio.logme.domain.entities import User


class LoginParameters(BaseModel):
    username: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: Literal["bearer"]


class TokenPayload(BaseModel):
    user_id: int

    @classmethod
    def from_user(cls, user: User):
        return cls(user_id=user.id)


class UserBase(BaseModel):
    """This schema will be used for reading Users."""

    id: PositiveInt
    first_name: constr(max_length=50)
    last_name: constr(max_length=50)
    username: constr(max_length=50)
    email: EmailStr


class IdentitySchema(BaseModel):
    first_name: constr(max_length=50) | None
    last_name: constr(max_length=50) | None
    username: constr(max_length=50) | None


class PasswordSchema(BaseModel):
    password: SecretStr | None


class UserRegistration(IdentitySchema, PasswordSchema):
    """This schema will be used to create
    new users.
    """

    email: EmailStr


class UserLookupResults(BaseModel):
    results: list[UserBase]
