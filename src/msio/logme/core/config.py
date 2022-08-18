from os import getenv, path
from typing import Any, Dict, Optional

import yaml
from pydantic import (
    BaseSettings,
    EmailStr,
    PostgresDsn,
    SecretStr,
    validator,
)

from msio.logme.core.constants import CONFIG_FILE


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

    REDIS_HOST: str
    REDIS_PORT: int


# FIXME: use pydantic.Field(...,env=...)
def load_config_from_file() -> Settings:
    config = None
    with open(CONFIG_FILE, "r") as f:
        data = yaml.safe_load(f)
        config = Settings(
            PROJECT_NAME=data.get(
                "MSIO_LOG_ME_PROJECT_NAME", default="LogMe"
            ),
            PG_NAME=data.get("MSIO_LOG_ME_PG_DB", default="LogMe"),
            PG_HOST=data.get("MSIO_LOG_ME_PG_HOST", default="localhost"),
            PG_USER=data.get("MSIO_LOG_ME_PG_USER", default="root"),
            PG_PASSWORD=data.get(
                "MSIO_LOG_ME_PG_PASSWORD", default="toor"
            ),
            PG_CHECK_SAME_THREAD=data.get(
                "MSIO_LOG_ME_PG_CHECK_SAME_THREAD", default=True
            ),
            FIRST_USER_EMAIL=data.get(
                "MSIO_LOG_ME_USER_EMAIL", default="admin@corporation.com"
            ),
            FIRST_USER_PASSWORD=data.get(
                "MSIO_LOG_ME_USER_PASSWORD", default="IsASecr3t"
            ),
            SECRET_KEY=data.get(
                "MSIO_LOG_ME_SECRET_KEY", default="mysecretkey"
            ),
            ACCESS_TOKEN_EXPIRE_MINUTES=data.get(
                "MSIO_LOG_ME_ACCESS_TOKEN_EXPIRE_MINUTES", default=30
            ),
            REDIS_HOST=data.get(
                "MSIO_LOG_ME_REDIS_HOST", default="localhost"
            ),
            REDIS_PORT=data.get("MSIO_LOG_ME_REDIS_PORT", default=6380),
        )
    return config


# FIXME: use pydantic.Field(...,env=...)
def load_config_file_from_env() -> Settings:
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
        REDIS_HOST=getenv("MSIO_LOG_ME_REDIS_HOST", default="localhost"),
        REDIS_PORT=getenv("MSIO_LOG_ME_REDIS_PORT", default=6380),
    )
    return config


def load_config_file() -> Settings:
    config = None
    if path.exists(CONFIG_FILE):
        config = load_config_from_file()
    else:
        config = load_config_file_from_env()
    return config


settings = load_config_file()
