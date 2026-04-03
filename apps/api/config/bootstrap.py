"""Runtime path bootstrap for local workspace libraries."""

import sys
from pathlib import Path


def configure_workspace_paths() -> None:
    """Allow direct imports from internal workspace Python libraries."""
    root = Path(__file__).resolve().parents[3]
    api_http_path = root / "libs" / "api-http"
    if api_http_path.exists() and str(api_http_path) not in sys.path:
        sys.path.insert(0, str(api_http_path))
