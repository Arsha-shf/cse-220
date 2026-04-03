"""Tests for decorator-based controller routing behavior."""

import json

from django.test.client import RequestFactory

from api_http import Controller, build_urlpatterns, controller, get, use


def test_build_urlpatterns_routes_get_method_and_payload():
    @controller(prefix="v1")
    class SampleController(Controller):
        @get("ping/")
        def ping(self):
            return self.ok({"message": "pong"})

    urlpatterns = build_urlpatterns(SampleController)
    assert len(urlpatterns) == 1
    assert str(urlpatterns[0].pattern) == "v1/ping/"

    request = RequestFactory().get("/v1/ping/")
    response = urlpatterns[0].callback(request)
    payload = json.loads(response.content)

    assert response.status_code == 200
    assert payload == {"data": {"message": "pong"}}


def test_build_urlpatterns_maps_method_not_allowed_to_json_error():
    @controller()
    class SampleController(Controller):
        @get("status/")
        def status(self):
            return self.ok({"ok": True})

    urlpatterns = build_urlpatterns(SampleController)
    request = RequestFactory().post("/status/")
    response = urlpatterns[0].callback(request)
    payload = json.loads(response.content)

    assert response.status_code == 405
    assert payload["error"]["code"] == "method_not_allowed"


def test_use_hook_is_applied_to_controller_method():
    def add_test_header(view):
        def wrapped(request, *args, **kwargs):
            response = view(request, *args, **kwargs)
            response["X-Test-Hook"] = "active"
            return response

        return wrapped

    @controller()
    class HookedController(Controller):
        @use(add_test_header)
        @get("hooked/")
        def hooked(self):
            return self.ok({"hooked": True})

    urlpatterns = build_urlpatterns(HookedController)
    request = RequestFactory().get("/hooked/")
    response = urlpatterns[0].callback(request)

    assert response.status_code == 200
    assert response["X-Test-Hook"] == "active"
