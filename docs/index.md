# dev-bootstrap

**dev-bootstrap** discovers repositories from GitHub and GitLab, reads a small metadata file from each one, and organises everything under `~/code/` — so your local environment mirrors exactly how you structure your work.

---

## How it works

```
gh repo list / GitLab API
        ↓
  git clone --depth 1
        ↓
  read .repo-meta.yml
        ↓
  ~/code/<dev_path>/<repo-name>
```

1. **Discover** — the CLI (or shell scripts) query GitHub via `gh` and/or a GitLab API.
2. **Clone** — each repo is shallow-cloned into a temporary staging area.
3. **Read metadata** — if the repo contains a `.repo-meta.yml`, its `dev_path` field determines the final location.
4. **Place** — the repo is moved to `~/code/<dev_path>/<name>`. Repos without metadata land in `~/code/misc/`.

---

## Quick start

```bash
git clone https://github.com/edgar-treischl/dev-bootstrap.git
cd dev-bootstrap
poetry install

# Preview repos without cloning
poetry run dev discover -gh -u <your-github-username>

# Bootstrap all repos for a GitHub user
poetry run dev bootstrap --github-user <your-github-username>
```

See [Installation](installation.md) for prerequisites and [Usage](usage.md) for all commands.
