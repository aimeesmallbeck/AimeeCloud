#!/bin/bash
# Aimee Robot - Backup to UNOQ Private Repo
# Backs up the full workspace state (including configs normally excluded from public repo)
#
# Usage:
#   bash deploy/backup-to-unoq.sh ["Optional commit message"]

set -e

WORKSPACE_DIR="$HOME/aimee-robot-ws"
BACKUP_REMOTE="backup"
BRANCH="main"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
MESSAGE="${1:-Board backup: $TIMESTAMP}"

cd "$WORKSPACE_DIR"

# Check if backup remote exists
if ! git remote | grep -q "^backup$"; then
    echo "Error: 'backup' remote not found. Run:"
    echo "  git remote add backup git@github.com:aimeesmallbeck/UNOQ.git"
    exit 1
fi

# Save current branch
CURRENT_BRANCH=$(git branch --show-current)
CURRENT_COMMIT=$(git rev-parse HEAD)

echo "Creating backup: $MESSAGE"

# Create a temporary backup branch
BACKUP_BRANCH="backup-$TIMESTAMP"
git checkout -b "$BACKUP_BRANCH" || true

# Force-add files that are normally ignored but needed for a full backup
# .env contains API keys - safe for private repo only
git add -f .env 2>/dev/null || true

# Add any other untracked config files
git add -f config/*.json config/*.yaml 2>/dev/null || true

# Commit everything (will include normally ignored files if added above)
git commit -m "$MESSAGE" || echo "Nothing new to commit"

# Push to UNOQ
echo "Pushing to UNOQ private repo..."
git push "$BACKUP_REMOTE" "$BACKUP_BRANCH:main" --force

# Return to original branch
git checkout "$CURRENT_BRANCH"
git branch -D "$BACKUP_BRANCH" 2>/dev/null || true

echo ""
echo "Backup complete!"
echo "  Branch: $BACKUP_BRANCH -> UNOQ/main"
echo "  Timestamp: $TIMESTAMP"

# Note about large files
echo ""
echo "Note: Large model files (>100MB) are NOT included in git."
echo "Use sync-models.sh to transfer models between boards."
