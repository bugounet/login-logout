# Waiting for python3.11 expected this year to be able to use
# Self in type hints... until then, use future annotations
from __future__ import annotations

from dataclasses import InitVar, dataclass, field

# I know domain should never import more than domain or system libs however
# rules are sometimes meant to be broken. Here I import jwt, hashlib
# and pydantic because it's the responsibility of our token to validate
# data and you can't validate data without these libs.
from hashlib import sha256

from jwt import PyJWTError, decode
from pydantic import ValidationError

from msio.logme.core.config import settings
from msio.logme.domain.exceptions import InvalidTokenError


@dataclass(frozen=True, slots=True)
class Token:
    value: str
    user_id: int

    @classmethod
    def parse_and_verify_token(cls, token: str, secret: str) -> Token:
        """Read raw token string to verify its signature AND decode it.
        If token is valid, this function returns a new TokenInstance.

        :raises: InvalidTokenError if token is invalid
        """
        try:
            payload = decode(
                token, secret, algorithms=[settings.JWT_ALGORITHM]
            )
        except (PyJWTError, ValidationError):
            raise InvalidTokenError("Token could not be deserialized")
        try:
            user_id = payload["user_id"]
        except KeyError:
            raise InvalidTokenError("Missing 'user_id' claim")
        return cls(value=token, user_id=user_id)


@dataclass(frozen=True, slots=True)
class User:
    id: int
    first_name: str
    last_name: str
    username: str
    email: str

    @staticmethod
    def compute_password_hash(password: str) -> str:
        # I'm using app's secret to hash the password.
        # It's easy to use sha256 even though a
        # hashing method that is specifically designed for this
        # like Argon2 as recommended by the OWASP.
        # I'm not in production so again, let's use the easiest for
        # commodity
        concatenated_password = password + str(
            settings.SECRET_KEY.get_secret_value()
        )
        return sha256(concatenated_password.encode("utf-8")).hexdigest()


@dataclass(slots=True)
class UserRegistrationRequest:
    first_name: str
    last_name: str
    username: str
    email: str
    password: InitVar[str]
    password_hash: str = field(init=False)

    def __post_init__(self, password: str):
        self.password_hash = User.compute_password_hash(password)
