from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import HTTPException, RequestValidationError
from loguru import logger
from app.api.schemas.responses import ErrorResult
from app.api.routes import api
from app.config import config
from starlette.responses import JSONResponse


def get_application() -> FastAPI:
    application = FastAPI(
        title=config.SERVICE_NAME,
        description=config.DESCRIPTION,
        debug=config.DEBUG,
    )

    @application.exception_handler(HTTPException)
    def http_exception_handler(request: Request, exc: HTTPException):
        logger.error(exc)
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResult(code=exc.status_code,
                                message=exc.detail).dict(),
        )

    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        logger.error(exc)
        return JSONResponse(
            status_code=400,
            content=ErrorResult(code=400,
                                message='Validation Failed').dict(),
        )

    application.include_router(api.login_api_router)

    return application


app = get_application()




