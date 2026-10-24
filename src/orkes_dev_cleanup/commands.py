"""
Core delete operations. Each function returns (deleted_count, error_count).
"""

from __future__ import annotations

import sys
from collections import defaultdict

import requests
from conductor.client.configuration.configuration import Configuration
from conductor.client.orkes.orkes_metadata_client import OrkesMetadataClient
from conductor.client.orkes.orkes_prompt_client import OrkesPromptClient
from conductor.client.orkes.orkes_scheduler_client import OrkesSchedulerClient
from conductor.client.orkes.orkes_secret_client import OrkesSecretClient


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _confirm(count: int, noun: str) -> bool:
    print(f"\nThis will permanently delete ALL {count} {noun}(s) listed above.")
    answer = input("Type 'yes' to confirm: ").strip().lower()
    if answer != "yes":
        print("Aborted.")
        return False
    return True


# ---------------------------------------------------------------------------
# Workflow definitions
# ---------------------------------------------------------------------------

def delete_workflows(server_url: str, yes: bool = False) -> tuple[int, int]:
    config = Configuration(server_api_url=server_url, debug=False)
    client = OrkesMetadataClient(config)

    workflows = client.get_all_workflow_defs()
    if not workflows:
        print("No workflow definitions found.")
        return 0, 0

    by_name: dict[str, list] = defaultdict(list)
    for wf in workflows:
        by_name[wf.name].append(wf.version)

    print(f"\nFound {len(workflows)} workflow definition(s) across {len(by_name)} name(s):\n")
    for name, versions in sorted(by_name.items()):
        print(f"  {name}  (versions: {sorted(versions)})")

    if not yes and not _confirm(len(workflows), "workflow definition"):
        sys.exit(0)

    print()
    deleted, errors = 0, 0
    for wf in workflows:
        try:
            client.unregister_workflow_def(wf.name, wf.version)
            print(f"  Deleted: {wf.name} v{wf.version}")
            deleted += 1
        except Exception as e:
            print(f"  Failed:  {wf.name} v{wf.version} -> {e}")
            errors += 1

    return deleted, errors


# ---------------------------------------------------------------------------
# Task definitions
# ---------------------------------------------------------------------------

def delete_tasks(server_url: str, yes: bool = False) -> tuple[int, int]:
    config = Configuration(server_api_url=server_url, debug=False)
    client = OrkesMetadataClient(config)

    tasks = client.get_all_task_defs()
    if not tasks:
        print("No task definitions found.")
        return 0, 0

    print(f"\nFound {len(tasks)} task definition(s):\n")
    for task in sorted(tasks, key=lambda t: t.name):
        print(f"  {task.name}")

    if not yes and not _confirm(len(tasks), "task definition"):
        sys.exit(0)

    print()
    deleted, errors = 0, 0
    for task in tasks:
        try:
            client.unregister_task_def(task.name)
            print(f"  Deleted: {task.name}")
            deleted += 1
        except Exception as e:
            print(f"  Failed:  {task.name} -> {e}")
            errors += 1

    return deleted, errors


# ---------------------------------------------------------------------------
# AI prompts
# ---------------------------------------------------------------------------

def delete_prompts(server_url: str, yes: bool = False) -> tuple[int, int]:
    config = Configuration(server_api_url=server_url, debug=False)
    client = OrkesPromptClient(config)

    prompts = client.get_prompts()
    if not prompts:
        print("No AI prompts found.")
        return 0, 0

    print(f"\nFound {len(prompts)} AI prompt(s):\n")
    for prompt in sorted(prompts, key=lambda p: p.name):
        print(f"  {prompt.name}")

    if not yes and not _confirm(len(prompts), "AI prompt"):
        sys.exit(0)

    print()
    deleted, errors = 0, 0
    for prompt in prompts:
        try:
            client.delete_prompt(prompt.name)
            print(f"  Deleted: {prompt.name}")
            deleted += 1
        except Exception as e:
            print(f"  Failed:  {prompt.name} -> {e}")
            errors += 1

    return deleted, errors


# ---------------------------------------------------------------------------
# Schedules
# ---------------------------------------------------------------------------

def delete_schedules(server_url: str, yes: bool = False) -> tuple[int, int]:
    config = Configuration(server_api_url=server_url, debug=False)
    client = OrkesSchedulerClient(config)

    schedules = client.get_all_schedules()
    if not schedules:
        print("No schedules found.")
        return 0, 0

    print(f"\nFound {len(schedules)} schedule(s):\n")
    for schedule in sorted(schedules, key=lambda s: s.name):
        print(f"  {schedule.name}")

    if not yes and not _confirm(len(schedules), "schedule"):
        sys.exit(0)

    print()
    deleted, errors = 0, 0
    for schedule in schedules:
        try:
            client.delete_schedule(schedule.name)
            print(f"  Deleted: {schedule.name}")
            deleted += 1
        except Exception as e:
            print(f"  Failed:  {schedule.name} -> {e}")
            errors += 1

    return deleted, errors


# ---------------------------------------------------------------------------
# Secrets
# ---------------------------------------------------------------------------

def delete_secrets(server_url: str, yes: bool = False) -> tuple[int, int]:
    config = Configuration(server_api_url=server_url, debug=False)
    client = OrkesSecretClient(config)

    secret_names = sorted(client.list_all_secret_names())
    if not secret_names:
        print("No secrets found.")
        return 0, 0

    print(f"\nFound {len(secret_names)} secret(s):\n")
    for name in secret_names:
        print(f"  {name}")

    if not yes and not _confirm(len(secret_names), "secret"):
        sys.exit(0)

    print()
    deleted, errors = 0, 0
    for name in secret_names:
        try:
            client.delete_secret(name)
            print(f"  Deleted: {name}")
            deleted += 1
        except Exception as e:
            print(f"  Failed:  {name} -> {e}")
            errors += 1

    return deleted, errors


# ---------------------------------------------------------------------------
# User form templates
# ---------------------------------------------------------------------------

def delete_forms(server_url: str, token: str, yes: bool = False) -> tuple[int, int]:
    headers = {
        "X-Authorization": token,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    resp = requests.get(f"{server_url}/human/template", headers=headers)
    if not resp.ok:
        print(f"Error listing user forms: {resp.status_code} {resp.text}", file=sys.stderr)
        sys.exit(1)

    templates = resp.json()
    if not templates:
        print("No user form templates found.")
        return 0, 0

    by_name: dict[str, list] = defaultdict(list)
    for t in templates:
        by_name[t["name"]].append(t["version"])

    print(f"\nFound {len(templates)} user form template(s) across {len(by_name)} name(s):\n")
    for name, versions in sorted(by_name.items()):
        print(f"  {name}  (versions: {sorted(versions)})")

    if not yes and not _confirm(len(templates), "user form template"):
        sys.exit(0)

    print()
    deleted, errors = 0, 0
    for t in templates:
        name, version = t["name"], t["version"]
        r = requests.delete(
            f"{server_url}/human/template/{name}/{version}", headers=headers
        )
        if r.ok:
            print(f"  Deleted: {name} v{version}")
            deleted += 1
        else:
            print(f"  Failed:  {name} v{version} -> {r.status_code} {r.text}")
            errors += 1

    return deleted, errors
