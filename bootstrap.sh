#!/bin/bash
set -e

echo "Creating main dev folder..."
mkdir -p ~/code

echo "Cloning repositories..."
./clone-repos.sh

echo "POC bootstrap complete!"