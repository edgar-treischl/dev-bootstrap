import os
from typing import Optional

import typer

from devbootstrap.bootstrap import bootstrap as _bootstrap
from devbootstrap.bootstrap import update_all

app = typer.Typer(help="dev-bootstrap: manage your multi-repo development environment.")


@app.command()
def bootstrap(
    github_user: Optional[str] = typer.Option(
        None, "--github-user", "-g", help="GitHub username or org to discover repos from."
    ),
    gitlab_token: Optional[str] = typer.Option(
        None, "--gitlab-token", help="GitLab private token (overrides $GITLAB_TOKEN)."
    ),
    gitlab_url: str = typer.Option(
        "https://gitlab.com", "--gitlab-url", help="GitLab instance base URL."
    ),
):
    """Discover, clone, and place all repositories under ~/code."""
    token = gitlab_token or os.environ.get("GITLAB_TOKEN")
    _bootstrap(github_user=github_user, gitlab_token=token, gitlab_url=gitlab_url)


@app.command()
def update():
    """Fetch full history and pull every repo under ~/code."""
    update_all()