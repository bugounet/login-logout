from msio.logme.domain.entities import User as UserEntity
from msio.logme.models.users import User as ORMUser

TESTING_ORM_USER = ORMUser(
    id=11,
    firstname="John",
    lastname="Doe",
    username="john-doe",
    email="john.doe@example.com",
    password="password",
)

TESTING_USER = UserEntity(
    id=11,
    first_name="John",
    last_name="Doe",
    username="john-doe",
    email="john.doe@example.com",
)
