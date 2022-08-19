from fastapi import APIRouter, Depends, Form, HTTPException
from pydantic import EmailStr
from starlette.responses import JSONResponse, Response

from msio.logme.api.dependencies import (
    get_token_payload,
    get_token_repository,
    get_user_repository,
)
from msio.logme.domain.entities import Token as TokenEntity
from msio.logme.domain.exceptions import (
    InvalidCredentialsError,
    UnavailableRepositoryError,
    UnknownUserError,
)
from msio.logme.domain.repositories import TokenRepository, UserRepository
from msio.logme.domain.schemas import Login, Token
from msio.logme.use_cases import LoginUseCase, LogoutUseCase

router = APIRouter()


def token_to_api_adapter(token: TokenEntity) -> Token:
    return Token(access_token=token.value, token_type="bearer")


@router.post("/login")
async def login_view(
    username: EmailStr = Form(),
    password: str = Form(),
    user_repository: UserRepository = Depends(get_user_repository),
    token_repository: TokenRepository = Depends(get_token_repository),
):
    """Log user in using simple HTTP Form encoded request.

    Given an email and a password, this view will check
    proposed data and return an access token in case of success.
    """
    use_case = LoginUseCase(user_repository, token_repository)
    try:

        token = await use_case(Login(username=username, password=password))
        response = token_to_api_adapter(token).dict()
        return JSONResponse(status_code=200, content=response)
    except (UnknownUserError, InvalidCredentialsError):
        raise HTTPException(401, detail="Invalid credentials")
    except UnavailableRepositoryError:
        raise HTTPException(503, detail="Service temporarily down")


async def request_to_token_adapter(token: Token) -> TokenEntity:
    token_payload = await get_token_payload(token.access_token)
    return TokenEntity(
        value=token.access_token, user_id=token_payload.user_id
    )


@router.post("/logout")
async def logout_view(
    token: Token,
    token_repository: TokenRepository = Depends(get_token_repository),
):
    """Invalidate an access token you did generate"""
    use_case = LogoutUseCase(token_repository)
    token_entity = await request_to_token_adapter(token)
    await use_case(token_entity)
    return Response(status_code=204)
