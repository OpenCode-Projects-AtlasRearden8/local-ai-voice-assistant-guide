#!/usr/bin/env bash
# Run the whole House Voice test suite (site build + links + secrets + starter logic).
set -euo pipefail
cd "$(dirname "$0")/.."
python3 tests/test_all.py "$@"
