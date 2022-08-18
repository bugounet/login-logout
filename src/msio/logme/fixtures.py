from sqlalchemy.ext.asyncio import AsyncSession

from msio.logme.core.config import Settings
from msio.logme.core.database import engine
from msio.logme.crud.users import PostgresUserRepository
from msio.logme.domain.entities import UserRegistrationRequest
from msio.logme.domain.use_cases import GetOrCreateFirstUser


async def create_first_user(configuration: Settings):
    session = AsyncSession(bind=engine)
    try:
        first_user_definition = UserRegistrationRequest(
            first_name="first",
            last_name="user",
            username="first-user",
            email=configuration.FIRST_USER_EMAIL,
            password=configuration.FIRST_USER_PASSWORD.get_secret_value(),
        )
        use_case = GetOrCreateFirstUser(PostgresUserRepository(session))
        await use_case(first_user_definition)
    finally:
        # in any case (crash or success) always close the session
        await session.close()
