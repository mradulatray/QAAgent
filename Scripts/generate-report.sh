#!/bin/bash
# ./Scripts/generate-report.sh [RUN_ID]   (default: latest run) -> Reports/runs/<RUN_ID>/report.html + Reports/latest.html
source "$(dirname "$0")/_common.sh"; python3 Agent/Reporting/report.py "$@"
