import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError

from msio.logme.core.cache import in_memory_cache
from msio.logme.core.config import settings
from msio.logme.core.database import SessionLocal
from msio.logme.crud.tokens import ThreadMemoryTokenRepository
from msio.logme.crud.users import PostgresUserRepository
from msio.logme.domain.entities import Token
from msio.logme.domain.exceptions import UnavailableRepositoryError
from msio.logme.domain.repositories import TokenRepository, UserRepository
from msio.logme.schemas.token import TokenPayload

current_api = "v1"
oauth2 = OAuth2PasswordBearer(tokenUrl=f"/api/{current_api}/login")


async def get_session():
    async with SessionLocal() as session:
        yield session


async def get_user_repository():
    async with SessionLocal() as session:
        repository = PostgresUserRepository(database_session=session)
        yield repository


async def get_token_repository():
    repository = ThreadMemoryTokenRepository(cache=in_memory_cache.map)
    yield repository


async def get_token_data(
    token: str = Depends(oauth2),
    token_repository: TokenRepository = Depends(get_token_repository),
) -> TokenPayload:
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
    # return token_data
    has_token = await token_repository.has_token(
        Token(value=token, user_id=token_data.user_id)
    )
    if not has_token:
        raise HTTPException(
            status_code=403, detail="Could not validate credentials"
        )
    return token_data


async def get_current_user(
    user_repository: UserRepository = Depends(get_user_repository),
    token: TokenPayload = Depends(get_token_data),
):
    try:
        user = await user_repository.find_user_by_id(user_id=token.user_id)
    except UnavailableRepositoryError:
        raise HTTPException(
            status_code=503, detail="Service temporarily down"
        )
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
