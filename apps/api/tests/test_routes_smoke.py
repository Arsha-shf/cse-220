"""Smoke tests for controller-routed API endpoints."""

import uuid

from django.contrib.auth import get_user_model
from django.test import Client


def test_health_route_smoke():
    client = Client()
    response = client.get("/api/v1/health/")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"


def test_restaurants_routes_smoke():
    client = Client()

    list_response = client.get("/api/v1/restaurants/")
    detail_response = client.get("/api/v1/restaurants/test-place/")

    assert list_response.status_code == 200
    assert list_response.json()["data"] == []
    assert detail_response.status_code == 200
    assert detail_response.json()["data"]["slug"] == "test-place"


def test_reviews_route_smoke():
    client = Client()
    review_id = uuid.uuid4()
    response = client.get(f"/api/v1/reviews/{review_id}/")

    assert response.status_code == 200
    assert response.json()["data"]["id"] == str(review_id)


def test_users_route_requires_authentication():
    client = Client()

    me_response = client.get("/api/v1/users/me/")

    assert me_response.status_code == 302


def test_users_authenticated_smoke():
    client = Client()
    user_model = get_user_model()
    suffix = uuid.uuid4().hex[:8]
    user = user_model.objects.create_user(
        email=f"route-smoke-{suffix}@example.com",
        username=f"route-smoke-{suffix}",
        password="test-password-123",
        display_name="Route Smoke",
    )
    client.force_login(user)

    me_response = client.get("/api/v1/users/me/")

    assert me_response.status_code == 200
    assert me_response.json()["data"]["email"] == user.email
