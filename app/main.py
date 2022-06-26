from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from starlette.middleware.authentication import AuthenticationMiddleware

from app.api.routes import api
from app.config import config

from app.core.engine import engine, get_session

from app.core.models import Base
from definitions import STATIC_DIR


def get_application() -> FastAPI:
    application = FastAPI(
        title=config.SERVICE_NAME,
        description=config.DESCRIPTION,
        debug=config.DEBUG,
    )

    @application.exception_handler(status.HTTP_401_UNAUTHORIZED)
    def auth_exception_handler(  # pylint: disable=unused-argument
        request: Request, exc: HTTPException
    ) -> RedirectResponse:
        """
        Redirect the user to the login page if not logged in
        """
        return RedirectResponse(url='/signin')

    @application.on_event('startup')
    def startup() -> None:
        Base.metadata.create_all(engine)
        get_session()

    @application.on_event('shutdown')
    def shutdown() -> None:
        pass

    application.include_router(api.login_api_router)

    return application


app = get_application()




