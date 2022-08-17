from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from msio.logme.core.database import SessionLocal
from msio.logme.core.authentication import ALGORITHM
#from msio.logme.crud.users import crud_user
from msio.logme.schemas.token import TokenPayload
from msio.logme.core.config import settings

current_api = "v1"
oauth2 = OAuth2PasswordBearer(tokenUrl=f"/api/{current_api}/login")


async def get_session():
    async with SessionLocal() as session:
        yield session


def get_token_data(token: str = Depends(oauth2)) -> TokenPayload:
    try:
        secret_key = settings.SECRET_KEY.get_secret_value()
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return token_data


async def get_current_user(token: TokenPayload = Depends(get_token_data), session: AsyncSession = Depends(get_session)):
    user = await crud_user.get(session, id=token.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


