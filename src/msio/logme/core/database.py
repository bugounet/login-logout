from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from importlib.resources import read_text
from msio.logme.core import config

engine = create_async_engine(config.settings.DB_HOST)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

