from typing import Literal, Optional

from pydantic import BaseModel

from msio.logme.domain.entities import User


class Token(BaseModel):
    access_token: str
    token_type: Literal["bearer"]


class TokenPayload(BaseModel):
    user_id: Optional[int]

    @classmethod
    def from_user(cls, user: User):
        return cls(user_id=user.id)
