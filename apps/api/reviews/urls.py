"""URL routes for reviews app."""

from api_http import build_urlpatterns

from reviews.views import ReviewsController

urlpatterns = build_urlpatterns(ReviewsController)
