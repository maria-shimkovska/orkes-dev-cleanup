"""
orkes-cleanup  —  reset your Orkes developer edition environment

Usage:
  orkes-cleanup workflows   Delete all workflow definitions
  orkes-cleanup tasks       Delete all task definitions
  orkes-cleanup forms       Delete all user form templates
  orkes-cleanup prompts     Delete all AI prompts
  orkes-cleanup schedules   Delete all schedules
  orkes-cleanup secrets     Delete all secrets
  orkes-cleanup all         Delete everything above

Set these env vars before running:
  CONDUCTOR_SERVER_URL    (default: https://developer.orkescloud.com/api)
  CONDUCTOR_AUTH_KEY
  CONDUCTOR_AUTH_SECRET
"""

import argparse
import sys

from .auth import get_config
from .commands import (
    delete_workflows,
    delete_tasks,
    delete_forms,
    delete_prompts,
    delete_schedules,
    delete_secrets,
)


def main():
    parser = argparse.ArgumentParser(
        prog="orkes-cleanup",
        description="Reset your Orkes developer edition environment.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Set CONDUCTOR_AUTH_KEY and CONDUCTOR_AUTH_SECRET before running.\n"
            "CONDUCTOR_SERVER_URL defaults to https://developer.orkescloud.com/api"
        ),
    )
    parser.add_argument(
        "resource",
        choices=["workflows", "tasks", "forms", "prompts", "schedules", "secrets", "all"],
        help="What to delete",
    )
    parser.add_argument(
        "-y", "--yes",
        action="store_true",
        help="Skip the confirmation prompt",
    )

    args = parser.parse_args()

    server_url, token = get_config()
    print(f"Server: {server_url}\n")

    targets = (
        ["workflows", "tasks", "forms", "prompts", "schedules", "secrets"]
        if args.resource == "all"
        else [args.resource]
    )

    total_deleted = total_errors = 0

    for target in targets:
        if len(targets) > 1:
            print(f"--- {target.upper()} ---")

        if target == "workflows":
            d, e = delete_workflows(server_url, yes=args.yes)
        elif target == "tasks":
            d, e = delete_tasks(server_url, yes=args.yes)
        elif target == "forms":
            d, e = delete_forms(server_url, token, yes=args.yes)
        elif target == "prompts":
            d, e = delete_prompts(server_url, yes=args.yes)
        elif target == "schedules":
            d, e = delete_schedules(server_url, yes=args.yes)
        elif target == "secrets":
            d, e = delete_secrets(server_url, yes=args.yes)

        total_deleted += d
        total_errors += e

        if len(targets) > 1:
            print()

    print()
    if total_errors:
        print(f"Done. {total_deleted} deleted, {total_errors} failed.")
        sys.exit(1)
    else:
        print(f"Done. {total_deleted} item(s) deleted.")


if __name__ == "__main__":
    main()
