import pytest

from msio.logme.__main__ import load_fixtures


@pytest.mark.asyncio
async def test_fixtures_loading(testing_environment_variables):
    await load_fixtures()
