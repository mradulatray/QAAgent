#!/bin/bash
# Runs every APPROVED test case, then writes the report
source "$(dirname "$0")/_common.sh"; python3 Agent/Execution/runner.py --approved && python3 Agent/Reporting/report.py
