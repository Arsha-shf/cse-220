"""Views for restaurant endpoints."""

from api_http import Controller, controller, get


@controller()
class RestaurantsController(Controller):
    """Controller for restaurant endpoints."""

    @get()
    def restaurants_list(self):
        """Placeholder restaurant list endpoint."""
        return self.json(
            {"data": [], "pagination": {"cursor": None, "has_more": False}}
        )

    @get("<slug:slug>/")
    def restaurant_detail(self, slug):
        """Placeholder restaurant detail endpoint."""
        return self.json(
            {
                "data": {
                    "slug": slug,
                    "message": "Restaurant detail endpoint is scaffolded and ready for implementation.",
                }
            }
        )
