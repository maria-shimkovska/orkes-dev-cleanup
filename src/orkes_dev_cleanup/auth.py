import os
import sys

from conductor.client.configuration.configuration import Configuration
from conductor.client.http.api_client import ApiClient


def get_config() -> tuple[str, str]:
    """
    Read env vars, build a Configuration, fetch a token via the SDK, and
    return (server_url, bearer_token).
    """
    server_url = os.environ.get(
        "CONDUCTOR_SERVER_URL", "https://developer.orkescloud.com/api"
    ).rstrip("/")
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
