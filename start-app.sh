#!/bin/sh
# Start the demo application only; the candidate prepares the test environment.
set -eu
project_dir=$(CDPATH= cd -P "$(dirname "$0")" && pwd)
for interpreter in python3 python python3.15 python3.14 python3.13 python3.12 python3.11; do
    if command -v "$interpreter" >/dev/null 2>&1 &&
        "$interpreter" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)' >/dev/null 2>&1; then
        exec "$interpreter" -B -u "$project_dir/qa-demo-app/run.py" "$@"
    fi
done
printf '%s\n' 'Python 3.11+ was not found. Install Python and make its command available in PATH, then run sh ./start-app.sh again.' >&2
exit 1
