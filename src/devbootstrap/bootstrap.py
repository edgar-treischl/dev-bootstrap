from pathlib import Path
import shutil
import subprocess
import json
import urllib.request
from urllib.parse import quote
from urllib.error import HTTPError

import pandas as pd
import yaml

BASE = Path.home() / "code"


def discover_github(user_or_org: str) -> list[str]:
    """Return HTTPS URLs for all repos of a GitHub user or org via the gh CLI."""
    result = subprocess.run(
        [
            "gh", "repo", "list", user_or_org,
            "--limit", "500",
            "--json", "url",
            "--jq", ".[].url",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return [u for u in result.stdout.splitlines() if u.strip()]



def discover_gitlab(
    token: str,
    base_url: str = "https://gitlab.lrz.de",
) -> list[str]:
    """
    Discover all GitLab repositories for the authenticated user, including:
      - personal repos
      - all group repos the user belongs to

    Args:
        token: Personal Access Token (PAT) with `api` scope
        base_url: GitLab instance URL

    Returns:
        List of SSH URLs for all repositories
    """
    headers = {"PRIVATE-TOKEN": token}

    def fetch_all(url: str) -> list[dict]:
        """Fetch all pages of a GitLab API endpoint."""
        results = []
        page = 1

        while True:
            paged_url = f"{url}&page={page}"
            #print(f"DEBUG fetching: {paged_url}")  # debug output
            req = urllib.request.Request(paged_url, headers=headers)

            try:
                with urllib.request.urlopen(req) as resp:
                    data = json.loads(resp.read())
                    results.extend(data)
                    next_page = resp.headers.get("X-Next-Page")
                    if not next_page:
                        break
                    page = int(next_page)
            except HTTPError as e:
                body = e.read().decode()
                raise RuntimeError(f"GitLab API error {e.code}: {body}")

        return results

    all_repos = []

    # --- Step 1: Personal repos ---
    personal_url = f"{base_url}/api/v4/projects?owned=true&per_page=100"
    personal_projects = fetch_all(personal_url)
    all_repos.extend([p["ssh_url_to_repo"] for p in personal_projects])

    # --- Step 2: Groups the user is a member of ---
    groups_url = f"{base_url}/api/v4/groups?min_access_level=10&per_page=100"
    groups = fetch_all(groups_url)

    for group in groups:
        group_id = group["id"]
        group_projects_url = f"{base_url}/api/v4/groups/{group_id}/projects?per_page=100&include_subgroups=true"
        group_projects = fetch_all(group_projects_url)
        all_repos.extend([p["ssh_url_to_repo"] for p in group_projects])

    # --- Deduplicate repos just in case ---
    all_repos = list(dict.fromkeys(all_repos))

    return all_repos






def _dev_path(meta: dict) -> str:
    """Extract a usable dev_path string from repo metadata, defaulting to 'misc'."""
    value = meta.get("dev_path")
    if not value:
        return "misc"
    if isinstance(value, list):
        return "/".join(value) if value else "misc"
    return str(value)


def clone_and_place(urls: list[str]) -> None:
    """Shallow-clone each repo, read its .repo-meta.yml, and place it under BASE."""
    tmp = BASE / "_tmp"
    tmp.mkdir(parents=True, exist_ok=True)

    for url in urls:
        name = url.rstrip("/").split("/")[-1].removesuffix(".git")
        print(f"Cloning {name} ...")

        dest = tmp / name
        try:
            subprocess.run(["git", "clone", "--depth", "1", url, str(dest)], check=True)
        except subprocess.CalledProcessError:
            print(f"  ✗ failed to clone {name}, skipping.")
            continue

        meta_file = dest / ".repo-meta.yml"
        if meta_file.exists():
            with open(meta_file) as f:
                dev_path = _dev_path(yaml.safe_load(f) or {})
        else:
            dev_path = "misc"

        target = BASE / dev_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(dest), str(target))
        print(f"  → placed in {BASE / dev_path}/")

    try:
        tmp.rmdir()
    except OSError:
        pass


def update_all() -> None:
    """Fetch full history and pull every repo found under BASE."""
    print(f"Updating all repos under {BASE} ...")
    for git_dir in sorted(BASE.rglob(".git")):
        if not git_dir.is_dir():
            continue
        repo_dir = git_dir.parent
        print(f"  {repo_dir}")
        subprocess.run(["git", "fetch", "--unshallow"], cwd=repo_dir, capture_output=True)
        subprocess.run(["git", "pull", "--ff-only"], cwd=repo_dir, check=True)
    print("Done.")


def scan_repos(base: Path | None = None) -> pd.DataFrame:
    """Scan for all .repo-meta.yml files under *base* and return them as a DataFrame."""
    search_root = base or BASE
    rows: list[dict] = []

    for meta_file in sorted(search_root.rglob(".repo-meta.yml")):
        with open(meta_file) as fh:
            data: dict = yaml.safe_load(fh) or {}

        # Flatten list values → comma-separated strings
        row: dict = {"repo_path": str(meta_file.parent)}
        for key, value in data.items():
            if isinstance(value, list):
                row[key] = ", ".join(str(v) for v in value if v)
            else:
                row[key] = value

        rows.append(row)

    return pd.DataFrame(rows)


def bootstrap(
    github: bool = False,
    gitlab: bool = False,
    user: Optional[str] = None,
    gitlab_token: Optional[str] = None,
    gitlab_url: str = "https://gitlab.lrz.de",
) -> None:
    """Discover repos, clone them, and place them under ~/code."""
    BASE.mkdir(parents=True, exist_ok=True)

    urls: list[str] = []

    # GitHub discovery
    if github:
        if not user:
            print("GitHub discovery requires --user/-u")
            return
        print(f"Discovering GitHub repos for '{user}' ...")
        urls += discover_github(user)

    # GitLab discovery
    token = gitlab_token or os.environ.get("GITLAB_TOKEN")
    if gitlab:
        if not token:
            print("GitLab discovery requires --gitlab-token or $GITLAB_TOKEN")
            return
        print(f"Discovering GitLab repos at {gitlab_url} ...")
        urls += discover_gitlab(token, gitlab_url)

    if not urls:
        print("No repositories discovered. Pass --github/-gh or --gitlab/-gl with required info.")
        return

    print(urls)
    urls: list[str] = ['https://github.com/edgar-treischl/dev-bootstrap']
    clone_and_place(urls)
    print("Bootstrap complete!")