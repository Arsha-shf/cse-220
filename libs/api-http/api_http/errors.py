"""Error types and response mapping for api_http."""

from django.http import JsonResponse


class ApiHttpError(Exception):
    """Base error type for controller exceptions."""

    status_code = 400
    code = "bad_request"

    def __init__(self, message: str, *, details=None, status_code: int | None = None):
        super().__init__(message)
        self.message = message
        self.details = details
        if status_code is not None:
            self.status_code = status_code

    def to_payload(self) -> dict:
        error = {
            "code": self.code,
            "message": self.message,
        }
        if self.details is not None:
            error["details"] = self.details
        return {"error": error}


class BadRequestError(ApiHttpError):
    code = "bad_request"
    status_code = 400


class UnauthorizedError(ApiHttpError):
    code = "unauthorized"
    status_code = 401


class NotFoundError(ApiHttpError):
    code = "not_found"
    status_code = 404


class MethodNotAllowedError(ApiHttpError):
    code = "method_not_allowed"
    status_code = 405


class InternalServerError(ApiHttpError):
    code = "internal_server_error"
    status_code = 500


def map_exception_to_response(exc: Exception) -> JsonResponse:
    """Convert exceptions into uniform JSON responses."""

    if isinstance(exc, ApiHttpError):
        return JsonResponse(exc.to_payload(), status=exc.status_code)

    fallback = InternalServerError("An unexpected error occurred.")
    return JsonResponse(fallback.to_payload(), status=fallback.status_code)
