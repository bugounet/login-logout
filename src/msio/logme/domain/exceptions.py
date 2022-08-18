class IdentityAlreadyInUse(Exception):
    """This exception is raised whenever user is trying to
    register a new user while his email address id already in use.
    """

    pass


class UnavailableRepositoryError(Exception):
    """This exception is raised when database is unavailable
    so that the API can handle it and return a 503 error or whatever
    you'll expect to tell the user to retry later.
    """

    pass


class UnknownUserError(Exception):
    """We didn't find user with given email/id"""

    pass


class InvalidCredentialsError(Exception):
    """Invalid passowrd given"""

    pass


class InvalidTokenError(Exception):
    """Raised when the given token is not a JWT or is missing
    Essential claims
    """

    pass
