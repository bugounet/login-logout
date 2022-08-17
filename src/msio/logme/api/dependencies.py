import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError

from msio.logme.core.config import settings
from msio.logme.core.database import SessionLocal
from msio.logme.domain.exceptions import UnavailableRepositoryError
from msio.logme.domain.repositories import UserRepository
from msio.logme.schemas.token import TokenPayload

current_api = "v1"
oauth2 = OAuth2PasswordBearer(tokenUrl=f"/api/{current_api}/login")


# usage  session: AsyncSession = Depends(get_session),
async def get_session():
    async with SessionLocal() as session:
        yield session


def get_token_data(token: str = Depends(oauth2)) -> TokenPayload:
    try:
        secret_key = settings.SECRET_KEY.get_secret_value()
        payload = jwt.decode(
            token, secret_key, algorithms=[settings.JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=403, detail="Could not validate credentials"
        )
    return token_data


async def get_current_user(
    user_repository: UserRepository,
    token: TokenPayload = Depends(get_token_data),
):
    try:
        user = await user_repository.find_user_by_id(user_id=token.user_id)
    except UnavailableRepositoryError:
        raise HTTPException(status_code=503, detail="Service temporarily down")
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
