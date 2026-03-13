# Dev Bootstrap POC

This repo provides a **proof-of-concept bootstrap for your development environment**.  
It discovers repositories from GitHub and GitLab, reads `.repo-meta.yml` for folder placement,  
and organizes them under `~/code`.

---

## Requirements

- Git
- GitHub CLI (`gh`) - https://cli.github.com/
- `yq` for YAML parsing (`brew install yq`)
- `jq` for JSON parsing (`brew install jq`)
- GitLab personal access token (for `discover-gitlab.sh`) as `$GITLAB_TOKEN`

---

## Setup

1. Clone this bootstrap repo:

```bash
git clone git@github.com:you/dev-bootstrap.git
cd dev-bootstrap
```


2. Run the bootstrap:

```bash
./bootstrap.sh
```

Repos are placed in ~/code/<dev_path_from_repo-meta>
Only .repo-meta.yml is downloaded initially (fast bootstrap)
Full code can be fetched later on-demand

Each repo should contain a .repo-meta.yml file like:

```yaml
dev_path: backend/payments
type: service
team: platform
language: go
```

dev_path → local folder placement
Other fields can be used for automation (CI, dashboards, etc.)