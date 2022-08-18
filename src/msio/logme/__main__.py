from fastapi import FastAPI

from msio.logme.api import router
from msio.logme.core import config
from msio.logme.core.dependencies import use_database
from msio.logme.fixtures import create_first_user
from msio.logme.implementation.users import PostgresUserRepository


def create_application() -> FastAPI:
    configuration = config.load_config_file()
    application = FastAPI(title=configuration.PROJECT_NAME)
    application.include_router(router)
    return application


app = create_application()


@app.on_event("startup")
async def load_fixtures():
    configuration = config.load_config_file()
    async with use_database() as database_session:
        user_repository = PostgresUserRepository(database_session)
        await create_first_user(configuration, user_repository)
