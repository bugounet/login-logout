from dataclasses import dataclass
from http.client import NOT_FOUND, HTTPException

import jwt
from pydantic import EmailStr

from msio.logme.core.config import settings
from msio.logme.domain.entities import Token, User, UserRegistrationRequest
from msio.logme.domain.exceptions import UnavailableRepositoryError
from msio.logme.domain.repositories import TokenRepository, UserRepository
from msio.logme.domain.schemas import (
    Identity,
    Login,
    Password,
    TokenPayload,
)


@dataclass
class GetOrCreateFirstUser:
    user_repository: UserRepository

    async def __call__(
        self, first_user_definition: UserRegistrationRequest
    ) -> bool:
        try:
            found_user = await self.user_repository.find_user_by_email(
                email_address=EmailStr(first_user_definition.email)
            )
            if not found_user:
                await self.user_repository.register_user(
                    first_user_definition
                )
            return True
        except UnavailableRepositoryError:
            return False


@dataclass
class LoginUseCase:
    user_repository: UserRepository
    token_repository: TokenRepository

    async def __call__(self, login_form: Login) -> Token:
        password_hash = User.compute_password_hash(
            login_form.password.get_secret_value(),
            settings.SECRET_KEY.get_secret_value(),
        )
        user = await self.user_repository.find_user_using_credentials(
            login_form.username,
            password_hash,
        )
        payload = TokenPayload.from_user(user).dict()
        access_token = jwt.encode(
            payload,
            key=settings.SECRET_KEY.get_secret_value(),
        )
        token = Token(value=access_token, user_id=user.id)
        await self.token_repository.save_token(token)
        return token


@dataclass
class LogoutUseCase:
    token_repository: TokenRepository

    async def __call__(self, access_token: Token):
        if await self.token_repository.has_token(access_token):
            await self.token_repository.forget_token(access_token)


@dataclass
class ResetPasswordUseCase:
    user_repository: UserRepository
    token_repository: TokenRepository

    async def __call__(
        self, *, requester_id: int, user_id: int, new_password: Password
    ):
        # Password has changed... we must invite user to log-in again.
        hashed_password = User.compute_password_hash(
            new_password.password.get_secret_value(),
            settings.SECRET_KEY.get_secret_value(),
        )
        await self.user_repository.change_password_using_id(
            user_id, hashed_password
        )
        # forget target use not requester...
        # except if requester == user ¯\_(ツ)_/¯
        await self.token_repository.forget_user(user_id)


@dataclass
class IdentityChangeUseCase:
    user_repository: UserRepository

    async def __call__(self, user_id: int, new_identity: Identity) -> User:
        return await self.user_repository.rename_user_using_id(
            user_id, new_identity
        )


@dataclass
class ForgetUserUseCase:
    user_repository: UserRepository
    token_repository: TokenRepository

    async def __call__(self, user_id: int):
        user = await self.user_repository.find_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=NOT_FOUND)

        await self.user_repository.forget_user(user.id)
        await self.token_repository.forget_user(user.id)
