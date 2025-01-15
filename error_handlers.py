from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError



async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "errors": [{"code": "HTTP_ERROR", "message": exc.detail}]
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "errors": [{"code": "VALIDATION_ERROR", "message": str(exc)}]
        },
    )


async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "errors": [{"code": "INTERNAL_ERROR", "message": str(exc)}]
        },
    )

async def type_error_handler(request: Request, exc: TypeError):
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "errors": [
                {"code": "TYPE_ERROR", "message": str(exc)}
            ]
        },
    )

