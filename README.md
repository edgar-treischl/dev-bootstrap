# Dev Bootstrap

Discovers repositories from GitHub and/or GitLab, reads `.repo-meta.yml` metadata from each repo, and organizes them under `~/code/<dev_path>/`.

```
gh repo list / GitLab API
        ↓
  git clone --depth 1
        ↓
  read .repo-meta.yml
        ↓
  ~/code/<dev_path>/<repo-name>
```

---

## Requirements

- Python ≥ 3.14 + [Poetry](https://python-poetry.org/)
- [GitHub CLI (`gh`)](https://cli.github.com/) — for GitHub discovery (`brew install gh && gh auth login`)
- GitLab personal access token in `$GITLAB_TOKEN` — for GitLab discovery

---

## Install

```bash
git clone git@github.com:you/dev-bootstrap.git
cd dev-bootstrap
poetry install
```

---

## Usage

### Bootstrap from GitHub

Discovers all repos for a GitHub user or organisation, clones them, and places them under `~/code`:

```bash
poetry run dev bootstrap --github-user <your-github-username>
```

### Bootstrap from GitLab

```bash
export GITLAB_TOKEN=<your-token>
poetry run dev bootstrap --gitlab-url https://gitlab.example.com
```

### Bootstrap from both at once

```bash
poetry run dev bootstrap --github-user <user> --gitlab-token <token> --gitlab-url https://gitlab.example.com
```

### Update all repos

Fetches full history (unshallows) and pulls every repo already under `~/code`:

```bash
poetry run dev update
```

### Help

```bash
poetry run dev --help
poetry run dev bootstrap --help
```

---

## How repos are placed

Each repo can contain a `.repo-meta.yml` file that controls where it lands locally:

```yaml
name: my-app
dev_path: work/apps   # → cloned to ~/code/work/apps/my-app
role: project
tags: [python]
language: python
setup:
  - pip install -e .
env: []
services: []
depends_on: []
```

| `dev_path` value | Local path |
|---|---|
| `work/apps` | `~/code/work/apps/<name>` |
| *(empty or missing)* | `~/code/misc/<name>` |


Updated:

```
poetry run dev discover -gh -u edgar-treischl
```