"""Tests for restaurant create/update/delete authorization and failures."""

import uuid

import pytest
from django.contrib.auth import get_user_model
from django.test import Client

from restaurants.models import Category, Restaurant
from users.models import UserRole

pytestmark = pytest.mark.django_db


def _create_user(*, role: str):
    suffix = uuid.uuid4().hex[:8]
    user_model = get_user_model()
    return user_model.objects.create_user(
        email=f"{role}-{suffix}@example.com",
        username=f"{role}-{suffix}",
        password="test-password-123",
        display_name=f"{role.title()} {suffix}",
        role=role,
    )


def _create_category(name_prefix: str = "Category"):
    suffix = uuid.uuid4().hex[:8]
    return Category.objects.create(
        name=f"{name_prefix} {suffix}",
        description="Category for tests",
    )


def _restaurant_payload(category_id):
    suffix = uuid.uuid4().hex[:8]
    return {
        "name": f"Owner Place {suffix}",
        "description": "Test restaurant",
        "category_id": str(category_id),
        "address_line1": "Street 1",
        "city": "Istanbul",
        "district": "Besiktas",
        "price_range": "2",
    }


def test_restaurant_create_requires_authentication():
    client = Client()
    category = _create_category("Create Auth")

    response = client.post(
        "/api/v1/restaurants/",
        data=_restaurant_payload(category.id),
        content_type="application/json",
    )

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "auth_required"


def test_restaurant_create_requires_owner_role():
    client = Client()
    category = _create_category("Create Role")
    regular_user = _create_user(role=UserRole.USER)
    client.force_login(regular_user)

    response = client.post(
        "/api/v1/restaurants/",
        data=_restaurant_payload(category.id),
        content_type="application/json",
    )

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "forbidden"


def test_restaurant_create_rejects_admin_role():
    client = Client()
    category = _create_category("Create Admin")
    admin = _create_user(role=UserRole.ADMIN)
    client.force_login(admin)

    response = client.post(
        "/api/v1/restaurants/",
        data=_restaurant_payload(category.id),
        content_type="application/json",
    )

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "forbidden"


