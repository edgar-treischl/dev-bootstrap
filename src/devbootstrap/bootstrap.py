from pathlib import Path
import shutil
import subprocess

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


def discover_gitlab(token: str, base_url: str = "https://gitlab.com") -> list[str]:
    """Return SSH URLs for all member projects of a GitLab instance."""
    import json
    import urllib.request

    req = urllib.request.Request(
        f"{base_url}/api/v4/projects?membership=true&per_page=100",
        headers={"PRIVATE-TOKEN": token},
    )
    with urllib.request.urlopen(req) as resp:
        projects = json.loads(resp.read())
    return [p["ssh_url_to_repo"] for p in projects]


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


def bootstrap(
    github_user: str | None = None,
    gitlab_token: str | None = None,
    gitlab_url: str = "https://gitlab.com",
) -> None:
    """Discover repos, clone them, and place them under ~/code."""
    BASE.mkdir(parents=True, exist_ok=True)

    urls: list[str] = []
    if github_user:
        print(f"Discovering GitHub repos for '{github_user}' ...")
        urls += discover_github(github_user)
    if gitlab_token:
        print(f"Discovering GitLab repos at {gitlab_url} ...")
        urls += discover_gitlab(gitlab_token, gitlab_url)

    if not urls:
        print("No repositories discovered. Pass --github-user or --gitlab-token.")
        return

    clone_and_place(urls)
    print("Bootstrap complete!")