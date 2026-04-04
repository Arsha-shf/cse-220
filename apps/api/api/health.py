"""Health check endpoint for FlavorMap API."""

from datetime import datetime, timezone

from api_http import Controller, controller, get

START_TIME = datetime.now(timezone.utc)


@controller()
class HealthController(Controller):
    """Controller for health endpoint."""

    @get()
    def health(self):
        """Return API health status as JSON."""
        now = datetime.now(timezone.utc)
        uptime_seconds = int((now - START_TIME).total_seconds())
        return self.json(
            {
                "status": "ok",
                "version": "1.0.0",
                "service": "flavormap-api",
                "uptime_seconds": uptime_seconds,
            }
        )
