from pydantic import EmailStr

from msio.logme.domain.entities import User, UserRegistration
from msio.logme.domain.repositories import UserRepository


class GetOrCreateFirstUser:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def __call__(self, first_user_definition: UserRegistration):
        found_user = await self.user_repository.find_user_by_email(email_address=EmailStr(first_user_definition.email))
        if not found_user:
            await self.user_repository.register_user(first_user_definition)

