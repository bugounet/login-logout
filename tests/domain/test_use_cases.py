import pytest

from msio.logme.domain.exceptions import (
    InvalidCredentialsError,
    UnavailableRepositoryError,
)
from msio.logme.domain.schemas import Login
from msio.logme.use_cases import (
    GetOrCreateFirstUser,
    LoginUseCase,
    LogoutUseCase,
)
from tests.domain.testing_repositories import (
    TestingTokenRepository,
    TestingUserRepository,
)
from tests.testing_datasets import (
    TESTING_ACCESS_TOKEN,
    TESTING_FIRST_USER_DEFINITION,
    TESTING_VALID_TOKEN,
)


class TestGetOrCreateFirstUser:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "lookup_success,create_success,db_down,fixture_state",
        [
            # User found (no matter creation state)
            # - expected: fixture state OK
            (True, False, False, True),
            # User not found, creation OK
            # - expected: user created and fixture state OK
            (False, True, False, True),
            # No DB
            # - expected: Fixture state invalid
            (False, False, True, False),
            # Invalid case: User found but creation would work
            # too (True, True, False, True)
            ##
            # Invalid case: User not found, creation failed,
            # but fixture sate OK (False, False, False, True)
            ##
            # Invalid case: User DB unreachable but fixture state
            # OK (False, False, True, True),
        ],
    )
    async def test_use_case_call(
        self, lookup_success, create_success, db_down, fixture_state
    ):
        repository = TestingUserRepository(
            lookup_success=lookup_success,
            create_success=create_success,
            db_down=db_down,
        )
        use_case_output = await GetOrCreateFirstUser(repository)(
            TESTING_FIRST_USER_DEFINITION
        )
        assert use_case_output == fixture_state


class TestLoginUseCase:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "lookup_success,db_down,expected_error",
        [
            # User not found, creation OK - expected: Login error
            (False, False, InvalidCredentialsError),
            # No DB - expected: login error
            (False, True, UnavailableRepositoryError),
        ],
    )
    async def test_failre_use_case_call(
        self, lookup_success, db_down, expected_error
    ):
        repository = TestingUserRepository(
            lookup_success=lookup_success, db_down=db_down
        )
        login_parameters = Login(
            username="john.doe@example.com", password="password"
        )

        with pytest.raises(expected_error):
            await LoginUseCase(repository, TestingTokenRepository())(
                login_parameters
            )

    @pytest.mark.asyncio
    async def test_success_use_case_call(self):
        # User found (no matter creation state) - expected: Login success
        repository = TestingUserRepository(
            lookup_success=True, db_down=False
        )
        login_parameters = Login(
            username="john.doe@example.com", password="password"
        )

        access_token = await LoginUseCase(
            repository, TestingTokenRepository()
        )(login_parameters)

        # thanks to dataclasses this check is valid
        assert access_token == TESTING_ACCESS_TOKEN


class TestLogoutUseCase:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "known_tokens,logging_out_token",
        [
            # unknown token: just say nothing and let it go
            ({"abc": 12}, TESTING_ACCESS_TOKEN),
            # known token: drop the token
            ({"abc": 12, TESTING_VALID_TOKEN: 11}, TESTING_ACCESS_TOKEN),
        ],
    )
    async def test_use_case_call(self, known_tokens, logging_out_token):
        token_repository = TestingTokenRepository(known_tokens)
        await LogoutUseCase(token_repository)(logging_out_token)

        assert token_repository.cache == {"abc": 12}
