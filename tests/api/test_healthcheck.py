import asyncio

import pytest
from sqlalchemy.exc import InterfaceError

from msio.logme.api.health import health


@pytest.mark.asyncio
async def test_working_healthcheck(mocker):
    session = mocker.Mock()
    execute = asyncio.Future()
    execute.set_result(None)
    session.execute.return_value = execute

    response = await health(session)

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_db_lost_healthcheck(mocker):
    session = mocker.Mock()
    execute = asyncio.Future()
    execute.set_exception(InterfaceError("SELECT 1", "1", ""))
    session.execute.return_value = execute

    response = await health(session)

    assert response.status_code == 503
