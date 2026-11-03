#!/bin/bash
# Import TestPlans/*.json into the repository (dedup, versioning, approved tests protected)
source "$(dirname "$0")/_common.sh"; python3 Agent/TestGeneration/import_plan.py "${@:-TestPlans/*.json}"
