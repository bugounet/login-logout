from dataclasses import dataclass, field, InitVar
from hashlib import sha256

from msio.logme.core.config import settings


@dataclass(frozen=True, slots=True)
class User:
    id: int
    first_name: str
    last_name: str
    username: str
    email: str


@dataclass(slots=True)
class UserRegistration:
    first_name: str
    last_name: str
    username: str
    email: str
    password: InitVar[str]
    password_hash: str = field(init=False)

    def __post_init__(self, password):
        # I'm using app's secret to hash the password.
        # It's easy to use sha256 even though a
        # hashing method that is specifically designed for this
        # like Argon2 as recommended by the OWASP.
        # I'm not in production so again, let's use the easiest for
        # commodity
        concatenated_password = str(password) + str(settings.SECRET_KEY)
        self.password_hash = sha256(concatenated_password.encode('utf-8')).hexdigest()
