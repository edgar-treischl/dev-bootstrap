from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
import os
import json

import typer

from devbootstrap.bootstrap import bootstrap as _bootstrap
from devbootstrap.bootstrap import scan_repos, update_all
from devbootstrap.bootstrap import discover_github, discover_gitlab

# Load environment variables from .env automatically
env_path = Path(".env")
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

app = typer.Typer(help="dev-bootstrap: manage your multi-repo development environment.")


@app.command()
def bootstrap(
    github_user: Optional[str] = typer.Option(None, "--github-user", help="GitHub username/org"),
    gitlab_token: Optional[str] = typer.Option(None, "--gitlab-token", help="GitLab token"),
    gitlab_url: str = typer.Option(os.environ.get("GITLAB_URL", "https://gitlab.com"), "--gitlab-url", help="GitLab base URL"),
):
    """Discover, clone, and place all repositories under ~/code."""
    token = gitlab_token or os.environ.get("GITLAB_TOKEN")
    _bootstrap(github_user=github_user, gitlab_token=token, gitlab_url=gitlab_url)


@app.command()
def update():
    """Fetch full history and pull every repo under ~/code."""
    update_all()


@app.command()
def scan(
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Export CSV file"),
):
    """Scan ~/code for .repo-meta.yml files and display a summary table."""
    df = scan_repos()
    if df.empty:
        typer.echo("No .repo-meta.yml files found under ~/code.")
        raise typer.Exit()
    typer.echo(df.to_string(index=False))
    if output:
        df.to_csv(output, index=False)
        typer.echo(f"\nExported {len(df)} repos → {output}")


@app.command()
def discover(
    github: bool = typer.Option(False, "--github", "-gh", help="Enable GitHub discovery"),
    gitlab: bool = typer.Option(False, "--gitlab", "-gl", help="Enable GitLab discovery"),
    user: Optional[str] = typer.Option(None, "--user", "-u", help="Username or org (GitHub or GitLab)"),
    gitlab_token: Optional[str] = typer.Option(None, "--gitlab-token", help="GitLab token (overrides $GITLAB_TOKEN)"),
    gitlab_url: str = typer.Option(os.environ.get("GITLAB_URL", "https://gitlab.com"), "--gitlab-url", help="GitLab base URL"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """
    Discover repositories without cloning them.

    Examples:
      # GitHub only
      poetry run dev discover -gh -u <username>

      # GitLab only
      poetry run dev discover -gl -u <username>

      # Both providers
      poetry run dev discover -gh -gl -u <username>

      # JSON output
      poetry run dev discover -gh -gl -u <username> --json
    """
    all_repos: list[str] = []

    # GitHub discovery
    if github:
        if not user:
            typer.echo("GitHub discovery requires --user/-u")
            raise typer.Exit(code=1)
        all_repos.extend(discover_github(user))

    # GitLab discovery
    token = gitlab_token or os.environ.get("GITLAB_TOKEN")
    if gitlab:
        if not token:
            typer.echo("GitLab discovery requires --gitlab-token or $GITLAB_TOKEN")
            raise typer.Exit(code=1)
        all_repos.extend(discover_gitlab(token, gitlab_url))

    if not all_repos:
        typer.echo("No repositories found.")
        raise typer.Exit(code=1)

    if json_output:
        typer.echo(json.dumps(all_repos, indent=2))
        return

    for repo in all_repos:
        provider = "GitHub" if "github.com" in repo else "GitLab"
        name = repo.split("/")[-1].removesuffix(".git")
        typer.echo(f"[{provider}] {name} → {repo}")