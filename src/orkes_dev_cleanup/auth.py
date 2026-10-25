import os
import sys

from conductor.client.configuration.configuration import Configuration
from conductor.client.http.api_client import ApiClient

ALLOWED_SERVER_URL = "https://developer.orkescloud.com/api"


def get_config() -> tuple[str, str]:
    """
    Build a Configuration for the Orkes developer-edition server, fetch a
    token via the SDK, and return (server_url, bearer_token).

    The server URL is hardcoded to developer.orkescloud.com — this tool is
    destructive and is not allowed to target any other Orkes instance.
    """
    stray_url = os.environ.get("CONDUCTOR_SERVER_URL")
    if stray_url and stray_url.rstrip("/") != ALLOWED_SERVER_URL:
        print(
            f"Error: orkes-cleanup only targets {ALLOWED_SERVER_URL}.\n"
            f"CONDUCTOR_SERVER_URL is set to {stray_url!r} — unset it to continue.",
            file=sys.stderr,
        )
        sys.exit(1)

    server_url = ALLOWED_SERVER_URL
    auth_key = os.environ.get("CONDUCTOR_AUTH_KEY")
    auth_secret = os.environ.get("CONDUCTOR_AUTH_SECRET")

    if not auth_key or not auth_secret:
        print(
            "Error: CONDUCTOR_AUTH_KEY and CONDUCTOR_AUTH_SECRET must be set.",
            file=sys.stderr,
        )
        sys.exit(1)

    config = Configuration(server_api_url=server_url, debug=False)
    ApiClient(config)  # triggers token refresh

    if not config.AUTH_TOKEN:
        print(
            "Error: failed to obtain auth token. Check your credentials.",
            file=sys.stderr,
        )
        sys.exit(1)

    return server_url, config.AUTH_TOKEN
