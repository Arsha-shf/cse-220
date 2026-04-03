"""URL patterns for the api app."""

from api_http import build_urlpatterns

from .health import HealthController

urlpatterns = build_urlpatterns(HealthController)
