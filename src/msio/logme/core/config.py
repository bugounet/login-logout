from os import getenv
from typing import Any, Dict, Optional

from pydantic import (
    BaseSettings,
    EmailStr,
    PostgresDsn,
    SecretStr,
    validator,
)


class Settings(BaseSettings):
    # Store here values we want to keep configurable, even though
    # there is no actual way to customize them on the run.
    API_PAGES_SIZE = 20
    # default algorithm to use with JWTs.
    JWT_ALGORITHM = "HS256"

    PROJECT_NAME: str
    PG_NAME: str
    PG_HOST: str
    PG_USER: str
    PG_PASSWORD: SecretStr
    PG_URI: Optional[PostgresDsn] = None
    PG_CHECK_SAME_THREAD: bool

    @validator("PG_URI", pre=True)
    def validate_postgres_conn(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> str:
        if isinstance(v, str):
            return v
        password: SecretStr = values.get("PG_PASSWORD", SecretStr(""))
        return "{scheme}://{user}:{password}@{host}/{db}".format(
            scheme="postgresql+asyncpg",
            user=values.get("PG_USER"),
            password=password.get_secret_value(),
            host=values.get("PG_HOST"),
            db=values.get("PG_NAME"),
        )

    FIRST_USER_EMAIL: EmailStr
    FIRST_USER_PASSWORD: SecretStr

    SECRET_KEY: SecretStr
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    TESTING: bool = False


def load_config_from_env() -> Settings:
    config = Settings(
        PROJECT_NAME=getenv("MSIO_LOG_ME_PROJECT_NAME", default="LogMe"),
        PG_NAME=getenv("MSIO_LOG_ME_PG_DB", default="LogMe"),
        PG_HOST=getenv("MSIO_LOG_ME_PG_HOST", default="postgres"),
        PG_USER=getenv("MSIO_LOG_ME_PG_USER", default="root"),
        PG_PASSWORD=getenv("MSIO_LOG_ME_PG_PASSWORD", default="toor"),
        PG_CHECK_SAME_THREAD=getenv(
            "MSIO_LOG_ME_PG_CHECK_SAME_THREAD", default=True
        ),
        FIRST_USER_EMAIL=getenv(
            "MSIO_LOG_ME_USER_EMAIL", default="admin@corporation.com"
        ),
        FIRST_USER_PASSWORD=getenv(
            "MSIO_LOG_ME_USER_PASSWORD", default="IsASecr3t"
        ),
        SECRET_KEY=getenv("MSIO_LOG_ME_SECRET_KEY", default="mysecretkey"),
        ACCESS_TOKEN_EXPIRE_MINUTES=getenv(
            "MSIO_LOG_ME_ACCESS_TOKEN_EXPIRE_MINUTES", default=30
        ),
        TESTING=getenv("MSIO_LOG_ME_TESTING", default=False),
    )
    return config


settings = load_config_from_env()
