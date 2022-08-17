from fastapi import FastAPI
from msio.logme.core import config
from msio.logme.api import router


def create_application() -> FastAPI:
    configuration = config.load_config_file()
    application = FastAPI(title=configuration.PROJECT_NAME)
    application.include_router(router)
    return application


app = create_application()
