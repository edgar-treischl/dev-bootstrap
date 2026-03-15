#!/bin/bash
BASE="$HOME/code"
TMP="$BASE/_tmp"
mkdir -p "$TMP"

# Combine GitHub + GitLab repos
#REPOS=$(./discover-github.sh; ./discover-gitlab.sh)
REPOS=$(./discover-github.sh)

for url in $REPOS; do
    name=$(basename "$url" .git)
    echo "Cloning $name ..."

    git clone --depth 1 "$url" "$TMP/$name"

    META="$TMP/$name/.repo-meta.yml"
    if [ -f "$META" ]; then
        dev_path=$(yq '.dev_path' "$META")
    else
        dev_path="misc"
    fi

    target="$BASE/$dev_path/$name"
    mkdir -p "$(dirname "$target")"
    mv "$TMP/$name" "$target"

    echo "→ $name placed in $BASE/$dev_path/"
done