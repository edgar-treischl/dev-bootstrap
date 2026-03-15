#!/bin/bash
BASE="$HOME/code"

echo "Updating all repos under $BASE ..."

find "$BASE" -name ".git" -type d | while read repo; do
    DIR=$(dirname "$repo")
    echo "Updating $DIR"

    cd "$DIR"

    # Fetch full history if sparse/shallow
    git fetch --unshallow 2>/dev/null || true

    # Pull latest changes
    git pull --ff-only
done

echo "All repos updated."