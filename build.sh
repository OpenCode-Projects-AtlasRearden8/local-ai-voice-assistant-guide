#!/usr/bin/env bash
# Build the static HTML site from docs/ into site/.
set -euo pipefail
cd "$(dirname "$0")"
if ! python3 -c "import markdown" 2>/dev/null; then
  echo "Missing dependency. Install it with:" >&2
  echo "  pip install markdown" >&2
  exit 1
fi
exec python3 build.py "$@"
