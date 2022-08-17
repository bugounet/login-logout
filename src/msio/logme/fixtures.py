from sqlalchemy.ext.asyncio import AsyncSession

from msio.logme.core.config import Settings
from msio.logme.core.database import engine
from msio.logme.crud.users import PostgresRepository
from msio.logme.domain.entities import UserRegistration
from msio.logme.domain.use_cases import GetOrCreateFirstUser


async def create_first_user(configuration: Settings):
    session = AsyncSession(bind=engine)
    try:
        first_user_definition = UserRegistration(
            first_name="first",
            last_name="user",
            username="first-user",
            email=configuration.FIRST_USER_EMAIL,
            password=str(configuration.FIRST_USER_PASSWORD),
        )
        use_case = GetOrCreateFirstUser(PostgresRepository(session))
        await use_case(first_user_definition)
    finally:
        # in any case (crash or success) always close the session
        await session.close()
