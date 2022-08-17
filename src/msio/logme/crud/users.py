from abc import abstractmethod, ABC
from hashlib import sha256
from typing import List

from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from msio.logme.domain.entities import User as UserEntity, UserRegistration
from msio.logme.domain.exceptions import IdentityAlreadyInUse
from msio.logme.domain.repositories import UserRepository

from msio.logme.models.users import User as ORMUser
from msio.logme.core.config import settings


def orm_user_adapter(database_user_model: ORMUser) -> UserEntity:
    # adapters in clean architecture or hex architecture are dump
    # pieces of software passing data from an application layer to another
    return UserEntity(
        id=database_user_model.id,
        first_name=database_user_model.firstname,
        last_name=database_user_model.lastname,
        username=database_user_model.username,
        email=database_user_model.email,
    )


class PostgresRepository(UserRepository):
    """ This AsyncIO based repository will implement postgresql
    interactions with the API by following interface defined by the
    UserRepository interface.
    """
    def __init__(self, database_session: AsyncSession):
        self.database_session = database_session

    async def find_user_by_id(self, user_id: int) -> UserEntity | None:
        lookup = select(ORMUser).filter(ORMUser.id == user_id)
        result = await self.database_session.execute(lookup)
        return result.scalars().first()

    async def find_user_by_email(self, email_address: EmailStr) -> UserEntity | None:
        lookup = select(ORMUser).filter(ORMUser.email == str(email_address))
        result = await self.database_session.execute(lookup)
        return result.scalars().first()

    async def fetch_all_users(self, *, offset: int, limit: int = settings.API_PAGES_SIZE) -> List[UserEntity]:
        lookup = select(ORMUser).offset(offset).limit(limit)
        users = await self.database_session.execute(lookup)
        return map(orm_user_adapter, users.scalars())

    async def register_user(self, user_registration: UserRegistration) -> UserEntity:
        # create user in database
        db_user = ORMUser(
            firstname=user_registration.first_name,
            lastname=user_registration.last_name,
            username=user_registration.username,
            email=user_registration.email,
            password=user_registration.password_hash,
        )
        self.database_session.add(db_user)

        try:
            await self.database_session.commit()
        except IntegrityError:
            raise IdentityAlreadyInUse()

        # the refresh method allows us to get the ID back from DB's call
        await self.database_session.refresh(db_user)
        # convert ORM data to domain entity User
        return orm_user_adapter(db_user)

    async def forget_user(self, user_id: int) -> None:
        pass
