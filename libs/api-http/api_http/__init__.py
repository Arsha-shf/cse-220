"""Decorator-driven class-based HTTP utilities for Django."""

from .errors import (
    ApiHttpError,
    BadRequestError,
    InternalServerError,
    MethodNotAllowedError,
    NotFoundError,
    UnauthorizedError,
    map_exception_to_response,
)
from .route import RouteDefinition, route
from .urlpatterns import build_urlpatterns
from .controller import Controller, controller
from .methods import get, post, put, patch, delete
from .use import use

__all__ = [
    "ApiHttpError",
    "BadRequestError",
    "RouteDefinition",
    "InternalServerError",
    "MethodNotAllowedError",
    "NotFoundError",
    "UnauthorizedError",
    "map_exception_to_response",
    "Controller",
    "build_urlpatterns",
    "controller",
    "route",
    "get",
    "post",
    "put",
    "patch",
    "delete",
    "use",
]
