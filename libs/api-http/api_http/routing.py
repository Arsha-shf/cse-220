"""URL pattern assembly and request execution for api_http controllers."""

from __future__ import annotations

from functools import wraps
from typing import Any, Callable

from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.urls import path

from .constants import CONTROLLER_PREFIX_ATTR, ROUTE_ATTR
from .errors import ApiHttpError, InternalServerError, ResponseHandlingError
from .route_definition import RouteDefinition
from .utils import join_paths


def build_urlpatterns(controller_cls: type[Any]) -> list[Any]:
    """Build Django urlpatterns from a decorated controller class."""

    prefix = getattr(controller_cls, CONTROLLER_PREFIX_ATTR, "")
    urlpatterns: list[Any] = []

    for value in controller_cls.__dict__.values():
        route = getattr(value, ROUTE_ATTR, None)
        if route is None:
            continue

        route_path = join_paths(prefix, route.route)
        view = _build_view(controller_cls, value, route)
        urlpatterns.append(path(route_path, view))

    return urlpatterns


def _build_view(
    controller_cls: type[Any],
    route_func: Callable[..., Any],
    route: RouteDefinition,
) -> Callable[..., HttpResponse]:
    allowed_methods = [route.method]
    if route.method == "GET":
        allowed_methods.append("HEAD")

    @wraps(route_func)
    def view(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.method.upper() not in allowed_methods:
            return HttpResponseNotAllowed([route.method])

        try:
            handler = route_func.__get__(controller_cls(request), controller_cls)
            response = handler(*args, **kwargs)
            return _ensure_http_response(response, controller_cls, route_func)
        except ApiHttpError as error:
            return error.to_response()
        except Exception as error:
            details = None
            if settings.DEBUG:
                details = {
                    "type": error.__class__.__name__,
                    "message": str(error),
                }
            return InternalServerError(details=details).to_response()

    decorated_view = view
    for decorator in reversed(route.decorators):
        decorated_view = decorator(decorated_view)

    return decorated_view


def _ensure_http_response(
    response: Any,
    controller_cls: type[Any],
    route_func: Callable[..., Any],
) -> HttpResponse:
    if isinstance(response, HttpResponse):
        return response

    raise ResponseHandlingError(
        message=(
            f"{controller_cls.__name__}.{route_func.__name__} must return "
            "an HttpResponse-compatible object."
        ),
        details={"returned_type": type(response).__name__},
    )
