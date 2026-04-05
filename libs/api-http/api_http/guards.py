from __future__ import annotations

from functools import wraps
from typing import Any, Callable

from django.http import HttpResponse

from .decorators import use


class UserIsAuthenticated:
    """Guard requiring an authenticated request user."""

    def __call__(
        self, func: Callable[..., HttpResponse]
    ) -> Callable[..., HttpResponse]:
        @wraps(func)
        def wrapper(self: Any, *args: Any, **kwargs: Any) -> HttpResponse:
            user = getattr(self.request, "user", None)
            if user is None or not user.is_authenticated:
                return self.error(
                    status=401,
                    code="auth_required",
                    message="Authentication is required.",
                )

            return func(self, *args, **kwargs)

        return wrapper


class UserRoleRequired:
    """Guard requiring the authenticated user to have a specific role."""

    def __init__(self, role: Any) -> None:
        self.role = role

    def __call__(
        self, func: Callable[..., HttpResponse]
    ) -> Callable[..., HttpResponse]:
        @wraps(func)
        def wrapper(self: Any, *args: Any, **kwargs: Any) -> HttpResponse:
            user = getattr(self.request, "user", None)
            if user is None or not user.is_authenticated:
                return self.error(
                    status=401,
                    code="auth_required",
                    message="Authentication is required.",
                )

            if user.role != self.role:
                return self.error(
                    status=403,
                    code="forbidden",
                    message="You do not have permission to perform this action.",
                )

            return func(self, *args, **kwargs)

        return wrapper


def guard(guard_definition: Any) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Attach a guard to a route handler through the existing use(...) system."""

    guard_instance = (
        guard_definition() if isinstance(guard_definition, type) else guard_definition
    )
    return use(guard_instance)