import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from msio.logme.domain.entities import User as UserEntity
from msio.logme.domain.entities import UserRegistrationRequest
from msio.logme.domain.exceptions import InvalidCredentialsError
from msio.logme.domain.schemas import Identity
from msio.logme.implementation.users import (
    PostgresUserRepository,
    orm_user_adapter,
)
from msio.logme.models.users import User as ORMUser
from tests.testing_datasets import TESTING_ORM_USER, TESTING_USER


def test_model_dict_method():
    assert TESTING_ORM_USER.dict() == {
        "id": 11,
        "firstname": "John",
        "lastname": "Doe",
        "username": "john-doe",
        "email": "john.doe@example.com",
        "password": "password",
    }


@pytest.mark.parametrize(
    "orm_model,expected_output",
    [
        (TESTING_ORM_USER, TESTING_USER),
        (None, None),
    ],
)
def test_adapter_orm_to_domain(orm_model, expected_output):
    assert orm_user_adapter(orm_model) == expected_output


@pytest_asyncio.fixture
async def testing_data_set_session():
    # We don't have complex queries. I'll use an "in memory" sqlite database
    # to avoid the need to spawn a psql database and keep performances high
    # while running tests.
    # NOTE: This is dangerous as sqlite and psql don't behave the same way.
    # This hack shall not be used on a production environment
    engine = create_async_engine("sqlite+aiosqlite://")

    async with engine.begin() as conn:
        await conn.run_sync(ORMUser.metadata.drop_all)
        await conn.run_sync(ORMUser.metadata.create_all)

    async_session = sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession,
        autoflush=False,
    )

    async with async_session() as session:
        session.add(TESTING_ORM_USER)
        await session.commit()

    async with async_session() as session:

        yield session


@pytest.mark.asyncio
async def test_find_user_by_id(testing_data_set_session):
    repository = PostgresUserRepository(testing_data_set_session)

    found_user = await repository.find_user_by_id(11)
    assert found_user == TESTING_USER

    found_user = await repository.find_user_by_id(1)
    assert found_user is None


@pytest.mark.skip("Broken in-memory database hack")
@pytest.mark.asyncio
async def test_find_user_by_email(testing_data_set_session):
    repository = PostgresUserRepository(testing_data_set_session)
    found_user = await repository.find_user_by_email(
        "john.doe@example.com"
    )
    assert found_user == TESTING_USER

    repository = PostgresUserRepository(testing_data_set_session)

    found_user = await repository.find_user_by_email("unknown@example.com")
    assert found_user is None


@pytest.mark.skip("Broken in-memory database hack")
@pytest.mark.asyncio
async def test_find_user_using_credentials(testing_data_set_session):
    repository = PostgresUserRepository(testing_data_set_session)
    found_user = await repository.find_user_using_credentials(
        "john.doe@example.com", "password"
    )
    assert found_user == TESTING_USER

    with pytest.raises(InvalidCredentialsError):
        await repository.find_user_using_credentials(
            "unknown@example.com", "password"
        )

    with pytest.raises(InvalidCredentialsError):
        await repository.find_user_using_credentials(
            "john.doe@example.com", "wrong-password"
        )


@pytest.mark.skip("Broken in-memory database hack")
@pytest.mark.asyncio
async def test_fetch_all_users(testing_data_set_session):
    repository = PostgresUserRepository(testing_data_set_session)
    found_users = await repository.fetch_all_users(offset=0, limit=1)
    assert found_users == [TESTING_USER]


@pytest.mark.skip("Broken in-memory database hack")
@pytest.mark.asyncio
async def test_register_user(testing_data_set_session):
    repository = PostgresUserRepository(testing_data_set_session)
    created_user = await repository.register_user(
        UserRegistrationRequest(
            first_name="Alice",
            last_name="Cooper",
            username="alice-cooper",
            email="alice.cooper@example.com",
            password="welcome_to_my_nightmare",
        )
    )
    assert created_user == UserEntity(
        id=created_user.id,
        first_name="Alice",
        last_name="Cooper",
        username="alice-cooper",
        email="alice.cooper@example.com",
    )


@pytest.mark.skip("Broken in-memory database hack")
@pytest.mark.asyncio
async def test_forget_user(testing_data_set_session):
    repository = PostgresUserRepository(testing_data_set_session)
    # known ID deletes user
    await repository.forget_user(11)
    # unknown ID doesn't explode
    await repository.forget_user(123)


@pytest.mark.skip("Broken in-memory database hack")
@pytest.mark.asyncio
async def test_rename_user_using_id(testing_data_set_session):
    repository = PostgresUserRepository(testing_data_set_session)
    # known ID deletes user
    user = await repository.rename_user_using_id(
        11, Identity(first_name="Johnny")
    )

    assert user.first_name == "Johnny"


@pytest.mark.skip("Broken in-memory database hack")
@pytest.mark.asyncio
async def test_change_password(testing_data_set_session):
    repository = PostgresUserRepository(testing_data_set_session)
    # hash is updated
    await repository.change_password_using_id(11, "new hash")