def test_restaurant_create_validates_required_fields():
    client = Client()
    owner = _create_user(role=UserRole.OWNER)
    category = _create_category("Create Validation")
    client.force_login(owner)

    payload = _restaurant_payload(category.id)
    del payload["name"]

    response = client.post(
        "/api/v1/restaurants/",
        data=payload,
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "validation_error"
    assert "name" in response.json()["error"]["details"]["missing_fields"]


def test_restaurant_create_owner_success_and_owner_hidden_in_response():
    client = Client()
    owner = _create_user(role=UserRole.OWNER)
    category = _create_category("Create Success")
    client.force_login(owner)

    payload = _restaurant_payload(category.id)

    response = client.post(
        "/api/v1/restaurants/",
        data=payload,
        content_type="application/json",
    )

    assert response.status_code == 201
    body = response.json()["data"]
    assert body["name"] == payload["name"]
    assert "owner" not in body

    created = Restaurant.objects.get(slug=body["slug"])
    assert created.owner_id == owner.id


def test_restaurant_update_requires_authentication():
    client = Client()
    owner = _create_user(role=UserRole.OWNER)
    category = _create_category("Update Auth")
    restaurant = Restaurant.objects.create(
        name="Update Auth Place",
        description="Desc",
        category=category,
        owner=owner,
        address_line1="Street 1",
        city="Istanbul",
    )

    response = client.patch(
        f"/api/v1/restaurants/{restaurant.slug}/",
        data={"name": "Changed"},
        content_type="application/json",
    )

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "auth_required"


def test_restaurant_update_requires_ownership():
    client = Client()
    owner = _create_user(role=UserRole.OWNER)
    another_owner = _create_user(role=UserRole.OWNER)
    category = _create_category("Update Ownership")
    restaurant = Restaurant.objects.create(
        name="Update Ownership Place",
        description="Desc",
        category=category,
        owner=owner,
        address_line1="Street 1",
        city="Istanbul",
    )
    client.force_login(another_owner)

    response = client.patch(
        f"/api/v1/restaurants/{restaurant.slug}/",
        data={"name": "Changed"},
        content_type="application/json",
    )

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "forbidden"


def test_restaurant_update_rejects_admin_role():
    client = Client()
    owner = _create_user(role=UserRole.OWNER)
    admin = _create_user(role=UserRole.ADMIN)
    category = _create_category("Update Admin")
    restaurant = Restaurant.objects.create(
        name="Update Admin Place",
        description="Desc",
        category=category,
        owner=owner,
        address_line1="Street 1",
        city="Istanbul",
    )
    client.force_login(admin)

    response = client.patch(
        f"/api/v1/restaurants/{restaurant.slug}/",
        data={"name": "Changed"},
        content_type="application/json",
    )

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "forbidden"


def test_restaurant_update_not_found_for_owner():
    client = Client()
    owner = _create_user(role=UserRole.OWNER)
    client.force_login(owner)

    response = client.patch(
        "/api/v1/restaurants/not-found-slug/",
        data={"name": "Changed"},
        content_type="application/json",
    )

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "not_found"


def test_restaurant_update_owner_success():
    client = Client()
    owner = _create_user(role=UserRole.OWNER)
    category = _create_category("Update Success")
    restaurant = Restaurant.objects.create(
        name="Update Success Place",
        description="Desc",
        category=category,
        owner=owner,
        address_line1="Street 1",
        city="Istanbul",
    )
    client.force_login(owner)

    response = client.patch(
        f"/api/v1/restaurants/{restaurant.slug}/",
        data={"name": "Updated Name", "city": "Ankara"},
        content_type="application/json",
    )

    assert response.status_code == 200
    payload = response.json()["data"]
    assert payload["name"] == "Updated Name"
    assert payload["city"] == "Ankara"
    assert "owner" not in payload

    restaurant.refresh_from_db()
    assert restaurant.name == "Updated Name"
    assert restaurant.city == "Ankara"


def test_restaurant_delete_requires_authentication():
    client = Client()
    owner = _create_user(role=UserRole.OWNER)
    category = _create_category("Delete Auth")
    restaurant = Restaurant.objects.create(
        name="Delete Auth Place",
        description="Desc",
        category=category,
        owner=owner,
        address_line1="Street 1",
        city="Istanbul",
    )

    response = client.delete(f"/api/v1/restaurants/{restaurant.slug}/")

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "auth_required"


def test_restaurant_delete_requires_admin_role():
    client = Client()
    owner = _create_user(role=UserRole.OWNER)
    category = _create_category("Delete Role")
    restaurant = Restaurant.objects.create(
        name="Delete Role Place",
        description="Desc",
        category=category,
        owner=owner,
        address_line1="Street 1",
        city="Istanbul",
    )
    client.force_login(owner)

    response = client.delete(f"/api/v1/restaurants/{restaurant.slug}/")

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "forbidden"


def test_restaurant_delete_admin_not_found():
    client = Client()
    admin = _create_user(role=UserRole.ADMIN)
    client.force_login(admin)

    response = client.delete("/api/v1/restaurants/not-found-slug/")

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "not_found"


def test_restaurant_delete_admin_success():
    client = Client()
    owner = _create_user(role=UserRole.OWNER)
    admin = _create_user(role=UserRole.ADMIN)
    category = _create_category("Delete Success")
    restaurant = Restaurant.objects.create(
        name="Delete Success Place",
        description="Desc",
        category=category,
        owner=owner,
        address_line1="Street 1",
        city="Istanbul",
    )
    client.force_login(admin)

    response = client.delete(f"/api/v1/restaurants/{restaurant.slug}/")

    assert response.status_code == 204
    assert not Restaurant.objects.filter(id=restaurant.id).exists()
