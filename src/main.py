from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from operations.router import router as operation_router


app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """
    Handle RequestValidationError exceptions.

    This exception is raised when the request validation fails.

    Return a JSONResponse with a 422 status code, containing the
    validation errors and the request method and URL.

    :param request: The request object.
    :param exc: The RequestValidationError exception.
    :return: A JSONResponse with the validation errors.
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "message": f"{request.method}: {request.url}",
        },
    )


app.include_router(operation_router)
