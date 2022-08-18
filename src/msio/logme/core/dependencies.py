from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from msio.logme.core.database import engine


@asynccontextmanager
async def use_database():
    """This context mananger implementation allows me to
    use the "with" syntax to get an active database session
    and be sure to close it at the end.

    Connection to the database can be slow, therefore
    we're making an async connection so that the server can
    still take new requests as we're waiting for the
    connection to be established.
    """
    db = AsyncSession(bind=engine)
    try:
        yield db
    finally:
        # in any case (crash or success) always close the session
        await db.close()


async def database_session():
    async with use_database() as session:
        yield session
