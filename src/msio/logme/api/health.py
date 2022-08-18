import asyncio
import socket

from fastapi import APIRouter, Depends
from sqlalchemy.exc import InterfaceError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from msio.logme.api.dependencies import get_session

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", status_code=204)
async def health(session: AsyncSession = Depends(get_session)):
    """Service healthcheck."""
    try:
        await asyncio.wait_for(session.execute("SELECT 1"), timeout=1)
    except (asyncio.TimeoutError, socket.gaierror, InterfaceError):
        return Response(status_code=503)
    return Response(status_code=204)
