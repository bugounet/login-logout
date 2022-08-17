from fastapi import FastAPI
from msio.logme.core import config
from msio.logme.api import router
from msio.logme.fixtures import create_first_user

def create_application() -> FastAPI:
    configuration = config.load_config_file()
    application = FastAPI(title=configuration.PROJECT_NAME)
    application.include_router(router)
    return application


app = create_application()


@app.on_event("startup")
async def load_fixtures():
    configuration = config.load_config_file()
    await create_first_user(configuration)
