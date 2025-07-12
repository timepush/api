from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from psycopg import errors as pg_errors
import traceback

def format_error(message: str, type_: str, status: int, code: str | None = None):
    body = {
        "error": {
            "message": message,
            "type": type_,
            "status": status
        }
    }
    if code:
        body["error"]["code"] = code
    return JSONResponse(status_code=status, content=body)

async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        return format_error(str(exc.detail), "http_exception", exc.status_code)

    if isinstance(exc, (RequestValidationError, ValidationError)):
        return format_error("Validation failed", "validation_error", 422)

    if isinstance(exc, pg_errors.UniqueViolation):
        return format_error("Unique constraint violated", "db_error", 400, code="unique_violation")

    traceback.print_exception(type(exc), exc, exc.__traceback__)
    return format_error(str(exc), "internal_error", 500)

# ✅ Register all at once
def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(HTTPException, global_exception_handler)
    app.add_exception_handler(RequestValidationError, global_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)
