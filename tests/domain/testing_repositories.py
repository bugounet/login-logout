from typing import Dict, List

from msio.logme.domain.entities import User
from msio.logme.domain.exceptions import (
    IdentityAlreadyInUse,
    InvalidCredentialsError,
    NonExistentUser,
    UnavailableRepositoryError,
)
from msio.logme.domain.repositories import UserRepository
from msio.logme.implementation.tokens import ThreadMemoryTokenRepository
from tests.testing_datasets import TESTING_USER


class TestingUserRepository(UserRepository):
    def __init__(
        self, *, lookup_success=False, create_success=False, db_down=False
    ):
        self.db_down = db_down
        self.lookup_success = lookup_success
        self.create_success = create_success

    async def find_user_using_credentials(
        self, email, hashed_password
    ) -> User:
        if self.db_down:
            raise UnavailableRepositoryError()
        if self.lookup_success:
            return TESTING_USER
        else:
            raise InvalidCredentialsError()

    async def find_user_by_id(self, user_id: int) -> User:
        if self.db_down:
            raise UnavailableRepositoryError()
        if self.lookup_success:
            return TESTING_USER
        else:
            return None

    async def find_user_by_email(self, email_address) -> User:
        if self.db_down:
            raise UnavailableRepositoryError()
        if self.lookup_success:
            return TESTING_USER
        else:
            return None

    async def fetch_all_users(self, offset, limit) -> List[User]:
        if self.db_down:
            raise UnavailableRepositoryError()
        if self.lookup_success:
            return [TESTING_USER]
        else:
            return []

    async def register_user(self, registration_request) -> User:
        if self.db_down:
            raise UnavailableRepositoryError()
        if self.create_success:
            return TESTING_USER
        else:
            raise IdentityAlreadyInUse()

    async def forget_user(self, user_id: int) -> None:
        if self.db_down:
            raise UnavailableRepositoryError()
        if self.lookup_success:
            return TESTING_USER
        else:
            raise NonExistentUser()


# The "ThreadMemory" repository doesn't need network or anything so I'll
# use if to test my use cases
class TestingTokenRepository(ThreadMemoryTokenRepository):
    def __init__(self, known_tokens: Dict[str, int] = None):
        super().__init__(cache=known_tokens or {})
