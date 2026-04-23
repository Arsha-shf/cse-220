"""Health unit test module."""

import json

from api.health import HealthController


def test_health():
    """Test the health function."""
    response = HealthController(None).health()

    assert response.status_code == 200
    payload = json.loads(response.content)
    assert payload["status"] == "ok"
    assert payload["service"] == "flavormap-api"
