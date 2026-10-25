# 🧹 orkes-dev-cleanup

**Wipe your [Orkes developer edition](https://developer.orkescloud.com) environment back to zero with one command.**

![PyPI not published](https://img.shields.io/badge/install-pip%20%2B%20git-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-Apache--2.0-green)

If you build on Orkes, you know the drill: a few weeks of experimenting and your dev
account is a graveyard of half-finished workflows, orphaned task defs, test prompts,
schedules firing into the void, and secrets you don't remember creating. I built this tool so you can reset your Developer Edition from the terminal,
with one command per resource type (or all of them at once).

![demo](demo.gif)

## Install

```bash
pip install git+https://github.com/maria-shimkovska/orkes-dev-cleanup.git
```

Or clone and install locally:

```bash
git clone https://github.com/maria-shimkovska/orkes-dev-cleanup.git
cd orkes-dev-cleanup
pip install .
```

## Setup

Create an application in your Orkes developer account and copy the key and secret, then export them:

```bash
export CONDUCTOR_AUTH_KEY=your-key-id
export CONDUCTOR_AUTH_SECRET=your-key-secret
```

> ⚠️**This tool only ever targets** `https://developer.orkescloud.com/api` and it's
> hardcoded, not configurable, so there's no risk of accidentally pointing it
> at a different Orkes instance.

## Usage

```bash
orkes-cleanup workflows   # Delete all workflow definitions
orkes-cleanup tasks       # Delete all task definitions
orkes-cleanup forms       # Delete all user form templates
orkes-cleanup prompts     # Delete all AI prompts
orkes-cleanup schedules   # Delete all schedules
orkes-cleanup secrets     # Delete all secrets
orkes-cleanup all         # Delete everything above

orkes-cleanup all --yes   # Skip the confirmation prompt (handy in scripts)
```

Every command lists exactly what it found before it touches anything, then asks you
to type `yes` to confirm. 

```
🔍 Found 7 workflow definition(s) across 3 name(s):

  demo_order_flow  (versions: [1, 2])
  test_retry_wf    (versions: [1])
  scratch_wf       (versions: [1, 2, 3])

⚠️  This will permanently delete ALL 7 workflow definition(s) listed above.
Type 'yes' to confirm: yes

  ✅ Deleted: demo_order_flow v1
  ✅ Deleted: demo_order_flow v2
  ✅ Deleted: test_retry_wf v1
  ✅ Deleted: scratch_wf v1
  ✅ Deleted: scratch_wf v2
  ✅ Deleted: scratch_wf v3

🎉 Done. 7 item(s) deleted.
```

## Why this exists

- **One command instead of a dozen clicks.** The Orkes UI makes you delete
  workflows, tasks, prompts, schedules, and secrets one at a time for safety. But because Developer Edition is amazing for experiments this lets you reset your environement when you need it.
- **Safe by default.** Every command shows you exactly what it found before
  asking for confirmation, so you always see what would be deleted.
- **Scriptable.** `--yes` skips the prompt, so you can drop a full reset into
  CI, a demo-prep script, or a pre-test hook.
- **Covers everything,** not just workflows: task definitions, user form
  templates, AI prompts, schedules, and secrets all get the same treatment.

> ⚠️ **This is a destructive tool.** It's locked to Orkes Developer Edition
> (`developer.orkescloud.com`) and can't target any other Orkes instance,
> but within that account, deletions are permanent, so use it on sandboxes
> you're actively iterating on, not anything you'd miss.

## Getting your API key

1. Go to [developer.orkescloud.com](https://developer.orkescloud.com)
2. Navigate to **Access Control → Applications**
3. Create an application and give it **Admin** permissions
4. Copy the **Key ID** and **Key Secret**