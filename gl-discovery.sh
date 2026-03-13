#!/bin/bash
# discover-gitlab.sh

# Set your GitLab private token
export GITLAB_TOKEN="YOUR_TOKEN"

# List your projects (membership)
curl --silent --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
"https://gitlab.com/api/v4/projects?membership=true&per_page=200" \
| jq -r '.[].ssh_url_to_repo'