from fastapi import FastAPI
from msio.logme.core import config
from msio.logme.api import router


def create_application() -> FastAPI:
    configuration = config.load_config_file()
    application = FastAPI(title=configuration.project_name)
    application.include_router(router)
    return application


app = create_application()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
