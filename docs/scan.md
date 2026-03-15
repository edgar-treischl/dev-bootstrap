# Scanning Repos

The `scan` command walks `~/code/` and collects every `.repo-meta.yml` it finds into a single table — useful for auditing what's cloned, what metadata is missing, and how projects are organised.

---

## Running a scan

```bash
poetry run dev scan
```

Sample output:

```
 repo_path                        name        role  language  tags          dev_path
 ~/code/work/apps/my-api          my-api      project  python  backend       work/apps
 ~/code/work/apps/frontend        frontend    project  node    frontend      work/apps
 ~/code/misc/old-tool             old-tool    tool     bash                  misc
```

---

## Exporting to CSV

```bash
poetry run dev scan --output repos.csv
```

This writes the same table to `repos.csv` and prints a confirmation line:

```
Exported 3 repos → repos.csv
```

---

## DataFrame columns

Each row corresponds to one repo. The columns map directly to `.repo-meta.yml` fields, plus one extra:

| Column | Source | Notes |
|---|---|---|
| `repo_path` | filesystem | Absolute path to the repo directory |
| `name` | `.repo-meta.yml` | Repository name |
| `description` | `.repo-meta.yml` | Short description |
| `dev_path` | `.repo-meta.yml` | Subdirectory under `~/code/` |
| `role` | `.repo-meta.yml` | e.g. `project`, `tool`, `library` |
| `tags` | `.repo-meta.yml` | Comma-separated list |
| `language` | `.repo-meta.yml` | Primary language |
| `setup` | `.repo-meta.yml` | Setup commands, comma-separated |
| `env` | `.repo-meta.yml` | Environment files, comma-separated |
| `services` | `.repo-meta.yml` | Required services, comma-separated |
| `depends_on` | `.repo-meta.yml` | Repo dependencies, comma-separated |

!!! note "List fields"
    YAML list fields are flattened to comma-separated strings so the DataFrame stays flat and CSV-exportable.

---

## Using the function directly

`scan_repos()` is importable for use in your own scripts or notebooks:

```python
from devbootstrap.bootstrap import scan_repos
from pathlib import Path

# Scan the default ~/code directory
df = scan_repos()

# Or scan a specific directory
df = scan_repos(base=Path("/tmp/my-repos"))

print(df.head())
df.to_csv("repos.csv", index=False)
```
