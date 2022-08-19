import pytest
from fastapi import HTTPException

from msio.logme.api.dependencies import (
    get_current_user,
    get_token_payload,
    verify_token,
)
from msio.logme.implementation.tokens import ThreadMemoryTokenRepository
from msio.logme.schemas.token import TokenPayload
from tests.domain.testing_repositories import TestingUserRepository
from tests.testing_datasets import TESTING_USER, TESTING_VALID_TOKEN


@pytest.mark.asyncio
async def test_get_current_user():
    # if you can get the user, return it.
    repo = TestingUserRepository(lookup_success=True)
    user = await get_current_user(repo, TokenPayload(user_id=1))
    assert user == TESTING_USER

    # if user doesn't exist, return a 404 (Not found)
    with pytest.raises(HTTPException) as raised_error:
        repo = TestingUserRepository(lookup_success=False)
        await get_current_user(repo, TokenPayload(user_id=1))
    assert raised_error.value.status_code == 404

    # if db is down, tell about it with a 503 (Temporarily down)
    with pytest.raises(HTTPException) as raised_error:
        repo = TestingUserRepository(db_down=True)
        await get_current_user(repo, TokenPayload(user_id=1))
    assert raised_error.value.status_code == 503


@pytest.mark.asyncio
async def test_get_token_payload():
    payload = await get_token_payload(TESTING_VALID_TOKEN)
    assert payload == TokenPayload(user_id=11)
    with pytest.raises(HTTPException):
        await get_token_payload("toto.tutu.titi")


@pytest.mark.asyncio
async def test_verify_token():
    repo = ThreadMemoryTokenRepository({})
    with pytest.raises(HTTPException):
        await verify_token(TESTING_VALID_TOKEN, repo)

    repo = ThreadMemoryTokenRepository({TESTING_VALID_TOKEN: 11})
    token_payload = await verify_token(TESTING_VALID_TOKEN, repo)
    assert token_payload == TokenPayload(user_id=11)
