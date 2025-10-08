#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
DIST_DIR="$PROJECT_DIR/dist"
TARGET="/srv/site"

if [[ ! -d "$DIST_DIR" ]]; then
  echo "dist/ not found. Run 'npm run build' first." >&2
  exit 1
fi

rsync -avz --delete "$DIST_DIR"/ "${DEPLOY_USER:-deploy}"@"${DEPLOY_HOST}"":"$TARGET"/
