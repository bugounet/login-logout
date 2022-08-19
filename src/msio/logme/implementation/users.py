import socket
from typing import List

from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from msio.logme.core.config import settings
from msio.logme.domain.entities import User as UserEntity
from msio.logme.domain.entities import UserRegistrationRequest
from msio.logme.domain.exceptions import (
    IdentityAlreadyInUse,
    InvalidCredentialsError,
    UnavailableRepositoryError,
)
from msio.logme.domain.repositories import UserRepository
from msio.logme.domain.schemas import Identity
from msio.logme.models.users import User as ORMUser


def orm_user_adapter(database_user_model: ORMUser) -> UserEntity:
    if not database_user_model:
        return None
    # adapters in clean architecture or hex architecture are dump
    # pieces of software passing data from an application layer to another
    return UserEntity(
        id=database_user_model.id,
        first_name=database_user_model.firstname,
        last_name=database_user_model.lastname,
        username=database_user_model.username,
        email=database_user_model.email,
    )


class PostgresUserRepository(UserRepository):
    """This AsyncIO based repository will implement postgresql
    interactions with the API by following interface defined by the
    UserRepository interface.
    """

    def __init__(self, database_session: AsyncSession):
        self.database_session = database_session

    async def _fetch_data(self, lookup):
        try:
            return await self.database_session.execute(lookup)
        except socket.gaierror:
            raise UnavailableRepositoryError()

    async def find_user_using_credentials(
        self, email: EmailStr, hashed_password: str
    ) -> UserEntity:
        lookup = select(ORMUser).filter(
            ORMUser.email == email, ORMUser.password == hashed_password
        )
        result = await self._fetch_data(lookup)
        db_user = result.scalars().first()
        if not db_user:
            raise InvalidCredentialsError()
        return orm_user_adapter(db_user)

    async def find_user_by_id(self, user_id: int) -> UserEntity | None:
        lookup = select(ORMUser).filter(ORMUser.id == user_id)
        result = await self._fetch_data(lookup)
        db_user = result.scalars().first()
        return orm_user_adapter(db_user)

    async def find_user_by_email(
        self, email_address: EmailStr
    ) -> UserEntity | None:
        lookup = select(ORMUser).filter(
            ORMUser.email == str(email_address)
        )
        result = await self._fetch_data(lookup)
        db_user = result.scalars().first()
        return orm_user_adapter(db_user)

    async def fetch_all_users(
        self, *, offset: int, limit: int = settings.API_PAGES_SIZE
    ) -> List[UserEntity]:
        lookup = select(ORMUser).offset(offset).limit(limit)
        users = await self._fetch_data(lookup)
        return list(map(orm_user_adapter, users.scalars()))

    async def register_user(
        self, registration_request: UserRegistrationRequest
    ) -> UserEntity:
        # create user in database
        db_user = ORMUser(
            firstname=registration_request.first_name,
            lastname=registration_request.last_name,
            username=registration_request.username,
            email=registration_request.email,
            password=registration_request.password_hash,
        )
        self.database_session.add(db_user)

        try:
            await self.database_session.commit()
        except socket.gaierror:
            raise UnavailableRepositoryError()
        except IntegrityError:
            raise IdentityAlreadyInUse()

        # the refresh method allows us to get the ID back from DB's call
        await self.database_session.refresh(db_user)
        # convert ORM data to domain entity User
        return orm_user_adapter(db_user)

    async def forget_user(self, user_id: int) -> None:
        def delete_user(session: Session):
            """Synchronous update method that is
            called using run_sync.
            """
            session.query(ORMUser).filter(ORMUser.id == user_id).delete()

        try:
            await self.database_session.run_sync(delete_user)
            await self.database_session.commit()
        except socket.gaierror:
            raise UnavailableRepositoryError()

    async def rename_user_using_id(
        self, user_id: int, identity: Identity
    ) -> UserEntity:
        def update_identities(session: Session):
            """Synchronous update method that is
            called using run_sync.
            """

            update_dict = {}
            if identity.first_name:
                update_dict[ORMUser.firstname] = identity.first_name
            if identity.last_name:
                update_dict[ORMUser.lastname] = identity.last_name
            if identity.username:
                update_dict[ORMUser.username] = identity.username
            session.query(ORMUser).filter(ORMUser.id == user_id).update(
                update_dict
            )

        try:
            await self.database_session.run_sync(update_identities)
            await self.database_session.commit()
        except socket.gaierror:
            raise UnavailableRepositoryError()

        return await self.find_user_by_id(user_id)

    async def change_password_using_id(
        self, user_id: int, hashed_password: str
    ) -> None:
        def update_password(session: Session):
            """Synchronous update method that is
            called using run_sync.
            """
            session.query(ORMUser).filter(ORMUser.id == user_id).update(
                {ORMUser.password: hashed_password}
            )

        try:
            await self.database_session.run_sync(update_password)
            await self.database_session.commit()
        except socket.gaierror:
            raise UnavailableRepositoryError()

        return await self.find_user_by_id(user_id)
