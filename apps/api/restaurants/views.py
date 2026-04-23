"""Views for restaurant endpoints."""
from api_http import (
    Controller,
    UserIsAuthenticated,
    UserRoleRequired,
    controller,
    delete,
    get,
    guard,
    patch,
    post,
)
from restaurants.dtos import RestaurantDto, RestaurantUpdateDto
from restaurants.models import Restaurant, Category
from users.models import UserRole


@controller()
class RestaurantsController(Controller):
    """Controller for restaurant endpoints."""

    @get()
    def restaurants_list(self):
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

    @post()
    @guard(UserIsAuthenticated)
    @guard(UserRoleRequired(UserRole.OWNER))
    def create_restaurant(self, data: RestaurantDto):
        user = getattr(self.request, "user", None)

        category = Category.objects.filter(id=data.category_id).first()
        if not category:
            return self.error(
                status=400,
                code="invalid_category",
                message="Category does not exist."
            )

        # TODO: Adding level for phone, price, ... validation
        restaurant = Restaurant.objects.create(
            name=data.name,
            description=data.description,
            address_line1=data.address_line1,
            city=data.city,
            category=category,
            owner=user,
            price_range=data.price_range
        )
        return self.created({"data": RestaurantDto.from_model(restaurant)})

    @patch("<slug:slug>/")
    @guard(UserIsAuthenticated)
    @guard(UserRoleRequired(UserRole.OWNER))
    def restaurant_update(self, slug):
        """Scaffold for owner-only restaurant update."""
        restaurant = Restaurant.objects.filter(slug=slug).first()
        if restaurant is None:
            return self.error(
                status=404,
                code="not_found",
                message="Restaurant not found.")
        if restaurant.owner_id != self.request.user.id:
            return self.error(
                status=403,
                code="forbidden",
                message="You do not have permission to update this restaurant."
            )

        dto = RestaurantUpdateDto.from_dict(self.request.data)
        if not isinstance(dto, dict):
            return self.error(
                status=400,
                code="invalid_request",
                message="Request body must be a JSON object.",
            )

        for field, value in dto.items():
            setattr(restaurant, field, value)
        restaurant.save()
        return self.json({"data": RestaurantDto.from_model(restaurant)})

    @delete("<slug:slug>/")
    @guard(UserIsAuthenticated)
    @guard(UserRoleRequired(UserRole.ADMIN))
    def delete_restaurant(self, slug):
        """Scaffold for admin-only restaurant deletion."""
        restaurant = Restaurant.objects.filter(slug=slug).first()
        if restaurant is None:
            return self.error(
                status=404,
                code="not_found",
                message="Restaurant not found.",
            )

        restaurant.delete()
        return self.no_content()
