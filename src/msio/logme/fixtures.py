from msio.logme.core.config import Settings
from msio.logme.domain.entities import UserRegistrationRequest
from msio.logme.domain.repositories import UserRepository
from msio.logme.use_cases import GetOrCreateFirstUser


async def create_first_user(
    configuration: Settings, user_repository: UserRepository
):
    first_user_definition = UserRegistrationRequest(
        first_name="first",
        last_name="user",
        username="first-user",
        email=configuration.FIRST_USER_EMAIL,
        password=configuration.FIRST_USER_PASSWORD.get_secret_value(),
    )
    use_case = GetOrCreateFirstUser(user_repository)
    await use_case(first_user_definition)
