#!/bin/bash
# ./Scripts/run-tests.sh --feature Login   |   ./Scripts/run-tests.sh --tests LOGIN_001,LOGIN_005
source "$(dirname "$0")/_common.sh"; python3 Agent/Execution/runner.py "$@" && python3 Agent/Reporting/report.py
