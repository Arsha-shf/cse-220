"""Views for review endpoints."""

from api_http import Controller, controller, get


@controller()
class ReviewsController(Controller):
    """Controller for review endpoints."""

    @get("<uuid:review_id>/")
    def review_detail(self, review_id):
        """Placeholder review detail endpoint."""
        return self.json(
            {
                "data": {
                    "id": str(review_id),
                    "message": "Review endpoint is scaffolded and ready for implementation.",
                }
            }
        )
