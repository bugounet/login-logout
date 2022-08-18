from abc import ABC, abstractmethod
from typing import List

from pydantic import EmailStr

from msio.logme.core.config import settings
from msio.logme.domain.entities import Token, User, UserRegistrationRequest


class UserRepository(ABC):
    """User repository is the interface we chose to
    interact with persistence layer when it comes to
    storing and retrieving user data.
    """

    @abstractmethod
    async def find_user_using_credentials(
        self, email: EmailStr, hashed_password: str
    ) -> User:
        """Validate user credentials as we're finding
        the user using his email address.

        :raises: InvalidCredentialsError if given credentials
        don't match any user.
        :raises: UnavailableRepositoryError when the repository
        can't access data.

        :param email: User email submitted on our service.
        :type email: EmailStr

        :param hashed_password: hashed password to verify
        :type hashed_password: str

        :return: User matching parameters
        :rtype: User
        """
        ...  # pragma: no cover

    @abstractmethod
    async def find_user_by_id(self, user_id: int) -> User:
        """Find a user using his unique identifier (id).

        :raises: UnavailableRepositoryError when the repository
        can't access data.

        :param user_id: ID is a positive integer.
        :type user_id: int

        :rtype: User | None
        :return: Found user or None
        """
        ...  # pragma: no cover

    @abstractmethod
    async def find_user_by_email(
        self, email_address: EmailStr
    ) -> User | None:
        """Find a user using his email address which must be unique
        in our project.

        :raises: UnavailableRepositoryError when the repository can't
        access data.

        :param email_address: email address of the user we're looking for.
        :type email_address: EmailStr

        :return: Found user or None if email missing
        :rtype: User | None
        """
        ...  # pragma: no cover

    @abstractmethod
    async def fetch_all_users(
        self, *, offset: int, limit: int = settings.API_PAGES_SIZE
    ) -> List[User]:
        """Get a list of all users.
        This query can return lots of Users, so you can paginate the result.

        :raises: UnavailableRepositoryError when the repository can't access
        data.

        :param offset: Number of lines to skip
        :type offset: int

        :param limit: Page size, i.e. max number of users to get in a row.
        :type limit: int

        :return: Found users list. Potentially empty if no users found.
        :rtype: List[User]
        """
        ...  # pragma: no cover

    @abstractmethod
    async def register_user(
        self, registration_request: UserRegistrationRequest
    ) -> User:
        """Whe a new user joins the platform, we'll save it to
        our data storage.

        :raises: UnavailableRepositoryError
        :raises: IdentityAlreadyInUse

        :param user: User registration request data
        :type user: UserRegistrationRequest

        :return: created user object without password
        :type: User
        """
        ...  # pragma: no cover

    @abstractmethod
    async def forget_user(self, user_id: int) -> None:
        """Forget user information based on his unique identifier.

        :raises: UnavailableRepositoryError
        :raises: UnkownUserError

        :param user_id: User identifier
        :type user_id: int
        """
        ...  # pragma: no cover


class TokenRepository(ABC):
    """Store tokens somewhere so that if user logs-out
    we can deny access to his tokens
    """

    @abstractmethod
    async def has_token(self, token: Token) -> bool:
        """Tell whether given token has been produced or not?

        we could think of exceptions here but I'm too tired to
        write more docstrings...

        :param token: Access token value
        :type token: Token

        :return: Existence
        :rtype: bool
        """
        ...  # pragma: no cover

    @abstractmethod
    async def save_token(self, token: Token) -> None:
        """Save a token we created so we can make sure it's still valid

        :param token: Access token value
        :type token: Token
        """
        ...  # pragma: no cover

    @abstractmethod
    async def forget_token(self, token: Token) -> None:
        """Forget a token so that it becomes invalid

        :param token: Access token value
        :type token: Token
        """
        ...  # pragma: no cover
