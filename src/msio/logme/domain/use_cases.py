import jwt
from pydantic import EmailStr

from msio.logme.core.config import settings
from msio.logme.domain.entities import Token, User, UserRegistrationRequest
from msio.logme.domain.repositories import TokenRepository, UserRepository
from msio.logme.schemas.login import LoginParameters
from msio.logme.schemas.token import TokenPayload


class GetOrCreateFirstUser:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def __call__(
        self, first_user_definition: UserRegistrationRequest
    ):
        found_user = await self.user_repository.find_user_by_email(
            email_address=EmailStr(first_user_definition.email)
        )
        if not found_user:
            await self.user_repository.register_user(first_user_definition)


class LoginUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        token_repository: TokenRepository,
    ):
        self.user_repository = user_repository
        self.token_repository = token_repository

    async def __call__(self, login_parameters: LoginParameters) -> Token:
        user = await self.user_repository.find_user_using_credentials(
            login_parameters.username,
            User.compute_password_hash(login_parameters.password),
        )
        payload = TokenPayload.from_user(user).dict()
        access_token = jwt.encode(
            payload,
            key=settings.SECRET_KEY.get_secret_value(),
        )
        token = Token(value=access_token, user_id=user.id)
        await self.token_repository.save_token(token)
        return token


class LogoutUseCase:
    def __init__(self, token_repository: TokenRepository):
        self.token_repository = token_repository

    async def __call__(self, access_token: Token):
        if await self.token_repository.has_token(access_token):
            await self.token_repository.forget_token(access_token)
