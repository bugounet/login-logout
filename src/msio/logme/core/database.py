from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from msio.logme.core import config

engine = create_async_engine(config.settings.PG_URI)
SessionLocal = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)
