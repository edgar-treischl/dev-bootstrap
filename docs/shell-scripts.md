# Shell Scripts

The `shell/` directory contains the original Bash proof-of-concept scripts that the Python CLI is built on top of. They can be used standalone if preferred.

---

## `bootstrap.sh`

Entry point. Creates `~/code/` and calls `clone-repos.sh`.

```bash
cd shell/
./bootstrap.sh
```

**Dependencies:** `clone-repos.sh`, `gh-discovery.sh`

---

## `clone-repos.sh`

Orchestrates the full bootstrap flow for GitHub repos:

1. Calls `gh-discovery.sh` to get a list of SSH URLs
2. Shallow-clones each repo into `~/code/_tmp/`
3. Reads `.repo-meta.yml` with `yq` to extract `dev_path`
4. Moves the repo to `~/code/<dev_path>/<name>`

**Dependencies:** `gh`, `git`, `yq`

!!! note
    GitLab support is commented out in `clone-repos.sh`. Use the Python CLI (`poetry run dev bootstrap`) for combined GitHub + GitLab discovery.

---

## `gh-discovery.sh`

Lists SSH URLs for all repos of a GitHub user or organisation using the `gh` CLI.

```bash
./gh-discovery.sh
```

Edit the `USER_OR_ORG` variable at the top of the script to change the target account. Output is one SSH URL per line.

**Dependencies:** `gh` (authenticated)

---

## `gl-discovery.sh`

Lists SSH URLs for all GitLab projects you are a member of.

```bash
export GITLAB_TOKEN=<your-token>
./gl-discovery.sh
```

Edit the `GITLAB_TOKEN` export and the base URL inside the script if you're targeting a self-hosted GitLab instance.

**Dependencies:** `curl`, `jq`

---

## `update-all.sh`

Finds every `.git` directory under `~/code/`, unshallows the clone if needed, and pulls the latest changes.

```bash
./update-all.sh
```

Equivalent to `poetry run dev update`.

**Dependencies:** `git`

---

## Script vs CLI comparison

| Task | Shell script | Python CLI |
|---|---|---|
| Bootstrap from GitHub | `./bootstrap.sh` | `poetry run dev bootstrap --github-user <user>` |
| Bootstrap from GitLab | edit `gl-discovery.sh` | `poetry run dev bootstrap --gitlab-token <token>` |
| Bootstrap from both | manual combination | `poetry run dev bootstrap --github-user <user> --gitlab-token <token>` |
| Update all repos | `./update-all.sh` | `poetry run dev update` |
| Scan metadata | — | `poetry run dev scan` |
