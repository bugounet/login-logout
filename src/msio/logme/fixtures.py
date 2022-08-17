from msio.logme.models.users import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from msio.logme.core.config import Settings
from msio.logme.core.database import engine

async def create_first_user(configuration: Settings):
    session = AsyncSession(bind=engine)
    user = User(
        firstname="first",
        lastname="user",
        username="alpha",
        email=configuration.FIRST_USER_EMAIL,
        password=str(configuration.FIRST_USER_PASSWORD)
    )
    session.add(user)
    await session.commit()
    await session.close()
