"""Import a TestPlans/*.json file into the test repository (dedup + versioning, approved tests protected).
Usage: python3 Agent/TestGeneration/import_plan.py TestPlans/login_pilot.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Core.repository import import_plan  # noqa: E402

if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(path, json.dumps(import_plan(path)))
