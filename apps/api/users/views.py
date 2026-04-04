"""Views for user endpoints."""

from api_http import Controller, controller, get, use
from django.contrib.auth.decorators import login_required


@controller()
class UsersController(Controller):
    """Controller for users endpoints."""

    @use(login_required)
    @get("me/")
    def me(self):
        """Return the authenticated user profile."""
        user = self.request.user
        return self.json(
            {
                "data": {
                    "id": str(user.id),
                    "email": user.email,
                    "username": user.username,
                    "display_name": user.display_name,
                    "role": user.role,
                }
            }
        )
