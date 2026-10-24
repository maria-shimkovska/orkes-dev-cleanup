# orkes-dev-cleanup

A CLI tool to quickly reset your [Orkes developer edition](https://developer.orkescloud.com) environment — delete workflow definitions, task definitions, user form templates, AI prompts, schedules, and secrets in one command.

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

# Optional — defaults to https://developer.orkescloud.com/api
export CONDUCTOR_SERVER_URL=https://developer.orkescloud.com/api
```

## Usage

```bash
# Delete all workflow definitions
orkes-cleanup workflows

# Delete all task definitions
orkes-cleanup tasks

# Delete all user form templates
orkes-cleanup forms

# Delete all AI prompts
orkes-cleanup prompts

# Delete all schedules
orkes-cleanup schedules

# Delete all secrets
orkes-cleanup secrets

# Delete everything
orkes-cleanup all

# Skip the confirmation prompt
orkes-cleanup all --yes
```

Each command lists what it found before asking you to confirm. Pass `-y` / `--yes` to skip the prompt (useful in scripts).

## Getting your API key

1. Go to [developer.orkescloud.com](https://developer.orkescloud.com)
2. Navigate to **Access Control → Applications**
3. Create an application and give it **Admin** permissions
4. Copy the **Key ID** and **Key Secret**
