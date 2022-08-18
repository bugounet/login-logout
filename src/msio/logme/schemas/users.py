from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """This schema will be used for reading Users."""

    id: int
    first_name: str
    last_name: str
    username: str
    email: str


class UserRegistration(BaseModel):
    """This schema will be used to create
    new users.
    """

    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str


class UserLookupResults(BaseModel):
    results: list[UserBase]
