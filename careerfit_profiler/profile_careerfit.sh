#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
PROFILE_OUTPUT="$SCRIPT_DIR/${TIMESTAMP}_careerfit_profile.stats"

if [ $# -eq 0 ]; then
    echo "Usage: $0 [CareerFit arguments]"
    echo "Example: $0 --python"
    exit 1
fi

echo "Running cProfile on careerfit CLI..."
python -m cProfile -o $PROFILE_OUTPUT $(which careerfit) "$@"

if ! command -v snakeviz &> /dev/null
then
    echo "snakeviz is not installed. Installing it now..."
    pip install snakeviz
fi

echo "Launching snakeviz..."
snakeviz $PROFILE_OUTPUT
