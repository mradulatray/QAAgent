"""Deterministic test executor: xcodebuild -> xcresult -> SQLite history. No AI needed.

Usage:
  python3 Agent/Execution/runner.py --feature Login          # all automated tests of a feature
  python3 Agent/Execution/runner.py --tests LOGIN_001,LOGIN_005
  python3 Agent/Execution/runner.py --approved                # full regression of APPROVED tests
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Core.db import AGENT_ROOT, connect, dumps  # noqa: E402

CONFIG = json.load(open(os.path.join(AGENT_ROOT, "Configuration", "agent.json")))
REPO = CONFIG["app_repo"]
TEST_NAME_RE = re.compile(r"test_(OBS_)?([A-Z][A-Z_]*_\d{3})_")

ENV_PATTERNS = ["Lost connection", "Failed to launch", "Unable to boot", "simulator", "Couldn’t communicate",
                "timed out while", "Failed to get matching snapshot", "Application failed preflight",
                "Test crashed with signal", "Restarting after unexpected exit"]
AUTOMATION_PATTERNS = ["not found on Jobs home", "field not shown", "No matches found", "Failed to tap",
                       "Multiple matching elements"]


def git(*args):
    try:
        return subprocess.check_output(["git", "-C", REPO] + list(args), stderr=subprocess.DEVNULL).decode().strip()
    except subprocess.CalledProcessError:
        return ""


def classify(message):
    m = message or ""
    if any(p.lower() in m.lower() for p in ENV_PATTERNS):
        return "ENVIRONMENT"
    if any(p.lower() in m.lower() for p in AUTOMATION_PATTERNS):
        return "AUTOMATION"
    return "APP_DEFECT_SUSPECTED"


def select_cases(conn, args):
    q = "SELECT * FROM test_cases WHERE approval_status <> 'DEPRECATED'"
    params = []
    if args.approved:
        q += " AND approval_status='APPROVED'"
    if args.feature:
        q += " AND feature=?"
        params.append(args.feature)
    if args.tests:
        ids = [t.strip() for t in args.tests.split(",")]
        q += " AND test_id IN (%s)" % ",".join("?" * len(ids))
        params += ids
    return [dict(r) for r in conn.execute(q + " ORDER BY test_id", params)]


def walk(nodes):
    for n in nodes:
        yield n
        yield from walk(n.get("children", []))


def run(args):
    conn = connect()
    cases = select_cases(conn, args)
    if not cases:
        print("No test cases selected.")
        return None
    runnable = [c for c in cases if c["automation_status"] in ("AUTOMATED", "OBSERVATION") and c["automation_ref"]]

    run_id = datetime.datetime.now().strftime("RUN_%Y%m%d_%H%M%S")
    run_dir = os.path.join(AGENT_ROOT, "Reports", "runs", run_id)
    shots_dir = os.path.join(AGENT_ROOT, "Screenshots", run_id)
    os.makedirs(run_dir, exist_ok=True)
    bundle = os.path.join(run_dir, "result.xcresult")
    log_path = os.path.join(AGENT_ROOT, "Logs", run_id + ".log")
    started = datetime.datetime.now().isoformat(timespec="seconds")

    results, build_error = {}, ""
    if runnable:
        cls = {"Login": "LoginPilotUITests"}
        only = ["-only-testing:%s/%s/%s" % (CONFIG["ui_test_scheme"], cls.get(c["feature"], c["feature"] + "UITests"),
                                            c["automation_ref"]) for c in runnable]
        cmd = ["xcodebuild", "test", "-workspace", CONFIG["workspace"], "-scheme", CONFIG["ui_test_scheme"],
               "-destination", "platform=iOS Simulator,id=%s" % CONFIG["simulator_id"],
               "-resultBundlePath", bundle] + only
        print("Running %d automated tests (%s)..." % (len(runnable), run_id), flush=True)
        with open(log_path, "w") as log:
            rc = subprocess.call(cmd, cwd=REPO, stdout=log, stderr=subprocess.STDOUT)
        if os.path.exists(bundle):
            raw = subprocess.check_output(["xcrun", "xcresulttool", "get", "test-results", "tests", "--path", bundle])
            for node in walk(json.loads(raw).get("testNodes", [])):
                if node.get("nodeType") != "Test Case":
                    continue
                m = TEST_NAME_RE.search(node["name"])
                if not m:
                    continue
                failures = [ch.get("name", "") for ch in walk(node.get("children", []))
                            if ch.get("nodeType") == "Failure Message"]
                results[m.group(2)] = {"result": node.get("result"), "duration": node.get("durationInSeconds", 0),
                                       "failures": failures, "identifier": node.get("nodeIdentifier")}
            subprocess.call(["xcrun", "xcresulttool", "export", "attachments", "--path", bundle,
                             "--output-path", shots_dir], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if rc != 0 and not results:
            build_error = "xcodebuild exited %d before producing results; see %s" % (rc, log_path)

    attachments = _attachments_by_test(shots_dir)
    summary = {}
    for c in cases:
        tid, r = c["test_id"], results.get(c["test_id"])
        att = attachments.get(c["automation_ref"], {})
        actual, error, fclass = att.get("observation", ""), "", ""
        if c["automation_status"] in ("BLOCKED", "MANUAL"):
            status, actual = "NOT_EXECUTED", c["review_note"]
        elif r is None:
            status = "BLOCKED" if build_error else "NOT_EXECUTED"
            error = build_error or "Test not found in result bundle"
            fclass = "ENVIRONMENT" if build_error else ""
        elif r["result"] == "Passed":
            status = "NEEDS_REVIEW" if c["automation_status"] == "OBSERVATION" else "PASSED"
            actual = actual or ("As expected" if status == "PASSED" else "")
        elif r["result"] == "Skipped":
            status = "SKIPPED"
        else:
            status = "FAILED"
            error = " | ".join(r["failures"])[:2000]
            fclass = classify(error)
            actual = actual or error
        summary[status] = summary.get(status, 0) + 1
        conn.execute("INSERT INTO executions(run_id,test_id,status,duration_s,actual,error,failure_class,attachments) "
                     "VALUES(?,?,?,?,?,?,?,?)",
                     (run_id, tid, status, (r or {}).get("duration", 0), actual, error, fclass,
                      dumps(att.get("files", []))))

    conn.execute("INSERT INTO runs(run_id,started_at,finished_at,kind,git_branch,commit_sha,app_build,device,"
                 "environment,result_bundle,summary) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                 (run_id, started, datetime.datetime.now().isoformat(timespec="seconds"),
                  args.kind, git("rev-parse", "--abbrev-ref", "HEAD"), git("rev-parse", "HEAD"),
                  "Debug (simulator)", CONFIG["simulator_name"], CONFIG["environment"]["debug_build_hits"],
                  bundle if runnable else "", dumps(summary)))
    conn.commit()
    print(json.dumps({"run_id": run_id, "summary": summary}, indent=2))
    return run_id


def _attachments_by_test(shots_dir):
    out = {}
    manifest = os.path.join(shots_dir, "manifest.json")
    if not os.path.exists(manifest):
        return out
    for entry in json.load(open(manifest)):
        method = entry["testIdentifier"].split("/")[-1].rstrip("()")
        info = out.setdefault(method, {"files": [], "observation": ""})
        for a in entry["attachments"]:
            rel = os.path.join("Screenshots", os.path.basename(shots_dir), a["exportedFileName"])
            if a["exportedFileName"].endswith(".txt"):
                text = open(os.path.join(shots_dir, a["exportedFileName"]), errors="ignore").read()
                if a["suggestedHumanReadableName"].startswith("observation"):
                    info["observation"] = (info["observation"] + " " + text).strip()
            else:
                info["files"].append(rel)
    return out


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--feature")
    p.add_argument("--tests")
    p.add_argument("--approved", action="store_true")
    p.add_argument("--kind", default="manual")
    a = p.parse_args()
    if a.approved and a.kind == "manual":
        a.kind = "full_regression"
    run(a)
