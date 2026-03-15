# Installation

## Prerequisites

| Tool | Purpose | Install |
|---|---|---|
| Python ≥ 3.14 | Runtime | [python.org](https://www.python.org/downloads/) |
| [Poetry](https://python-poetry.org/) | Dependency & packaging manager | `curl -sSL https://install.python-poetry.org \| python3 -` |
| [GitHub CLI (`gh`)](https://cli.github.com/) | GitHub repo discovery | `brew install gh` |
| `yq` | YAML parsing in shell scripts | `brew install yq` |
| `jq` | JSON parsing in shell scripts | `brew install jq` |

!!! note "GitLab"
    GitLab discovery requires a personal access token stored in the `GITLAB_TOKEN` environment variable — no extra CLI tool needed.

---

## Install dev-bootstrap

```bash
git clone https://github.com/edgar-treischl/dev-bootstrap.git
cd dev-bootstrap
poetry install
```

This installs the `dev` command into the project's virtual environment.

---

## Authenticate GitHub CLI

```bash
gh auth login
```

Follow the prompts to authenticate. After this, `dev bootstrap --github-user` will work without any token.

---

## Set a GitLab token

```bash
export GITLAB_TOKEN=<your-personal-access-token>
```

Add this to your shell profile (`~/.zshrc`, `~/.bashrc`, etc.) to make it permanent.

---

## Verify the installation

```bash
poetry run dev --help
```

You should see the list of available commands.
