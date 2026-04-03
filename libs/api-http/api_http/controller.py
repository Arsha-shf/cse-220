from django.http import HttpResponse, JsonResponse
from constants import _PREFIX_ATTR, _HOOKS_ATTR


def controller(*, prefix: str = ""):
    """Mark a class as an HTTP controller."""

    def decorator(cls):
        setattr(cls, _PREFIX_ATTR, prefix)
        if not hasattr(cls, _HOOKS_ATTR):
            setattr(cls, _HOOKS_ATTR, [])
        return cls

    return decorator


class Controller:
    """Base class for controller methods and JSON helpers."""

    def __init__(self, request):
        self.request = request

    def json(self, payload: dict, *, status: int = 200) -> JsonResponse:
        """Helper method to return a JSON response."""
        return JsonResponse(payload, status=status)

    def ok(self, data=None) -> JsonResponse:
        """Helper method to return a 200 OK response with optional data."""
        return self.json({"data": data})

    def created(self, data=None) -> JsonResponse:
        """
        Helper method to return a 201 Created response with optional data.
        """
        return self.json({"data": data}, status=201)

    def no_content(self) -> HttpResponse:
        """Helper method to return a 204 No Content response."""
        return HttpResponse(status=204)
