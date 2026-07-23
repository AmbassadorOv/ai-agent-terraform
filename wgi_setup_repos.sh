#!/usr/bin/env bash
# ==============================================================================
# WGI Topology v1.0 Repository Splitter and Deployer
# This script initializes, commits, and prepares 12 separate Git repositories
# to be pushed to your sovereign enterprise Git server at institute.wgo.ai.
# ==============================================================================

set -e

BASE_DIR="wgi_topology"
ENTERPRISE_HOST="institute.wgo.ai"
ENTERPRISE_ORG="wgi"

if [ ! -d "$BASE_DIR" ]; then
  echo "Error: $BASE_DIR directory not found in current path."
  exit 1
fi

echo "🚀 Starting repository split and configuration for 12 sub-branches..."

# Iterate through each subdirectory in wgi_topology/
for dir in "$BASE_DIR"/*; do
  if [ -d "$dir" ]; then
    BRANCH_NAME=$(basename "$dir")
    echo "--------------------------------------------------------"
    echo "📦 Processing branch: $BRANCH_NAME"

    # Enter directory
    cd "$dir"

    # Check if git is already initialized, if not initialize it
    if [ ! -d ".git" ]; then
      git init -b main
      echo "  - Initialized empty local Git repository"
    fi

    # Configure local git user if not globally set
    git config user.name "WGI Admin" || true
    git config user.email "admin@wgo.ai" || true

    # Add files and commit
    git add docker-compose.yml
    git commit -m "feat: initial commit with Edge-CPU docker-compose config for $BRANCH_NAME" || echo "  - No changes to commit"

    # Add or update remote origin
    REMOTE_URL="git@${ENTERPRISE_HOST}:${ENTERPRISE_ORG}/${BRANCH_NAME}.git"
    if git remote | grep -q "origin"; then
      git remote set-url origin "$REMOTE_URL"
    else
      git remote add origin "$REMOTE_URL"
    fi
    echo "  - Configured remote origin: $REMOTE_URL"
    echo "  - Ready to push! Run: 'git push -u origin main' inside $dir"

    # Go back to base directory
    cd - >/dev/null
  fi
done

echo "========================================================"
echo "✅ Successfully split WGI Topology v1.0 into 12 separate local repositories!"
echo "To push all repositories to the remote host ($ENTERPRISE_HOST), execute:"
echo "  wgi_setup_repos.sh --push"
echo "========================================================"

if [ "$1" == "--push" ]; then
  echo "📡 Attempting to push all 12 repositories..."
  for dir in "$BASE_DIR"/*; do
    if [ -d "$dir" ]; then
      BRANCH_NAME=$(basename "$dir")
      echo "🔺 Pushing $BRANCH_NAME to $ENTERPRISE_HOST..."
      cd "$dir"
      git push -u origin main || echo "  - Push failed (make sure SSH keys and repositories are configured on $ENTERPRISE_HOST)"
      cd - >/dev/null
    fi
  done
fi
