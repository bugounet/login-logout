# Token
from msio.logme.domain.entities import Token, User, UserRegistrationRequest

TESTING_TOKEN_SIGNATURE = "mysecretkey"
TESTING_VALID_TOKEN = (
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
    # payload {"user_id": 11}
    "eyJ1c2VyX2lkIjoxMX0."
    # signature = "mysecretkey" using HS256
    "8IS3kwaPqVUBccyzV_B2GeAzcVjqSXVOIN0ZuewI798"
    # "gs1A-nt7aQudYr_rS_eqSLXU8rLQ4NqVoiJi1ualTeQ"
)

TOKEN_WITHOUT_USER_ID_CLAIM = (
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
    # payload {"sub": 11}
    "eyJzdWIiOjExfQ."
    # signature = "mysecretkey" using HS256
    "QNAxFfmGgmH9LzD99UmzHz3aosLMqi01Kz7BG3eo3_0"
    # "WvzsDqFTKPDnB8QDexq0UZOqfNPKNaFq1EldQTWu-QI"
)

# User registration
TESTING_PASSWORD_VALUE = "Some ƒunn¥ P@$$WØRD"
# Secret key used at testing time is "mysecretkey"
TESTING_PASSWORD_HASH = (
    "ba57461419de5df7170abe265a6685401744d3812a1ca159b3ac9043ac03e10f"
)
# hash with secret key "secondsecret"
TESTING_PASSWORD_HASH_2 = (
    "5a5dc66cb6410cb6390c7fdd3ba0b298de37ce5e607b035f46952bd62b9129c0"
)


TESTING_USER = User(
    id=11,
    first_name="John",
    last_name="Doe",
    username="john-doe",
    email="john.doe@example.com",
)

TESTING_FIRST_USER_DEFINITION = UserRegistrationRequest(
    first_name="first_name",
    last_name="last_name",
    username="username",
    email="email",
    password="password",
)

TESTING_ACCESS_TOKEN = Token(
    value=TESTING_VALID_TOKEN,
    user_id=11,
)
