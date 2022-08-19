import pytest

from msio.logme.domain.entities import Token, User, UserRegistrationRequest
from msio.logme.domain.exceptions import (
    InvalidRegistrationRequestError,
    InvalidTokenError,
)
from tests.testing_datasets import (
    TESTING_PASSWORD_HASH,
    TESTING_PASSWORD_HASH_2,
    TESTING_PASSWORD_VALUE,
    TESTING_TOKEN_SIGNATURE,
    TESTING_VALID_TOKEN,
    TOKEN_WITHOUT_USER_ID_CLAIM,
)


class TestToken:
    def test_parsing_a_malformed_token(self):
        with pytest.raises(InvalidTokenError):
            Token.parse_and_verify_token("bad data", "secret")
        with pytest.raises(InvalidTokenError):
            Token.parse_and_verify_token("bad.data.encoding", "secret")

    def test_parsing_a_valid_token(self):
        token = Token.parse_and_verify_token(
            TESTING_VALID_TOKEN, TESTING_TOKEN_SIGNATURE
        )

        assert token.user_id == 11
        assert token.value == TESTING_VALID_TOKEN

    def test_parsing_a_token_with_wrong_claims(self):
        with pytest.raises(InvalidTokenError):
            Token.parse_and_verify_token(
                TOKEN_WITHOUT_USER_ID_CLAIM, TESTING_TOKEN_SIGNATURE
            )

    def test_providing_invalid_signature(self):
        # function signature doesn't support bytes so it must fail
        with pytest.raises(InvalidTokenError):
            Token.parse_and_verify_token(
                TESTING_VALID_TOKEN, TESTING_TOKEN_SIGNATURE + "oops"
            )

    def test_create_a_token(self):
        with pytest.raises(InvalidTokenError):
            Token(value="raw data", user_id=-1)


class TestUser:
    @pytest.mark.parametrize(
        "password,secret,expected_hash",
        [
            (TESTING_PASSWORD_VALUE, "mysecretkey", TESTING_PASSWORD_HASH),
            (
                TESTING_PASSWORD_VALUE,
                "secondsecret",
                TESTING_PASSWORD_HASH_2,
            ),
        ],
    )
    def test_hash_generation(self, password, secret, expected_hash):
        assert (
            User.compute_password_hash(password=password, secret=secret)
            == expected_hash
        )


class TestUserRegistrationRequest:
    def test_valid_registration(self, mocker):
        registration_request = UserRegistrationRequest(
            first_name="John",
            last_name="Doe",
            username="john-doe",
            email="john.doe@example.com",
            password=TESTING_PASSWORD_VALUE,
        )

        assert (
            registration_request.password_hash == TESTING_PASSWORD_HASH
        ), "Either testing secret key changed, or hashing algorithm is broken"

    @pytest.mark.parametrize(
        "first_name,last_name,username,expected_error_message",
        [
            (
                "John" * 50,
                "Doe",
                "john-doe",
                "First name cannot exceed 50 chars",
            ),
            (
                "John",
                "Doe" * 50,
                "john-doe",
                "Last name cannot exceed 50 chars",
            ),
            (
                "John",
                "Doe",
                "john-doe" * 50,
                "Chosen username cannot exceed 50 chars",
            ),
        ],
    )
    def test_registration_validation(
        self, first_name, last_name, username, expected_error_message
    ):

        with pytest.raises(
            InvalidRegistrationRequestError
        ) as picked_error:
            UserRegistrationRequest(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email="john.doe@example.com",
                password=TESTING_PASSWORD_VALUE,
            )

        assert str(picked_error.value) == expected_error_message
