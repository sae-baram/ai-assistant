#!/usr/bin/env bash
set -euo pipefail

# Script to clone and prepare Open-WebUI as the project frontend.
# Run this from the repo root: ./scripts/install_open_webui.sh

REPO_DIR=frontend
OPEN_WEBUI_GIT=https://github.com/open-webui/open-webui.git

echo "This script will clone open-webui into '$REPO_DIR' (overwrites if exists)."
read -p "Proceed? [y/N] " yn
if [[ "$yn" != "y" && "$yn" != "Y" ]]; then
  echo "Aborted."
  exit 1
fi

# Remove existing frontend (backup if you want)
if [ -d "$REPO_DIR" ]; then
  echo "Removing existing $REPO_DIR ..."
  rm -rf "$REPO_DIR"
fi

echo "Cloning open-webui into $REPO_DIR ..."
git clone "$OPEN_WEBUI_GIT" "$REPO_DIR"

cd "$REPO_DIR"

echo "Installing dependencies (may take a while)..."
npm install

cat > .env.local <<'EOF'
# Local overrides to point frontend to our backend
# When running open-webui dev server, set the API base to the FastAPI /ask endpoint
VITE_API_BASE_URL=http://localhost:8000
# If open-webui expects a specific path, use: VITE_API_BASE_URL=http://localhost:8000/ask
EOF

echo "Finished. To run the open-webui frontend dev server:
  cd $REPO_DIR
  npm run dev

Then open the UI (likely at http://localhost:3000) and ensure the frontend is configured to POST questions to http://localhost:8000/ask (see .env.local)."
