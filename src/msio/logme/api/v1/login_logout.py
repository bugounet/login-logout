from fastapi import APIRouter, Depends, Form, Header, HTTPException
from pydantic import EmailStr
from starlette.responses import JSONResponse

from msio.logme.api.dependencies import (
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
from msio.logme.domain.use_cases import LoginUseCase, LogoutUseCase
from msio.logme.schemas.login import LoginParameters
from msio.logme.schemas.token import Token

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
    use_case = LoginUseCase(user_repository, token_repository)
    try:

        token = await use_case(
            LoginParameters(username=username, password=password)
        )
        response = token_to_api_adapter(token).dict()
        return JSONResponse(status_code=200, content=response)
    except (UnknownUserError, InvalidCredentialsError):
        raise HTTPException(401, detail="Invalid credentials")
    except UnavailableRepositoryError:
        raise HTTPException(503, detail="Service temporarily down")


@router.get("/logout")
async def logout_view(
    Authorization: str | None = Header(default=None),
    token_repository: TokenRepository = Depends(get_token_repository),
):
    """Invalidate an access token you did generate"""
    use_case = LogoutUseCase(token_repository)
    await use_case(Authorization)
    return JSONResponse(status_code=204)
