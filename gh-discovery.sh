#!/bin/bash
# discover-github.sh

# Replace with your GitHub username or organization
USER_OR_ORG="YOUR_USERNAME"

# List SSH URLs of repos (personal + org)
gh repo list "$USER_OR_ORG" --limit 500 --json sshUrl --jq '.[].sshUrl'