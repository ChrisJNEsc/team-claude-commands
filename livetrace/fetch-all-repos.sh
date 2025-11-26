#!/bin/bash

GITHUB_DIR="/Users/garrett.young/Documents/GitHub"

echo "📦 Pulling latest code from all repositories..."
echo "================================"

for dir in "$GITHUB_DIR"/*; do
  if [ -d "$dir/.git" ]; then
    repo_name=$(basename "$dir")
    echo "Pulling: $repo_name"
    (cd "$dir" && git pull 2>&1 | grep -v "^$") || echo "  ⚠ Failed to pull"
  fi
done

echo "================================"
echo "✓ Repository pull complete"
echo ""
