"""Views for restaurant endpoints."""

from api_http import Controller, controller, get
from restaurants.dtos import RestaurantDto
from restaurants.models import Restaurant


@controller()
class RestaurantsController(Controller):
    """Controller for restaurant endpoints."""

    @get()
    def restaurants_list(self):
        """Return paginated restaurant results with DTO serialization."""
        include_fields, omit_fields, with_fields = self.list_query_fields()
        active_with_fields = self.resolve_list_with_fields(
            RestaurantDto,
            include_fields=include_fields,
            with_fields=with_fields,
        )

        queryset = self.apply_list_query_options(
            Restaurant.objects.all(),
            dto_class=RestaurantDto,
            active_with_fields=active_with_fields,
        )

        page_obj, pagination = self.paginate_queryset(queryset)

        data = RestaurantDto.from_models(
            page_obj.object_list,
            include=include_fields or None,
            omit=omit_fields or None,
            with_=active_with_fields,
        )

        return self.json(
            {
                "data": data,
                "pagination": pagination,
            }
        )

    @get("<slug:slug>/")
    def restaurant_detail(self, slug):
        """Return restaurant detail with full DTO serialization."""
        restaurant = Restaurant.objects.filter(slug=slug).first()
        if restaurant is None:
            return self.error(
                status=404,
                code="not_found",
                message="Restaurant not found.",
            )

        data = RestaurantDto.from_model(restaurant)
        return self.json({"data": data})
