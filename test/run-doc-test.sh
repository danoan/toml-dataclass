#! /usr/bin/env bash

SCRIPT_FOLDER="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

pushd "${SCRIPT_FOLDER}/.." >/dev/null
python -m doctest docs/getting-started.md docs/how-to/task-manager.md -o NORMALIZE_WHITESPACE
popd >/dev/null
