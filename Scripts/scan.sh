#!/bin/bash
# Incremental code scan -> knowledge base (add --full to rescan everything)
source "$(dirname "$0")/_common.sh"; python3 Agent/CodeAnalysis/scanner.py "$@"
