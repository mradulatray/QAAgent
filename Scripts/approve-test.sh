#!/bin/bash
# ./Scripts/approve-test.sh LOGIN_001 [LOGIN_002 ...]   -> moves candidates into the approved regression suite
source "$(dirname "$0")/_common.sh"
for id in "$@"; do python3 -c "import sys;sys.path.insert(0,'Agent');from Core.repository import set_approval;set_approval('$id','APPROVED')" && echo "Approved $id"; done
