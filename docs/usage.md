# CLI Commands

All commands are run through the `dev` entry point inside the Poetry environment:

```bash
poetry run dev <command> [OPTIONS]
```

---

## `bootstrap`

Discovers repos from GitHub and/or GitLab, shallow-clones them, and places each one under `~/code/<dev_path>/`.

```bash
poetry run dev bootstrap [OPTIONS]
```

| Option | Default | Description |
|---|---|---|
| `--github-user`, `-g` | — | GitHub username or organisation to discover repos from |
| `--gitlab-token` | `$GITLAB_TOKEN` | GitLab private token (overrides the environment variable) |
| `--gitlab-url` | `https://gitlab.com` | GitLab instance base URL |

### Examples

=== "GitHub only"

    ```bash
    poetry run dev bootstrap --github-user alice
    ```

=== "GitLab only"

    ```bash
    export GITLAB_TOKEN=glpat-xxxxxxxxxxxx
    poetry run dev bootstrap --gitlab-url https://gitlab.example.com
    ```

=== "Both at once"

    ```bash
    poetry run dev bootstrap \
      --github-user alice \
      --gitlab-token glpat-xxxx \
      --gitlab-url https://gitlab.example.com
    ```

!!! tip "Where do repos land?"
    Each repo's `.repo-meta.yml` controls its final path. See [`.repo-meta.yml` Schema](repo-meta.md) for details.

---

## `update`

Fetches full history (unshallows) and pulls every repo already present under `~/code/`.

```bash
poetry run dev update
```

No options. Walks all `.git` directories under `~/code` and runs:

```
git fetch --unshallow
git pull --ff-only
```

---

## `scan`

Scans `~/code/` for `.repo-meta.yml` files, loads them into a DataFrame, and prints a summary table.

```bash
poetry run dev scan [OPTIONS]
```

| Option | Default | Description |
|---|---|---|
| `--output`, `-o` | — | Export the result as a CSV file to the given path |

### Examples

=== "Display table"

    ```bash
    poetry run dev scan
    ```

=== "Export to CSV"

    ```bash
    poetry run dev scan --output repos.csv
    ```

See [Scanning Repos](scan.md) for more detail on the output format.

---

## Help

```bash
poetry run dev --help
poetry run dev bootstrap --help
poetry run dev scan --help
```
