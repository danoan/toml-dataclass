#! /usr/bin/env bash

SCRIPT_PATH="$( cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_PATH="${SCRIPT_PATH%toml-dataclass*}toml-dataclass"

INPUT_FOLDER="${SCRIPT_PATH}/input"
OUTPUT_FOLDER="${SCRIPT_PATH}/output"
mkdir -p "${OUTPUT_FOLDER}"

pushd "${PROJECT_PATH}" > /dev/null

if [[ -d .venv ]]
then
  echo ".venv directory exists. Removing it."
  rm -rf "${PROJECT_PATH}/.venv"
fi

python3.8 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -e .
pip install black bandit pylint mypy pytest pytest-cov

popd > /dev/null

