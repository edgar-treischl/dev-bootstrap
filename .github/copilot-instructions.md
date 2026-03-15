# Copilot Instructions

## Project Overview

This is a **proof-of-concept** tool for bootstrapping multi-repo development environments. It discovers repositories from GitHub and GitLab, reads `.repo-meta.yml` metadata from each repo, and organizes cloned repos under `~/code/{dev_path}/` based on that metadata.

## Architecture

The core logic lives in **Bash scripts**, not Python. The Python layer is a thin CLI wrapper.

**Bootstrap flow:**
```
bootstrap.sh → clone-repos.sh → gh-discovery.sh / gl-discovery.sh
                                  ↓ (shallow git clone)
                                reads .repo-meta.yml via yq
                                  ↓
                                moves repo to ~/code/{dev_path}/{name}
```

**Shell scripts:**
- `bootstrap.sh` — entry point; creates `~/code`, calls `clone-repos.sh`
- `clone-repos.sh` — orchestrates discovery → clone → metadata read → placement
- `gh-discovery.sh` — lists GitHub repos as SSH URLs using `gh repo list`
- `gl-discovery.sh` — lists GitLab repos via REST API (requires `$GITLAB_TOKEN`)
- `update-all.sh` — finds all `.git` dirs under `~/code`, runs `git fetch --unshallow` + `git pull --ff-only`

**Python module (`src/devbootstrap/`):**
- `cli.py` — Typer CLI; `poetry run dev` invokes it
- `bootstrap.py` — stub with `BASE` path constant and empty `bootstrap()` function

## Commands

```bash
poetry install          # install dependencies
poetry run dev          # run the CLI
```

No test suite or linter is currently configured.

## Key Conventions

- **Metadata-driven placement**: repos are organized by the `dev_path` field in `.repo-meta.yml`; repos without this file fall back to `~/code/misc/`
- **Shallow-clone first**: scripts use `git clone --depth 1`; full history fetched later with `git fetch --unshallow`
- **`yq` for YAML, `jq` for JSON**: shell scripts parse metadata with these tools, not Python
- **External CLI tools required**: `gh` (GitHub CLI) for GitHub access; `$GITLAB_TOKEN` env var for GitLab
- **`repo-meta.yml`** at the repo root is the canonical metadata format — see this repo's file for the schema (`name`, `dev_path`, `role`, `tags`, `language`, `setup`, `env`, `services`, `depends_on`)

## Python Environment

- **Python**: `>=3.14,<3.15`
- **Dependency manager**: Poetry
- **Key dependencies**: `typer ^0.24.1`, `pyyaml ^6.0.3`
