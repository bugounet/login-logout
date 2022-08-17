from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """This schema will be used for reading Users."""

    id: int = None
    first_name: str
    last_name: str
    username: str
    email: EmailStr


class UserRegistration(UserBase):
    """This schema will be used to create
    new users.
    """

    password: str
