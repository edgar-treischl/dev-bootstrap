# .repo-meta.yml Schema

Each repository can contain a `.repo-meta.yml` at its root. This file drives where the repo is placed locally and provides structured metadata visible via `dev scan`.

---

## Full example

```yaml
name: my-api
description: REST API for the core platform
dev_path: work/apps        # → ~/code/work/apps/my-api
role: project
tags:
  - backend
  - python
language: python
setup:
  - pip install -e .
  - pre-commit install
env:
  - .env.example
services:
  - postgres
  - redis
depends_on:
  - my-core-lib
workspace: []
update_strategy: []
priority: []
```

---

## Field reference

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | no | Display name (falls back to the git repo name) |
| `description` | string | no | One-line description of the repository |
| `dev_path` | string \| list | **yes** | Path suffix under `~/code/`. Missing or empty → `misc` |
| `role` | string | no | Classification: `project`, `tool`, `library`, `service`, … |
| `tags` | list[string] | no | Free-form labels for filtering / searching |
| `language` | string | no | Primary programming language |
| `setup` | list[string] | no | Commands to run after cloning (not run automatically yet) |
| `env` | list[string] | no | Environment template files (e.g. `.env.example`) |
| `services` | list[string] | no | External services the repo requires (postgres, redis, …) |
| `depends_on` | list[string] | no | Other repo names this one depends on |
| `workspace` | list | no | Workspace configuration (reserved) |
| `update_strategy` | list | no | Git update strategy hints (reserved) |
| `priority` | list | no | Priority hints (reserved) |

---

## `dev_path` in detail

`dev_path` is the only field that affects runtime behaviour — everything else is informational.

```yaml
# String form
dev_path: work/apps           # → ~/code/work/apps/<name>

# List form (joined with "/")
dev_path:
  - work
  - apps                      # → ~/code/work/apps/<name>

# Empty or missing
dev_path: []                  # → ~/code/misc/<name>
```

---

## Minimal file

```yaml
dev_path: work/apps
```

That's enough to have the repo placed correctly. All other fields are optional.
