from http.client import FORBIDDEN

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from msio.logme.core.cache import in_memory_cache
from msio.logme.core.config import settings
from msio.logme.core.dependencies import use_database
from msio.logme.domain.entities import Token, User
from msio.logme.domain.exceptions import (
    InvalidTokenError,
    UnavailableRepositoryError,
)
from msio.logme.domain.repositories import TokenRepository, UserRepository
from msio.logme.implementation.tokens import ThreadMemoryTokenRepository
from msio.logme.implementation.users import PostgresUserRepository
from msio.logme.schemas.token import TokenPayload

current_api = "v1"
oauth2 = OAuth2PasswordBearer(tokenUrl=f"/api/{current_api}/login")


async def get_user_repository():
    async with use_database() as session:
        repository = PostgresUserRepository(database_session=session)
        yield repository


async def get_token_repository():
    repository = ThreadMemoryTokenRepository(cache=in_memory_cache.map)
    yield repository


async def get_token_payload(
    token: str = Depends(oauth2),
) -> TokenPayload:
    try:
        payload = Token.parse_and_verify_token(
            token, settings.SECRET_KEY.get_secret_value()
        )
        token_data = TokenPayload(user_id=payload.user_id)
    except InvalidTokenError:
        raise HTTPException(
            status_code=403, detail="Could not validate credentials"
        )
    # return token_data
    return token_data


async def verify_token(
    token: str = Depends(oauth2),
    token_repository: TokenRepository = Depends(get_token_repository),
) -> TokenPayload:
    token_payload = await get_token_payload(token)
    # verify it's a known token
    has_token = await token_repository.has_token(
        Token(value=token, user_id=token_payload.user_id)
    )
    if not has_token:
        raise HTTPException(
            status_code=403, detail="Could not validate credentials"
        )
    return token_payload


async def get_current_user(
    user_repository: UserRepository = Depends(get_user_repository),
    token_payload: TokenPayload = Depends(verify_token),
) -> User:
    try:
        user = await user_repository.find_user_by_id(
            user_id=token_payload.user_id
        )
    except UnavailableRepositoryError:
        raise HTTPException(
            status_code=503, detail="Service temporarily down"
        )
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_logged_admin(logged_user: User = Depends(get_current_user)) -> User:
    if logged_user.email != settings.FIRST_USER_EMAIL:
        raise HTTPException(
            status_code=FORBIDDEN, detail="Permission denied."
        )
    return logged_user