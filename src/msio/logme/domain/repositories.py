from abc import abstractmethod, ABC
from typing import List

from pydantic import EmailStr
from msio.logme.domain.entities import User
from msio.logme.schemas.users import UserRegistration
from msio.logme.core.config import settings


class UserRepository(ABC):
    @abstractmethod
    async def find_user_by_id(self, user_id: int) -> User:
        """ Find a user using his unique identifier (id).

        :raises: UnavailableRepositoryError when the repository can't access data.

        :param user_id: ID is a positive integer.
        :type user_id: int

        :rtype: User | None
        :return: Found user or None
        """
        ...

    @abstractmethod
    async def find_user_by_email(self, email_address: EmailStr) -> User | None:
        """ Find a user using his email address which must be unique
        in our project.

        :raises: UnavailableRepositoryError when the repository can't access data.

        :param email_address: email address of the user we're looking for.
        :type email_address: EmailStr

        :return: Found user or None if email missing
        :rtype: User | None
        """
        ...

    @abstractmethod
    async def fetch_all_users(self, *, offset: int, limit: int = settings.API_PAGES_SIZE) -> List[User]:
        """ Get a list of all users.
        This query can return lots of Users, so you can paginate the result.

        :raises: UnavailableRepositoryError when the repository can't access data.

        :param offset: Number of lines to skip
        :type offset: int

        :param limit: Page size, i.e. max number of users to get in a row.
        :type limit: int

        :return: Found users list. Potentially empty if no users found.
        :rtype: List[User]
        """
        ...

    @abstractmethod
    async def register_user(self, user: UserRegistration) -> User:
        """ Whe a new user joins the platform, we'll save it to
        our data storage.

        :raises: UnavailableRepositoryError
        :raises: IdentityAlreadyInUse

        :param user: User registration data
        :type user: UserRegistration

        :return: created user object without password
        :type: User
        """
        ...

    @abstractmethod
    async def forget_user(self, user_id: int) -> None:
        """ Forget user information based on his unique identifier.

        :raises: UnavailableRepositoryError
        :raises: UnkownUserError

        :param user_id: User identifier
        :type user_id: int
        """
        ...
