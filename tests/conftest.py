import pytest

TESTING_ENVIRONMENT_VARIABLES = {
    "MSIO_LOG_ME_PROJECT_NAME": "MatasLogMe",
    "MSIO_LOG_ME_PG_DB": "LogMe",
    "MSIO_LOG_ME_PG_HOST": "pg",
    "MSIO_LOG_ME_PG_USER": "pguser",
    "MSIO_LOG_ME_PG_PASSWORD": "pgpwd",
    "MSIO_LOG_ME_PG_CHECK_SAME_THREAD": True,
    "MSIO_LOG_ME_USER_EMAIL": "john.doe@example.com",
    "MSIO_LOG_ME_USER_PASSWORD": "toto1234",
    "MSIO_LOG_ME_SECRET_KEY": "mysecretkey",
    "MSIO_LOG_ME_ACCESS_TOKEN_EXPIRE_MINUTES": "60",
}


@pytest.fixture
def testing_environment_variables(monkeypatch):
    # api image required env variables
    for variable_name, value in TESTING_ENVIRONMENT_VARIABLES.items():
        monkeypatch.setenv(variable_name, value)


@pytest.fixture
def SECRET_secret_key(monkeypatch):
    monkeypatch.setenv("MSIO_LOG_LE_SECRET_KEY", "SECRET!")
