"""URL routes for users app."""

from api_http import build_urlpatterns

from users.views import UsersController

urlpatterns = build_urlpatterns(UsersController)
