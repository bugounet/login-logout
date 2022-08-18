from os import environ

import pytest
from pydantic import ValidationError

from msio.logme.core.config import Settings, load_config_from_env


@pytest.mark.parametrize("project_name", ("my_backend", "logme"))
def test_load_config_from_env(project_name):
    environ["MSIO_LOG_ME_PROJECT_NAME"] = project_name
    config = load_config_from_env()
    assert config.PROJECT_NAME is not None
    assert config.PROJECT_NAME == project_name


def test_pg_uri_validation():
    Settings(
        PROJECT_NAME="MatasLogMe",
        PG_NAME="LogMe",
        PG_HOST="pg",
        PG_USER="pguser",
        PG_PASSWORD="pgpwd",
        PG_CHECK_SAME_THREAD=True,
        PG_URI="postgres://pguser:pgpwd@pg:5432/LogMe",
        FIRST_USER_EMAIL="john.doe@example.com",
        FIRST_USER_PASSWORD="toto1234",
        SECRET_KEY="mysecretkey",
        ACCESS_TOKEN_EXPIRE_MINUTES="60",
    )
    with pytest.raises(ValidationError):
        Settings(
            PROJECT_NAME="MatasLogMe",
            PG_NAME="LogMe",
            PG_HOST="pg",
            PG_USER="pguser",
            PG_PASSWORD="pgpwd",
            PG_CHECK_SAME_THREAD=True,
            PG_URI="psql://pguser:pgpwd@pg:5432/LogMe",
            FIRST_USER_EMAIL="john.doe@example.com",
            FIRST_USER_PASSWORD="toto1234",
            SECRET_KEY="mysecretkey",
            ACCESS_TOKEN_EXPIRE_MINUTES="60",
        )
