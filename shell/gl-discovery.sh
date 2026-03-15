#!/bin/bash
# discover-gitlab.sh

# Set your GitLab private token
export GITLAB_TOKEN="Insert token"

# List your projects (membership)
curl --silent --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
"https://gitlab.lrz.de/api/v4/projects?membership=true&per_page=100" \
| jq -r '.[].ssh_url_to_repo'